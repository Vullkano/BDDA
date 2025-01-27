-- Carregar o arquivo CSV com o caminho correto dentro do contêiner
data = LOAD '/data/processed/artist_details.csv' USING PigStorage(',') AS (artist_name:chararray, gender:chararray, age:int, country_born:chararray, artist_id:int, followers:int, popularity:int, genres:chararray, image_url:chararray);

-- Dividir a coluna 'genres' em uma lista de gêneros
genres_list = FOREACH data GENERATE artist_name, gender, age, country_born, artist_id, followers, popularity, TOKENIZE(genres, ';') AS genre_array;

-- Explodir a lista de gêneros para que cada gênero seja uma linha separada
exploded_data = FOREACH genres_list GENERATE FLATTEN(genre_array) AS genre, 1 AS count;

-- Agrupar os dados por gênero
grouped_data = GROUP exploded_data BY genre;

-- Contar as ocorrências de cada gênero
counted_data = FOREACH grouped_data GENERATE group AS genre, SUM(exploded_data.count) AS genre_count;

-- Armazenar o resultado no diretório correto dentro do contêiner
STORE counted_data INTO '/data/processed/genres_count' USING PigStorage(',');
