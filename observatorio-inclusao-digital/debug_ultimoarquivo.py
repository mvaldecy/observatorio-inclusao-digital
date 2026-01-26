import pandas as pd
from pathlib import Path

path = Path('conectividade_escolas/parquet')
arquivo = sorted(path.glob('Conectividade_Escolas_*.parquet'))[-1]

df = pd.read_parquet(arquivo)
print(f'Arquivo: {arquivo.name}')
print(f'\nPrimeira linha:')
for col in df.columns:
    if col not in ['Data']:
        print(f'  {col}: {df.iloc[0][col]}')
