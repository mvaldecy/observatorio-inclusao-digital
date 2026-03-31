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
from utils.data_loader import (
    get_analisador_pcd,
    get_anos_disponiveis_pcd,
    carregar_dados_pcd_brasil_nordeste,
)


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


def first_existing_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


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


def preparar_visualizacao(df_base: pd.DataFrame, base_percentual: float) -> pd.DataFrame:
    df_out = df_base.copy()
    if base_percentual > 0 and 'Quantidade' in df_out.columns:
        df_out['Percentual'] = (df_out['Quantidade'] / base_percentual) * 100
    else:
        df_out['Percentual'] = 0.0
    return df_out


def exibir_grafico_barras(df_plot: pd.DataFrame, x_col: str, modo: str, titulo: str, y_label: str = ""):
    if df_plot.empty:
        return

    if modo == 'Percentual (%)':
        y_col = 'Percentual'
        texttemplate = '%{text:.2f}%'
    else:
        y_col = 'Quantidade'
        texttemplate = '%{text:,.0f}'

    fig = px.bar(df_plot, x=x_col, y=y_col, text=y_col, title=titulo)
    fig.update_traces(texttemplate=texttemplate, textposition='outside')
    if y_label:
        fig.update_yaxes(title=y_label)
    st.plotly_chart(fig, use_container_width=True)


def montar_comparativo_territorial_pcd(
    df_agregado_br_ne: pd.DataFrame | None,
    df_base_piaui: pd.DataFrame | None,
) -> tuple[pd.DataFrame, dict]:
    if df_agregado_br_ne is None:
        df_agregado_br_ne = pd.DataFrame()
    if df_base_piaui is None:
        df_base_piaui = pd.DataFrame()

    col_total_ag = first_existing_col(df_agregado_br_ne, ['TOTAL_PESSOAS_2_MAIS', 'total_pessoas_2_mais'])
    col_pcd_ag = first_existing_col(df_agregado_br_ne, ['PESSOAS_COM_DEFICIENCIA_2_MAIS', 'pessoas_com_deficiencia_2_mais'])
    col_recorte_ag = first_existing_col(df_agregado_br_ne, ['MUNICIPIO', 'municipio', 'REGIAO', 'regiao'])

    col_total_pi = first_existing_col(df_base_piaui, ['TOTAL_PESSOAS_2_MAIS', 'total_pessoas_2_mais'])
    col_pcd_pi = first_existing_col(df_base_piaui, ['PESSOAS_COM_DEFICIENCIA_2_MAIS', 'pessoas_com_deficiencia_2_mais'])

    if (not col_total_ag or not col_pcd_ag or not col_recorte_ag) and (not col_total_pi or not col_pcd_pi):
        return pd.DataFrame(), {
            'tem_colunas_minimas': False,
            'tem_recorte_nacional': False,
            'recortes_distintos': 0
        }

    dados = []

    if col_total_ag and col_pcd_ag and col_recorte_ag:
        serie_recorte = df_agregado_br_ne[col_recorte_ag].astype(str).str.strip().str.lower()

        for nome_recorte, nome_saida in [('brasil', 'Brasil'), ('nordeste', 'Nordeste')]:
            df_rec = df_agregado_br_ne[serie_recorte == nome_recorte]
            if df_rec.empty:
                continue

            total = sum_col(df_rec, col_total_ag)
            pcd = sum_col(df_rec, col_pcd_ag)
            dados.append({
                'Recorte': nome_saida,
                'Total 2+': total,
                'Com deficiência (2+)': pcd,
                'Percentual (%)': (pcd / total * 100) if total > 0 else 0.0
            })

    if col_total_pi and col_pcd_pi:
        total_pi = sum_col(df_base_piaui, col_total_pi)
        pcd_pi = sum_col(df_base_piaui, col_pcd_pi)
        dados.append({
            'Recorte': 'Piauí',
            'Total 2+': total_pi,
            'Com deficiência (2+)': pcd_pi,
            'Percentual (%)': (pcd_pi / total_pi * 100) if total_pi > 0 else 0.0
        })

    recortes_distintos = len(pd.DataFrame(dados)['Recorte'].dropna().unique()) if dados else 0
    return pd.DataFrame(dados), {
        'tem_colunas_minimas': recortes_distintos > 0,
        'tem_recorte_nacional': recortes_distintos >= 2,
        'recortes_distintos': recortes_distintos
    }


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
        df_base_piaui = df.copy()
        df_br_ne = carregar_dados_pcd_brasil_nordeste(ano=ano_selecionado)
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ Nenhum dado disponível")
    st.stop()

