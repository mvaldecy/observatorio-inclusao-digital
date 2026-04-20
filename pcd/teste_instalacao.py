"""
Script de teste para verificar instalação do módulo PCD

Execute este script para verificar se tudo está funcionando corretamente.
"""

import sys
from pathlib import Path

print("=" * 70)
print("🔍 TESTE DE INSTALAÇÃO - MÓDULO PCD")
print("=" * 70)

# ============================================================================
# Teste 1: Importações
# ============================================================================

print("\n📦 Teste 1: Verificando importações...")

erros = []

try:
    import pandas as pd
    print("   ✓ pandas importado")
except ImportError as e:
    erros.append("pandas")
    print(f"   ✗ pandas: {e}")

try:
    import openpyxl
    print("   ✓ openpyxl importado")
except ImportError as e:
    erros.append("openpyxl")
    print(f"   ✗ openpyxl: {e}")

try:
    import pyarrow
    print("   ✓ pyarrow importado")
except ImportError as e:
    erros.append("pyarrow")
    print(f"   ✗ pyarrow: {e}")

try:
    import plotly
    print("   ✓ plotly importado")
except ImportError as e:
    erros.append("plotly")
    print(f"   ✗ plotly: {e}")

try:
    import streamlit
    print("   ✓ streamlit importado")
except ImportError as e:
    erros.append("streamlit")
    print(f"   ✗ streamlit: {e}")

if erros:
    print(f"\n⚠️  Faltam dependências: {', '.join(erros)}")
    print("   Execute: pip install -r requirements.txt")
else:
    print("\n✅ Todas as dependências instaladas!")

# ============================================================================
# Teste 2: Módulos PCD
# ============================================================================

print("\n📚 Teste 2: Verificando módulos PCD...")

try:
    from pcd.metadados import get_todos_campos
    campos = get_todos_campos()
    print(f"   ✓ metadados.py OK ({len(campos)} campos definidos)")
except Exception as e:
    print(f"   ✗ metadados.py: {e}")

try:
    from pcd.dicionario_dados import DICIONARIO
    print(f"   ✓ dicionario_dados.py OK ({len(DICIONARIO)} campos)")
except Exception as e:
    print(f"   ✗ dicionario_dados.py: {e}")

try:
    from pcd.conversor_xlsx import ConversorXLSX
    print("   ✓ conversor_xlsx.py OK")
except Exception as e:
    print(f"   ✗ conversor_xlsx.py: {e}")

try:
    from pcd.analisador_pcd import AnalisadorPCD
    print("   ✓ analisador_pcd.py OK")
except Exception as e:
    print(f"   ✗ analisador_pcd.py: {e}")

try:
    from pcd.estatisticas import EstatisticasPCD
    print("   ✓ estatisticas.py OK")
except Exception as e:
    print(f"   ✗ estatisticas.py: {e}")

try:
    from pcd.visualizacoes import VisualizadorPCD
    print("   ✓ visualizacoes.py OK")
except Exception as e:
    print(f"   ✗ visualizacoes.py: {e}")

# ============================================================================
# Teste 3: Estrutura de pastas
# ============================================================================

print("\n📁 Teste 3: Verificando estrutura de pastas...")

base_path = Path(__file__).parent.parent

# Verificar pastas principais
pastas = [
    ('pcd', base_path / 'pcd'),
    ('data/cache/pcd', base_path / 'data' / 'cache' / 'pcd'),
    ('streamlit/pages', base_path / 'streamlit' / 'pages'),
    ('streamlit/utils', base_path / 'streamlit' / 'utils'),
]

todas_ok = True
for nome, caminho in pastas:
    if caminho.exists():
        print(f"   ✓ {nome}")
    else:
        print(f"   ✗ {nome} não encontrada")
        todas_ok = False

if todas_ok:
    print("\n✅ Estrutura de pastas OK!")

# ============================================================================
# Teste 4: Arquivos criados
# ============================================================================

print("\n📄 Teste 4: Verificando arquivos criados...")

arquivos_pcd = [
    '__init__.py',
    'README.md',
    'QUICKSTART.md',
    'metadados.py',
    'dicionario_dados.py',
    'conversor_xlsx.py',
    'converter_dados.py',
    'analisador_pcd.py',
    'estatisticas.py',
    'visualizacoes.py',
    'exemplo_uso.py',
]

