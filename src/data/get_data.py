import kagglehub
import os
import shutil
import pandas as pd
from pathlib import Path
import csv

def kaggleDownload(current_directory, links: list[str]):
    """
    Função para descarregar datasets do Kaggle, mover os ficheiros para o diretório atual
    e convertê-los para formatos CSV e Parquet.

    Args:
        current_directory (str): Diretório atual onde os ficheiros serão movidos.
        links (list[str]): Lista de identificadores de datasets no Kaggle.
    """
    # Garantir que o diretório de destino existe
    if not os.path.exists(current_directory):
        os.makedirs(current_directory)
        print(f"Diretório criado: {current_directory}")

    for i in links:
        try:
            # Faz o download do dataset usando kagglehub
            path = kagglehub.dataset_download(i)
            print(f"Dataset '{i}' foi descarregado para: {path}")

            # Lista os arquivos no diretório baixado
            files = os.listdir(path)
            print(f"Arquivos encontrados no diretório baixado: {files}")

            # Move e converte os ficheiros
            for file_name in files:
                full_file_name = os.path.join(path, file_name)
                if os.path.isfile(full_file_name):  # Verifica se é um ficheiro
                    destination_file_name = os.path.join(current_directory, file_name)
                    shutil.move(full_file_name, destination_file_name)
                    print(f"Ficheiro movido para: {destination_file_name}")

                    # Converte para CSV se for XLSX
                    if destination_file_name.endswith('.xlsx'):
                        try:
                            df = pd.read_excel(destination_file_name)
                            csv_file_path = destination_file_name.replace('.xlsx', '.csv')
                            df.to_csv(csv_file_path, index=False, sep=',', encoding='utf-8')
                            os.remove(destination_file_name)  # Remove o XLSX original
                            print(f"Ficheiro XLSX convertido para CSV: {csv_file_path}")
                            destination_file_name = csv_file_path  # Atualiza para o novo ficheiro CSV
                        except Exception as e:
                            print(f"Erro ao converter XLSX para CSV: {e}")

                    # Converte para Parquet se for CSV
                    if destination_file_name.endswith('.csv'):
                        try:
                            # Deteção automática do delimitador
                            with open(destination_file_name, 'r', encoding='utf-8') as f:
                                sniffer = csv.Sniffer()
                                sample = f.read(2048)  # Lê uma amostra para análise
                                delimiter = sniffer.sniff(sample).delimiter
                                print(f"Delimitador detetado: '{delimiter}' no ficheiro {destination_file_name}")

                            # Ler o ficheiro CSV com o delimitador detetado
                            df = pd.read_csv(destination_file_name, sep=delimiter, encoding='utf-8')

                            # Atualizar o ficheiro CSV para usar o separador correto ","
                            df.to_csv(destination_file_name, index=False, sep=',', encoding='utf-8')
                            print(f"Ficheiro CSV atualizado com separador correto: {destination_file_name}")

                            # Convertê-lo para Parquet
                            parquet_file_path = destination_file_name.replace('.csv', '.parquet')
                            df.to_parquet(parquet_file_path)
                            print(f"Ficheiro CSV convertido para Parquet: {parquet_file_path}")
                        except Exception as e:
                            print(f"Erro ao processar o ficheiro CSV {destination_file_name}: {e}")
        except Exception as e:
            print(f"Erro ao processar o dataset '{i}': {e}")

        # Remove o diretório temporário baixado
        try:
            shutil.rmtree(path)
            print(f"Diretório temporário {path} removido.")
        except Exception as e:
            print(f"Erro ao remover o diretório {path}: {e}")

    # Remove a pasta 'kaggle' se existir no diretório atual
    kaggle_dir = os.path.join(current_directory, 'kaggle')
    if os.path.exists(kaggle_dir):
        try:
            shutil.rmtree(kaggle_dir)
            print(f"Diretório {kaggle_dir} removido.")
        except Exception as e:
            print(f"Erro ao remover o diretório {kaggle_dir}: {e}")

    print("Ficheiros movidos e convertidos para CSV e Parquet no diretório atual:", current_directory)


if __name__ == "__main__":
    # Diretório atual onde o script está localizado
    current_directory = Path.cwd()
    data_directory = os.path.join(current_directory.parent, 'data')
    print(current_directory)

    # Lista de links dos datasets no Kaggle
    links = [
        "hedizekri/top-charts-artists-country",  # Países dos artistas
        "jackharding/spotify-artist-metadata-top-10k",  # Idade, género dos artistas
        "rodolfofigueroa/spotify-12m-songs",  # Spotify 12M Songs
    ]

    # Executa o processo de download e conversão
    kaggleDownload(data_directory, links)
