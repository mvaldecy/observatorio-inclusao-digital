"""
Exemplo de uso do módulo PCD

Este script demonstra como:
1. Converter arquivos XLSX para cache
2. Carregar e analisar dados
3. Gerar estatísticas e visualizações
"""

# ============================================================================
# EXEMPLO 1: Converter arquivo XLSX para cache
# ============================================================================

print("=" * 70)
print("EXEMPLO 1: Convertendo arquivo XLSX para cache")
print("=" * 70)

from pcd.conversor_xlsx import ConversorXLSX

# Inicializa o conversor
conversor = ConversorXLSX()

# Exemplo: converter arquivo único
# conversor.processar_arquivo('caminho/para/dados_pcd_2024.xlsx', ano=2024)

# Exemplo: converter múltiplas planilhas
# conversor.processar_multiplas_planilhas('caminho/para/dados_pcd_2024.xlsx', ano=2024)

# Listar arquivos em cache
conversor.listar_arquivos_cache()

print("\n")

# ============================================================================
# EXEMPLO 2: Usar o analisador diretamente (sem Streamlit)
# ============================================================================

print("=" * 70)
print("EXEMPLO 2: Analisando dados com AnalisadorPCD")
print("=" * 70)

import pandas as pd
from pcd.analisador_pcd import AnalisadorPCD
from pcd.estatisticas import EstatisticasPCD

# Criar DataFrame de exemplo para demonstração
# (Em uso real, você carregaria do cache)
dados_exemplo = pd.DataFrame({
    'ano': [2024] * 100,
    'uf': ['SP'] * 50 + ['RJ'] * 50,
    'regiao': ['Sudeste'] * 100,
    'area': ['urbana'] * 70 + ['rural'] * 30,
    'tem_deficiencia': [True] * 100,
    'tipo_deficiencia': ['visual'] * 40 + ['auditiva'] * 30 + ['motora'] * 30,
    'tem_internet': [True] * 70 + [False] * 30,
    'tem_computador': [True] * 50 + [False] * 50,
    'tem_smartphone': [True] * 80 + [False] * 20,
    'usa_tecnologia_assistiva': [True] * 60 + [False] * 40,
    'encontra_barreiras': [True] * 40 + [False] * 60,
    'frequencia_uso': ['diaria'] * 50 + ['semanal'] * 30 + ['raramente'] * 20,
})

# Criar analisador
analisador = AnalisadorPCD(df=dados_exemplo, ano=2024)

# Aplicar filtros
print("\n📍 Filtrando por UF: SP")
analisador.filtrar_por_uf('SP')
print(f"   Registros após filtro: {analisador.contar_registros()}")

print("\n♿ Filtrando por tipo de deficiência: visual")
analisador.filtrar_por_tipo_deficiencia('visual')
print(f"   Registros após filtro: {analisador.contar_registros()}")

# Resetar filtros
print("\n🔄 Resetando filtros...")
analisador.reset_filtros()
print(f"   Registros após reset: {analisador.contar_registros()}")

print("\n")

# ============================================================================
# EXEMPLO 3: Gerar estatísticas
# ============================================================================

print("=" * 70)
print("EXEMPLO 3: Calculando estatísticas")
print("=" * 70)

# Criar objeto de estatísticas
stats = EstatisticasPCD(dados_exemplo)

# Percentual de acesso à internet
perc_internet = stats.percentual_acesso_internet()
print(f"\n📊 Percentual com acesso à internet: {perc_internet:.1f}%")

# Acesso por tipo de deficiência
print("\n📈 Acesso por tipo de deficiência:")
acesso_tipo = stats.acesso_por_tipo_deficiencia()
print(acesso_tipo)

# Distribuição de dispositivos
print("\n📱 Distribuição de dispositivos:")
dispositivos = stats.distribuicao_dispositivos()
print(dispositivos)

# Percentual com barreiras
perc_barreiras = stats.percentual_com_barreiras()
print(f"\n⚠️  Percentual que encontra barreiras: {perc_barreiras:.1f}%")

# Resumo geral
print("\n📋 Resumo geral:")
resumo = stats.resumo_geral()
for chave, valor in resumo.items():
    print(f"   {chave}: {valor}")

print("\n")

# ============================================================================
# EXEMPLO 4: Criar visualizações (apenas estrutura, não exibe)
# ============================================================================

print("=" * 70)
print("EXEMPLO 4: Criando visualizações")
print("=" * 70)

from pcd.visualizacoes import VisualizadorPCD

viz = VisualizadorPCD()

# Criar gráficos (objetos Plotly)
print("\n📊 Criando gráficos Plotly...")

# Gráfico de barras
if not dispositivos.empty:
    fig_barras = viz.grafico_barras_horizontais(
        dispositivos,
        titulo="Distribuição de Dispositivos"
    )
    print("   ✓ Gráfico de barras criado")

# Gráfico de pizza
if not acesso_tipo.empty:
    fig_pizza = viz.grafico_pizza(
        acesso_tipo.set_index('tipo_deficiencia')['percentual'],
        titulo="Acesso por Tipo de Deficiência"
    )
    print("   ✓ Gráfico de pizza criado")

# Gauge de percentual
fig_gauge = viz.grafico_percentual_acesso(
    perc_internet,
    titulo="Acesso à Internet"
)
print("   ✓ Gauge de percentual criado")

print("\n   (Para exibir os gráficos, use fig.show() ou integre com Streamlit)")

print("\n")

# ============================================================================
# EXEMPLO 5: Uso em Streamlit (código de exemplo)
# ============================================================================

print("=" * 70)
print("EXEMPLO 5: Como usar no Streamlit")
print("=" * 70)

codigo_streamlit = """
import streamlit as st
from streamlit.utils.data_loader import get_analisador_pcd
from pcd.estatisticas import EstatisticasPCD
from pcd.visualizacoes import VisualizadorPCD

# Carregar dados (com cache automático)
analisador = get_analisador_pcd(ano=2024)
df = analisador.get_dados_atuais()

# Criar estatísticas
stats = EstatisticasPCD(df)
viz = VisualizadorPCD()

# Exibir métricas
st.metric("Acesso à Internet", f"{stats.percentual_acesso_internet():.1f}%")

# Exibir gráficos
acesso_tipo = stats.acesso_por_tipo_deficiencia()
fig = viz.grafico_barras_horizontais(
    acesso_tipo.set_index('tipo_deficiencia')['percentual'],
    titulo="Acesso por Tipo de Deficiência"
)
st.plotly_chart(fig)
"""

print("\nCódigo de exemplo para Streamlit:")
print("-" * 70)
print(codigo_streamlit)
print("-" * 70)

print("\n")

# ============================================================================
# RESUMO E PRÓXIMOS PASSOS
# ============================================================================

print("=" * 70)
print("✅ PRÓXIMOS PASSOS")
print("=" * 70)

print("""
1. 📥 Coloque seus arquivos XLSX na pasta do projeto

2. 🔄 Converta para cache:
   from pcd.conversor_xlsx import converter_xlsx
   converter_xlsx('caminho/arquivo.xlsx', ano=2024)

3. 🚀 Execute o Streamlit:
   streamlit run streamlit/Home.py
   
4. 📊 Acesse a página "PCD - Inclusão Digital" no menu

5. 🎨 Personalize conforme necessário

📚 Para mais informações, consulte: pcd/README.md
""")

print("=" * 70)
