# Exemplo de código para obter informações de uma faixa utilizando o Track ID no Spotify

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

# Configuração do cliente e da autorização
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="ca14c7679c394052af165d2168f3361f",
    client_secret="8b250ef320964c2a9197f5453f3c449d",
    redirect_uri="https://localhost:1234/callback",
    scope="user-library-read"))  # Definindo a scope necessária

# Artist stats
def get_artist_details(df, column_name, sp):
    """
    Adiciona colunas com informações dos artistas ao DataFrame, com base nos seus nomes.

    Args:
        df (pd.DataFrame): DataFrame contendo os nomes dos artistas.
        column_name (str): Nome da coluna no DataFrame que contém os nomes dos artistas.

    Returns:
        pd.DataFrame: DataFrame atualizado com novas colunas 'artist_id', 'followers', 'popularity', 'genres' e 'image_url'.
    """
    artist_ids = []
    followers = []
    popularity = []
    genres = []
    image_urls = []

    for artist_name in df[column_name]:
        try:
            # Pesquisa o artista na API do Spotify
            if artist_name == "Playboi Carti":
                results = sp.search(q="PlayBoi", type='artist', limit=1)
            else:
                results = sp.search(q=artist_name, type='artist', limit=1)

            if results['artists']['items']:
                artist = results['artists']['items'][0]

                # Verifica se o nome retornado pela API é igual ao nome fornecido
                api_artist_name = artist['name']
                if api_artist_name.lower().strip() == artist_name.lower().strip():
                    artist_ids.append(artist['id'])
                    followers.append(artist['followers']['total'])
                    popularity.append(artist['popularity'])
                    genres.append(", ".join(artist['genres']))  # Concatena os géneros numa string
                    image_urls.append(artist['images'][0]['url'] if artist['images'] else None)
                else:
                    # Se os nomes não coincidirem, adiciona None
                    print(f"Nome fornecido: {artist_name}, Nome retornado pela API: {api_artist_name}")
                    artist_ids.append(api_artist_name)
                    followers.append(None)
                    popularity.append(None)
                    genres.append(None)
                    image_urls.append(None)
            else:
                # Caso o artista não seja encontrado
                artist_ids.append(None)
                followers.append(None)
                popularity.append(None)
                genres.append(None)
                image_urls.append(None)
        except Exception as e:
            print(f"Erro ao procurar o artista '{artist_name}': {e}")
            artist_ids.append(None)
            followers.append(None)
            popularity.append(None)
            genres.append(None)
            image_urls.append(None)

    # Adiciona as novas colunas ao DataFrame
    df['artist_id'] = artist_ids
    df['followers'] = followers
    df['popularity'] = popularity
    df['genres'] = genres
    df['image_url'] = image_urls

    # Reorganiza o DataFrame para ter 'artist_id' como a primeira coluna
    cols = ['artist_id'] + [col for col in df.columns if col != 'artist_id']
    df = df[cols]

    return df