municipios = sorted(df['MUNICIPIO'].dropna().unique().tolist()) if 'MUNICIPIO' in df.columns else []
municipio_sel = st.sidebar.selectbox(
    "🏙️ Município",
    options=['Todos'] + municipios,
    index=0
)
if municipio_sel != 'Todos':
    df = df[df['MUNICIPIO'] == municipio_sel]

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

faixa_idade_sel = st.sidebar.selectbox(
    "👶 Idade (deficiência)",
    options=['Todas'] + faixas_disponiveis,
    index=0
)

modo_visualizacao = st.sidebar.radio(
    "📐 Exibir valores",
    options=['Número de pessoas', 'Percentual (%)', 'Ambos'],
    index=2,
    help="Escolha se os gráficos e tabelas exibem contagem, percentual ou ambos"
)

st.sidebar.success(f"✅ {len(df):,} municípios no recorte")


# ============================================================================
# Comparativo Territorial (Topo da Tela)
# ============================================================================

st.markdown("### 🌎 Comparativo geral: Brasil x Nordeste x Piauí")
st.caption("Indicador: percentual de pessoas com deficiência entre pessoas de 2 anos ou mais.")

df_comp, status_comp = montar_comparativo_territorial_pcd(df_br_ne, df_base_piaui)

if not status_comp['tem_colunas_minimas']:
    st.warning("A base atual não contém as colunas necessárias para o comparativo territorial.")
elif df_comp.empty:
    st.warning("Não foi possível montar o comparativo territorial com os dados atuais.")
