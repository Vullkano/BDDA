#import "setup/template.typ": *
#include "setup/capa.typ"
#import "setup/sourcerer.typ": code
#show: project
#counter(page).update(1)
#import "@preview/algo:0.3.3": algo, i, d, comment, code //https://github.com/platformer/typst-algorithms
#import "@preview/tablex:0.0.8": gridx, tablex, rowspanx, colspanx, vlinex, hlinex
#set text(lang: "pt", region: "pt")
#show link: set text(rgb("#004C99"))
#show ref: set text(rgb("#00994C"))
#set heading(numbering: "1.")
#show raw.where(block: false): box.with(
  fill: luma(240),
  inset: (x: 0pt, y: 0pt),
  outset: (y: 3pt),
  radius: 3pt,
)

#page(numbering:none)[
  #outline(indent: 2em, depth: 7)  
  // #outline(target: figure)
]
#pagebreak()
#counter(page).update(1)

#set list(marker: ([•], [‣]))

= Introdução <1.Introdução>
- *Contextualização*:  
  Breve introdução sobre Algorithmic Trading (AT) e a relevância de analisar empresas tecnológicas como a NVIDIA, uma das líderes no mercado de semicondutores e GPUs, que apresenta alta volatilidade e atratividade para estratégias quantitativas. *FEITO*
- *Objetivos principais*:  
  Desenvolver e avaliar estratégias algorítmicas para maximizar os retornos em operações com ações da NVIDIA, equilibrando risco e retorno.  *FEITO*
- *Motivação*:  
  - Potencial lucrativo devido à volatilidade e crescimento acelerado da NVIDIA.  
  - Relevância de aplicar inteligência artificial e algoritmos de reforço, alinhados ao mercado-alvo da NVIDIA.  *FEITO*
  
  
- *Estrutura do relatório*:  
  Breve descrição das secções do relatório.

#line(length: 100%)
  
= Problema do Projeto <2.ProblemasProjeto>
- *Definição do problema*:  
  Criar uma abordagem automatizada para negociar ações da NVIDIA com base em dados históricos, utilizando tanto estratégias estatísticas como aprendizagem por reforço.  
- *Motivação para a escolha da NVIDIA*:  
  - Empresa com crescimento significativo, impulsionada pela IA e computação avançada.  
  - Volatilidade alta, ideal para estratégias baseadas em AT.  
- *Desafios específicos*:  
  - Previsibilidade limitada devido à dependência de eventos externos, como anúncios de produtos e regulações.  
  - Avaliação do impacto das flutuações macroeconómicas.

#line(length: 100%)
  
= Dados <3.Dados>
== Descrição dos dados
- Histórico das ações da NVIDIA de 2019 a 2024.  
- Estatísticas básicas:  
  - Média, mediana, e volatilidade diária (aumenta).

== Características
- Análise de tendências nos preços. (sazonalidade -> não tem; ex: Disney sazonalidade)
- Visualizações gráficas:  
  - Evolução do preço ao longo do tempo.  
  - Retornos acumulados por período.
  - _Dashboard_

== Limitações
- Dados históricos não refletem todas as condições futuras (ex.: choques económicos).  
- Dependência de eventos externos como lançamentos de produtos e anúncios financeiros.



= Metodologia <4.Metodologia>
== Aquisição e preparação dos dados
- *Fonte de dados*:  
  Histórico de preços das ações da NVIDIA obtido através de yfinance do Python.  
- *Preparação*:  
  - Limpeza e preenchimento de dados ausentes (não tem, mas importante referir que não tem + falar de feriados).  
  - Transformação de preços em retornos logarítmicos.  
  - Visualização inicial dos preços e retornos.

== Cálculos estatísticos
- Retorno simples e logarítmico.  
- Risco (desvio padrão).  
- Correlação com índices relevantes, como o NASDAQ-100.  

== Estratégias de trading
- *Estratégia 1*:  
  Média móvel exponencial (EMA) para identificar tendências.  
- *Estratégia 2*:  
  ML regressão e/ou classificação.

== Algoritmos de Aprendizagem por Reforço
- *Algoritmo selecionado*:  
  Q-Learning.  
- *Definição do ambiente*:  
  - *Estados*: Preços históricos, retornos, e indicadores técnicos.  
  - *Ações*: Comprar, vender, ou manter.  
  - *Recompensa*: Maximizar o retorno acumulado.  

== Avaliação
- Critérios de desempenho:  
  - *Sharpe Ratio*.  
  - Retorno cumulativo.  
  - Drawdown máximo.  

== Comparação e afinação
- Ajuste dos hiperparâmetros do algoritmo de Q-Learning.  
- Comparação das estratégias estatísticas e de reforço.


= Resultados <Resultados>
== Estratégias estatísticas
- *Desempenho da EMA*:  
  - Efetividade em identificar tendências de alta.  
  - Limitações durante períodos de alta volatilidade.  
- *Desempenho do ML*:  
  - Eficácia em pontos de entrada e saída.  

== Algoritmo de Aprendizagem por Reforço
- *Desempenho inicial*: Resultados antes do ajuste de hiperparâmetros.  
- *Desempenho otimizado*: Impacto da afinação nos retornos e redução de riscos.

== Comparação
- Estatísticas detalhadas das abordagens.  
- Gráficos de evolução dos retornos.  
- Identificação da estratégia mais eficiente.

= Conclusões <Conclusões>
- Resumo dos principais achados.  
- Reflexão sobre os benefícios e limitações do uso de estratégias algorítmicas na negociação das ações da NVIDIA.  
- Implicações práticas para investidores no mercado tecnológico.  
- Sugestões para futuras melhorias:  
  - Inclusão de variáveis externas como sentimento de mercado.  
  - Testes com outros ativos do setor tecnológico.


#set heading(numbering: none)
= Anexos <Anexos>
#set heading(numbering: (level1, level2,..levels ) => {
  if (levels.pos().len() > 0) {
    return []
  }
  ("Anexo", str.from-unicode(level2 + 64)/*, "-"*/).join(" ")
}) // seria so usar counter(heading).display("I") se nao tivesse o resto
//show heading(level:3)
- Código Python relevante.  
- Tabelas auxiliares.  
- Detalhes técnicos adicionais das estratégias e algoritmos.







