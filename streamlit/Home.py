import streamlit as st
import sys
import os

# Adiciona o diretório streamlit ao path
streamlit_path = os.path.dirname(__file__)
if streamlit_path not in sys.path:
    sys.path.append(streamlit_path)

from components.header import render_header

st.set_page_config(
    page_title="Observatório",
    page_icon="🏠",
    layout="wide"
)

# Renderizar header com logo
render_header("Observatório de Inclusão Digital", "🌐")

st.markdown("""
Bem-vindo ao **Observatório de Inclusão Digital** do Piauí!

Este sistema integra e visualiza dados sobre acesso à tecnologia, conectividade e inclusão digital no Brasil, 
com foco especial nas análises regionais e estaduais.
""")

st.divider()

# Cards com as fontes de dados
st.markdown("### 📊 Fontes de Dados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; background-color: #1e3a5f; margin-bottom: 10px;">
        <h4>🔍 CETIC.br</h4>
        <p><strong>Centro Regional de Estudos para o Desenvolvimento da Sociedade da Informação</strong></p>
        <ul>
            <li>📱 TIC Domicílios (2023-2025)</li>
            <li>👤 TIC Indivíduos (2023-2025)</li>
        </ul>
        <p style="font-size: 0.9em; color: #aaa;">Pesquisas anuais sobre acesso e uso de tecnologia</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding: 20px; border-radius: 10px; background-color: #1e3a5f; margin-bottom: 10px;">
        <h4>📡 ANATEL</h4>
        <p><strong>Agência Nacional de Telecomunicações</strong></p>
        <ul>
            <li>🏫 Conectividade nas Escolas (2022-2025)</li>
            <li>📶 Cobertura Móvel 4G/5G</li>
        </ul>
        <p style="font-size: 0.9em; color: #aaa;">Dados de infraestrutura e cobertura de rede</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Como navegar
st.markdown("### 🗺️ Dashboards Disponíveis")

# Cards dos dashboards
st.markdown("""
<div style="padding: 15px; border-left: 4px solid #4CAF50; background-color: #1a1a1a; margin-bottom: 15px; border-radius: 5px;">
    <h4>📱 CETIC - Domicílios</h4>
    <p>Análise de acesso à internet, dispositivos e tecnologia nos domicílios brasileiros. 
    Visualize indicadores por região, estado, área (urbana/rural), classe social e renda.</p>
</div>

<div style="padding: 15px; border-left: 4px solid #2196F3; background-color: #1a1a1a; margin-bottom: 15px; border-radius: 5px;">
    <h4>👤 CETIC - Indivíduos</h4>
    <p>Análise do comportamento individual no uso da internet, redes sociais, dispositivos móveis e atividades online.
    Compare perfis por faixa etária, escolaridade, gênero e localização.</p>
</div>

<div style="padding: 15px; border-left: 4px solid #FF9800; background-color: #1a1a1a; margin-bottom: 15px; border-radius: 5px;">
    <h4>🏫 Conectividade nas Escolas</h4>
    <p>Dados da ANATEL sobre infraestrutura de internet em escolas públicas e privadas.
    Analise velocidades de conexão, tipos de tecnologia e cobertura por município.</p>
</div>

<div style="padding: 15px; border-left: 4px solid #9C27B0; background-color: #1a1a1a; margin-bottom: 15px; border-radius: 5px;">
    <h4>📡 Cobertura Móvel</h4>
    <p>Dados de cobertura de rede móvel 4G e 5G da ANATEL.
    Visualize a evolução da cobertura por UF e região ao longo do tempo.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Funcionalidades
st.markdown("### 🔍 Funcionalidades")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📊 Análise Visual**
    - Gráficos interativos
    - Mapas geográficos
    - Tabelas dinâmicas
    """)

with col2:
    st.markdown("""
    **🎯 Filtros Avançados**
    - Por região/estado
    - Por período
    - Por categorias
    """)

with col3:
    st.markdown("""
    **💾 Exportação**
    - Download de dados
    - Relatórios customizados
    - Análise offline
    """)

st.divider()

st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    <p><em>Desenvolvido pelo Observatório de Inclusão Digital - Governo do Estado do Piauí</em></p>
    <p style="font-size: 0.9em;">Utilize o menu lateral (☰) para começar sua análise</p>
</div>
""", unsafe_allow_html=True)

