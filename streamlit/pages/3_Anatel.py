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

from utils.data_loader import carregar_conectividade_escola_anatel, get_anos_disponiveis_anatel, get_analisador_anatel
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
    # Usa o analisador para carregar e analisar os dados
    try:
        analisador = get_analisador_anatel(ano=ano_selecionado)
        
        st.success(f"✅ Dados de {ano_selecionado} carregados com sucesso! Total de registros: {len(analisador.df):,}")
        
        # Tabs para organizar conteúdo
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumo", "🗺️ Por Região/UF", "🏙️ Urbano x Rural", "📋 Dados Brutos"])
        
        with tab1:
            st.subheader("Resumo Geral")
            resumo = analisador.resumo_geral()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Escolas", f"{resumo['total_registros']:,}")
            with col2:
                st.metric("Ano da Pesquisa", resumo['ano'])
            with col3:
                st.metric("Colunas Disponíveis", resumo['total_colunas'])
            
            st.markdown("---")
            st.subheader("Colunas Disponíveis")
            st.write(resumo['colunas'])
        
        with tab2:
            st.subheader("Distribuição por Região")
            regioes = analisador.escolas_por_regiao()
            if not regioes.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(regioes, use_container_width=True)
                with col2:
                    st.bar_chart(regioes.set_index('Valor')['Contagem'])
            else:
                st.info("Coluna de região não encontrada nos dados")
            
            st.markdown("---")
            st.subheader("Top 10 UFs com Mais Escolas")
            ufs = analisador.escolas_por_uf(top=10)
            if not ufs.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(ufs, use_container_width=True)
                with col2:
                    st.bar_chart(ufs.set_index('Valor')['Contagem'])
            else:
                st.info("Coluna de UF não encontrada nos dados")
        
        with tab3:
            st.subheader("Comparação Urbano x Rural")
            st.info("Selecione uma coluna numérica para comparar entre áreas urbanas e rurais")
            
            # Lista colunas numéricas
            colunas_numericas = analisador.df.select_dtypes(include=['number']).columns.tolist()
            
            if colunas_numericas:
                coluna_selecionada = st.selectbox("Escolha uma coluna:", colunas_numericas)
                
                if coluna_selecionada:
                    comparacao = analisador.comparar_localizacao(coluna_selecionada)
                    
                    if not comparacao.empty:
                        st.dataframe(comparacao, use_container_width=True)
                        st.bar_chart(comparacao.set_index('Localização')['Total'])
                    else:
                        st.warning("Não foi possível fazer a comparação. Verifique se a coluna de localização existe.")
            else:
                st.warning("Nenhuma coluna numérica encontrada nos dados")
        
        with tab4:
            st.subheader("Pré-visualização dos Dados (Top 100)")
            st.dataframe(analisador.df.head(100), use_container_width=True)
            
            st.subheader("Resumo Estatístico")
            sample_size = min(10000, len(analisador.df))
            st.write(analisador.df.sample(sample_size).describe(include='all'))
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar analisador: {str(e)}")
        st.info("Tentando carregar dados sem o analisador...")
        
        # Fallback: carrega sem analisador
        df = carregar_conectividade_escola_anatel(ano=ano_selecionado, force_download=force_reload)
        if df is not None:
            st.success(f"✅ Dados carregados. Total de registros: {len(df):,}")
            st.dataframe(df.head(100), use_container_width=True)
        else:
            st.error(f"❌ Falha ao carregar dados da ANATEL para o ano {ano_selecionado}.")
else:
    st.warning("⚠️ Nenhum ano disponível. Verifique a configuração.")
