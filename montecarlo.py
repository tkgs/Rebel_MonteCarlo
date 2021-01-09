import base64
from io import BytesIO
import numpy as np
from Rebel_MonteCarlo.utils import montecarlo, calc_pmt, montecarlo_bool, calc_irr, calc_payback, calc_duration, calc_dv01, create_figure

def montecarlo_simulation(prazo, juros, divida, n_sim=1000, curva_default=[0]):

    prazo_min = int(prazo[0])
    prazo_med = int(prazo[1])
    prazo_max = int(prazo[2])
    prazo_std = float(prazo[3])
    juros_min = float(juros[0])
    juros_med = float(juros[1])
    juros_max = float(juros[2])
    juros_std = float(juros[3])
    divida_min = float(divida[0])
    divida_med = float(divida[1])
    divida_max = float(divida[2])
    divida_std = float(divida[3])
    #random.seed(0)

    """
    curva_default é uma lista que será inputada pelo usuário e representa a probabilidade, em %, de default em um determinado mês.
    A lista inputada não precisa necessariamente ter um valor de probabilidade atribuído para cada mês. Caso o tamanho da lista seja menor 
    do que o número de meses necessário, o algoritmo irá considerar a última probabilidade inputada como um valor terminal que irá valer
    para todos os meses subsequentes.
    Ex: curva_default = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]. Nesse caso, para prazos maiores do que 12 meses, a probabilidade de
    default será de 12%.
    """
    # Verifica se algum valor de probabilidade é inválido.
    for i, d in enumerate(curva_default):
        assert (curva_default[i] >= 0 and curva_default[i] <= 100), "Probabilidade inválida."
    tamanho_curva = len(curva_default)
    if tamanho_curva < prazo_max:
        valor_terminal = curva_default[-1]
        lista_terminal = [valor_terminal] * (prazo_max - tamanho_curva)
        curva_default.extend(lista_terminal)

    # Sorteia os valores
    prazos = []
    juros = []
    dividas = []
    for i in range(n_sim):
        prazos.append(montecarlo(prazo_min, prazo_med, prazo_max, prazo_std, 0))
        juros.append(montecarlo(juros_min, juros_med, juros_max, juros_std, 4))
        dividas.append(montecarlo(divida_min, divida_med, divida_max, divida_std, -3))

    cashflows_total = np.zeros(prazo_max+1) # cashflows totais caso nunca  houvesse default
    cashflows_mc = np.zeros(prazo_max + 1)  # cashflows após os eventos de default
    for i in range(n_sim):
        prazo_int = int(prazos[i])
        pmt_div = calc_pmt(dividas[i], juros[i]/100, prazo_int)
        # Inicializa array 'pmts' com os pmts
        pmts = np.array([pmt_div] * prazo_max)
        pmts[prazo_int:] = 0
        pmts = np.insert(pmts, 0, -dividas[i]) # Insere o valor da divida na posicao 0
        cashflows_total += pmts
        # Aplica a funcao que randomiza o recebimento ou nao dos pmts de acordo com as probabilidades da 'curva_default'
        for p in range(1, prazo_int+1):
            pmts[p] = pmts[p] * montecarlo_bool(curva_default[p-1]/100)
        cashflows_mc += pmts

    # IRR com e sem default
    irr_nodefault = calc_irr(cashflows_total)
    irr_mc = calc_irr(cashflows_mc)
    irr = [irr_mc, irr_nodefault]

    total_dividas = sum(dividas) # Total dívidas
    net_cashflows = cashflows_mc.sum() # Net cashflows
    payback = calc_payback(cashflows_mc) # Payback simples
    duration = calc_duration(cashflows_mc, irr_mc) # Duration
    dv01 = calc_dv01(irr_mc, cashflows_mc) # DV01

    # Formata curva default considerada
    curva_default_str = ""
    for i, d in enumerate(curva_default):
        curva_default_str += ' {}[{}],'.format(i,d)
    curva_default_str = curva_default_str[:-1]

    # Gera os gráficos e os armazena em 'data'
    fig = create_figure(prazos, juros, dividas)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return irr, curva_default_str, total_dividas, net_cashflows, payback, duration, dv01, data