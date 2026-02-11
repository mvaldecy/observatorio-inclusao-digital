"""
Componente reutilizável para exploração de dados
Permite carregar e visualizar a estrutura de qualquer dataset
"""
import streamlit as st
import pandas as pd
from typing import Callable, List, Dict, Optional


def explorador_dados(
    tipos_dados: Dict[str, Dict[str, any]],
    titulo: str = "🔍 Exploração de Dados",
    descricao: str = "",
    fonte: str = ""
):
    """
    Componente para explorar diferentes tipos de dados com interface interativa

    Args:
        tipos_dados: Dicionário com configurações dos tipos de dados
                    Formato: {
                        "Nome do Tipo": {
                            "loader": função_que_carrega_dados,
                            "descricao": "Descrição do tipo de dado"
                        }
                    }
        titulo: Título da página
        descricao: Descrição introdutória
        fonte: Nome da fonte dos dados (ex: "ANATEL", "CETIC")
    """

    # Título da página
    st.title(titulo)
    st.markdown("---")

    # Sidebar para seleção do tipo de dado
    st.sidebar.header("Configurações")

    # Lista de tipos disponíveis
    tipos_disponiveis = list(tipos_dados.keys())

    tipo_selecionado = st.sidebar.selectbox(
        "Selecione o tipo de dado:",
        tipos_disponiveis
    )

    force_download = st.sidebar.checkbox(
        "Forçar novo download",
        value=False,
        help="Recarregar os dados mesmo se existir cache"
    )

    # Botão para carregar dados
    if st.sidebar.button("🔄 Carregar Dados", type="primary"):
        st.session_state['carregar_dados'] = True
        st.session_state['tipo_atual'] = tipo_selecionado

    # Carregar dados conforme seleção
    if st.session_state.get('carregar_dados', False):
        # Verifica se mudou o tipo de dado
        if st.session_state.get('tipo_atual') != tipo_selecionado:
            st.session_state['carregar_dados'] = False
            st.info("👈 Clique em 'Carregar Dados' novamente para carregar o novo tipo selecionado")
            return

        st.markdown(f"### Carregando: **{tipo_selecionado}**")

        # Pega a função de carregamento
        config_tipo = tipos_dados[tipo_selecionado]
        loader_func = config_tipo['loader']

        with st.spinner("Carregando dados..."):
            try:
                # Carrega os dados
                df = loader_func(force_download=force_download)

                if df is not None and not df.empty:
                    st.success(f"✅ Dados carregados com sucesso!")

                    # Renderiza as abas de exploração
                    _renderizar_tabs_exploracao(df, tipo_selecionado)

                else:
                    st.error("❌ Erro ao carregar os dados ou dataset vazio.")

            except Exception as e:
                st.error(f"❌ Erro ao carregar dados: {str(e)}")
                st.exception(e)
    else:
        # Instruções iniciais
        st.info("👈 Selecione o tipo de dado na barra lateral e clique em 'Carregar Dados'")

        if descricao:
            st.markdown(descricao)
        else:
            # Descrição padrão
            st.markdown("### Sobre os Dados")
            st.markdown("Esta página permite explorar os seguintes tipos de dados:")
            st.markdown("")

            for nome_tipo, config in tipos_dados.items():
                desc = config.get('descricao', 'Sem descrição disponível')
                st.markdown(f"**{nome_tipo}**: {desc}")

        st.markdown("""
        #### Como usar:
        
        1. Selecione o tipo de dado desejado na barra lateral
        2. Clique no botão "Carregar Dados"
        3. Explore as diferentes abas para ver:
           - Visão geral do dataset
           - Primeiras linhas
           - Estatísticas descritivas
           - Dataset completo com opção de download
        
        #### Opções:
        
        - **Forçar novo download**: Recarrega os dados diretamente da fonte, ignorando o cache local
        """)

    # Rodapé
    if fonte:
        st.markdown("---")
        st.caption(f"📊 Dados fornecidos por: {fonte}")


def _renderizar_tabs_exploracao(df: pd.DataFrame, nome_dataset: str):
    """
    Renderiza as abas de exploração do dataset

    Args:
        df: DataFrame a ser explorado
        nome_dataset: Nome do dataset para download
    """
    # Criar tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Visão Geral",
        "📋 Primeiras Linhas",
        "🔢 Estatísticas",
        "🔍 Dados Completos"
    ])

    with tab1:
        _renderizar_visao_geral(df)

    with tab2:
        _renderizar_primeiras_linhas(df)

    with tab3:
        _renderizar_estatisticas(df)

    with tab4:
        _renderizar_dados_completos(df, nome_dataset)


