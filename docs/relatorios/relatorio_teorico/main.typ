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

// #page(numbering:none)[
//   #outline(indent: 2em, depth: 7)  
//   // #outline(target: figure)
// ]
#pagebreak()
#counter(page).update(1)

#set list(marker: ([•], [‣], [–]))

= HDFS <HDFS> 

#link("https://www.databricks.com/glossary/hadoop-distributed-file-system-hdfs#:~:text=As%20an%20open%20source%20subproject%20within%20Hadoop%2C%20HDFS,Stores%20large%20amounts%20of%20data.%20...%20Mais%20itens")[HDFS] (Hadoop Distributed File System) é um sistema de ficheiros distribuído projetado para armazenar grandes volumes de dados em _hardware_ comum (_commodity hardware_). É constituído por blocos que são distribuídos e replicados, através de um ou mais nós de um _cluster_. O sistema segue o princípio WORM (Write Once, Read Many), ou seja, os dados armazenados são imutáveis e não podem ser atualizados após serem escritos.

Num *ambiente de produção* será feito o _upload_ dos dados e os ficheiros serão divididos em blocos com uma determinada dimensão, geralmente de 128MB (conhecida também como a fase de _data ingestion_). Terá um NameNode que guarda os metadados, e onde depois a _client application_ obtém deste NameNode a lista dos DataNodes. Os DataNodes armazenam os blocos de dados e fazem operações de leitura e escrita diretamente para o _client_. Pode ainda ser configurado um Secondary NameNode ou Standby NameNode para garantir alta disponibilidade e que esse outro NameNode assuma automaticamente em caso de falha principal de dados. Para garantir tolerância a falhas geralmente é definido um fator de replicação de 3#footnote[no modo pseudo-distribuído, o fator é 1].

O sistema distribuído em nós garante que grandes volumes de dados sejam armazenados e processados de maneira eficiente e aproveita os conceitos fundamentais de bases de dados distribuídas, como particionamento, na divisão de ficheiros em blocos de dados de tamanho fixo; replicação, para garantir a tolerância a falhas e alta disponibilidade; e escalabilidade, no sentido em que é escalável (vertical e horizontalmente) com base no tamanho do sistema do ficheiro. O HDFS, por estas razões, aborda o teorema CAP, um _trade-off_ entre consistência, disponibilidade e tolerância a partições; no sentido em que se houver desconexão temporária entre os nós, os dados continuam acessíveis, inclusive os sistemas que dependem do HDFS. 




// O HDFS (Hadoop Distributed File System) utiliza conceitos de sistemas distribuídos para armazenar grandes volumes de dados de forma escalável e tolerante a falhas. Aplica particionamento, dividindo os dados em blocos distribuídos entre os nós do cluster; replicação, criando múltiplas cópias para garantir alta disponibilidade; e um modelo de consistência write-once-read-many, simplificando a leitura e evitando conflitos de escrita. O sistema equilibra os princípios do teorema CAP, priorizando consistência e disponibilidade, com tolerância a falhas gerenciada por NameNodes redundantes e replicação automática. Diferente de bases de dados transacionais, o HDFS é otimizado para leitura de grandes volumes, sendo ideal para big data.




= YARN <YARN>

O #link("https://www.geeksforgeeks.org/hadoop-yarn-architecture/")[YARN]#footnote[https://www.linkedin.com/pulse/hadoop-123-rui-cunha/] (Yet Another Resource Negotiator) é uma parte do Hadoop que foi criada para resolver problemas de desempenho na versão 1.0 do Hadoop, onde o #link("https://www.linkedin.com/pulse/understanding-yarn-yet-another-resource-negotiator-madhu-m/")[*Job Tracker*] ficava sobrecarregado#footnote[https://jayvardhan-reddy-v.medium.com/bigdata-part3-hadoop-1-0-architecture-763f51a0f5f]. Introduzido no Hadoop 2.0, o #link("https://jose-antonio-zezinho.medium.com/bigdata-34-hadoop-yarn-bb531e67aa27")[YARN] é agora um sistema eficiente para processar grandes volumes de dados, conhecido como um "#link("https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceModel.html")[_Redesigned Resource Manager_]".

O principal diferencial do YARN é que ele separa a gestão de recursos (quem usa o quê) do processamento de dados. No Hadoop 1.0, o *Job Tracker* fazia tudo sozinho, mas no YARN essa tarefa é dividida entre dois componentes: 
- #link("https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceModel.html")[*Resource Manager*] (RM): É o principal responsável por gerenciar os recursos do cluster. O RM decide como alocar recursos como memória, CPU e outros para as aplicações em execução. Além disso, o RM mantém o controle sobre os recursos disponíveis e assegura que as aplicações recebam os recursos necessários para a execução eficiente.
- #link("https://stackoverflow.com/questions/42078296/role-of-the-applicationmanager-in-yarn")[*Application Manager*] (AM): Cada aplicação submetida ao YARN possui um Application Manager dedicado. O  AM gerencia a execução da aplicação, monitorando o estado e a execução das tarefas, garantindo que sejam processadas corretamente.

