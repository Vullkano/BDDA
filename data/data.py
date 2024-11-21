import kagglehub
import os
import shutil


def kaggleDownload(current_directory, links:list[str]):
    for i in links:
        # Faz o download do dataset usando kagglehub
        path = kagglehub.dataset_download(i)
        print("Dataset foi descarregado para:", path)

        # Move o dataset para o diretório atual
        for file_name in os.listdir(path):
            full_file_name = os.path.join(path, file_name)
            if os.path.isfile(full_file_name):  # Verifica se é ficheiro
                shutil.move(full_file_name, current_directory)

        print("Ficheiros movidos para o diretório atual:", current_directory)

if __name__ == "__main__":
    # Diretório atual onde está o script .py
    current_directory = os.path.dirname(os.path.abspath(__file__))
    links = ["nicolasfierro/spotify-1986-2023", "joebeachcapital/30000-spotify-songs"]
    kaggleDownload(current_directory, links)