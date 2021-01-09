<h1>Rebel MonteCarlo</h1>
<h2>Descrição</h2>
O objetivo do projeto é criar uma simulação de Monte Carlo em Python para a Rebel.
Baseando-se nos parâmetros fornecidos pelo usuário (prazo, juros e valor das dívidas, e curva esperada de default), o modelo gera simulações estocásticas e retorna métricas financeiras e outras estatísticas.
A implementação foi feita em Flask.

<h2>Inputs</h2>
O usuário preenche os inputs da simulação através via web browser.
Os parâmetros de input são então considerados para gerar valores aleatórios via Monte Carlo. O modelo assume que as variáveis seguem uma distribuição normal truncada pelos valores mínimo e máximo fornecidos. Desse modo, se um número sorteado estiver fora do range mínimo e máximo permitido, outro número é sorteado.

- Número de simulações: número de dívidas que serão geradas na simulação. Cada dívida irá possuir um valor aleatório de prazo, juros e valor de dívida.

- Prazo da dívida (mín, máx, média, desvio padrão): prazo da dívida em meses.

- Taxa de juros: (mín, máx, média, desvio padrão): taxa de juros da dívida, em % a.m.

- Valor da dívida (mín, máx, média, desvio padrão): valor do empréstimo, em R$. A simulação gera apenas valores múltiplos de R$ 1 mil.

- Curva de default (lista de valores): valor esperado de default para cada mês, em %. Não é necessário preencher valores para todos os meses. Nesse caso, o modelo assume o último valor fornecido como um valor terminal que irá valer para todos os meses subsequentes.

Ex: supondo que o número de simulações seja 100 e que o default no primeiro mês seja 5%, espera-se que 5 dos 100 pagamentos do primeiro mês não serão recebidos (o valor real irá depender da aleatoriedade da simulação). A premissa usada é que os pagamentos mensais são independentes e que o valor das parcelas não é reajustado em caso de default. Assim, caso aconteça um evento de default, esse valor é efetivamente perdido e não será recuperado posteriormente.

<h2>Outputs</h2>
- IRR (com default): Taxa interna de retorno do somatório de cashflows das dívidas, considerando os eventos aleatórios de default.

- IRR (sem default): Taxa interna de retorno do somatório de cashflows das dívidas, considerando 100% de adimplência.

- Duration: Macauley duration do portfólio de dívidas, em meses.

- Payback: Payback simples do portfólio, em meses.

- DV01: Mudança esperada no Valor Presente do portfólio para uma mudança de 1bp na taxa de juros, em R$.

- Total dívidas: Somatório das dívidas (desembolso inicial), em R$.

- Net cashflows: Somatório das dívidas e dos pagamentos recebidos, em R$.

- Gráficos e estatísticas: Histogramas dos prazos, juros e dívidas geradas pela simulação. A linha vertical indica a média dos valores sorteados.

- Curva de default: a curva efetivamente usada na simulação, que pode ser diferente da curva inputada caso o número de meses fornecidos seja insuficiente.
