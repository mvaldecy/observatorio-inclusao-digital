"""
Exemplo de uso do AnalisadorAnatel

Este script demonstra como usar o analisador ANATEL para análise de dados
de conectividade escolar.

Uso no Streamlit:
    from utils.data_loader import get_analisador_anatel
    analisador = get_analisador_anatel(ano=2024)

Uso standalone (fora do Streamlit):
    Carregue o DataFrame manualmente e passe para o AnalisadorAnatel
"""

import sys
import os

# Adiciona o caminho do projeto ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

# Para uso com Streamlit, descomente as linhas abaixo:
# from streamlit.utils.data_loader import get_analisador_anatel
# analisador = get_analisador_anatel(ano=2024)

# Para uso standalone, carregue o DataFrame e crie o analisador:
"""
import pandas as pd
from anatel.analisador_anatel import AnalisadorAnatel

# Carregue seu DataFrame
df = pd.read_parquet('caminho/para/dados.parquet')

# Crie o analisador
analisador = AnalisadorAnatel(df=df, ano=2024)

# Use os métodos do analisador
print("\n=== RESUMO GERAL ===")
print(analisador.resumo_geral())

print("\n=== ESCOLAS POR REGIÃO ===")
print(analisador.escolas_por_regiao())

print("\n=== TOP 10 UFS ===")
print(analisador.escolas_por_uf(top=10))

# Filtrar dados
print("\n=== FILTRAR POR UF (PIAUÍ) ===")
analisador.filtrar_por_uf('PI')
print(f"Total de escolas no Piauí: {len(analisador.df):,}")

# Resetar filtros
analisador.reset_filtros()
print(f"\nApós reset: {len(analisador.df):,} registros")

# Filtrar por região
print("\n=== FILTRAR POR REGIÃO (NORDESTE) ===")
analisador.filtrar_por_regiao('NORDESTE')
print(f"Total de escolas no Nordeste: {len(analisador.df):,}")

# Comparar urbano x rural
print("\n=== COMPARAR URBANO X RURAL ===")
# Substitua 'COLUNA_NUMERICA' por uma coluna numérica real do seu dataset
# print(analisador.comparar_localizacao('COLUNA_NUMERICA'))

# Agrupar por múltiplas colunas
print("\n=== AGRUPAR POR UF E LOCALIZAÇÃO ===")
# print(analisador.agrupar_por('UF', 'LOCALIZACAO'))
"""

if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*60)
    print("EXEMPLOS DE USO DO ANALISADOR ANATEL")
    print("="*60)
    print("\nPara executar os exemplos, descomente o código no arquivo")
    print("e ajuste os nomes das colunas conforme seu dataset.")
