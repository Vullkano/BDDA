# Exemplo de código para obter informações de uma faixa utilizando o Track ID no Spotify

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configuração do cliente e da autorização
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",
    client_secret="",
    redirect_uri="",
    scope=""))  # Definindo a scope necessária


def get_artist_details(df, column_name):
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

    # x = ['Drake', 'Post Malone', 'Ed Sheeran', 'J Balvin', 'Bad Bunny',
       # 'Justin Bieber', 'Ozuna', 'Ariana Grande', 'Khalid']
    x = ['Playboi']
    for i in x:
        p = get_artist_id_ind(i)
        print(p)