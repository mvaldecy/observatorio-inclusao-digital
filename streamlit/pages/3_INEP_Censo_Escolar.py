"""
Página do INEP - Censo Escolar da Educação Básica
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Adiciona a raiz do projeto e o diretório streamlit ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from utils.data_loader import get_analisador_inep, get_anos_disponiveis_inep
from utils.http_loader import HTTPDataLoader
from components.inep import CATEGORIAS_INEP, AGREGADORES_INEP, FiltroINEP, ComparativoGeograficoINEP
from components.header import render_header
from inep import get_label, get_valores

st.set_page_config(page_title="INEP - Censo Escolar", layout="wide", page_icon="🏫")

# ============================================================================
# SIDEBAR - CONFIGURAÇÕES
# ============================================================================

st.sidebar.title("⚙️ Configurações")

# Seletor de ano
anos_disponiveis = get_anos_disponiveis_inep()

ano_selecionado = st.sidebar.selectbox(
    "📅 Ano do Censo",
    options=anos_disponiveis,
    index=0,
    help="Selecione o ano do Censo Escolar"
)

# Botões de gerenciamento de cache
col_btn1, col_btn2 = st.sidebar.columns(2)

loader = HTTPDataLoader(fonte='inep')

with col_btn1:
    if st.button("🔄 Atualizar", help="Baixar nova versão dos dados", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        loader.carregar_dados(ano_selecionado, 'educacao-basica', force_download=True)
        st.rerun()

with col_btn2:
    if st.button("🗑️ Limpar Cache", help="Remover dados em cache", use_container_width=True):
        loader.limpar_cache(ano_selecionado)
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

# Info sobre cache
with st.sidebar.expander("💾 Informações do Cache", expanded=False):
    cache_info = loader.info_cache()

    if cache_info:
        for ano, arquivos in cache_info.items():
            st.markdown(f"**{ano}:**")
            for tipo, info in arquivos.items():
                icone = "✅" if info['existe'] else "❌"
                st.markdown(f"  {icone} **{tipo}**: {info['tamanho_mb']} MB")
    else:
        st.info("📂 Nenhum arquivo em cache")

st.sidebar.markdown("---")

# ============================================================================
# CARREGAR DADOS
# ============================================================================

try:
    analisador = get_analisador_inep(ano=ano_selecionado)
except Exception as e:
    st.error(f"❌ Erro ao carregar dados de {ano_selecionado}: {str(e)}")
    st.info("💡 **Dica:** Verifique sua conexão com a internet ou tente limpar o cache.")
    st.stop()

# ============================================================================
# FILTROS
# ============================================================================

filtro_helper = FiltroINEP(analisador)
filtros_ativos = filtro_helper.render_todos_filtros()

# ============================================================================
# HEADER
# ============================================================================

render_header(f"INEP - Censo Escolar {ano_selecionado}", "🏫")

# Mostrar resumo dos filtros
if filtros_ativos:
    filtro_helper.mostrar_resumo_filtros()

# ============================================================================
# SELEÇÃO DE INDICADORES
# ============================================================================

# Contar indicadores
total_indicadores = sum(1 for cat in CATEGORIAS_INEP.values() for k, v in cat.items() if isinstance(v, str))
total_comparativos = sum(1 for cat in CATEGORIAS_INEP.values() for k, v in cat.items() if isinstance(v, list))

st.markdown(f"""
### Selecione um Indicador para Análise
Escolha a categoria e depois o indicador específico que deseja analisar.

