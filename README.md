# **BDDA - Bases de Dados Distribuídas Avançadas**  
_Relatório componente técnica_

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
4. [Análise ao utilizar a imagem Hue](#análises-e-resultados)
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
### Dataset 1: _Nome do Dataset_
Como primeiro dataset decidimos, através da API do Spotify, extrair [informações dos artistas](https://developer.spotify.com/documentation/web-api/reference/get-an-artist). Para a seleção dos artistas que iríamos recolher, decidimos retirá-los segundo um link do Kaggle que já agrupava o nome dos artistas e o país dos mesmos. 
- **Fonte do Kaggle**: [Link para o Dataset](https://www.kaggle.com/datasets/hedizekri/top-charts-artists-country)

Após esta fase, o processo subjacente à recolha e preparação dos dados foi executado um pouco da mesma maneira que o _publisher_ deste dataset fez.
- Inspirar num dataset existente (do próprio _publisher_);
- Retirar os dados da API oficial do Spotify, nomeadamente:

**Descrição**:
Embaixo podemos ver um exemplo do dataset final
  
| Id         | Nome         | Idade                           |
|----------------|--------------|-------------------------------------|
| `coluna1`      | Inteiro      | Descrição breve da coluna1          |
| `coluna2`      | Texto        | Descrição breve da coluna2          |
| `coluna3`      | Data         | Descrição breve da coluna3          |

**Exemplo de Dados**:
```csv

```

## **Metodologia e stack Hadoop**
Para a realização deste projeto foi utilizado um dockercompose.yml que utiliza imagens do DockerHub, ou seja, a estrutura já vem pré-montada. Este ficheiro cria os containers seguintes:
- ...



