"""
Página Streamlit: Desenvolvimento Territorial - Municípios do Piauí

Análise de dados populacionais e alfabetização por raça/cor nos municípios do Piauí
Fonte: Territórios de Desenvolvimento - PCD/TEA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Adiciona a raiz do projeto ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from utils.data_loader import get_analisador_pcd, get_anos_disponiveis_pcd
from components.header import criar_header

# ============================================================================
# Configuração da Página
# ============================================================================

st.set_page_config(
    page_title="Municípios PI - PCD/TEA",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header da página
criar_header(
    titulo="📍 Desenvolvimento Territorial - Piauí",
    descricao="""
    Análise de dados populacionais e alfabetização por raça/cor 
    nos municípios do estado do Piauí.
    """,
    icon="📍"
)

# ============================================================================
# Sidebar - Filtros
# ============================================================================

st.sidebar.title("⚙️ Filtros")

# Verificar anos disponíveis
anos_disponiveis = get_anos_disponiveis_pcd()

if not anos_disponiveis:
    st.error("❌ Nenhum dado encontrado!")
    st.info("Configure a fonte de dados em data_sources.py")
    st.stop()

# Seleção de ano
ano_selecionado = st.sidebar.selectbox(
    "📅 Ano",
    anos_disponiveis,
    index=0
)

# ============================================================================
# Carregamento de Dados
# ============================================================================

try:
    with st.spinner('🔄 Carregando dados dos municípios...'):
        analisador = get_analisador_pcd(ano=ano_selecionado)
        df = analisador.get_dados_atuais()
        
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    import traceback
    st.error(traceback.format_exc())
    st.stop()

if df.empty:
    st.warning("⚠️ Nenhum dado disponível")
    st.stop()

st.sidebar.success(f"✅ {len(df):,} municípios carregados")

# Filtros adicionais
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros")

# Filtro por município
municipios = ['Todos'] + sorted(df['MUNICIPIO'].unique().tolist())
municipio_selecionado = st.sidebar.selectbox("🏙️ Município", municipios)

if municipio_selecionado != 'Todos':
    df = df[df['MUNICIPIO'] == municipio_selecionado]

# Filtro por variação populacional
variacao_opcoes = ['Todos', 'Crescimento', 'Decrescimento']
variacao_selecionada = st.sidebar.selectbox("📈 Variação Populacional", variacao_opcoes)

if variacao_selecionada == 'Crescimento':
    df = df[df['VARIACAO_POPULACAO'] > 0]
elif variacao_selecionada == 'Decrescimento':
    df = df[df['VARIACAO_POPULACAO'] < 0]

# ============================================================================
# Métricas Principais
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏙️ Municípios",
        f"{len(df):,}"
    )

with col2:
    pop_total = df['POPULACAO_2022'].sum()
    st.metric(
        "👥 População Total (2022)",
        f"{pop_total:,.0f}"
    )

with col3:
    taxa_media = df['TAXA_ALFABETIZACAO_GERAL'].mean()
    st.metric(
        "📚 Taxa Alfabetização Média",
        f"{taxa_media:.1f}%"
    )

with col4:
    var_total = df['VARIACAO_POPULACAO'].sum()
    st.metric(
        "📈 Variação Populacional",
        f"{var_total:+,.0f}",
        delta=f"{(var_total / df['POPULACAO_2010'].sum() * 100):.1f}%"
    )

# ============================================================================
# Tabs
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "👥 População",
    "📚 Alfabetização",
    "🎨 Raça/Cor"
])

# ============================================================================
# TAB 1: Visão Geral
# ============================================================================

with tab1:
    st.markdown("### 📊 Panorama Geral dos Municípios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Maiores Municípios (População 2022)")
        top10 = df.nlargest(10, 'POPULACAO_2022')[['MUNICIPIO', 'POPULACAO_2022', 'TAXA_ALFABETIZACAO_GERAL']]
        top10 = top10.copy()
        top10['POPULACAO_2022'] = top10['POPULACAO_2022'].apply(lambda x: f"{x:,.0f}")
        top10['TAXA_ALFABETIZACAO_GERAL'] = top10['TAXA_ALFABETIZACAO_GERAL'].apply(lambda x: f"{x:.1f}%")
        top10.columns = ['Município', 'População', 'Taxa Alfabetização']
        st.dataframe(top10, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 📉 Menor Taxa de Alfabetização")
        bottom10 = df.nsmallest(10, 'TAXA_ALFABETIZACAO_GERAL')[['MUNICIPIO', 'TAXA_ALFABETIZACAO_GERAL', 'POPULACAO_2022']]
        bottom10 = bottom10.copy()
        bottom10['TAXA_ALFABETIZACAO_GERAL'] = bottom10['TAXA_ALFABETIZACAO_GERAL'].apply(lambda x: f"{x:.1f}%")
        bottom10['POPULACAO_2022'] = bottom10['POPULACAO_2022'].apply(lambda x: f"{x:,.0f}")
        bottom10.columns = ['Município', 'Taxa Alfabetização', 'População']
        st.dataframe(bottom10, use_container_width=True, hide_index=True)
    
    # Mapa de distribuição
    st.markdown("---")
    st.markdown("### 🗺️ Distribuição das Taxas de Alfabetização")
    
    fig = px.scatter(
        df,
        x='POPULACAO_2022',
        y='TAXA_ALFABETIZACAO_GERAL',
        size='POPULACAO_TOTAL',
        hover_data=['MUNICIPIO'],
        labels={
            'POPULACAO_2022': 'População 2022',
            'TAXA_ALFABETIZACAO_GERAL': 'Taxa de Alfabetização (%)',
            'POPULACAO_TOTAL': 'População Total'
        },
        title="Relação entre População e Taxa de Alfabetização"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: População
# ============================================================================

with tab2:
    st.markdown("### 👥 Análise Populacional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Crescimento Populacional (2010-2022)")
        df_crescimento = df[df['VARIACAO_POPULACAO'] > 0].nlargest(15, 'VARIACAO_POPULACAO')
        fig = px.bar(
            df_crescimento,
            x='VARIACAO_POPULACAO',
            y='MUNICIPIO',
            orientation='h',
            labels={'VARIACAO_POPULACAO': 'Variação', 'MUNICIPIO': 'Município'},
            title="Top 15 - Maior Crescimento"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📉 Decrescimento Populacional (2010-2022)")
        df_dec = df[df['VARIACAO_POPULACAO'] < 0].nsmallest(15, 'VARIACAO_POPULACAO')
        fig = px.bar(
            df_dec,
            x='VARIACAO_POPULACAO',
            y='MUNICIPIO',
            orientation='h',
            labels={'VARIACAO_POPULACAO': 'Variação', 'MUNICIPIO': 'Município'},
            title="Top 15 - Maior Decrescimento",
            color_discrete_sequence=['#EF553B']
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribuição geral
    st.markdown("---")
    st.markdown("### 📊 Distribuição de População por Município")
    
    fig = px.histogram(
        df,
        x='POPULACAO_2022',
        nbins=30,
        labels={'POPULACAO_2022': 'População'},
        title="Distribuição de Frequência"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: Alfabetização
# ============================================================================

with tab3:
    st.markdown("### 📚 Análise de Alfabetização")
    
    # Estatísticas gerais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Média Geral", f"{df['TAXA_ALFABETIZACAO_GERAL'].mean():.1f}%")
    with col2:
        st.metric("Maior Taxa", f"{df['TAXA_ALFABETIZACAO_GERAL'].max():.1f}%")
    with col3:
        st.metric("Menor Taxa", f"{df['TAXA_ALFABETIZACAO_GERAL'].min():.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Distribuição das Taxas")
        fig = px.box(
            df,
            y='TAXA_ALFABETIZACAO_GERAL',
            labels={'TAXA_ALFABETIZACAO_GERAL': 'Taxa de Alfabetização (%)'},
            title="Box Plot - Taxa de Alfabetização"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🏆 Municípios por Faixa de Alfabetização")
        
        df_faixas = df.copy()
        df_faixas['faixa'] = pd.cut(
            df_faixas['TAXA_ALFABETIZACAO_GERAL'],
            bins=[0, 70, 75, 80, 85, 100],
            labels=['< 70%', '70-75%', '75-80%', '80-85%', '> 85%']
        )
        
        contagem = df_faixas['faixa'].value_counts().sort_index()
        
        fig = px.bar(
            x=contagem.index,
            y=contagem.values,
            labels={'x': 'Faixa', 'y': 'Quantidade de Municípios'},
            title="Municípios por Faixa de Taxa"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Comparação por raça/cor
    st.markdown("---")
    st.markdown("### 🎨 Taxas de Alfabetização por Raça/Cor")
    
    taxas_raca = pd.DataFrame({
        'Raça/Cor': ['Branca', 'Preta', 'Parda'],
        'Taxa Média (%)': [
            df['TAXA_ALFA_BRANCA'].mean(),
            df['TAXA_ALFA_PRETA'].mean(),
            df['TAXA_ALFA_PARDA'].mean()
        ]
    })
    
    fig = px.bar(
        taxas_raca,
        x='Raça/Cor',
        y='Taxa Média (%)',
        title="Comparação das Taxas Médias de Alfabetização",
        text_auto='.1f'
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4: Raça/Cor
# ============================================================================

with tab4:
    st.markdown("### 🎨 Análise de Raça/Cor")
    
    # Distribuição total
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Distribuição da População por Raça/Cor")
        
        pop_total_raca = pd.DataFrame({
            'Raça/Cor': ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
            'População': [
                df['POP_BRANCA'].sum(),
                df['POP_PRETA'].sum(),
                df['POP_AMARELA'].sum(),
                df['POP_PARDA'].sum(),
                df['POP_INDIGENA'].sum()
            ]
        })
        
        fig = px.pie(
            pop_total_raca,
            values='População',
            names='Raça/Cor',
            title="Composição Racial - Piauí"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📈 População por Raça/Cor (em milhares)")
        
        fig = px.bar(
            pop_total_raca,
            x='Raça/Cor',
            y='População',
            title="Total por Categoria"
        )
        fig.update_layout(yaxis_tickformat=',')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela detalhada
    st.markdown("---")
    st.markdown("### 📋 Dados Detalhados por Município")
    
    df_display = df[[
        'MUNICIPIO', 'POPULACAO_2022',
        'POP_BRANCA', 'POP_PRETA', 'POP_PARDA',
        'TAXA_ALFABETIZACAO_GERAL',
        'TAXA_ALFA_BRANCA', 'TAXA_ALFA_PRETA', 'TAXA_ALFA_PARDA'
    ]].copy()
    
    df_display.columns = [
        'Município', 'Pop. 2022',
        'Pop. Branca', 'Pop. Preta', 'Pop. Parda',
        'Taxa Alf. Geral', 'Taxa Alf. Branca', 'Taxa Alf. Preta', 'Taxa Alf. Parda'
    ]
    
    st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)
    
    # Download
    st.markdown("---")
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar dados em CSV",
        data=csv,
        file_name=f"municipios_piaui_pcd_{ano_selecionado}.csv",
        mime="text/csv",
    )

# ============================================================================
# Footer
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Fonte:</strong> Territórios de Desenvolvimento - PCD/TEA</p>
    <p><strong>Estado:</strong> Piauí | <strong>Região:</strong> Nordeste</p>
    <p>Dados populacionais (2010, 2022) e Taxas de Alfabetização por Raça/Cor</p>
</div>
""", unsafe_allow_html=True)
