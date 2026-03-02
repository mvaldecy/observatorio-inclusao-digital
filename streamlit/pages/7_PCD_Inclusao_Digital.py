"""
Página Streamlit: PCD e Autismo - Indicadores 2022 por Município (PI)
"""

import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from components.header import criar_header
from utils.data_loader import get_analisador_pcd, get_anos_disponiveis_pcd


st.set_page_config(
    page_title="PCD e Autismo - Municípios PI",
    page_icon="♿",
    layout="wide",
    initial_sidebar_state="expanded"
)

criar_header(
    titulo="♿ PCD e TEA - Municípios do Piauí (2022)",
    descricao="""
    Filtros e comparativos de deficiência e autismo por município:
    população 2+, cor/raça, idade, instrução, sexo e domicílios com morador com autismo.
    """,
    icon="♿"
)


# ============================================================================
# Helpers
# ============================================================================

def col_exists(df: pd.DataFrame, col: str) -> bool:
    return col in df.columns


def sum_col(df: pd.DataFrame, col: str) -> float:
    if not col_exists(df, col):
        return 0.0
    return pd.to_numeric(df[col], errors='coerce').fillna(0).sum()


def avg_col(df: pd.DataFrame, col: str) -> float:
    if not col_exists(df, col):
        return 0.0
    serie = pd.to_numeric(df[col], errors='coerce').dropna()
    if serie.empty:
        return 0.0
    return float(serie.mean())


def build_series(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    dados = []
    for rotulo, coluna in mapping.items():
        if col_exists(df, coluna):
            valor = sum_col(df, coluna)
            if valor > 0:
                dados.append({"Categoria": rotulo, "Quantidade": valor})
    return pd.DataFrame(dados)


# ============================================================================
# Sidebar
# ============================================================================

st.sidebar.title("⚙️ Filtros")

anos_disponiveis = get_anos_disponiveis_pcd()
if not anos_disponiveis:
    st.error("❌ Nenhum dado PCD disponível")
    st.stop()

ano_selecionado = st.sidebar.selectbox("📅 Ano", anos_disponiveis, index=0)

try:
    with st.spinner('🔄 Carregando base PCD...'):
        analisador = get_analisador_pcd(ano=ano_selecionado)
        df = analisador.get_dados_atuais()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ Nenhum dado disponível")
    st.stop()

municipios = sorted(df['MUNICIPIO'].dropna().unique().tolist()) if 'MUNICIPIO' in df.columns else []
municipios_sel = st.sidebar.multiselect(
    "🏙️ Municípios",
    options=municipios,
    default=[]
)
if municipios_sel:
    df = df[df['MUNICIPIO'].isin(municipios_sel)]

faixas_idade_map = {
    '2 a 4 anos': 'PCD_IDADE_2_4',
    '5 a 9 anos': 'PCD_IDADE_5_9',
    '10 a 14 anos': 'PCD_IDADE_10_14',
    '15 a 19 anos': 'PCD_IDADE_15_19',
    '20 a 24 anos': 'PCD_IDADE_20_24',
    '25 a 29 anos': 'PCD_IDADE_25_29',
    '30 a 34 anos': 'PCD_IDADE_30_34',
    '35 a 39 anos': 'PCD_IDADE_35_39',
    '40 a 44 anos': 'PCD_IDADE_40_44',
    '45 a 49 anos': 'PCD_IDADE_45_49',
    '50 a 54 anos': 'PCD_IDADE_50_54',
    '55 a 59 anos': 'PCD_IDADE_55_59',
    '60 a 64 anos': 'PCD_IDADE_60_64',
    '65 a 69 anos': 'PCD_IDADE_65_69',
    '70 a 74 anos': 'PCD_IDADE_70_74',
    '75 a 79 anos': 'PCD_IDADE_75_79',
    '80 a 84 anos': 'PCD_IDADE_80_84',
    '85 a 89 anos': 'PCD_IDADE_85_89',
    '90 a 94 anos': 'PCD_IDADE_90_94',
    '95 a 99 anos': 'PCD_IDADE_95_99',
    '100 anos ou mais': 'PCD_IDADE_100_MAIS'
}

faixas_disponiveis = [
    faixa for faixa, col in faixas_idade_map.items()
    if col_exists(df, col)
]

faixas_sel = st.sidebar.multiselect(
    "👶 Idades (deficiência)",
    options=faixas_disponiveis,
    default=faixas_disponiveis
)

st.sidebar.success(f"✅ {len(df):,} municípios no recorte")


# ============================================================================
# Métricas principais
# ============================================================================

total_2_mais = sum_col(df, 'TOTAL_PESSOAS_2_MAIS')
com_def = sum_col(df, 'PESSOAS_COM_DEFICIENCIA_2_MAIS')
sem_def = sum_col(df, 'PESSOAS_SEM_DEFICIENCIA_2_MAIS')
perc_com_def = (com_def / total_2_mais * 100) if total_2_mais > 0 else 0

pop_residente = sum_col(df, 'POPULACAO_RESIDENTE_TOTAL')
autismo_diag = sum_col(df, 'POPULACAO_RESIDENTE_DIAGNOSTICADA_COM_AUTISMO')
perc_autismo = (autismo_diag / pop_residente * 100) if pop_residente > 0 else 0

dom_total = sum_col(df, 'DOMICILIOS_TOTAL')
dom_autismo = sum_col(df, 'DOMICILIOS_COM_MORADOR_AUTISMO')
perc_dom_autismo = (dom_autismo / dom_total * 100) if dom_total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👥 Pessoas 2+ anos", f"{total_2_mais:,.0f}")
with col2:
    st.metric("♿ Pessoas 2+ com deficiência", f"{com_def:,.0f}", f"{perc_com_def:.2f}%")
with col3:
    st.metric("🧩 Diagnosticadas com autismo", f"{autismo_diag:,.0f}", f"{perc_autismo:.2f}%")
with col4:
    st.metric("🏠 Domicílios com morador autista", f"{dom_autismo:,.0f}", f"{perc_dom_autismo:.2f}%")


# ============================================================================
# Tabs
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "♿ Deficiência 2+",
    "📊 Perfil da Deficiência",
    "📚 Educação",
    "🧩 Autismo"
])