pcd_path = base_path / 'pcd'
todos_ok = True
for arquivo in arquivos_pcd:
    if (pcd_path / arquivo).exists():
        print(f"   ✓ {arquivo}")
    else:
        print(f"   ✗ {arquivo} não encontrado")
        todos_ok = False

if todos_ok:
    print("\n✅ Todos os arquivos criados!")

# Verificar página Streamlit
pagina_streamlit = base_path / 'streamlit' / 'pages' / '7_PCD_Inclusao_Digital.py'
if pagina_streamlit.exists():
    print("   ✓ Página Streamlit criada")
else:
    print("   ✗ Página Streamlit não encontrada")

# ============================================================================
# Teste 5: Teste funcional básico
# ============================================================================

print("\n🧪 Teste 5: Teste funcional básico...")

try:
    import pandas as pd
    from pcd.analisador_pcd import AnalisadorPCD
    from pcd.estatisticas import EstatisticasPCD
    from pcd.visualizacoes import VisualizadorPCD
    
    # Criar dados de teste
    df_teste = pd.DataFrame({
        'ano': [2024] * 10,
        'uf': ['SP'] * 10,
        'tem_deficiencia': [True] * 10,
        'tipo_deficiencia': ['visual'] * 5 + ['auditiva'] * 5,
        'tem_internet': [True] * 7 + [False] * 3,
        'tem_smartphone': [True] * 8 + [False] * 2,
    })
    
    # Testar analisador
    analisador = AnalisadorPCD(df=df_teste, ano=2024)
    print("   ✓ AnalisadorPCD instanciado")
    
    # Testar filtro
    analisador.filtrar_por_tipo_deficiencia('visual')
    dados_filtrados = analisador.get_dados_atuais()
    assert len(dados_filtrados) == 5, "Filtro não funcionou corretamente"
    print("   ✓ Filtros funcionando")
    
    # Testar estatísticas
    analisador.reset_filtros()
    stats = EstatisticasPCD(analisador.get_dados_atuais())
    perc = stats.percentual_acesso_internet()
    assert perc == 70.0, f"Percentual incorreto: {perc}"
    print("   ✓ Estatísticas funcionando")
    
    # Testar visualizações
    viz = VisualizadorPCD()
    dispositivos = pd.Series({'Smartphone': 8, 'Computador': 5})
    fig = viz.grafico_barras_simples(dispositivos)
    assert fig is not None, "Gráfico não foi criado"
    print("   ✓ Visualizações funcionando")
    
    print("\n✅ Testes funcionais passaram!")
    
except Exception as e:
    print(f"\n❌ Erro nos testes funcionais: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# Teste 6: Verificar dados
# ============================================================================

print("\n💾 Teste 6: Verificando dados em cache...")

cache_path = base_path / 'data' / 'cache' / 'pcd'
arquivos_cache = list(cache_path.glob('*.parquet'))

if arquivos_cache:
    print(f"   ✓ {len(arquivos_cache)} arquivo(s) em cache:")
    for arquivo in arquivos_cache:
        tamanho = arquivo.stat().st_size / 1024  # KB
        print(f"      - {arquivo.name} ({tamanho:.1f} KB)")
else:
    print("   ⚠️  Nenhum arquivo em cache ainda")
    print("      Execute converter_dados.py para adicionar dados")

# ============================================================================
# Resumo Final
# ============================================================================

print("\n" + "=" * 70)
print("📊 RESUMO DO TESTE")
print("=" * 70)

if not erros and todas_ok and todos_ok:
    print("""
✅ INSTALAÇÃO COMPLETA E FUNCIONAL!

🎯 Próximos passos:
1. Coloque seu arquivo XLSX na pasta do projeto
2. Execute: python pcd/converter_dados.py arquivo.xlsx 2024
3. Execute: streamlit run streamlit/Home.py
4. Acesse a página "PCD - Inclusão Digital"

📚 Documentação:
- pcd/README.md - Documentação completa
- pcd/QUICKSTART.md - Guia rápido
- pcd/exemplo_uso.py - Exemplos de código
    """)
else:
    print("""
⚠️  ALGUNS PROBLEMAS ENCONTRADOS

Verifique os erros acima e:
1. Instale dependências: pip install -r requirements.txt
2. Verifique se todos os arquivos foram criados corretamente
3. Execute este teste novamente: python pcd/teste_instalacao.py
    """)

print("=" * 70)
