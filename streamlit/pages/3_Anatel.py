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

from utils.data_loader import carregar_conectividade_escola_anatel, get_anos_disponiveis_anatel
from components.header import render_header

st.set_page_config(page_title="Anatel - Escolas", layout="wide")

render_header("Dados ANATEL - Conectividade Escolas", "🏫")

st.sidebar.title("⚙️ Configurações")

# Seleção de ano (igual ao CETIC)
anos_disponiveis = get_anos_disponiveis_anatel('conectividade-escola')
ano_selecionado = st.sidebar.selectbox(
    "📅 Ano da Pesquisa",
    options=anos_disponiveis,
    index=0 if anos_disponiveis else None
)

# Botão de forçar recarregamento
force_reload = st.sidebar.button("🔄 Forçar Recarregamento")

# Carrega dados do ano selecionado
if ano_selecionado:
    df = carregar_conectividade_escola_anatel(ano=ano_selecionado, force_download=force_reload)

    if df is not None:
        st.success(f"✅ Dados de {ano_selecionado} carregados com sucesso! Total de registros: {len(df):,}")

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
        st.error(f"❌ Falha ao carregar dados da ANATEL para o ano {ano_selecionado}.")
else:
    st.warning("⚠️ Nenhum ano disponível. Verifique a configuração.")