with tab1:
    st.markdown("### ♿ Pessoas de 2 anos ou mais: com e sem deficiência")

    comparativo = pd.DataFrame({
        'Grupo': ['Pessoa com deficiência', 'Pessoa sem deficiência'],
        'Quantidade': [com_def, sem_def],
        'Percentual': [
            (com_def / total_2_mais * 100) if total_2_mais > 0 else 0,
            (sem_def / total_2_mais * 100) if total_2_mais > 0 else 0,
        ]
    })

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            comparativo,
            x='Grupo',
            y='Quantidade',
            text='Percentual',
            title='Quantidade de pessoas com e sem deficiência (2+ anos)'
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(
            comparativo,
            names='Grupo',
            values='Percentual',
            title='Comparativo percentual: com vs sem deficiência'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(comparativo, use_container_width=True, hide_index=True)


with tab2:
    st.markdown("### 📊 Perfil da deficiência")

    st.markdown("#### Idade (pessoas com deficiência)")
    idade_map_filtrado = {k: v for k, v in faixas_idade_map.items() if k in faixas_sel}
    df_idade = build_series(df, idade_map_filtrado)
    if not df_idade.empty:
        fig = px.bar(
            df_idade,
            x='Categoria',
            y='Quantidade',
            title='Quantidade de pessoas com deficiência por idade'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados de idade para os filtros selecionados.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Cor/raça (pessoas com deficiência)")
        df_cor_pcd = build_series(df, {
            'Branca': 'PCD_COR_BRANCA',
            'Preta': 'PCD_COR_PRETA',
            'Amarela': 'PCD_COR_AMARELA',
            'Parda': 'PCD_COR_PARDA',
            'Indígena': 'PCD_COR_INDIGENA'
        })
        if not df_cor_pcd.empty:
            fig = px.bar(df_cor_pcd, x='Categoria', y='Quantidade', title='PCD por cor/raça')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de cor/raça para deficiência.")

    with c2:
        st.markdown("#### Quantidade de dificuldades funcionais")
        df_qtd_dif = build_series(df, {
            '1 dificuldade': 'PCD_QTD_1_DIFICULDADE',
            '2 ou mais dificuldades': 'PCD_QTD_2_MAIS_DIFICULDADES'
        })
        if not df_qtd_dif.empty:
            fig = px.pie(df_qtd_dif, names='Categoria', values='Quantidade', title='1 dificuldade vs 2+')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de quantidade de dificuldades.")

    st.markdown("#### Tipos de dificuldades funcionais")
    df_tipos_dif = build_series(df, {
        'Enxergar': 'PCD_DIFICULDADE_ENXERGAR',
        'Ouvir': 'PCD_DIFICULDADE_OUVIR',
        'Andar/Subir degraus': 'PCD_DIFICULDADE_ANDAR',
        'Pegar objetos': 'PCD_DIFICULDADE_PEGAR_OBJETOS',
        'Funções mentais/comunicação': 'PCD_DIFICULDADE_MENTAL'
    })
    if not df_tipos_dif.empty:
        fig = px.bar(df_tipos_dif, x='Categoria', y='Quantidade', title='Tipos de dificuldades e quantidade')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados de tipos de dificuldades.")


with tab3:
    st.markdown("### 📚 Educação")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Taxa de analfabetismo por cor/raça (PCD)")
        df_analf = pd.DataFrame({
            'Cor/Raça': ['Total', 'Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
            'Taxa (%)': [
                avg_col(df, 'TAXA_ANALFABETISMO_PCD_TOTAL'),
                avg_col(df, 'TAXA_ANALFABETISMO_PCD_BRANCA'),
                avg_col(df, 'TAXA_ANALFABETISMO_PCD_PRETA'),
                avg_col(df, 'TAXA_ANALFABETISMO_PCD_AMARELA'),
                avg_col(df, 'TAXA_ANALFABETISMO_PCD_PARDA'),
                avg_col(df, 'TAXA_ANALFABETISMO_PCD_INDIGENA')
            ]
        })
        df_analf = df_analf[df_analf['Taxa (%)'] > 0]
        if not df_analf.empty:
            fig = px.bar(df_analf, x='Cor/Raça', y='Taxa (%)', title='Taxa média de analfabetismo')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de taxa de analfabetismo por cor/raça.")

    with c2:
        st.markdown("#### Nível de instrução das pessoas com deficiência")
        df_instr = build_series(df, {
            'Sem instrução e fund. incompleto': 'PCD_INSTRUCAO_SEM_INSTR_FUND_INCOMP',
            'Fund. completo e médio incompleto': 'PCD_INSTRUCAO_FUND_COMP_MEDIO_INCOMP',
            'Médio completo e sup. incompleto': 'PCD_INSTRUCAO_MEDIO_COMP_SUP_INCOMP',
            'Superior completo': 'PCD_INSTRUCAO_SUPERIOR_COMP'
        })
        if not df_instr.empty:
            fig = px.bar(df_instr, x='Categoria', y='Quantidade', title='Nível de instrução - pessoas com deficiência')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de instrução para pessoas com deficiência.")


with tab4:
    st.markdown("### 🧩 Autismo")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Taxa de pessoas diagnosticadas com autismo")
        autismo_df = pd.DataFrame({
            'Indicador': ['População residente', 'Diagnosticada com autismo'],
            'Quantidade': [pop_residente, autismo_diag]
        })
        fig = px.bar(autismo_df, x='Indicador', y='Quantidade', title=f'Taxa estimada de autismo: {perc_autismo:.2f}%')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Pessoas com autismo por cor/raça")
        df_aut_cor = build_series(df, {
            'Branca': 'AUTISMO_COR_BRANCA',
            'Preta': 'AUTISMO_COR_PRETA',
            'Amarela': 'AUTISMO_COR_AMARELA',
            'Parda': 'AUTISMO_COR_PARDA',
            'Indígena': 'AUTISMO_COR_INDIGENA'
        })
        if not df_aut_cor.empty:
            fig = px.bar(df_aut_cor, x='Categoria', y='Quantidade', title='Autismo por cor/raça')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de autismo por cor/raça.")

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Pessoas com autismo: homens x mulheres")
        df_sexo = pd.DataFrame({
            'Sexo': ['Homens', 'Mulheres'],
            'Valor': [sum_col(df, 'AUTISMO_HOMENS'), sum_col(df, 'AUTISMO_MULHERES')]
        })
        df_sexo = df_sexo[df_sexo['Valor'] > 0]
        if not df_sexo.empty:
            fig = px.bar(df_sexo, x='Sexo', y='Valor', title='Comparativo homens x mulheres')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de homens x mulheres para autismo.")

    with c4:
        st.markdown("#### Pessoas 25+ com autismo por nível de instrução")
        df_aut_25 = build_series(df, {
            'Sem instrução e fund. incompleto': 'AUTISMO_25_MAIS_SEM_INSTR_FUND_INCOMP',
            'Fund. completo e médio incompleto': 'AUTISMO_25_MAIS_FUND_COMP_MEDIO_INCOMP',
            'Médio completo e sup. incompleto': 'AUTISMO_25_MAIS_MEDIO_COMP_SUP_INCOMP',
            'Superior completo': 'AUTISMO_25_MAIS_SUPERIOR_COMP'
        })
        if not df_aut_25.empty:
            fig = px.bar(df_aut_25, x='Categoria', y='Quantidade', title='Autismo (25+) por instrução')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de autismo (25+) por instrução.")

    st.markdown("#### Domicílios particulares permanentes ocupados com pelo menos um morador diagnosticado com autismo")
    dom_df = pd.DataFrame({
        'Indicador': [
            'Domicílios particulares permanentes ocupados (Total)',
            'Domicílios com ao menos um morador autista'
        ],
        'Quantidade': [dom_total, dom_autismo]
    })
    fig = px.bar(
        dom_df,
        x='Indicador',
        y='Quantidade',
        title=f'Percentual de domicílios com morador autista: {perc_dom_autismo:.2f}%'
    )
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# Exportação
# ============================================================================

st.markdown("---")

colunas_exportar = [c for c in [
    'MUNICIPIO',
    'TOTAL_PESSOAS_2_MAIS',
    'PESSOAS_COM_DEFICIENCIA_2_MAIS',
    'PESSOAS_SEM_DEFICIENCIA_2_MAIS',
    'POPULACAO_RESIDENTE_DIAGNOSTICADA_COM_AUTISMO',
    'AUTISMO_HOMENS',
    'AUTISMO_MULHERES',
    'DOMICILIOS_COM_MORADOR_AUTISMO'
] if c in df.columns]

if colunas_exportar:
    csv = df[colunas_exportar].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar recorte atual em CSV",
        data=csv,
        file_name=f"pcd_autismo_municipios_pi_{ano_selecionado}.csv",
        mime="text/csv",
    )

st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666; padding: 12px;'>
    <p><strong>Fonte:</strong> Territórios de Desenvolvimento - PCD/TEA (PI)</p>
    <p>Indicadores municipais com base em 2022</p>
</div>
""",
    unsafe_allow_html=True
)
