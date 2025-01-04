# Exemplo de código para obter informações de uma faixa utilizando o Track ID no Spotify

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

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
            results = sp.search(q=artist_name, type='artist', limit=1)

            if results['artists']['items']:
                artist = results['artists']['items'][0]
                api_artist_name = artist['name']
                if api_artist_name.lower().strip() == artist_name.lower().strip():
                    artist_ids.append(artist['id'])
                    followers.append(artist['followers']['total'])
                    popularity.append(artist['popularity'])
                    genres.append(";".join(artist['genres']))
                    image_urls.append(artist['images'][0]['url'] if artist['images'] else None)
                else:
                    artist_ids.append(None)
                    followers.append(None)
                    popularity.append(None)
                    genres.append(None)
                    image_urls.append(None)
            else:
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

    df['artist_id'] = artist_ids
    df['followers'] = followers
    df['popularity'] = popularity
    df['genres'] = genres
    df['image_url'] = image_urls

    cols = ['artist_id'] + [col for col in df.columns if col != 'artist_id']
    df = df[cols]

    return df


def get_artists_info_by_ids(artist_ids, sp):
    artists_data = {}

    for artist_id in artist_ids:
        try:
            artist = sp.artist(artist_id)

            artist_data = {
                'artist_id': artist['id'],
                'artist_name': artist['name'],
                'genres': ', '.join(artist['genres']),
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'image_url': artist['images'][0]['url'] if artist['images'] else None
            }

            artists_data[artist['name']] = artist_data

        except Exception as e:
            print(f"Erro ao buscar informações do artista com ID {artist_id}: {e}")

    return artists_data


# Wikipedia
def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_artist_birth_date(artist_name):
    url = f"https://en.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})

        if infobox:
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header and "Born" in header.text:
                    birth_date_cell = row.find("td")
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


def calculate_age(birth_date):
    try:
        birth_year = int(birth_date)
        current_year = datetime.datetime.now().year
        return int(current_year - birth_year)
    except Exception as e:
        print(f"Erro ao calcular a idade: {e}")
        return None


def update_artist_ages(df):
    ages = []

    for artist_name in df['artist_name']:
        birth_date = get_artist_birth_date(artist_name)
        if birth_date:
            age = calculate_age(birth_date)
            ages.append(int(age))
        else:
            ages.append(None)

    df['age'] = ages
    return df


def get_artist_id_ind(artist_name):
    """
    Pesquisa o ID de um artista no Spotify com base no nome.
    """
    results = sp.search(q=artist_name, type='artist', limit=1)
    if results['artists']['items']:
        artist = results['artists']['items'][0]
        return artist['id'], artist['name']
    else:
        return None, f"Artista '{artist_name}' não encontrado."


def get_artist_name_by_id(artist_id):
    """
    Pesquisa o nome de um artista no Spotify com base no seu ID.
    """
    try:
        artist = sp.artist(artist_id)
        return artist['name']
    except Exception as e:
        return f"Erro ao buscar o artista com ID '{artist_id}': {e}"


if __name__ == "__main__":

    client_id = "ca14c7679c394052af165d2168f3361f"
    client_secret = "8b250ef320964c2a9197f5453f3c449d"

    # Configuração do cliente e da autorização
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="https://localhost:1234/callback",
        scope="user-library-read",
        requests_timeout=15))  # Definindo a scope necessária

    test_artists = ['Anitta', "Agnes"]
    for artist in test_artists:
        artist_id, artist_name = get_artist_id_ind(artist)
        print(f"ID: {artist_id}, Nome: {artist_name}\n")

    test_ids = ['7FNnA9vBm6EKceENgCGRMb', '6SsTlCsuCYleNza6xGwynu', '2gBjLmx6zQnFGQJCAQpRgw',
                "6hyMWrxGBsOx6sWcVj1DqP", "0Q9slhIaEgg190iG8udYIV", "1mYsTxnqsietFxj1OgoGbG"]
    for artist_id in test_ids:
        artist_name = get_artist_name_by_id(artist_id)
        print(f"ID: {artist_id}, Nome: {artist_name}")

    x = get_artists_info_by_ids(test_ids, sp)