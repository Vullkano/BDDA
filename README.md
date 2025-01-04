# **BDDA - Bases de Dados Distribuídas Avançadas**  
_Relatório: Componente Técnica_

---

***<h1 style="text-align:center; background-color: #000000; color: #ffffff; padding: 20px; border-radius: 10px; font-family: 'Arial', sans-serif; font-size: 36px; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); letter-spacing: 1px;">A música é influenciada pelo local de nascimento do artista?</h1>***

---

### Tempo para apresentação do projeto:

![Countdown Timer](https://i.countdownmail.com/3w7q9r.gif)

## **Trabalho realizado por:**
- **Diogo Freitas** (104841)  
- **João Francisco Botas** (104782)  
- **Rebeca Sampaio** (126628)

---

## **Índice**
1. [Introdução](#introdução)
2. [Descrição dos conjuntos de dados a utilizar](#descrição-dos-conjuntos-de-dados-a-utilizar)
3. [Metodologia e stack Hadoop](#metodologia-e-stack-hadoop)
4. [Análise ao utilizar a imagem Hue](#análise-ao-utilizar-a-imagem-hue)
5. [Conclusão](#conclusão)

---

## **Introdução**
> **Objetivo**: Apresentar um relatório sobre o uso de bases de dados distribuídas avançadas no contexto do projeto desenvolvido.
Neste relatório, vamos contextualizar as seguintes etapas:

- **A recolha dos datasets essenciais para a recolha do projeto:**  
   Estes datasets foram recolhidos a partir do [Kaggle](https://www.kaggle.com) e da [_API_ da _Spotify_](https://dev.twitch.tv/docs/api/). Durante o processo de recolha, surgiram alguns precalces que precisaram ser corrigidos, e as soluções adotadas serão explicadas mais à frente. Após os ajustes necessários, os dados foram preparados e exportados para o [_HDFS_](https://www.geeksforgeeks.org/hadoop-hdfs-hadoop-distributed-file-system/). Os dois datasets recolhidos foram:
    1. **[_artist_details_](#dataset-1-_artist_details_)**  
       - Este dataset contém informações detalhadas sobre os artistas, incluindo características como o género musical, a idade, o local de nascimento e o género de cada artista.

    2. **[_artist_tracks_](#dataset-2-_artist_tracks_)**  
       - O segundo dataset descreve as características das músicas dos artistas, estando relacionado ao primeiro por meio da chave estrangeira (_foreign key_) associada ao _id_ de cada artista. Através deste dataset, é possível verificar o tipo de música de cada artista, analisando características como a dançabilidade, a duração e a complexidade da música.

   Abaixo, podemos visualizar a relação entre as tabelas, juntamente com as respetivas colunas, que serão explicadas mais detalhadamente à [frente](#descrição-dos-conjuntos-de-dados-a-utilizar).


   <div style="text-align: center;">
       <img src="docs/relatorios/relatorio_pratico_ imgs/drawSQL-BaseDataSets.png" alt="Texto alternativo" style="width: 550px;"/>
   </div>

- **As metodologias utilizadas e a stack _Hadoop_ empregue para a realização do projeto:**

   Neste trabalho, foram empregadas ferramentas como o [**Hadoop**](https://hadoop.apache.org/), [**Hive**](https://hive.apache.org/) e [**GetHue**](https://gethue.com/) para a análise e visualização dos dados. A integração dessas tecnologias permitiu uma análise eficiente e escalável, além de facilitar a interação com grandes volumes de dados. 

    - A [**stack Hadoop**](https://hadoop.apache.org/) foi utilizada para processar e executar as **queries** de forma distribuída e eficiente, aproveitando a escalabilidade do sistema.
    - O [**Hive**](https://hive.apache.org/) foi utilizado para a criação de tabelas e a execução de **queries SQL** sobre os dados armazenados no **HDFS**, proporcionando uma interface familiar para análise de grandes volumes de dados.
    - O [**Hue**](https://gethue.com/) foi empregado para facilitar a visualização dos dados e a criação de **dashboards** interativos, permitindo realizar **queries** de maneira intuitiva e facilitando a análise visual dos resultados.


- **Base do Projeto, Visualizações e Conclusões Extraídas**
   
   Para finalizar com a explicação de cada uma das etapas do projeto, destacam-se os seguintes pontos:

  1. **Objetivos de Estudo**  
     - A principal hipótese formulada pelo grupo é analisar se a região onde o artista nasceu exerce alguma influência nas suas músicas. Para validar essa hipótese, foi essencial comparar e correlacionar as diferentes características das músicas e dos artistas. Este estudo também incluiu a análise de outras propriedades dos artistas, como género, faixa etária e estilos musicais.

  2. **Visualizações**  
     - Todas as visualizações que corroboram as nossas conclusões foram realizadas na plataforma [_Hue_](https://gethue.com/), com exceção das visualizações geradas no _Jupyter Notebook_, que foram utilizadas para análises complementares e outros fins.

  3. **Base do Projeto**  
     - Antes de prosseguir com a explicação detalhada do projeto, é apresentada abaixo uma visão geral da sua estrutura:
   

```
Directory structure:
└── Vullkano-BDDA/
    ├── README.md
    ├── LICENSE
    ├── docker-compose.yml
    ├── hadoop-hive.env
    ├── hue-overrides.ini
    ├── requirements.txt
    ├── data/
    │   ├── .gitignore
    │   └── processed/
    │       ├── artist_details.csv
    │       ├── artist_details.parquet
    │       ├── artist_tracks.csv
    │       └── artist_tracks.parquet
    ├── docs/
    │   ├── Utilizador.txt
    │   ├── enunciado/
    │   └── relatorios/
    │       ├── relatorio pratico imgs/
    │       └── relatorio teorico/
    │           ├── main.typ
    │           └── setup/
    │               ├── capa.typ
    │               ├── esquema_relatorio.typ
    │               ├── sourcerer.typ
    │               └── template.typ
    ├── notebook/
    │   ├── main.ipynb
    │   ├── spotify.db
    │   ├── sql.ipynb
    │   └── .gitignore
    └── src/
        ├── data/
        │   ├── API_Spotify.py
        │   ├── get_data.py
        │   ├── parquet_converter.py
        │   ├── .gitignore
        │   └── __pycache__/
        └── model/
            ├── unsupervised.py
            └── .gitignore

```

  - **`data/`**: Diretório que armazena os datasets utilizados no projeto. Está organizado em duas categorias principais:  
     - **`raw/`**: Dados brutos recolhidos diretamente das fontes originais, sem qualquer tratamento ou modificação.  
     - **`processed/`**: Dados já tratados, limpos e prontos para serem utilizados na análise e visualização.
        e os processed (dados já tratados).
  - **`docs/`**: Contém a documentação do projeto, incluindo o enunciado, relatórios teóricos e práticos.
  - **`notebook/`**: Contém os notebooks utilizados para a análise dos dados e a criação de visualizações.
  - **`src/`**: Contém os scripts utilizados para a recolha, processamento e análise dos dados, bem como a implementação de modelos de aprendizagem não supervisionada.

<progress value="20" max="100" style="width: 100%; height: 25px; border-radius: 10px; background-color: #f0f0f0; border: none;">
  <div style="background-color: #4caf50; height: 100%; width: 5%; border-radius: 10px;"></div>
</progress>

---

## **Descrição dos conjuntos de dados a utilizar**
### Dataset 1: _artist_details_
Como primeiro dataset decidimos, através da API do Spotify, extrair [informações dos artistas](https://developer.spotify.com/documentation/web-api/reference/get-an-artist). Para a seleção dos artistas que iríamos recolher, decidimos retirá-los segundo um link do Kaggle que já agrupava o nome dos artistas e o país dos mesmos. 
- **Fonte do Kaggle**: [Link para o Dataset](https://www.kaggle.com/datasets/hedizekri/top-charts-artists-country)

Após esta fase, o processo subjacente à recolha e preparação dos dados foi executado um pouco da mesma maneira que o _publisher_ deste dataset fez.
- Inspirar num dataset existente (do próprio _publisher_);
- Retirar os dados da API oficial do Spotify;
- Fazer um hand-scrapping a linhas incoerentes ou com dados omissos que a API não recolheu bem.

**Descrição**:
Embaixo podemos ver um exemplo do dataset final
  
| Coluna        | Type         | Description                           |
|----------------|--------------|-------------------------------------|
| `artist_id`      | string      | Id único para o artista (do próprio Spotify)          |
| `artist_name`      | string | Nome do artista (apenas artistas solo) |
| `gender`      | string | Género do Artista |
| `age`      | int | Idade do artista (pode ter algumas incoerências) |
| `country_born`      | string | País em que o artista nasceu          |
| `followers`      | int | Número de seguidores que o artista tem no Spotify          |
| `popularity`      | int | Nível de popularidade do artista medido de 0 a 100          |
| `genres`      | array | Lista de todos os géneros de música do artista          |
| `image_url`      | string | Imagem do artista no Spotify (apenas para confirmar a identidade no processo de limpeza)          |


**Exemplo de Dados** (com _header_):
```csv
artist_name,gender,age,country_born,artist_id,followers,popularity,genres,image_url
Drake,male,37.0,Canada,3TVXtAsR1Inumwj472S9r4,94924678.0,97.0,"canadian hip hop, canadian pop, hip hop, pop rap, rap",https://i.scdn.co/image/ab6761610000e5eb4293385d324db8558179afd9
Post Malone,male,29.0,United States,246dkjvS1zLTtiykXe5h60,46205845.0,91.0,"dfw rap, melodic rap, pop, rap",https://i.scdn.co/image/ab6761610000e5ebe17c0aa1714a03d62b5ce4e0
Ed Sheeran,male,33.0,United Kingdom,6eUKZXaKkcviH0Ku9w2n3V,118303036.0,90.0,"pop, singer-songwriter pop, uk pop",https://i.scdn.co/image/ab6761610000e5eb784daff754ecfe0464ddbeb9
```
### Dataset 2: _artist_tracks_

|Id                    | Type        | Description
|----------------|--------------|-------------------------------------|
| `track_id`            | string          |Identificador único para cada faixa no Spotify.|
| `name`            | string      |É o título da música. Representa o nome da música de como é exibida no Spotify.|
| `album_id`            | string      |É o ID único de um álbum no Spotify. Assim como as músicas, cada álbum também tem um código exclusivo.|
| `album`            | string      |Nome do álbum ao qual a música pertence.|
| `artist_id`            | string      |Identificador único para o artista (do próprio Spotify).|
| `artist_name`            |string              | Nome do artista principal da música.|
| `release_date`            |string              |Data de lançamento da música (em formato AAAA-MM-DD).|
| `duration_ms`             |int              |Duração da música em milissegundos.|
| `explicit`            |boolean      |Indica se a música contém conteúdo explícito (true/false).|
| `danceability`            |float              |Medida de quão dançável é a música (0.0 a 1.0).|
| `energy`                    |float              |Medida de quão energética é a música (0.0 a 1.0).|
| `loudness`            |float              |Volume médio da música em decibéis (dB).|
| `speechiness`            |float              |Mede a presença de palavras faladas na música, variando de 0 (nenhuma fala) a 1 (somente fala).|
| `acousticness`            |float              |Probabilidade de a música ser acústica (0.0 a 1.0).|
| `instrumentalness`    |float              |Probabilidade de a música ser instrumental (0.0 a 1.0).|
| `liveness`            |float              |Probabilidade de a música ter sido gravada ao vivo (0.0 a 1.0).|
| `valence`                    |float               |Medida de positividade ou felicidade transmitida pela música (0.0 a 1.0).|
| `tempo`                    |float              |tempo estimado da música em batidas por minuto (BPM).|
| `time_signature`            |int              |Assinatura de tempo da música (ex: 4, 3).|
| `key`                    |int              |Representa a tonalidade principal da música usando números (0 a 11), |
| `mode`                    |boolean              |Indica se a música está em tom maior ou menor. (0=menor, 1=maior).|
| `is_solo`                    |boolean              |Indica se a música foi feita a solo ou com feature. (0=feature, 1=solo).|
| `cluster_hierarchical`                    |int              |Indica o grupo de agrupamento que foi atribuído no [clustering hierárquico](https://github.com/Vullkano/BDDA/blob/main/src/model/unsupervised.py). (0=menor, 1=maior).|



## **Metodologia e stack Hadoop**
Para a realização deste projeto foi utilizado um /[dockercompose.yml](https://github.com/Vullkano/BDDA/blob/main/docker-compose.yml) que utiliza imagens do DockerHub, ou seja, a estrutura já vem pré-montada.

- ...

## **Análise ao utilizar o Hue**

O processo desenvolvido nesta fase pode ser encontrado na seguinte [pasta](https://github.com/Vullkano/BDDA/tree/main/docs/relatorios/relatorio%20pratico%20imgs).

(...)

Com a tabela dos _artists_details_, conseguimos perceber que a distribuição de artistas nascidos nos EUA e fora dos EUA é bastante parecida. Daí, aos vermos as músicas dos artistas, vamos fazer uma análise exploratória de dados separada, a fim de retirar conclusões e descobrir padrões entre a música ouvida no Spotify para artistas nascidos nos EUA vs fora dos EUA.

### Relação entre danceability e energy (agrupado por is_solo)

Como primeira relação achámos relevante ver se o quão a música era dançável relacionava-se com a energia da mesma; agrupámos para as músicas solo e feature para perceber se os features tendiam para serem músicas mais "mexidas" ou não. Para isso, fizemos a query seguinte:
```sql
SELECT t.*
FROM spotify.hue__tmp_artist_tracks t
JOIN spotify.hue__tmp_artist_details d
  ON t.artist_id = d.artist_id
WHERE d.country_born = 'United States'; -- != 'United States'
```

**NOTA**: Uma das limitações é que só são mostrados 100 músicas nos gráficos de dispersão seguintes. Apesar disso, é válido fazer uma análise para esta amostra.

<details open>
  <summary>Gráfico de dispersão danceability/energy <strong>artistas nascidos nos EUA</strong></summary>
<div style="text-align: center;">
       <img src="docs/relatorios/relatorio_pratico_ imgs/EUA-disp-danceability_energy.jpg" alt="Texto alternativo" style="width: 550px;"/>
</div>
</details>

<details open>
  <summary>Gráfico de dispersão danceability/energy <strong>artistas nascidos fora dos EUA</strong></summary>
<div style="text-align: center;">
       <img src="docs/relatorios/relatorio_pratico_ imgs/noEUA-disp-danceability_energy.jpg" alt="Texto alternativo" style="width: 550px;"/>
</div>
</details>

Após observarmos os gráficos de dispersão para os artistas nascidos nos EUA e os que nasceram fora dos EUA, é possível perceber que as duas variáveis têm pouca correlação entre elas; não é muito evidente. Também reparamos que normalmente as músicas com features são mais energéticas e dançáveis, exceto algumas exceções (principalmente fora dos EUA)

Comparando os EUA com os de fora dos EUA, vemos que a dispersão é mais ou menos parecida. Porém, os artistas nascidos fora dos EUA atingem valores mais altos de energia e têm uma dispersão maior de valores de danceability para músicas com features, do que os nascidos nos EUA. 
De realçar também que as músicas com menos "dançabilidade" têm um tempo de duração inferior relativamente às dos artistas nascidos nos EUA (tamanho das bolhas).

### Relação entre  (agrupado por )

**NOTA**: Uma das limitações é que só são mostrados 100 músicas nos gráficos de dispersão seguintes. Apesar disso, é válido fazer uma análise para esta amostra.

<details open>
  <summary>Gráfico de dispersão  <strong>artistas nascidos nos EUA</strong></summary>
<div style="text-align: center;">
       <img src="docs/relatorios/relatorio_pratico_ imgs/" alt="Texto alternativo" style="width: 550px;"/>
</div>
</details>

<details open>
  <summary>Gráfico de dispersão  <strong>artistas nascidos fora dos EUA</strong></summary>
<div style="text-align: center;">
       <img src="docs/relatorios/relatorio_pratico_ imgs/" alt="Texto alternativo" style="width: 550px;"/>
</div>
</details>


### Média de danceability por artist_name

```sql
SELECT t.artist_name, AVG(t.danceability) AS avg_danceability
FROM spotify.hue__tmp_artist_tracks t
JOIN spotify.hue__tmp_artist_details d
  ON t.artist_id = d.artist_id
WHERE d.country_born = 'United States' -- != 'United States'
GROUP BY t.artist_name
ORDER BY avg_danceability DESC;
```

**NOTA**: Só são considerados os álbuns com 100 maior média de danceability.

<details>
  <summary>Tabela com músicas de artistas nascidos nos EUA (TOP-5 e LOW-5)</summary>

| Posição | Artista (Nascidos nos EUA)          | Mean(danceability)       |
|---------|-------------------------------------|--------------------------|
| 1       | Kanye West                         | 0.9045000000000001       |
| 2       | Jack Harlow                        | 0.8810588235294118       |
| 3       | Lil Pump                           | 0.8731694915254237       |
| 4       | Iggy Azalea                        | 0.8694054054054056       |
| 5       | Regard                             | 0.864                    |
| ...     | ...                                 | ...                      |
| 96      | Wyclef Jean                        | 0.6716569343065695       |
| 97      | Trevor Daniel                      | 0.671235294117647        |
| 98      | Jaymes Young                       | 0.67                     |
| 99      | NF                                 | 0.669                    |
| 100     | Kali Uchis                         | 0.6683636363636363       |

</details>

<details>
  <summary>Tabela com músicas de artistas nascidos nos EUA (TOP-5 e LOW-5)</summary>

| Posição | Artista (Nascidos fora dos EUA)          | Mean(danceability)       |
|---------|------------------------------------------|--------------------------|
| 1       | Drake                                   | 0.8546666666666667       |
| 2       | Daddy Yankee                            | 0.8325                   |
| 3       | Shaggy                                  | 0.8215                   |
| 4       | Nio Garcia                              | 0.8196666666666667       |
| 5       | Dizzee Rascal                           | 0.8168                   |
| ...     | ...                                     | ...                      |
| 96      | Ellie Goulding                          | 0.62                     |
| 97      | Dido                                    | 0.619891891891892        |
| 98      | MØ                                      | 0.6172608695652174       |
| 99      | Alan Walker                             | 0.61572                  |
| 100     | Olly Murs                               | 0.6138076923076923       |

</details>

<br>


Através desta relação queremos comparar os top-5 e os low-5 com média de dançabilidade entre os diferentes artistas. Nos EUA destacamos o Kanye West como a pessoa que produz músicas mais dançáveis, em média, e a Kali Uchis e NF como menos dançáveis (em média). Já dos artistas nascidos fora dos EUA destacamos o Drake e o Olly Murs a produzir músicas mais e menos dançáveis, em média, respetivamente. Os valores não variam muito e também está dependente do número de músicas que cada artista tem na base de dados.

### Média de energy por album

```sql
SELECT t.album, AVG(t.energy) AS avg_energy
FROM spotify.hue__tmp_artist_tracks t
JOIN spotify.hue__tmp_artist_details d
  ON t.artist_id = d.artist_id
WHERE d.country_born = 'United States' -- != 'United States'
GROUP BY t.album
HAVING COUNT(t.track_id) > 2
ORDER BY avg_energy DESC;
```

**NOTA**: Só são considerados os álbuns com 100 maior média de energy.

<details>
  <summary>Tabela com álbuns dos artistas nascidos nos EUA (TOP-5 e LOW-5)</summary>

| Posição | Álbum (Artistas nascidos nos EUA)            | Mean(energy)       |
|----------|----------------------------------------------|--------------------|
| 1        | 4OKI                                         | 0.9470000000000001 |
| 2        | Dirty Vibe (Remixes)                        | 0.93075            |
| 3        | 5OKI                                         | 0.9265             |
| 4        | Blow Me (One Last Kiss)                     | 0.9209999999999999 |
| 5        | My Prerogative                              | 0.92075            |
| ...      | ...                                          | ...                |
| 96       | Play It Again                               | 0.7581666666666668 |
| 97       | No Stylist                                  | 0.758              |
| 98       | 50 Hip Hop Classics                         | 0.7576666666666667 |
| 99       | Tempo (feat. Missy Elliott)                 | 0.757              |
| 100      | Cuz I Love You (Super Deluxe)               | 0.7549687500000002 |
</details>

<details>
  <summary>Tabela com álbuns dos artistas nascidos fora dos EUA (TOP-5 e LOW-5)</summary>

| Posição | Álbum (Artistas nascidos nos EUA)                                        | Mean(energy)       |
|----------|--------------------------------------------------------------------------|--------------------|
| 1        | Novo Sonic System                                                       | 0.9480000000000001 |
| 2        | Big Room EDM Anthems: Best of 2019 (Presented by Spinnin' Records)      | 0.9339999999999999 |
| 3        | New Rave                                                                | 0.92275            |
| 4        | Thinking About You (feat. Ayah Marar)                                   | 0.9031666666666668 |
| 5        | Summer (Remixes)                                                        | 0.88775            |
| ...      | ...                                                                     | ...                |
| 96       | Funk Wav Bounces Vol.1                                                  | 0.7425             |
| 97       | Dance                                                                   | 0.7413636363636363 |
| 98       | Laundry Service                                                         | 0.7413000000000001 |
| 99       | Remind Me to Forget (Remixes)                                           | 0.7412500000000001 |
| 100      | Pocketful Of Sunshine                                                   | 0.7411538461538463 |
</details>

<br>
Através da análise da energia média dos álbuns, destacamos os top-5 e os low-5 álbuns com maior e menor média de energia. Entre os artistas nascidos fora dos Estados Unidos, o álbum "Novo Sonic System" destaca-se como o mais energético, enquanto "Pocketful Of Sunshine" apresenta a menor energia média. Já entre os álbuns de artistas nascidos nos Estados Unidos, "4OKI" lidera como o álbum mais energético, enquanto "Cuz I Love You (Super Deluxe)" aparece como o menos energético. De destacar também o álbum "5OKI" que também aparece no TOP-3 (como o "4OKI"->TOP-1), álbuns de autoria de Steve Aoki, um cantor norte-americano de música eletrónica, normalmente mais "energética".


Embora haja variação na energia média, os valores permanecem em uma faixa relativamente estreita, que reflete uma consistência nos géneros ou estilos musicais representados. No entanto, esses resultados também são influenciados pelo número de músicas presentes em cada álbum na base de dados. Para que os valores não fossem demasiado altos optámos por considerar apenas álbuns com mais de 2 músicas presentes na base de dados.
