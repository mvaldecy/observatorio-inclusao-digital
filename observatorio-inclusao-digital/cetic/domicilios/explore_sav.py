import pandas as pd
import pyreadstat

# Caminho do arquivo
file_path = "tic_domicilios_2025_domicilios_base_de_microdados_v1.0.sav"

try:
    # Lendo o arquivo .sav e metadados
    # df contém os dados, meta contém os rótulos das variáveis e valores
    df, meta = pyreadstat.read_sav(file_path)

    print("--- Informações Básicas ---")
    print(f"Número de linhas: {len(df)}")
    print(f"Número de colunas: {len(df.columns)}")
    print("\n--- Primeiras 5 linhas (Amostra) ---")
    print(df.head())

    print("\n--- Dicionário Completo de Variáveis ---")
    # Mostra o nome da coluna e a descrição (label) de todas as colunas
    for col_name, col_label in meta.column_names_to_labels.items():
        print(f"{col_name}: {col_label}")

except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