O *YARN* permite que diferentes motores de processamento de dados, como *grafos*, *processamento interativo* e em *lote*, processem dados no *HDFS* de forma eficiente. O *YARN* é *escalável*, oferecendo capacidade para gerenciar milhares de nós e clusters, e garante *compatibilidade* com aplicações MapReduce (@MapReduce) existentes. O *YARN* também proporciona *otimização da utilização do cluster* através da alocação dinâmica de recursos e suporta #link("https://medium.com/@edytarcio/arquitetura-multi-tenancy-bb7b47d7ba")[*multi-tenancy*], permitindo que diferentes motores (diferentes _frameworks_ ou sistemas de processamento) acessem e utilizem os mesmos recursos simultaneamente. 

Numa *configuração em produção*, o *YARN* possui as seguintes características: 
+ #link("https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html")[*ResourceManager*] e #link("https://stackoverflow.com/questions/42078296/role-of-the-applicationmanager-in-yarn")[*Application Manager*] $arrow$ referidos anteriormente

+ #link("https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/NodeManager.html")[*NodeManagers*]: O *Node Manager* gere os recursos e o funcionamento de cada nó (máquina) num cluster Hadoop.
  - Envia sinais periódicos sobre o estado do nó ao *Resource Manager*
  - Monitora o uso de recursos, gere logs e pode terminar containers conforme as instruções do *Resource Manager*.
  - Cria e inicia containers quando solicitado pelo *Application Master*

+ #link("https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/WritingYarnApplications.html")[*ApplicationMaster*]: Uma *aplicação* é um trabalho enviado para um sistema. O *Application Master* é responsável por pedir recursos ao *Resource Manager*, acompanhar o progresso e o estado da aplicação.
  - Solicita o container ao *Node Manager*, enviando tudo o que a aplicação precisa para funcionar;
  - Durante a execução, o *Application Master* envia relatórios periódicos sobre o estado da aplicação para o *Resource Manager*.

+ #link("https://stackoverflow.com/questions/14365218/what-is-a-container-in-yarn")[*Container*]: Um *container* é um conjunto de recursos físicos, como memória RAM, núcleos de CPU e espaço em disco, em um único nó.

= MapReduce<MapReduce>

Modelo de programação para processamento paralelo de grandes volumes de dados. Inicializa com _input files_ guardados no HDFS e separa em _splits_. Cada _split_ é executado e depois separado nas fases: *Map* (+ Shuffle and Sort) e  *Reduce*.


Num *ambiente de produção* executa tarefas em etapas de Map e Reduce, distribuídas nos nós do _cluster_.

+ *_Fase Map_*: Dividir os dados de entrada em pequenas partes (_splits_) para serem processadas em paralelo nos nós do _cluster_. Produz pares chave-valor intermédios.

+ *_Fase Reduce_*: Consolida os dados agrupados e ordenados, para aplicar funções de agregação.As tarefas _Reduce_ são executadas em *containers* alocados pelo *YARN* nos nós do _cluster_. Os resultados finais são escritos no HDFS.

#image("images/MapReduce.png")

No MapReduce existe particionamento para dividir dados em blocos processados em paralelo na fase "Map" e redistribui por chaves para a fase de "Reduce". O MapReduce é essencial para dados distribuídos em larga escala (HDFS). 
#pagebreak()
= HBase<HBase> 
O HBase  é uma solução de armazenamento e processamento de dados NoSQL. Diferente das bases de dados relacionais tradicionais, o HBase utiliza tabelas numa coleção de linhas organizadas por famílias de colunas, o que permite um desempenho otimizado ao lidar com conjuntos de dados de larga escala e consultas em colunas específicas. O HBase funciona sobre o Hadoop Distributed File System (HDFS) e aproveita a sua arquitetura distribuída para garantir alta disponibilidade e escalabilidade.
 //É ideal para aplicações que exigem acesso aleatório e consistente a dados estruturados, oferecendo uma solução robusta e de alta performance para cenários com grandes demandas de processamento e armazenamento de informações.

