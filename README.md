# **BDDA - Bases de Dados Distribuídas Avançadas**  
_Relatório: Componente Técnica_

### Tempo para entrega do projeto:

![Countdown Timer](https://i.countdownmail.com/3w7q9r.gif)

---

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
- A descrição dos 2 datasets utilizados;
- As técnicas empregadas pré-análise dados;
- As visualizações retiradas após visualizar os 2 datasets.

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

## **Análise ao utilizar a imagem Hue**

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
WHERE d.country_born = 'United States';
```

Após observarmos os gráficos de dispersão para os artistas nascidos nos EUA e os que nasceram fora dos EUA, vemos que as 
normalmente as músicas com features são mais energéticas e 