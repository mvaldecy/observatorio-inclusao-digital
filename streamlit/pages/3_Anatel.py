import streamlit as st
import pandas as pd
import sys
import os

# Adiciona a raiz do projeto e o diretório streamlit ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from utils.data_loader import carregar_dados_anatel
from components.header import render_header

st.set_page_config(page_title="Anatel - Escolas", layout="wide")

render_header("Dados ANATEL - Conectividade Escolas", "🏫")

st.sidebar.title("⚙️ Configurações")

if st.sidebar.button("🔄 Forçar Recarregamento"):
    df, _ = carregar_dados_anatel(force_download=True)
else:
    df, _ = carregar_dados_anatel()

if df is not None:
    st.success(f"✅ Dados carregados com sucesso! Total de registros: {len(df):,}")
    
    st.subheader("Pré-visualização dos Dados (Top 100)")
    st.dataframe(df.head(100), use_container_width=True)
    
    st.subheader("Informações da Base")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Colunas disponíveis:**")
        st.write(list(df.columns))
    
    with col2:
        st.write("**Resumo estatístico (Amostra 10k):**")
        # Amostra para o describe para evitar gargalo de memória/CPU
        sample_size = min(10000, len(df))
        st.write(df.sample(sample_size).describe(include='all'))
else:
    st.error("❌ Falha ao carregar dados da ANATEL.")