O HBase depende do Hadoop para fornecer um sistema de ficheiros distribuído, confiável e escalável. Portanto, antes de iniciar o HBase, é necessário configurar a infraestrutura, que inclui um _cluster_ Hadoop com HDFS para armazenamento distribuído; o HBase Master para coordenar os _Region Servers_, responsáveis por armazenar e gerir tabelas e partições de dados, bem como processar operações de leitura e escrita. O #link("https://zookeeper.apache.org/ ")[*ZooKeeper*]  também desempenha um papel essencial para coordenar e distribuir a carga de trabalho nos nós do HBase (o que garante consistência). O HBase deve ser instalado em cada nó do _cluster_, com variáveis de ambiente como HBASE_HOME e _JAVA_HOME_ devidamente configuradas. O ficheiro `hbase-site.xml` deve ser ajustado para definir o diretório do HDFS, otimizar limites de memória para _Region Servers_ e habilitar alta disponibilidade (HA) para o HMaster. No `hbase-env.sh`, é importante ajustar os parâmetros de memória JVM para os serviços HBase, a fim de otimizar o desempenho.

O HBase utiliza escalabilidade para dividir tabelas em várias regiões, fragmentadas e distribuídas entre os nós do cluster. A replicação é gerida pelo HDFS, enquanto a fragmentação permite paralelismo e acesso eficiente aos dados nas diferentes regiões. Oferece consistência forte dentro de uma região e consistência eventual em operações globais. A alta disponibilidade é garantida pela realocação automática de regiões em caso de falhas, com logs de escrita a proteger as transações efetuadas.

= Phoenix <Phoenix>
O Phoenix é uma camada de abstração SQL desenvolvida para funcionar diretamente sobre o HBase. Combina a flexibilidade e escalabilidade do HBase com a familiaridade e simplicidade das consultas SQL (mapeia tabelas HBase) e faz transações #link("https://www.databricks.com/glossary/acid-transactions")[*ACID*]#footnote[Atomicidade, Consistência, Isolamento, Durabilidade].

Para o ambiente de produção, é fundamental entender os componentes do Phoenix que garantem a integração com o HBase. Como componentes existem: o Cliente Phoenix, por meio do #link("https://docs.cloudera.com/runtime/7.2.18/phoenix-access-data/topics/phoenix-using-jdbc-driver.html#:~:text=The%20Phoenix%20JDBC%20Driver%20enables%20you%20to%20connect,the%20Phoenix%20classpath%20and%20the%20Phoenix%20JDBC%20URL.")[*_driver_ JDBC*], facilita conexões entre os dados do Phoenix e aplicações que suportem conectividade JDBC; o Phoenix Query Server permite a execução escalável das consultas em ambientes distribuídos; o Phoenix Compiler otimiza as consultas SQL, traduzindo-as em comandos eficientes para o HBase. Associado à replicação, o Phoenix aproveita o suporte nativo do HBase para replicação de dados, ao permitir consultas SQL diretamente em réplicas secundárias. Isso não apenas aumenta a disponibilidade de dados, mas também melhora significativamente o desempenho de leitura em sistemas de produção.

Do HBase, o Phoenix herda a escabilidade e o processamento paralelo, ou seja, organiza as tabelas em regiões distribuídas por vários nós do _cluster_. A replicação, gerida pelo HDFS subjacente, garante alta disponibilidade e tolerância a falhas, enquanto_ logs_ de escrita asseguram a recuperação de transações; as transações ACID asseguram a integridade e confiabilidade dos dados.
#pagebreak()
= Hive <Hive>

// O #link("https://aws.amazon.com/pt/what-is/apache-hive/")[Hive] é uma solução de _data warehouse_ em ambientes Hadoop que permite a análise e a consulta de grandes conjuntos de dados armazenados em Hadoop. Utiliza uma linguagem chamada HiveQL, que é semelhante ao SQL, para possibilitar a pessoas sem experiência em programação, que conheçam SQL, poderem acessar e processar dados na escala dos _petabytes_; utiliza também um componente chamado Metastore (HMS) para armazenar metadados das tabelas.

O #link("https://aws.amazon.com/pt/what-is/apache-hive/")[*Hive*] é um sistema de armazenamento e consulta de dados para o ecossistema *Apache Hadoop*, desenvolvido inicialmente pelo #link("https://www.databricks.com/br/glossary/apache-hive")[*Facebook*]. É usado principalmente como uma solução de #link("https://cloud.google.com/learn/what-is-a-data-warehouse")[*data warehouse*] em ambientes Hadoop, permitindo a análise e consulta de grandes conjuntos de dados armazenados no *HDFS*. O Hive utiliza uma linguagem de consulta chamada #link("https://www.tutorialspoint.com/hive/hiveql_select_where.htm")[*HiveQL*], que é semelhante ao *SQL*, facilitando a interação com os dados para analistas que possuem conhecimento em SQL, mas não necessariamente em programação Java.

