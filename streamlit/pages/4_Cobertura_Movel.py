"""
Página de teste - Cobertura Móvel ANATEL
"""
import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório streamlit ao path para encontrar utils
streamlit_dir = str(Path(__file__).parent.parent)
if streamlit_dir not in sys.path:
    sys.path.insert(0, streamlit_dir)

from utils.data_loader import (
    carregar_cobertura_movel_anatel,
    carregar_cobertura_movel_5g_uf_anatel,
    carregar_cobertura_movel_4g_uf_anatel
)

st.title("📡 Cobertura Móvel - ANATEL")

# Seleção do dataset
dataset = st.selectbox("Dataset", [
    'Cobertura Geral',
    'Cobertura 5G por UF',
    'Cobertura 4G por UF'
])

# Carrega os dados automaticamente
try:
    with st.spinner('Carregando dados...'):
        if dataset == 'Cobertura Geral':
            df = carregar_cobertura_movel_anatel()
        elif dataset == 'Cobertura 5G por UF':
            df = carregar_cobertura_movel_5g_uf_anatel()
        else:  # Cobertura 4G por UF
            df = carregar_cobertura_movel_4g_uf_anatel()

        if df is not None:
            st.dataframe(df.head(100))
        else:
            st.error("❌ Não foi possível carregar os dados")

except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    st.exception(e)
