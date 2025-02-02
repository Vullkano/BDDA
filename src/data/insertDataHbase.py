import happybase
import pandas as pd
from pathlib import Path
import os

# Conectar ao HBase
def conectar_hbase():
    try:
        connection = happybase.Connection('localhost', port=9090, autoconnect=True)
        connection.open()
        print("\nConexão com HBase bem-sucedida!\n")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao HBase: {e}")
        exit(1)  # Sair do script se a conexão falhar

# Função para listar as tabelas existentes no HBase
def listar_tabelas(connection):
    tables = connection.tables()
    print("Tabelas no HBase:")
    for table in tables:
        print(table)

# Função para criar uma tabela no HBase
def criar_tabela(connection, table_name, column_family='info'):
    if table_name not in connection.tables():
        connection.create_table(table_name, {column_family: dict()})
        print(f"Tabela '{table_name}' criada com a coluna '{column_family}'.")
    else:
        print(f"Tabela '{table_name}' já existe.")

# Carregar os CSVs para um DataFrame
def carregar_csv():
    base_dir = Path(os.getcwd()).resolve().parent.parent
    processed_data = base_dir / 'data' / 'processed'
    artist_details_df = pd.read_csv(processed_data / "artist_details.csv")
    artist_tracks_df = pd.read_csv(processed_data / "artist_tracks.csv") # , nrows=100
    return artist_details_df, artist_tracks_df

# Função para inserir dados no HBase utilizando batches
def insert_data_to_hbase_with_batch(connection, df, table_name, batch_size=1000):
    table = connection.table(table_name)
    batch = table.batch(batch_size=batch_size)  # Define o tamanho do batch

    for index, row in df.iterrows():
        info_table = {}
        for column in df.columns:
            value = row[column]

            if pd.isna(value):
                value = ""  # Valor padrão para NaN
            elif isinstance(value, (int, float)):
                value = str(value)

            info_table[f'info:{column}'] = bytes(value, 'utf-8')

        # Usar 'track_id' como rowkey na tabela 'artist_tracks'
        if table_name == 'artist_tracks' and 'track_id' in row:
            rowkey = str(row['track_id'])
        elif 'artist_id' in row:  # Manter 'artist_id' na tabela artist_details
            rowkey = str(row['artist_id'])
        else:
            rowkey = str(index)  # Caso não tenha ID, usa o índice como fallback


        try:
            batch.put(rowkey, info_table)  # Adiciona ao batch
        except Exception as e:
            print(f"Erro ao inserir rowkey {rowkey}: {e}")

    try:
        batch.send()  # Envia os dados restantes no batch para o HBase
        print(f"Batch enviado com sucesso para a tabela '{table_name}'.")
    except Exception as e:
        print(f"Erro ao enviar batch para a tabela '{table_name}': {e}")

# Função para visualizar uma tabela no HBase (scan)
def visualizar_tabela(connection, table_name, row_limit=10):
    table = connection.table(table_name)
    rows = table.scan(limit=row_limit)
    print(f"\nVisualizando as primeiras {row_limit} linhas da tabela '{table_name}':\n")
    for key, data in rows:
        print(f"RowKey: {key}")
        for column, value in data.items():
            print(f"{column}: {value.decode('utf-8')}")
        print("-" * 50)

# Função principal para executar as operações
def main():
    # Conectar ao HBase
    connection = conectar_hbase()

    # Listar tabelas existentes
    listar_tabelas(connection)

    # Carregar dados
    artist_details_df, artist_tracks_df = carregar_csv()

    # Nome das tabelas
    Nome_details = 'artist_details'
    Nome_tracks = 'artist_tracks'

    # Criar tabelas no HBase se não existirem
    criar_tabela(connection, Nome_details)
    criar_tabela(connection, Nome_tracks)

    # Inserir dados nas tabelas utilizando batches
    insert_data_to_hbase_with_batch(connection, artist_details_df, Nome_details, batch_size=1000)
    insert_data_to_hbase_with_batch(connection, artist_tracks_df, Nome_tracks, batch_size=1000)

    # Visualizar conteúdo de uma tabela (exemplo)
    visualizar_tabela(connection, Nome_details, row_limit=2)  # Altere o limite conforme necessário
    visualizar_tabela(connection, Nome_tracks, row_limit=2)

    # Fechar a conexão
    connection.close()

    print("Dados importados para o HBase com sucesso!")

if __name__ == '__main__':
    main()
