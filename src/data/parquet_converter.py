import pandas as pd
import os
from pathlib import Path

"""
/data/ is in .gitignore. Download your CSV dataset from Kaggle or use your own.
You need to install pandas and pyarrow with pip before you run this script.
"""

def parquet(ficheiros):
    for i in ficheiros:
        # Obter o diretório e nome do ficheiro
        input_file = i
        input_dir = input_file.parent  # Diretório do ficheiro de entrada
        output_file = input_dir / (input_file.stem + '.parquet')  # Caminho do ficheiro de saída

        if input_file.suffix == '.csv':
            df = pd.read_csv(input_file)

        elif input_file.suffix == '.xlsx':
            df = pd.read_excel(input_file)

        else:
            print(f"Formato de ficheiro não suportado: {input_file}")
            continue

        # Verificar e corrigir tipos de dados
        for column in df.columns:
            if df[column].dtype == 'object':  # Colunas com texto
                # Garantir que não há valores mistos
                df[column] = df[column].astype(str)
            elif df[column].dtype.name.startswith('datetime'):
                # Verificar colunas datetime
                df[column] = pd.to_datetime(df[column], errors='coerce')
            else:
                # Garantir que colunas numéricas têm valores válidos
                df[column] = pd.to_numeric(df[column], errors='coerce')

        # Converter para formato Parquet
        try:
            df.to_parquet(path=output_file, engine="pyarrow", compression=None)
            print(f"Ficheiro convertido para Parquet e salvo como: {output_file}")
        except Exception as e:
            print(f"Erro ao converter {input_file} para Parquet: {e}")

# Executar a função principal
if __name__ == "__main__":
    base_dir = Path(os.getcwd()).resolve().parent.parent
    processed_data = base_dir / 'data' / 'processed'
    ficheiros = [processed_data / 'artist_details.csv']
    parquet(ficheiros)