# Tracks Stats
def get_artist_tracks(df, sp):
    """
    Obtém todas as faixas e características associadas para cada artista no DataFrame.

    Args:
        df (pd.DataFrame): DataFrame contendo 'artist_id' e 'artist_name'.
        sp (spotipy.Spotify): Instância autenticada da API do Spotify.

    Returns:
        pd.DataFrame: DataFrame com informações das músicas e suas características.
    """
    import time

    def get_with_retries(sp_function, *args, retries=3, delay=1):
        for attempt in range(retries):
            try:
                return sp_function(*args)
            except Exception as e:
                print(f"Erro: {e}. Tentativa {attempt + 1} de {retries}")
                time.sleep(delay)
        print("Falha após múltiplas tentativas.")
        return None

    tracks_data = []

    for index, row in df.iterrows():
        artist_id = row['artist_id']
        artist_name = row['artist_name']

        try:
            print(f"Processando artista {artist_name} ({index + 1}/{len(df)})")
            # Obter as faixas do artista
            results = get_with_retries(sp.artist_top_tracks, artist_id)
            if not results:
                continue

            for track in results['tracks']:
                track_id = track['id']
                track_name = track['name']
                release_date = track['album']['release_date']
                popularity = track['popularity']
                duration_ms = track['duration_ms']

                # Obter as características da música
                audio_features = get_with_retries(sp.audio_features, track_id)
                if audio_features and audio_features[0]:
                    audio_features = audio_features[0]
                else:
                    audio_features = {}

                track_info = {
                    "artist_id": artist_id,
                    "artist_name": artist_name,
                    "track_id": track_id,
                    "track_name": track_name,
                    "release_date": release_date,
                    "popularity": popularity,
                    "duration_ms": duration_ms,
                    "danceability": audio_features.get('danceability'),
                    "energy": audio_features.get('energy'),
                    "key": audio_features.get('key'),
                    "loudness": audio_features.get('loudness'),
                    "mode": audio_features.get('mode'),
                    "speechiness": audio_features.get('speechiness'),
                    "acousticness": audio_features.get('acousticness'),
                    "instrumentalness": audio_features.get('instrumentalness'),
                    "liveness": audio_features.get('liveness'),
                    "valence": audio_features.get('valence'),
                    "tempo": audio_features.get('tempo'),
                    "time_signature": audio_features.get('time_signature'),
                }
                tracks_data.append(track_info)

        except Exception as e:
            print(f"Erro ao obter dados para o artista '{artist_name}': {e}")

    # Criar o DataFrame com as músicas e características
    tracks_df = pd.DataFrame(tracks_data)
    return tracks_df

## Wikipédia

def is_convertible_to_int(s):
    try:
        int(s)  # Tenta converter para int
        return True  # Se não der erro, é conversível
    except ValueError:
        return False  # Caso contrário, não é

# Função para obter a data de nascimento de um artista na Wikipedia
def get_artist_birth_date(artist_name):
    # URL da Wikipedia do artista
    url = f"https://en.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parseando o conteúdo HTML da página
        soup = BeautifulSoup(response.content, "html.parser")

        # Procurando a infobox com as informações biográficas
        infobox = soup.find("table", {"class": "infobox"})

        if infobox:
            # Procurando pela data de nascimento
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header and "Born" in header.text:
                    # Encontrar a data de nascimento na célula da tabela
                    birth_date_cell = row.find("td")
                    # print(birth_date_cell)
                    if birth_date_cell:
                        birth_date = birth_date_cell.text.strip()
                        birth_date_split = birth_date.split(' ')
                        for i in birth_date_split:
                            if "(" in i and ")" in i and "-" in i:
                                age = int(i[i.find("(") + 1:i.find("-")])
                                return age
                        if is_convertible_to_int(birth_date_split[0]):
                            return int(datetime.datetime.now().year) - int(birth_date_split[0])
                        return None
    return None

# Função para calcular a idade com base na data de nascimento
def calculate_age(birth_date):
    try:
        # Tentando extrair o ano da data de nascimento (formato geralmente: 12 January 1990)
        birth_year = int(birth_date)  # Extrair o ano
        current_year = datetime.datetime.now().year
        return int(current_year - birth_year)
    except Exception as e:
        print(f"Erro ao calcular a idade: {e}")
        return None

# Função para atualizar as idades na tabela Artist_details
def update_artist_ages(df):
    ages = []  # Lista para armazenar as idades

    for artist_name in df['artist_name']:
        birth_date = get_artist_birth_date(artist_name)
        if birth_date:
            age = calculate_age(birth_date)
            ages.append(int(age))
        else:
            ages.append(None)  # Caso não consiga encontrar a idade

    # Atualizar a coluna 'age' com as idades obtidas
    df['age'] = ages
    return df


if __name__ == "__main__":

    def get_artist_id_ind(artist_name):
        """
        Pesquisa o ID de um artista no Spotify com base no nome.

        Args:
            artist_name (str): Nome do artista.

        Returns:
            str: ID do artista ou mensagem informativa caso não seja encontrado.
        """
        results = sp.search(q=artist_name, type='artist', limit=1)
        if results['artists']['items']:
            print(results)
            artist = results['artists']['items'][0]
            return artist['id'], artist['name']  # Retorna o ID e o nome completo do artista
        else:
            return None, f"Artista '{artist_name}' não encontrado."

    # Problemas: Nelly, Sebastian Ingrosso, Phili George
    x = ['Playboi']
    for i in x:
        p = get_artist_id_ind(i)
        print(p)