import pyreadstat
import os

# Caminho do arquivo SAV
base_path = os.path.dirname(__file__)
sav_path = os.path.join(base_path, 'tic_domicilios_2025_domicilios_base_de_microdados_v1.0.sav')
parquet_path = os.path.join(base_path, 'tic_domicilios_2025_domicilios_base_de_microdados_v1.0.parquet')

print(f"Convertendo {sav_path}...")
df, meta = pyreadstat.read_sav(sav_path)
df.to_parquet(parquet_path, compression='snappy')
print(f"Convertido com sucesso para {parquet_path}")
print(f"Tamanho original: {os.path.getsize(sav_path) / 1024 / 1024:.2f} MB")
print(f"Tamanho Parquet: {os.path.getsize(parquet_path) / 1024 / 1024:.2f} MB")