else:
    if not status_comp['tem_recorte_nacional']:
        st.warning(
            "A base atual de PCD está com cobertura territorial limitada "
            f"({status_comp['recortes_distintos']} recorte(s) disponível(is)). "
            "O valor de 'Brasil' pode refletir apenas esse subconjunto."
        )

    m1, m2, m3 = st.columns(3)
    for col_metric, recorte in zip([m1, m2, m3], ['Brasil', 'Nordeste', 'Piauí']):
        linha = df_comp[df_comp['Recorte'] == recorte]
        if linha.empty:
            col_metric.metric(recorte, "N/D")
        else:
            percentual = float(linha['Percentual (%)'].iloc[0])
            col_metric.metric(recorte, f"{percentual:.2f}%")

    fig_comp = px.bar(
        df_comp,
        x='Recorte',
        y='Percentual (%)',
        text='Percentual (%)',
        title='Percentual de pessoas com deficiência (2+) por recorte'
    )
    fig_comp.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_comp.update_yaxes(title='Percentual (%)')
    st.plotly_chart(fig_comp, use_container_width=True)

    df_comp_exibir = df_comp.copy()
    df_comp_exibir['Total 2+'] = df_comp_exibir['Total 2+'].round(0)
    df_comp_exibir['Com deficiência (2+)'] = df_comp_exibir['Com deficiência (2+)'].round(0)

    if modo_visualizacao == 'Número de pessoas':
        st.dataframe(
            df_comp_exibir[['Recorte', 'Total 2+', 'Com deficiência (2+)']],
            use_container_width=True,
            hide_index=True
        )
    elif modo_visualizacao == 'Percentual (%)':
        st.dataframe(
            df_comp_exibir[['Recorte', 'Percentual (%)']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.dataframe(df_comp_exibir, use_container_width=True, hide_index=True)

st.markdown("---")


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


if municipio_sel == 'Todos':
    st.info("Exibindo agregação de todos os municípios do recorte.")
else:
    st.info(f"Exibindo dados do município selecionado: **{municipio_sel}**")


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
        if modo_visualizacao == 'Percentual (%)':
            fig = px.bar(
                comparativo,
                x='Grupo',
                y='Percentual',
                text='Percentual',
                title='Pessoas com e sem deficiência (2+ anos)'
            )
            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        else:
            fig = px.bar(
                comparativo,
                x='Grupo',
                y='Quantidade',
                text='Quantidade',
                title='Pessoas com e sem deficiência (2+ anos)'
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.pie(
            comparativo,
            names='Grupo',
            values='Percentual',
            title='Comparativo percentual: com vs sem deficiência'
        )
        st.plotly_chart(fig, use_container_width=True)

    if modo_visualizacao == 'Número de pessoas':
        st.dataframe(comparativo[['Grupo', 'Quantidade']], use_container_width=True, hide_index=True)
    elif modo_visualizacao == 'Percentual (%)':
        st.dataframe(comparativo[['Grupo', 'Percentual']], use_container_width=True, hide_index=True)
    else:
        st.dataframe(comparativo, use_container_width=True, hide_index=True)


with tab2:
    st.markdown("### 📊 Perfil da deficiência")

    st.markdown("#### Idade (pessoas com deficiência)")
    if faixa_idade_sel == 'Todas':
        idade_map_filtrado = {k: v for k, v in faixas_idade_map.items() if col_exists(df, v)}
    else:
        idade_map_filtrado = {faixa_idade_sel: faixas_idade_map[faixa_idade_sel]}
    df_idade = preparar_visualizacao(build_series(df, idade_map_filtrado), com_def)
    if not df_idade.empty:
        exibir_grafico_barras(
            df_idade,
            x_col='Categoria',
            modo=modo_visualizacao,
            titulo='Pessoas com deficiência por idade',
            y_label='Valor'
        )
        if modo_visualizacao == 'Número de pessoas':
            st.dataframe(df_idade[['Categoria', 'Quantidade']], use_container_width=True, hide_index=True)
        elif modo_visualizacao == 'Percentual (%)':
            st.dataframe(df_idade[['Categoria', 'Percentual']], use_container_width=True, hide_index=True)
        else:
            st.dataframe(df_idade, use_container_width=True, hide_index=True)
    else:
        st.info("Sem dados de idade para os filtros selecionados.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Cor/raça (pessoas com deficiência)")
        df_cor_pcd = preparar_visualizacao(build_series(df, {
            'Branca': 'PCD_COR_BRANCA',
            'Preta': 'PCD_COR_PRETA',
            'Amarela': 'PCD_COR_AMARELA',
            'Parda': 'PCD_COR_PARDA',
            'Indígena': 'PCD_COR_INDIGENA'
        }), com_def)
        if not df_cor_pcd.empty:
            exibir_grafico_barras(df_cor_pcd, 'Categoria', modo_visualizacao, 'PCD por cor/raça')
            if modo_visualizacao == 'Número de pessoas':
                st.dataframe(df_cor_pcd[['Categoria', 'Quantidade']], use_container_width=True, hide_index=True)
            elif modo_visualizacao == 'Percentual (%)':
                st.dataframe(df_cor_pcd[['Categoria', 'Percentual']], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df_cor_pcd, use_container_width=True, hide_index=True)
        else:
            st.info("Sem dados de cor/raça para deficiência.")

    with c2:
        st.markdown("#### Quantidade de dificuldades funcionais")
        df_qtd_dif = preparar_visualizacao(build_series(df, {
            '1 dificuldade': 'PCD_QTD_1_DIFICULDADE',
            '2 ou mais dificuldades': 'PCD_QTD_2_MAIS_DIFICULDADES'
        }), com_def)
        if not df_qtd_dif.empty:
            valor_pizza = 'Percentual' if modo_visualizacao == 'Percentual (%)' else 'Quantidade'
            fig = px.pie(df_qtd_dif, names='Categoria', values=valor_pizza, title='1 dificuldade vs 2+')
            st.plotly_chart(fig, use_container_width=True)
            if modo_visualizacao == 'Número de pessoas':
                st.dataframe(df_qtd_dif[['Categoria', 'Quantidade']], use_container_width=True, hide_index=True)
            elif modo_visualizacao == 'Percentual (%)':
                st.dataframe(df_qtd_dif[['Categoria', 'Percentual']], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df_qtd_dif, use_container_width=True, hide_index=True)
        else:
            st.info("Sem dados de quantidade de dificuldades.")

    st.markdown("#### Tipos de dificuldades funcionais")
    df_tipos_dif = preparar_visualizacao(build_series(df, {
        'Enxergar': 'PCD_DIFICULDADE_ENXERGAR',
        'Ouvir': 'PCD_DIFICULDADE_OUVIR',
        'Andar/Subir degraus': 'PCD_DIFICULDADE_ANDAR',
        'Pegar objetos': 'PCD_DIFICULDADE_PEGAR_OBJETOS',
        'Funções mentais/comunicação': 'PCD_DIFICULDADE_MENTAL'
    }), com_def)
    if not df_tipos_dif.empty:
        exibir_grafico_barras(df_tipos_dif, 'Categoria', modo_visualizacao, 'Tipos de dificuldades e quantidade')
        if modo_visualizacao == 'Número de pessoas':
            st.dataframe(df_tipos_dif[['Categoria', 'Quantidade']], use_container_width=True, hide_index=True)
        elif modo_visualizacao == 'Percentual (%)':
            st.dataframe(df_tipos_dif[['Categoria', 'Percentual']], use_container_width=True, hide_index=True)
        else:
            st.dataframe(df_tipos_dif, use_container_width=True, hide_index=True)
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
        df_instr = preparar_visualizacao(build_series(df, {
            'Sem instrução e fund. incompleto': 'PCD_INSTRUCAO_SEM_INSTR_FUND_INCOMP',
            'Fund. completo e médio incompleto': 'PCD_INSTRUCAO_FUND_COMP_MEDIO_INCOMP',
            'Médio completo e sup. incompleto': 'PCD_INSTRUCAO_MEDIO_COMP_SUP_INCOMP',
            'Superior completo': 'PCD_INSTRUCAO_SUPERIOR_COMP'
        }), com_def)
        if not df_instr.empty:
            exibir_grafico_barras(df_instr, 'Categoria', modo_visualizacao, 'Nível de instrução - pessoas com deficiência')
            if modo_visualizacao == 'Número de pessoas':
                st.dataframe(df_instr[['Categoria', 'Quantidade']], use_container_width=True, hide_index=True)
            elif modo_visualizacao == 'Percentual (%)':
                st.dataframe(df_instr[['Categoria', 'Percentual']], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df_instr, use_container_width=True, hide_index=True)
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
        df_aut_cor = preparar_visualizacao(build_series(df, {
            'Branca': 'AUTISMO_COR_BRANCA',
            'Preta': 'AUTISMO_COR_PRETA',
            'Amarela': 'AUTISMO_COR_AMARELA',
            'Parda': 'AUTISMO_COR_PARDA',
            'Indígena': 'AUTISMO_COR_INDIGENA'
        }), autismo_diag)
        if not df_aut_cor.empty:
            exibir_grafico_barras(df_aut_cor, 'Categoria', modo_visualizacao, 'Autismo por cor/raça')
            if modo_visualizacao == 'Número de pessoas':
                st.dataframe(df_aut_cor[['Categoria', 'Quantidade']], use_container_width=True, hide_index=True)
            elif modo_visualizacao == 'Percentual (%)':
                st.dataframe(df_aut_cor[['Categoria', 'Percentual']], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df_aut_cor, use_container_width=True, hide_index=True)
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
            if autismo_diag > 0:
                df_sexo['Percentual'] = (df_sexo['Valor'] / autismo_diag) * 100
            else:
                df_sexo['Percentual'] = 0.0

            if modo_visualizacao == 'Percentual (%)':
                fig = px.bar(df_sexo, x='Sexo', y='Percentual', text='Percentual', title='Comparativo homens x mulheres')
                fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            else:
                fig = px.bar(df_sexo, x='Sexo', y='Valor', text='Valor', title='Comparativo homens x mulheres')
                fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            if modo_visualizacao == 'Número de pessoas':
                st.dataframe(df_sexo[['Sexo', 'Valor']], use_container_width=True, hide_index=True)
            elif modo_visualizacao == 'Percentual (%)':
                st.dataframe(df_sexo[['Sexo', 'Percentual']], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df_sexo[['Sexo', 'Valor', 'Percentual']], use_container_width=True, hide_index=True)
        else:
            st.info("Sem dados de homens x mulheres para autismo.")

    with c4:
        st.markdown("#### Pessoas 25+ com autismo por nível de instrução")
        df_aut_25 = preparar_visualizacao(build_series(df, {
            'Sem instrução e fund. incompleto': 'AUTISMO_25_MAIS_SEM_INSTR_FUND_INCOMP',
            'Fund. completo e médio incompleto': 'AUTISMO_25_MAIS_FUND_COMP_MEDIO_INCOMP',
            'Médio completo e sup. incompleto': 'AUTISMO_25_MAIS_MEDIO_COMP_SUP_INCOMP',
            'Superior completo': 'AUTISMO_25_MAIS_SUPERIOR_COMP'
        }), autismo_diag)
        if not df_aut_25.empty:
            exibir_grafico_barras(df_aut_25, 'Categoria', modo_visualizacao, 'Autismo (25+) por instrução')
            if modo_visualizacao == 'Número de pessoas':
                st.dataframe(df_aut_25[['Categoria', 'Quantidade']], use_container_width=True, hide_index=True)
            elif modo_visualizacao == 'Percentual (%)':
                st.dataframe(df_aut_25[['Categoria', 'Percentual']], use_container_width=True, hide_index=True)
            else:
                st.dataframe(df_aut_25, use_container_width=True, hide_index=True)
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
    dom_df['Percentual'] = [100.0 if dom_total > 0 else 0.0, perc_dom_autismo]
    if modo_visualizacao == 'Número de pessoas':
        st.dataframe(dom_df[['Indicador', 'Quantidade']], use_container_width=True, hide_index=True)
    elif modo_visualizacao == 'Percentual (%)':
        st.dataframe(dom_df[['Indicador', 'Percentual']], use_container_width=True, hide_index=True)
    else:
        st.dataframe(dom_df, use_container_width=True, hide_index=True)


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
