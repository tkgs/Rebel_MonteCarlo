import random
import numpy as np
import numpy_financial as npf
from matplotlib.figure import Figure

def montecarlo(min, med, max, std, round_pts):
    # Retorna um prazo (meses) aleatorio
    # Premissa: se o prazo sorteado for menor que prazo_min inputado ou maior que prazo_max, sorteia novamente
    # round_pts (int): numero de casas decimais para arredondamento

    rand = round(random.gauss(med, std), round_pts)
    max_iter = 100
    iter = 0
    while (rand < min or rand > max) and iter < max_iter:
        rand = round(random.gauss(med, std), round_pts)
        iter += 1
    if iter == max_iter:
        if rand < min:
            rand = min
        elif rand > max:
            rand = max
    return rand

def montecarlo_bool(prob):
    # Se rand < prob, retorna 0 (default). Caso contrario, retorna 1 (nao default)
    return 0 if random.random() < prob else 1

def calc_pmt(PV, i, n):
    # Calcula o PMT da divida usando a formula Price
    return round(PV * ((1+i)**n * i) / ((1+i)**n - 1),2)

def calc_irr(cashflows):
    return npf.irr(cashflows)

def calc_payback(cashflows):
    # Payback simples: tempo para recuperar o principal investido
    investment, cashflows = cashflows[0], cashflows[1:]
    if investment < 0: investment = -investment

    total, periods, cumulative = 0.0, 0, []
    if sum(cashflows) < investment:
        return 0
    for cashflow in cashflows:
        total += cashflow
        if total < investment:
            periods += 1
        cumulative.append(total)
    A = periods
    B = investment - cumulative[periods - 1]
    C = cumulative[periods] - cumulative[periods - 1]
    return A + (B / C)

def calc_duration(cashflows, rate):
    duration = 0
    for t, c in enumerate(cashflows[1:], start=1):
        df = 1 / (1 + rate) ** t
        duration += df * c * t
    return duration / cashflows[0] * -1

def calc_dv01(rate, cashflows):
    return (abs(npf.npv(rate + 0.0001, cashflows)) + abs(npf.npv(rate - 0.0001, cashflows))) / 2

def number_format(num):
    formatos = ['', 'mil', 'milhões']
    magnitude = 0
    while abs(num) >= 1000 and magnitude < len(formatos)-1:
        magnitude += 1
        num /= 1000.0
    return '{:.2f} {}'.format(num, formatos[magnitude])

def create_subplot(axis, x, title, xlabel, bins=15):
    mu = np.mean(x)
    median = np.median(x)
    sigma = np.std(x)

    axis.hist(x, bins)
    # Plota linha vertical que representa a media dos prazos
    ymax = axis.get_ybound()[1]
    axis.autoscale(False)
    axis.vlines(mu, ymin=0, ymax=ymax, color='k', label='mean')
    axis.set_title(title)
    axis.set_xlabel(xlabel)
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu,),
        r'$med=%.2f$' % (median,),
        r'$\sigma=%.2f$' % (sigma,)))
    # Define se o texto com as estatisticas fica a esquerda ou a direita de acordo com o skew do histograma
    if mu < median:
        x_text = 0.02
        horizontalalignment = 'left'
    else:
        x_text = 0.98
        horizontalalignment = 'right'
    axis.text(x_text, 0.8, textstr, transform=axis.transAxes, fontsize=8, horizontalalignment=horizontalalignment)

def create_figure(prazos, juros, dividas, cashflows):
    # Cria instancia do gráfico e ajusta as margens
    fig = Figure(figsize=(11,3))
    fig.subplots_adjust(bottom=0.18, top=0.9, left=0.05, right=0.95)

    # Cria os subgráficos de histogramas
    create_subplot(fig.add_subplot(1, 3, 1), prazos, 'Prazos', 'Meses')
    create_subplot(fig.add_subplot(1, 3, 2), juros, 'Juros', '% a.m.')
    create_subplot(fig.add_subplot(1, 3, 3), dividas, 'Dívidas', 'R$')

    # axis = fig.add_subplot(3, 2, 4)
    # axis.bar(range(1, len(cashflows)), cashflows[1:] / 1000)
    # axis.set_title('PMTs')
    # axis.set_xlabel('R$ mil')
    return fig