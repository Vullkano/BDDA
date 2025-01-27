-- Carregar o ficheiro de texto
lines = LOAD '/opt/pig/scripts/lyric.txt' USING TextLoader() AS (line:chararray);

-- Separar cada linha em palavras
words = FOREACH lines GENERATE FLATTEN(TOKENIZE(line)) AS word;

-- Agrupar as palavras e contar ocorrências
grouped_words = GROUP words BY word;
word_count = FOREACH grouped_words GENERATE group AS word, COUNT(words) AS count;

-- Ordenar por número de ocorrências (opcional)
sorted_word_count = ORDER word_count BY count DESC;

-- Salvar o resultado num ficheiro de saída
STORE sorted_word_count INTO '/opt/pig/scripts/output' USING PigStorage(',');