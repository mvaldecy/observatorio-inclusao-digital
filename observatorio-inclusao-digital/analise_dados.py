import pandas as pd
from pathlib import Path
from anatel.cobertura_movel import AnalisadorAnatel

# Carregar dados
print("[INFO] Carregando dados ANATEL...")
analisador = AnalisadorAnatel()
df = analisador.df

print('\nCOLUNAS DISPONÍVEIS NO DATAFRAME COMPLETO:')
print('=' * 80)
for i, col in enumerate(df.columns, 1):
    print(f'{i:2d}. {col}')

print('\n\nINFORMAÇÕES DOS DADOS:')
print('=' * 80)

# Verificar algumas combinações
print(f'\nOperadoras: {df["Operadora"].nunique()} únicas')
print(f'Regiões: {df["Região"].nunique()} únicas')
print(f'UFs: {df["UF"].nunique()} únicas')
print(f'Municípios: {df["Município"].nunique()} únicas')
print(f'Períodos: {df["Período"].nunique()} únicos')

print(f'\n\nOperadoras principais:')
print(df['Operadora'].value_counts().head(10))

print(f'\n\nRegiões:')
print(df['Região'].value_counts())

print(f'\n\nCOMBINAÇÕES INTERESSANTES PARA ANÁLISE:')
print('=' * 80)

# Análise 1: Operadora + Região
print("\n1. COBERTURA POR OPERADORA E REGIÃO:")
analise1 = df.groupby(['Operadora', 'Região'])['Cobertura_4G'].mean().round(2)
print(analise1.head(15))

# Análise 2: Operadora + Tecnologia
print("\n2. COMPARAÇÃO DE OPERADORAS (Média de Cobertura 5G):")
analise2 = df.groupby('Operadora')[['Cobertura_3G', 'Cobertura_4G', 'Cobertura_5G']].mean().round(2)
print(analise2)

# Análise 3: Região vs Tecnologia
print("\n3. COBERTURA POR REGIÃO (4G vs 5G):")
analise3 = df.groupby('Região')[['Cobertura_4G', 'Cobertura_5G', 'Cobertura_3G']].mean().round(2)
print(analise3)

# Análise 4: Setores sem cobertura
print("\n4. SETORES SEM COBERTURA POR REGIÃO:")
sem_4g = df[df['Cobertura_4G'].isna() | (df['Cobertura_4G'] == 0)].groupby('Região').size()
print(sem_4g)

# Análise 5: Distribuição de 5G
print("\n5. PENETRAÇÃO DE 5G POR REGIÃO:")
df_5g = df[df['Cobertura_5G'].notna()]
penetracao_5g = (df_5g[df_5g['Cobertura_5G'] > 0].groupby('Região').size() / df_5g.groupby('Região').size() * 100).round(2)
print(penetracao_5g)

print("\n" + "=" * 80)
print("RECOMENDAÇÕES DE FILTROS E COMBINAÇÕES:")
print("=" * 80)
print("""
✓ Filtro: Operadora + Região (Para ver performance regional de cada operadora)
✓ Filtro: Tipo de Cobertura (Nenhuma | Apenas 3G | 4G | 5G | Múltiplas)
✓ Filtro: Status de Cobertura (Adequada | Inadequada | Nenhuma)
✓ Análise: Comparativo de operadoras por região (Região + Operadora)
✓ Análise: Evolução de 5G (Período + 5G Coverage)
✓ Análise: Lacunas de cobertura (Municípios sem 4G/5G)
✓ Métrica: Setores com cobertura adequada (>50%)
✓ Métrica: Setores em transição (3G → 4G → 5G)
""")