def _renderizar_visao_geral(df: pd.DataFrame):
    """Renderiza a aba de visão geral"""
    st.markdown("### 📊 Informações Gerais do Dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Linhas", f"{len(df):,}")

    with col2:
        st.metric("Total de Colunas", len(df.columns))

    with col3:
        memoria_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric("Memória Utilizada", f"{memoria_mb:.2f} MB")

    st.markdown("---")
    st.markdown("### 📝 Colunas Disponíveis")

    # Criar DataFrame com informações das colunas
    info_colunas = []
    for col in df.columns:
        info_colunas.append({
            'Coluna': col,
            'Tipo': str(df[col].dtype),
            'Não-Nulos': df[col].notna().sum(),
            'Nulos': df[col].isna().sum(),
            '% Nulos': f"{(df[col].isna().sum() / len(df) * 100):.2f}%"
        })

    df_info = pd.DataFrame(info_colunas)
    st.dataframe(df_info, use_container_width=True, height=400)


def _renderizar_primeiras_linhas(df: pd.DataFrame, n_linhas: int = 20):
    """Renderiza a aba de primeiras linhas"""
    st.markdown(f"### 📋 Primeiras {n_linhas} Linhas do Dataset")

    # Slider para escolher número de linhas
    n_linhas_custom = st.slider(
        "Número de linhas para visualizar:",
        min_value=5,
        max_value=min(100, len(df)),
        value=min(20, len(df)),
        step=5
    )

    st.dataframe(df.head(n_linhas_custom), use_container_width=True, height=600)


def _renderizar_estatisticas(df: pd.DataFrame):
    """Renderiza a aba de estatísticas descritivas"""
    st.markdown("### 🔢 Estatísticas Descritivas")

    # Separar colunas numéricas e categóricas
    colunas_numericas = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns
    colunas_categoricas = df.select_dtypes(include=['object', 'category', 'string']).columns

    if len(colunas_numericas) > 0:
        st.markdown("#### Colunas Numéricas")
        st.dataframe(df[colunas_numericas].describe(), use_container_width=True)
    else:
        st.info("Nenhuma coluna numérica encontrada")

    if len(colunas_categoricas) > 0:
        st.markdown("---")
        st.markdown("#### Colunas Categóricas - Valores Únicos")

        info_categoricas = []
        for col in colunas_categoricas:
            valores_unicos = df[col].nunique()
            amostra = df[col].unique()[:5]
            info_categoricas.append({
                'Coluna': col,
                'Valores Únicos': valores_unicos,
                'Amostra de Valores': ', '.join(map(str, amostra))
            })

        df_cat_info = pd.DataFrame(info_categoricas)
        st.dataframe(df_cat_info, use_container_width=True)
    else:
        st.info("Nenhuma coluna categórica encontrada")


def _renderizar_dados_completos(df: pd.DataFrame, nome_dataset: str):
    """Renderiza a aba de dados completos com opção de download"""
    st.markdown("### 🔍 Dataset Completo")
    st.markdown(f"*Visualizando todas as {len(df):,} linhas*")

    # Opção para filtrar colunas
    colunas_selecionadas = st.multiselect(
        "Selecione colunas específicas (deixe vazio para ver todas):",
        options=list(df.columns),
        default=[]
    )

    if colunas_selecionadas:
        st.dataframe(df[colunas_selecionadas], use_container_width=True, height=600)
    else:
        st.dataframe(df, use_container_width=True, height=600)

    # Botão para baixar CSV
    st.markdown("---")
    st.markdown("### 💾 Download dos Dados")

    col1, col2 = st.columns(2)

    with col1:
        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Baixar CSV",
            data=csv,
            file_name=f"{nome_dataset.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )

    with col2:
        # Download Excel
        try:
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Dados')

            st.download_button(
                label="⬇️ Baixar Excel",
                data=buffer.getvalue(),
                file_name=f"{nome_dataset.lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except ImportError:
            st.info("Instale openpyxl para habilitar download em Excel")

