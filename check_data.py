import pandas as pd
import sys
import os

# Adiciona path
sys.path.insert(0, 'streamlit')
sys.path.insert(0, '.')

from streamlit.utils.data_loader import (
    carregar_cobertura_movel_4g_uf_anatel,
    carregar_cobertura_movel_5g_uf_anatel
)

print("Carregando dados 4G...")
df_4g = carregar_cobertura_movel_4g_uf_anatel()

if df_4g is not None:
    print("\n=== DADOS 4G ===")
    print(f"Colunas: {list(df_4g.columns)}")
    print(f"Shape: {df_4g.shape}")
    print("\nPrimeiras linhas:")
    print(df_4g.head(10))
    print("\nTipos:")
    print(df_4g.dtypes)
else:
    print("Erro ao carregar 4G")

print("\n" + "="*80)
print("Carregando dados 5G...")
df_5g = carregar_cobertura_movel_5g_uf_anatel()

if df_5g is not None:
    print("\n=== DADOS 5G ===")
    print(f"Colunas: {list(df_5g.columns)}")
    print(f"Shape: {df_5g.shape}")
    print("\nPrimeiras linhas:")
    print(df_5g.head(10))
    print("\nTipos:")
    print(df_5g.dtypes)
else:
    print("Erro ao carregar 5G")

