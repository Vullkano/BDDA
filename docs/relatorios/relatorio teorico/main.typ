#import "setup/template.typ": *
#include "setup/capa.typ"
#import "setup/sourcerer.typ": code
// #import "@preview/sourcerer:0.2.1": code

#show: project
#counter(page).update(1)
#import "@preview/algo:0.3.3": algo, i, d, comment //https://github.com/platformer/typst-algorithms
#import "@preview/tablex:0.0.8": gridx, tablex, rowspanx, colspanx, vlinex, hlinex, cellx
#set text(lang: "pt", region: "pt")
#show link: underline
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

#set list(marker: ([•], [‣], [–]))

= HDFS <HDFS>


É um Sistema de ficheiros distribuído projetado para armazenar grandes volumes de dados em hardware comum (_commodity hardware_), Constituído por blocos que são distribuídos (replicados) através de um ou mais nós de um cluster. Durante o upload, os ficheiros são divididos em blocos com uma dimensão padrão, geralmente de 128MB. O sistema segue o princípio WORM (Write Once, Read Many), ou seja, os dados armazenados são imutáveis e não podem ser atualizados após serem escritos. Em clusters com múltiplos nós, os blocos são distribuídos e replicados, com um fator de replicação padrão de 3 (no modo pseudo-distribuído, o fator é 1). Essa abordagem aumenta a probabilidade de _data locality_ e otimiza o desempenho durante o processamento dos dados

- *Configuração em Produção:*

+ NameNode (Master): Processo obrigatório e necessário para o funcionamento do HDFS. Gerencia os metadados, organiza o _namespace_ do sistema de arquivos, controla o acesso aos dados e acompanha a localização dos blocos nos DataNodes. Pode ser configurado com Secondary NameNode ou Standby NameNode para garantir alta disponibilidade.

+ DataNodes (slaves): Armazenam fisicamente os blocos de dados, executam operações de leitura e escrita diretamente para os clientes, replicam blocos e enviam relatórios periódicos ao NameNode.

+ Fator de Replicação: Por padrão, cada bloco de dados é replicado 3 vezes para garantir disponibilidade e tolerância a falhas.

+ Alta Disponibilidade (HA): Pode ser configurada com Zookeeper, garantindo que um NameNode Standby assuma automaticamente em caso de falha do principal.dados.

- *Relação com Bases de Dados Distribuídas*: O HDFS fornece a base para sistemas de Big Data e bases de dados distribuídas, garantindo um armazenamento confiável, eficiente e escalável, essencial para aplicações críticas e de larga escala.




= YARN <YARN>

Introduzido no Hadoop 2.0. Orquestrador de recursos do Hadoop que separa as funcionalidades de "gestão
de recursos" do "motor de
processamento".

- *Configuração em Produção: *
+  ResourceManager (Gerenciador de Recursos): Nó mestre responsável por gerenciar os recursos do cluster. Disponibilizados na forma de containers que são combinações pré-definidas de cores CPU e memória. Monitoriza a capacidade no cluster quando as aplicações terminam e libertam recursos

+ NodeManagers(Gerenciadores de Nós): Executam tarefas específicas em cada nó do cluster. Monitorizam o uso de recursos locais (CPU, memória). Gerenciam containers isolados para garantir a execução segura das aplicações.
+ ApplicationMaster: Criado para cada aplicação individualmente. Negocia recursos diretamente com o ResourceManager. Gerencia e monitoriza a execução das tarefas nos NodeManagers.
+ Container: 

+ Fluxo de Trabalho: O cliente submete uma aplicação ao YARN, e o ResourceManager cria um container inicial para executar o ApplicationMaster. Em seguida, o ApplicationMaster negocia recursos adicionais com o ResourceManager e, uma vez alocados, inicia a execução das tarefas nos containers designados nos NodeManagers.



- *Relação com Bases de Dados Distribuídas*: o o YARN atua como o orquestrador central em sistemas de bases de dados distribuídas, permitindo que os recursos do cluster sejam utilizados de forma eficiente, dinâmica e escalável, garantindo desempenho e alta disponibilidade. Em suma, as suas vantagens são maior escalabilidade, melhor utilização de recursos do cluster e suporta _workloads _não -MapReduce

= MapReduce <MapReduce>

Modelo de programação para processamento paralelo de grandes volumes de dados. Divide o processamento em duas fases: *Map* e *Reduce*


- Configuração em Produção: Executa tarefas em etapas de Map e Reduce distribuídas nos nós do cluster.

+ Fase Map: Dividir os dados de entrada em pequenas partes (splits) para serem processadas em paralelo nos nós do cluster. Produz pares chave-valor intermédios.

+ Fase Reduce: Consolidar os dados agrupados e aplicar funções de agregação.As tarefas _Reduce_ são executadas em *containers* alocados pelo *YARN* nos nós do cluster. Os resultados finais são escritos no HDFS.

- *Relação com Bases de Dados Distribuídas*: O MapReduce é altamente escalável, permitindo adicionar novos nós ao cluster sem comprometer o desempenho. Em caso de falhas, garante tolerância a falhas, redistribuindo automaticamente as tarefas afetadas. Oferece flexibilidade ao suportar diversos formatos de dados e operações complexas, além de assegurar alta disponibilidade, mantendo consistência e confiabilidade no processamento, mesmo em situações adversas.

= HBase <HBase>
- Descrição: Base de dados NoSQL baseado no HDFS, otimizado para leitura e escrita em tempo real.

- Configuração em Produção: Utiliza regiões distribuídas entre nós para armazenar dados.

- Relação com Bases de Dados Distribuídas: Suporta consistência forte e escalabilidade horizontal.

= Phoenix <Phoenix>
- Descrição: Interface SQL para o HBase que facilita consultas estruturadas. 

- Configuração em Produção: Integra-se diretamente com o HBase para otimizar consultas SQL.

- Relação com Bases de Dados Distribuídas: Simplifica a interação com dados distribuídos usando linguagem SQL.

= Hive <Hive>

- Descrição: Ferramenta que permite consultas SQL-like em dados armazenados no HDFS.

- Configuração em Produção: Usa um Metastore para gerenciar metadados e integra-se com motores como Tez e Spark.

- Relação com Bases de Dados Distribuídas: Facilita o particionamento de dados e otimiza consultas distribuídas.

= Hue <Hue>


#set heading(numbering: none)
= Anexos <Anexos>
#set heading(numbering: (level1, level2,..levels ) => {
  if (levels.pos().len() > 0) {
    return []
  }
  ("Anexo", str.from-unicode(level2 + 64)/*, "-"*/).join(" ")
}) // seria so usar counter(heading).display("I") se nao tivesse o resto
//show heading(level:3)

// #image("images/data_integration.png")

