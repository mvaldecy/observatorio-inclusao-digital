"""
Exemplo de uso do Data Loader do INEP
Execute: python exemplo_uso_inep.py
"""

import sys
from pathlib import Path

# Adiciona o diretório ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# =============================================================================
# 1. USANDO O DICIONÁRIO DE METADADOS
# =============================================================================

print("=" * 80)
print("1. USANDO O DICIONÁRIO DE METADADOS")
print("=" * 80)

from inep import (
    METADADOS_INEP,
    get_label,
    get_valores,
    formatar_valor,
    listar_categorias,
    listar_variaveis
)

# Listar categorias disponíveis
print("\nCategorias disponíveis:")
for cat in listar_categorias():
    n_vars = len(listar_variaveis(cat))
    print(f"  • {cat}: {n_vars} variáveis")

# Obter informações de uma variável
var = 'TP_DEPENDENCIA'
print(f"\nVariável: {var}")
print(f"  Label: {get_label(var)}")
print(f"  Valores possíveis:")
valores = get_valores(var)
if valores:
    for cod, desc in valores.items():
        print(f"    {formatar_valor(var, cod)}")

# Listar variáveis de internet
print("\nVariáveis de Internet e Computadores:")
for var in listar_variaveis('internet_computadores')[:5]:
    print(f"  • {var}: {get_label(var)}")

# =============================================================================
# 2. CARREGANDO DADOS (requer Streamlit)
# =============================================================================

print("\n" + "=" * 80)
print("2. COMO CARREGAR DADOS (use em scripts Streamlit)")
print("=" * 80)

print("""
# Em um script Streamlit (.py):

from streamlit.utils.data_loader import carregar_educacao_basica_inep

# Carregar dados de 2024
df = carregar_educacao_basica_inep(ano=2024)

if df is not None:
    st.write(f"Total de escolas: {len(df):,}")
    
    # Usar metadados para exibir labels
    from inep import get_label, formatar_valor
    
    # Filtrar por dependência administrativa
    dependencia = st.selectbox(
        'Dependência Administrativa',
        options=[1, 2, 3, 4],
        format_func=lambda x: formatar_valor('TP_DEPENDENCIA', x)
    )
    
    df_filtrado = df[df['TP_DEPENDENCIA'] == dependencia]
    st.write(f"Escolas filtradas: {len(df_filtrado):,}")
""")

# =============================================================================
# 3. ESTRUTURA DE CACHE
# =============================================================================

print("\n" + "=" * 80)
print("3. ESTRUTURA DE CACHE")
print("=" * 80)

print("""
Os dados são salvos em:
  data/cache/inep/{ano}/educacao-basica.parquet

Exemplo:
  data/cache/inep/2024/educacao-basica.parquet
  data/cache/inep/2023/educacao-basica.parquet
  data/cache/inep/2022/educacao-basica.parquet

Formato: Parquet com compressão Snappy (rápido e eficiente)
""")

print("=" * 80)
print("✓ Exemplo concluído!")
print("=" * 80)

