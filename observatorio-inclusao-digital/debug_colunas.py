import pandas as pd
from pathlib import Path

path = Path('conectividade_escolas/parquet')
arquivos = sorted(path.glob('Conectividade_Escolas_*.parquet'))[-3:]

for arquivo in arquivos:
    df = pd.read_parquet(arquivo)
    print(f'\n{arquivo.name}:')
    print(f'  Linhas: {len(df)}')
    print(f'  Tem Data: {"Data" in df.columns}')
    print(f'  Tem SG_UF: {"SG_UF" in df.columns}')
    print(f'  Tem NO_REGIAO: {"NO_REGIAO" in df.columns}')
    print(f'  Tem CONECT_POSSUI_INTERNET: {"CONECT_POSSUI_INTERNET" in df.columns}')
    if 'Data' in df.columns:
        print(f'  Primeiros values de Data: {df["Data"].head(3).tolist()}')
