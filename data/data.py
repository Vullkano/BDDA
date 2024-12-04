import kagglehub
import os
import shutil
import pandas as pd


def kaggleDownload(current_directory, links: list[str]):
    for i in links:
        # Faz o download do dataset usando kagglehub
        path = kagglehub.dataset_download(i)
        print("Dataset foi descarregado para:", path)

        # Lista os arquivos no diretório baixado
        files = os.listdir(path)
        print("Arquivos no diretório baixado:", files)

        # Move o dataset para o diretório atual e converte para CSV
        for file_name in files:
            full_file_name = os.path.join(path, file_name)
            print("Processando arquivo:", full_file_name)
            if os.path.isfile(full_file_name):  # Verifica se é ficheiro
                destination_file_name = os.path.join(current_directory, file_name)
                shutil.move(full_file_name, destination_file_name)
                print(f"Ficheiro movido para: {destination_file_name}")
                # Converte para CSV se for um arquivo XLSX
                if destination_file_name.endswith('.xlsx'):
                    df = pd.read_excel(destination_file_name)
                    csv_file_path = destination_file_name.replace('.xlsx', '.csv')
                    df.to_csv(csv_file_path, index=False)
                    os.remove(destination_file_name)  # Remove o arquivo XLSX original
                    print(f"Ficheiro XLSX convertido para CSV: {csv_file_path}")

        # Remove o diretório baixado
        shutil.rmtree(path)
        print(f"Diretório {path} removido.")

    # Remove a pasta kaggle no parent directory
    kaggle_dir = os.path.join(current_directory, 'kaggle')
    if os.path.exists(kaggle_dir):
        shutil.rmtree(kaggle_dir)
        print(f"Diretório {kaggle_dir} removido.")

    print("Ficheiros movidos e convertidos para CSV no diretório atual:", current_directory)


if __name__ == "__main__":
    # Diretório atual onde está o script .py
    current_directory = os.path.dirname(os.path.abspath(__file__))
    links = ["nicolasfierro/spotify-1986-2023", "joebeachcapital/30000-spotify-songs", "adnananam/spotify-artist-stats"]
    kaggleDownload(current_directory, links)