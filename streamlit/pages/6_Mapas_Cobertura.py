"""
Página de Visualização em Mapa - Cobertura 4G e 5G por UF
Apresenta mapas coropléticos do Brasil com dados de cobertura móvel
"""
import os
import sys
import streamlit as st

# Adiciona a raiz do projeto ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

# Importação robusta que funciona local e no deploy
try:
    from utils.data_loader import (
        carregar_cobertura_movel_4g_uf_anatel,
        carregar_cobertura_movel_5g_uf_anatel
    )
    from components.mapa_brasil import mapa_com_tabs_4g_5g
except ImportError:
    # Fallback para quando rodando do diretório raiz (deploy)
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils.data_loader import (
        carregar_cobertura_movel_4g_uf_anatel,
        carregar_cobertura_movel_5g_uf_anatel
    )
    from components.mapa_brasil import mapa_com_tabs_4g_5g

# Configuração da página
st.set_page_config(
    page_title="Mapas - Cobertura 4G e 5G",
    layout="wide",
    page_icon="🗺️"
)

# Título da página
st.title("🗺️ Mapas de Cobertura Móvel - Brasil")
st.markdown("Visualização geográfica da cobertura 4G e 5G por estado")
st.markdown("---")

# Carrega os dados
with st.spinner("Carregando dados de cobertura..."):
    try:
        # Carrega dados 4G
        df_4g = carregar_cobertura_movel_4g_uf_anatel()

        # Carrega dados 5G
        df_5g = carregar_cobertura_movel_5g_uf_anatel()

        if df_4g is not None and df_5g is not None and not df_4g.empty and not df_5g.empty:
            st.success("✅ Dados carregados com sucesso!")

            # Mostra preview dos dados
            with st.expander("🔍 Preview dos Dados"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Dados 4G:**")
                    st.dataframe(df_4g.head(10), use_container_width=True)
                    st.caption(f"Total de {len(df_4g)} registros")

                with col2:
                    st.markdown("**Dados 5G:**")
                    st.dataframe(df_5g.head(10), use_container_width=True)
                    st.caption(f"Total de {len(df_5g)} registros")

            st.markdown("---")

            # Identifica colunas automaticamente
            # Busca coluna de UF (pode ser 'UF', 'sigla', 'Estado', etc.)
            colunas_uf_possiveis = ['[NOME UF]', 'UF', 'sigla', 'Estado', 'uf', 'SIGLA', 'NOME UF']
            coluna_uf_4g = None
            coluna_uf_5g = None

            for col in colunas_uf_possiveis:
                if col in df_4g.columns and coluna_uf_4g is None:
                    coluna_uf_4g = col
                if col in df_5g.columns and coluna_uf_5g is None:
                    coluna_uf_5g = col

            # Se não encontrou, busca por colunas que contenham 'UF' ou 'NOME'
            if coluna_uf_4g is None:
                for col in df_4g.columns:
                    if 'UF' in col.upper() or 'NOME' in col.upper() or 'ESTADO' in col.upper():
                        coluna_uf_4g = col
                        break

            if coluna_uf_5g is None:
                for col in df_5g.columns:
                    if 'UF' in col.upper() or 'NOME' in col.upper() or 'ESTADO' in col.upper():
                        coluna_uf_5g = col
                        break

            # Busca coluna de cobertura (pode ter vários nomes)
            colunas_valor_possiveis = [
                '% MORADORES COBERTOS',
                'Cobertura',
                'cobertura',
                'percentual',
                'Percentual',
                'valor',
                'Valor',
                'MORADORES COBERTOS'
            ]
            coluna_valor_4g = None
            coluna_valor_5g = None

            for col in colunas_valor_possiveis:
                if col in df_4g.columns and coluna_valor_4g is None:
                    coluna_valor_4g = col
                if col in df_5g.columns and coluna_valor_5g is None:
                    coluna_valor_5g = col

            # Se não encontrou, busca por colunas que contenham '%' ou 'COBERTO' ou 'COBERTURA'
            if coluna_valor_4g is None:
                for col in df_4g.columns:
                    col_upper = col.upper()
                    if '%' in col or 'COBERTO' in col_upper or 'COBERTURA' in col_upper:
                        coluna_valor_4g = col
                        break

            if coluna_valor_5g is None:
                for col in df_5g.columns:
                    col_upper = col.upper()
                    if '%' in col or 'COBERTO' in col_upper or 'COBERTURA' in col_upper:
                        coluna_valor_5g = col
                        break

            # Se não encontrou, pega a segunda coluna (assumindo que a primeira é UF)
            if coluna_valor_4g is None and len(df_4g.columns) > 1:
                coluna_valor_4g = df_4g.columns[1]

            if coluna_valor_5g is None and len(df_5g.columns) > 1:
                coluna_valor_5g = df_5g.columns[1]

            # Mostra informações sobre as colunas detectadas
            st.info(f"""
            **Colunas detectadas:**
            - 4G: UF=`{coluna_uf_4g}`, Valor=`{coluna_valor_4g}`
            - 5G: UF=`{coluna_uf_5g}`, Valor=`{coluna_valor_5g}`
            """)

            # Valida se encontrou as colunas
            if coluna_uf_4g and coluna_uf_5g and coluna_valor_4g and coluna_valor_5g:
                # Renderiza os mapas com tabs
                mapa_com_tabs_4g_5g(
                    df_4g=df_4g,
                    df_5g=df_5g,
                    coluna_uf=coluna_uf_4g,  # Assumindo que são iguais
                    coluna_valor_4g=coluna_valor_4g,
                    coluna_valor_5g=coluna_valor_5g
                )

                # Informações adicionais
                st.markdown("---")
                st.markdown("### ℹ️ Sobre os Dados")

                st.markdown("""
                **Fonte dos Dados:** ANATEL - Agência Nacional de Telecomunicações
                
                **Descrição:**
                - **4G (LTE)**: Tecnologia de quarta geração de telefonia móvel
                - **5G**: Tecnologia de quinta geração com maior velocidade e menor latência
                
                **Interpretação:**
                - Os valores representam a **porcentagem de cobertura** em cada estado
                - Maior cobertura significa melhor acesso à internet móvel
                - O gap entre 4G e 5G mostra o avanço da tecnologia em cada região
                
                **Navegação:**
                - Use as **tabs** acima para alternar entre 4G, 5G e comparação
                - Passe o mouse sobre os estados para ver detalhes
                - A tab de comparação mostra o ranking e as diferenças
                """)

            else:
                st.error("❌ Não foi possível identificar as colunas de UF e/ou valor nos dados.")
                st.write("Colunas disponíveis em 4G:", list(df_4g.columns))
                st.write("Colunas disponíveis em 5G:", list(df_5g.columns))

        else:
            st.error("❌ Erro ao carregar os dados ou datasets vazios.")

    except Exception as e:
        st.error(f"❌ Erro ao carregar ou processar dados: {str(e)}")
        st.exception(e)

# Rodapé
st.markdown("---")
st.caption("🗺️ Mapas gerados com Plotly | Dados: ANATEL")


