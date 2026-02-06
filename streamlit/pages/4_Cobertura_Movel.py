"""
Página de visualização de dados de Cobertura Móvel da ANATEL
"""
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

from utils.data_loader import carregar_cobertura_movel_anatel, carregar_cobertura_movel_4g_uf_anatel

from components.header import render_header

# Configuração da página
st.set_page_config(
    page_title="Cobertura Móvel - ANATEL",
    page_icon="📡",
    layout="wide"
)

# Renderiza header
render_header("Cobertura Móvel - ANATEL", "📡")
st.markdown("""
Esta página exibe dados de cobertura móvel da ANATEL. Os dados são baixados em formato Excel
e convertidos automaticamente para Parquet para melhor performance.
""")

# Seção de controle
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Carregar Dados")

with col2:
    force_download = st.checkbox("Forçar novo download", value=False,
                                 help="Marca para baixar novamente, mesmo se já existir cache")

# Botão para carregar dados
if st.button("🔄 Carregar Dados de Cobertura Móvel", type="primary"):
    with st.spinner("Carregando dados..."):
        df = carregar_cobertura_movel_anatel(force_download=force_download)
        carregar_cobertura_movel_4g_uf_anatel(force_download=force_download)

        if df is not None:
            st.session_state['cobertura_movel_df'] = df
            st.success(f"✅ Dados carregados com sucesso! ({len(df):,} linhas)")
        else:
            st.error("❌ Falha ao carregar dados. Verifique o console para mais detalhes.")

# Divisor
st.divider()

# Exibe dados se estiverem carregados
if 'cobertura_movel_df' in st.session_state:
    df = st.session_state['cobertura_movel_df']

    # Informações gerais
    st.subheader("📊 Informações Gerais")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de Linhas", f"{len(df):,}")

    with col2:
        st.metric("Total de Colunas", len(df.columns))

    with col3:
        # Calcula tamanho em memória
        memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        st.metric("Memória Utilizada", f"{memory_mb:.2f} MB")

    with col4:
        # Verifica se o arquivo parquet existe
        from pathlib import Path
        cache_path = Path("data/cache/anatel/cobertura-movel/cobertura-movel.parquet")
        if cache_path.exists():
            size_mb = cache_path.stat().st_size / (1024 * 1024)
            st.metric("Tamanho em Disco", f"{size_mb:.2f} MB")
        else:
            st.metric("Tamanho em Disco", "N/A")

    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Dados", "📈 Estatísticas", "🔍 Colunas", "💾 Cache"])

    with tab1:
        st.subheader("Visualização dos Dados")

        # Opções de filtro
        col1, col2 = st.columns([1, 3])

        with col1:
            num_rows = st.selectbox(
                "Linhas a exibir:",
                options=[10, 50, 100, 500, 1000, "Todas"],
                index=2
            )

        # Exibe dados
        if num_rows == "Todas":
            st.dataframe(df, use_container_width=True, height=600)
        else:
            st.dataframe(df.head(num_rows), use_container_width=True, height=600)

        # Botão de download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar dados como CSV",
            data=csv,
            file_name="cobertura_movel_anatel.csv",
            mime="text/csv",
        )

    with tab2:
        st.subheader("Estatísticas Descritivas")

        # Estatísticas de colunas numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        if numeric_cols:
            st.write("**Colunas Numéricas:**")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("Nenhuma coluna numérica encontrada")

        st.divider()

        # Estatísticas de colunas categóricas
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        if categorical_cols:
            st.write("**Colunas Categóricas:**")

            selected_col = st.selectbox("Selecione uma coluna para ver a distribuição:", categorical_cols)

            if selected_col:
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Valores únicos em '{selected_col}':**")
                    value_counts = df[selected_col].value_counts()
                    st.dataframe(value_counts.reset_index().head(20), use_container_width=True)

                with col2:
                    st.write(f"**Top 10 mais frequentes:**")
                    st.bar_chart(value_counts.head(10))

    with tab3:
        st.subheader("Informações das Colunas")

        # Cria DataFrame com info das colunas
        col_info = pd.DataFrame({
            'Coluna': df.columns,
            'Tipo': df.dtypes.values,
            'Não Nulos': df.count().values,
            'Nulos': df.isnull().sum().values,
            '% Nulos': (df.isnull().sum() / len(df) * 100).round(2).values,
            'Valores Únicos': [df[col].nunique() for col in df.columns]
        })

        st.dataframe(col_info, use_container_width=True, height=600)

        # Resumo
        st.divider()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total de Colunas", len(df.columns))

        with col2:
            colunas_com_nulos = (df.isnull().sum() > 0).sum()
            st.metric("Colunas com Nulos", colunas_com_nulos)

        with col3:
            total_nulos = df.isnull().sum().sum()
            st.metric("Total de Valores Nulos", f"{total_nulos:,}")

    with tab4:
        st.subheader("Informações do Cache")

        from pathlib import Path
        from datetime import datetime

        cache_dir = Path("data/cache/anatel/cobertura-movel")

        if cache_dir.exists():
            st.success("✅ Diretório de cache existe")

            # Lista arquivos no cache
            files = list(cache_dir.glob("*"))

            if files:
                st.write("**Arquivos em cache:**")

                for file in files:
                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:
                        st.text(f"📄 {file.name}")

                    with col2:
                        size_mb = file.stat().st_size / (1024 * 1024)
                        st.text(f"{size_mb:.2f} MB")

                    with col3:
                        mtime = datetime.fromtimestamp(file.stat().st_mtime)
                        st.text(mtime.strftime("%Y-%m-%d %H:%M"))

                st.divider()

                # Botão para limpar cache
                if st.button("🗑️ Limpar Cache", type="secondary"):
                    try:
                        for file in files:
                            file.unlink()
                        st.success("Cache limpo com sucesso!")
                        # Remove do session_state
                        if 'cobertura_movel_df' in st.session_state:
                            del st.session_state['cobertura_movel_df']
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao limpar cache: {str(e)}")
            else:
                st.info("Nenhum arquivo em cache")
        else:
            st.warning("⚠️ Diretório de cache não existe")
            st.info(f"Caminho esperado: {cache_dir.absolute()}")

else:
    # Instruções iniciais
    st.info("""
    👆 Clique no botão acima para carregar os dados de cobertura móvel.

    **O que acontece:**
    1. Se não houver cache, o sistema baixa o arquivo Excel da ANATEL
    2. O arquivo é convertido automaticamente para formato Parquet
    3. Os dados são otimizados (tipos, categorias, compressão)
    4. O resultado é salvo em cache local
    5. Próximas cargas são instantâneas (usa o cache)

    **Opções:**
    - ✅ Normal: Usa cache se disponível
    - ✅ Forçar download: Baixa novamente mesmo se houver cache
    """)

    # Informações sobre o cache
    st.divider()
    st.subheader("📁 Status do Cache")

    from pathlib import Path
    cache_path = Path("data/cache/anatel/cobertura-movel/cobertura-movel.parquet")

    if cache_path.exists():
        from datetime import datetime

        size_mb = cache_path.stat().st_size / (1024 * 1024)
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Status", "✅ Cache existe")

        with col2:
            st.metric("Tamanho", f"{size_mb:.2f} MB")

        with col3:
            st.metric("Última atualização", mtime.strftime("%Y-%m-%d"))

        st.info("💡 Use 'Forçar novo download' se quiser atualizar os dados")
    else:
        st.warning("⚠️ Cache não existe - será criado no primeiro carregamento")

# Footer
st.divider()
st.caption("📡 Dados de Cobertura Móvel fornecidos pela ANATEL")