**Disponíveis:** {total_indicadores} indicadores individuais + {total_comparativos} análises comparativas
""")

# Seleção por categoria primeiro
col_cat, col_ind = st.columns([1, 2])

with col_cat:
    selected_category = st.selectbox(
        "📁 Categoria",
        options=list(CATEGORIAS_INEP.keys()),
        help="Selecione uma categoria de indicadores"
    )

# Planificar INDICADORES da categoria selecionada
INDICADORES_CATEGORIA = {}
for k, v in CATEGORIAS_INEP[selected_category].items():
    if isinstance(v, str):
        # v é o nome da coluna, k é o label amigável
        INDICADORES_CATEGORIA[k] = v
    else:
        # v é uma lista (comparativo)
        INDICADORES_CATEGORIA[k] = v

with col_ind:
    selected_indicador_key = st.selectbox(
        "📊 Indicador",
        options=list(INDICADORES_CATEGORIA.keys()),
        help="Selecione o indicador específico"
    )

# Determinar se é análise múltipla e pegar o indicador real (nome da coluna)
is_multiple = False
actual_indicador = INDICADORES_CATEGORIA[selected_indicador_key]

# Se for lista, é comparativo
if isinstance(actual_indicador, list):
    is_multiple = True
    # actual_indicador já é a lista de colunas

# Obter label amigável para exibição
if is_multiple:
    label_indicador = f"📊 {selected_indicador_key}"
else:
    # actual_indicador é o nome da coluna, usar get_label para obter descrição
    label_indicador = get_label(actual_indicador)

st.subheader(label_indicador)

# Card informativo sobre o indicador
with st.expander("ℹ️ Sobre este Indicador", expanded=False):
    col_info_ind1, col_info_ind2 = st.columns(2)

    with col_info_ind1:
        st.markdown(f"""
        **Código:** `{selected_indicador_key}`  
        **Categoria:** {selected_category}  
        **Tipo:** {'Análise Comparativa' if is_multiple else 'Indicador Individual'}
        """)

    with col_info_ind2:
        if is_multiple:
            st.markdown(f"""
            **Indicadores comparados:** {len(actual_indicador)}  
            """)
            for ind in actual_indicador:
                st.markdown(f"- `{ind}`: {get_label(ind)}")
        else:
            valores = get_valores(actual_indicador)
            if valores:
                st.markdown("**Valores possíveis:**")
                for cod, desc in valores.items():
                    st.markdown(f"- {cod}: {desc}")

# ============================================================================
# ANÁLISE PRINCIPAL
# ============================================================================

st.markdown("---")
st.markdown("### 📊 Análise")

# Realizar análise
resultado = analisador.analisar_indicador(actual_indicador)

if resultado is not None and not resultado.empty:

    # Mostrar quantidade de escolas analisadas
    total_escolas = len(analisador.df)
    st.metric("🏫 Total de Escolas Analisadas", f"{total_escolas:,}")

    # Exibir tabela de resultados
    col_res1, col_res2 = st.columns([1, 1])

    with col_res1:
        st.markdown("#### 📋 Resultados")
        st.dataframe(resultado, use_container_width=True, hide_index=True)

    with col_res2:
        st.markdown("#### 📈 Visualização")

        # Gráfico de barras para indicadores categóricos
        if 'Percentual' in resultado.columns and 'Descrição' in resultado.columns:
            # Extrair valores numéricos do percentual
            resultado['Percentual_Num'] = resultado['Percentual'].str.replace('%', '').astype(float)

            fig = px.bar(
                resultado,
                x='Descrição',
                y='Percentual_Num',
                text='Percentual',
                title=label_indicador,
                labels={'Percentual_Num': 'Percentual (%)', 'Descrição': ''},
                color='Percentual_Num',
                color_continuous_scale='Viridis'
            )

            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Gráfico para indicadores quantitativos
        elif 'Total' in resultado.columns and 'Descrição' in resultado.columns:
            fig = px.bar(
                resultado,
                x='Descrição',
                y='Total',
                text='Total',
                title=label_indicador,
                labels={'Total': 'Quantidade', 'Descrição': ''},
                color='Total',
                color_continuous_scale='Blues'
            )

            fig.update_traces(textposition='outside')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⚠️ Nenhum dado encontrado para os filtros aplicados.")

# ============================================================================
# ANÁLISE POR AGREGADOR
# ============================================================================

st.markdown("---")
st.markdown("### 🔍 Análise Detalhada por Agregador")

col_agg1, col_agg2 = st.columns([1, 1])

with col_agg1:
    usar_agregador = st.checkbox(
        "Analisar por agregador",
        value=False,
        help="Permite ver como o indicador varia por região, dependência, etc."
    )

if usar_agregador:
    with col_agg2:
        agregador_selecionado = st.selectbox(
            "Agregador",
            options=list(AGREGADORES_INEP.keys()),
            help="Campo para agrupar a análise"
        )

    campo_agregador = AGREGADORES_INEP[agregador_selecionado]

    # Realizar análise por agregador
    resultado_agg = analisador.analisar_por_agregador(actual_indicador, campo_agregador)

    if resultado_agg is not None and not resultado_agg.empty:

        # Mostrar tabela
        st.markdown(f"#### 📊 Resultados por {agregador_selecionado}")
        st.dataframe(resultado_agg, use_container_width=True, hide_index=True)

        # Gráfico agrupado
        st.markdown("#### 📈 Visualização Agrupada")

        # Determinar coluna de agrupamento (primeira coluna não numérica)
        col_grupo = resultado_agg.columns[0]

        if is_multiple and 'Indicador' in resultado_agg.columns:
            # Análise múltipla - gráfico agrupado por indicador
            fig = px.bar(
                resultado_agg[resultado_agg['Categoria'].str.contains('Sim', na=False)],
                x=col_grupo,
                y='Percentual_Num',
                color='Indicador',
                barmode='group',
                title=f"{selected_indicador_key} por {agregador_selecionado}",
                labels={'Percentual_Num': 'Percentual (%)'},
                text='Percentual'
            )
        else:
            # Análise simples - gráfico empilhado por categoria
            fig = px.bar(
                resultado_agg,
                x=col_grupo,
                y='Percentual_Num',
                color='Categoria',
                title=f"{label_indicador} por {agregador_selecionado}",
                labels={'Percentual_Num': 'Percentual (%)'},
                text='Percentual'
            )

        fig.update_traces(textposition='inside')
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Download dos resultados
        csv = resultado_agg.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Resultados (CSV)",
            data=csv,
            file_name=f"inep_{ano_selecionado}_{selected_indicador_key}_por_{campo_agregador}.csv",
            mime="text/csv"
        )

# ============================================================================
# COMPARATIVO GEOGRÁFICO
# ============================================================================

st.markdown("---")
st.markdown("### 🗺️ Comparativo Geográfico")

usar_comparativo = st.checkbox(
    "Comparar Brasil / Nordeste / Piauí",
    value=False,
    help="Análise comparativa entre diferentes níveis geográficos"
)

if usar_comparativo:
    # Criar componente de comparativo geográfico
    comparativo = ComparativoGeograficoINEP(analisador)

    # Pegar filtros extras aplicados (exceto geográficos)
    filtros_extras = {}
    if hasattr(filtro_helper, 'filtros_aplicados'):
        for col, valor in filtro_helper.filtros_aplicados.items():
            # Não incluir filtros geográficos no comparativo
            if col not in ['CO_REGIAO', 'CO_UF', 'CO_MUNICIPIO']:
                filtros_extras[col] = valor

    # Renderizar comparativo
    comparativo.renderizar(
        indicador=actual_indicador,
        filtros_extras=filtros_extras if filtros_extras else None,
        is_multiple=is_multiple
    )

# ============================================================================
# RESUMO ESTATÍSTICO
# ============================================================================

st.markdown("---")
st.markdown("### 📊 Resumo Estatístico Geral")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    total = len(analisador.df)
    st.metric("🏫 Total de Escolas", f"{total:,}")

with col_stat2:
    if 'QT_MAT_BAS' in analisador.df.columns:
        mat_total = analisador.df['QT_MAT_BAS'].sum()
        st.metric("👨‍🎓 Total de Matrículas", f"{int(mat_total):,}")
    else:
        st.metric("👨‍🎓 Total de Matrículas", "N/D")

with col_stat3:
    if 'QT_DOC_BAS' in analisador.df.columns:
        doc_total = analisador.df['QT_DOC_BAS'].sum()
        st.metric("👨‍🏫 Total de Docentes", f"{int(doc_total):,}")
    else:
        st.metric("👨‍🏫 Total de Docentes", "N/D")

with col_stat4:
    if 'IN_INTERNET' in analisador.df.columns:
        com_internet = (analisador.df['IN_INTERNET'] == 1).sum()
        perc_internet = (com_internet / total * 100) if total > 0 else 0
        st.metric("🌐 Com Internet", f"{perc_internet:.1f}%")
    else:
        st.metric("🌐 Com Internet", "N/D")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Dados: INEP - Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira</p>
    <p>Censo Escolar da Educação Básica</p>
</div>
""", unsafe_allow_html=True)