O Hive implementa uma abstração sobre os dados no HDFS, permitindo que sejam acedidos de forma mais simples através de comandos #link("https://pt.wikipedia.org/wiki/Linguagem_de_manipula%C3%A7%C3%A3o_de_dados")[*DML*] (Data Manipulation Language), como em bases de dados tradicionais. Ele também conta com um componente importante chamado #link("https://docs.cloudera.com/cdp-private-cloud-base/7.1.9/hive-hms-overview/topics/hive-hms-introduction.html")[*Metastore*], que armazena metadados sobre a estrutura e localização dos dados, ajudando na organização e otimização das consultas. Apesar de ser uma solução poderosa, o Hive apresenta algumas limitações em comparação com sistemas de bases de dados tradicionais. Por exemplo:

- *UPDATE* não é suportado.
- Não existem transações, #link("https://issues.apache.org/jira/browse/HIVE-20346")[_rollbacks_] ou níveis de isolamento transacional.
- Não há suporte para *chaves primárias*, *estrangeiras* ou outras restrições de integridade declarativas.
- Dados mal formatados são representados como *NULL*.

#quote[Desde a #link("https://cwiki.apache.org/confluence/display/hive/hive+transactions")[versão 0.14], o Hive oferece suporte a *transações ACID*, utilizando *MapReduce* ou *Tez* para garantir confiabilidade no processamento de dados.]

O Hive é composto por vários componentes, incluindo:

- #link("https://lakefs.io/blog/hive-metastore-why-its-still-here-and-what-can-replace-it/")[*Metastore*]: armazena os metadados das tabelas.
- #link("https://cwiki.apache.org/confluence/display/Hive/HiveJDBCInterface")[*Driver*]: responsável pela compilação e otimização das consultas.
- #link("https://docs.informatica.com/data-engineering/data-engineering-quality/10-2-1/big-data-management-user-guide/introduction-to-informatica-big-data-management/big-data-management-engines/hive-engine-architecture.html")[*Engine*]: executa as consultas, usando *MapReduce* ou *Spark*.

No que diz respeito à *fragmentação*, o Hive suporta o #link("https://delta.io/blog/pros-cons-hive-style-partionining/")[*particionamento*] de tabelas para melhorar a organização dos dados e também permite o #link("https://sparkbyexamples.com/apache-hive/hive-bucketing-explained-with-examples/")[_*bucketing*_], que ajuda na melhor distribuição dos dados. Além disso, o Hive otimiza as consultas através de #link("https://drill.apache.org/docs/partition-pruning-introduction/")[*_pruning_ de partições*], ou seja, só processando as partições relevantes para a consulta.



= Hue <Hue>

O Hue (Hadoop User Experience) é uma interface gráfica de utilizador de código aberto, baseada na Web. O Hue agrupa vários projetos de ecossistemas do Hadoop diferentes numa única interface configurável, atuando como uma ferramenta de _front-end_ para aplicações executadas no _cluster_ (que seja mais "user-friendly"). //O aplicativos no Hue, como os editores do Hive e do Pig, dispensam a necessidade de fazer login no cluster para executar scripts interativamente usando o shell de cada aplicativo. Depois que um cluster for iniciado, você pode interagir totalmente com os aplicativos usando o Hue ou uma interface similar

A configuração do HUE envolve instalar a ferramenta num servidor dedicado, conectá-la aos serviços do Hadoop (como Hive, HBase, entre outros) e configurar numa base de dados _back-end_ (geralmente MySQL ou PostgreSQL) para armazenar informação. Tem associado um editor SQL para consultas Hive e HBase; um File Browser para navegar no HDFS e um Job Browser para monitorizar os _jobs_. Por estas componentes torna-se uma ferramenta útil no ambiente de produção, pois permite ver todas as componentes adjacentes, numa interface amigável e intuitiva. Para otimização, é importante ajustar os limites de memória, conexões simultâneas e ativar _caching _de consultas frequentes.

 //A segurança é garantida por Kerberos, LDAP e ferramentas como Apache Ranger. O desempenho é otimizado com cache, balanceamento de carga e integração com motores como Tez ou Spark. O monitoramento é realizado com Ambari, Prometheus ou Grafana, e logs detalhados são ativados para auditoria

O Hue suporta particionamento para otimizar consultas, replicação para garantir alta disponibilidade e consistência eventual para manter a integridade dos dados. Além disso, permite executar e monitorizar tarefas distribuídas, aproveitando a localidade dos dados e processamento paralelo.

#set heading(numbering: none)
// = Anexos <Anexos>
#set heading(numbering: (level1, level2,..levels ) => {
  if (levels.pos().len() > 0) {
    return []
  }
  ("Anexo", str.from-unicode(level2 + 64)/*, "-"*/).join(" ")
}) // seria so usar counter(heading).display("I") se nao tivesse o resto
//show heading(level:3)

// #image("images/data_integration.png")

