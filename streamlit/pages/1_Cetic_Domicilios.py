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

from utils.data_loader import get_analisador_domicilios
from cetic.domicilios.metadados import Metadados

st.set_page_config(page_title="Cetic Domicílios", layout="wide")

st.title("📊 CETIC - TIC Domicílios")

# Categorias de indicadores - TODOS os indicadores disponíveis
CATEGORIAS = {
    "📊 Acesso e Conectividade": {
        'A4': 'Acesso à Internet',
        'A4_COB': 'Acesso à Internet (ampliado)',
        'A7D': 'Algum morador tem acesso à Internet',
        'A1A4': 'Presença de computador e Internet',
    },
    "💻 Equipamentos - Disponibilidade": {
        'A1_A': 'Possui Computador de mesa',
        'A1_B': 'Possui Notebook',
        'A1_C': 'Possui Tablet',
        'A1_AGREG': 'Possui algum tipo de computador',
        'A1_EXCLUSIVOS': 'Tipo de computador (exclusivo/simultâneo)',
        'DIC_CEL': 'Equipamentos TIC no domicílio',
        'EQUIPAMENTOS_COMPUTADOR': ['A1_A', 'A1_B', 'A1_C'],
    },
    "🔢 Equipamentos - Quantidade": {
        'A2_QTD_DESK': 'Quantidade de computadores de mesa',
        'A2_QTD_NOTE': 'Quantidade de notebooks',
        'A2_QTD_TAB': 'Quantidade de tablets',
        'A2_A_FAIXA': 'Faixa de quantidade - Computador de mesa',
        'A2_B_FAIXA': 'Faixa de quantidade - Notebook',
        'A2_C_FAIXA': 'Faixa de quantidade - Tablet',
    },
    "🌐 Tipo de Conexão": {
        'A7': 'Principal tipo de conexão',
        'A7A': 'Possui WiFi',
        'A7B': 'Internet compartilhada com vizinho',
        'A7C': 'Meio de acesso à rede móvel (3G/4G/5G)',
        'A7_AGREG': 'Tipo de conexão (agregado)',
    },
    "⚡ Velocidade e Custo": {
        'A8A': 'Velocidade da Internet contratada',
        'A9A': 'Valor pago pela Internet',
        'A9B': 'Valor inclui pacote/combo',
        'A9C': 'Sabe o valor apenas da Internet',
        'A9D': 'Valor pago apenas pela Internet',
        'A9_FAIXA': 'Faixa de valor pago pela conexão',
    },
    "🚫 Barreiras - Individual": {
        'A5_A': 'Falta de computador',
        'A5_B': 'Falta de necessidade',
        'A5_C': 'Falta de interesse',
        'A5_D': 'Acesso em outro lugar',
        'A5_E': 'Muito caro',
        'A5_F': 'Não sabem usar',
        'A5_G': 'Falta de disponibilidade na região',
        'A5_H': 'Preocupações com segurança/privacidade',
        'A5_I': 'Evitam conteúdo perigoso',
        'A5_OUTRO': 'Outro motivo',
    },
    "🎯 Barreiras - Análise": {
        'A5A': 'Principal motivo de falta de Internet',
        'A5_NENHUM': 'Motivos para falta de Internet',
        'BARREIRAS_PRINCIPAIS': ['A5_A', 'A5_B', 'A5_C', 'A5_E', 'A5_F'],
        'BARREIRAS_TODAS': ['A5_A', 'A5_B', 'A5_C', 'A5_D', 'A5_E', 'A5_F', 'A5_G', 'A5_H', 'A5_I'],
    },
    "🏠 Características do Domicílio": {
        'TV_ASSINATURA': 'Possui TV por assinatura',
        'ANTENA_PARABOLICA': 'Possui antena parabólica',
        'RUA': 'Tipo de pavimentação da rua',
    },
    "👥 Perfil Socioeconômico": {
        'RENDA_FAMILIAR': 'Renda familiar',
        'RENDA_FAMILIAR_2': 'Renda familiar (v2)',
        'CLASSE_2015': 'Classe social',
        'GRAU_INSTRUCAO': 'Escolaridade do responsável',
        'PNADC_RD_A': 'Recebe BPC-LOAS',
        'PNADC_RD_B': 'Recebe Bolsa Família/Auxílio Brasil',
    },
    "📍 Localização": {
        'COD_UF': 'UF',
        'COD_REGIAO_2': 'Região',
        'AREA': 'Área (Urbana/Rural)',
    },
}

# Contar indicadores
total_indicadores = sum(1 for cat in CATEGORIAS.values() for k, v in cat.items() if isinstance(v, str))
total_comparativos = sum(1 for cat in CATEGORIAS.values() for k, v in cat.items() if isinstance(v, list))

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
        options=list(CATEGORIAS.keys()),
        help="Selecione uma categoria de indicadores"
    )

# Planificar INDICADORES da categoria selecionada
INDICADORES_CATEGORIA = {}
for k, v in CATEGORIAS[selected_category].items():
    if isinstance(v, str):
        INDICADORES_CATEGORIA[k] = v
    else:
        INDICADORES_CATEGORIA[k] = f"COMPARATIVO: {k}"

with col_ind:
    selected_indicador_key = st.selectbox(
        "📊 Indicador",
        options=list(INDICADORES_CATEGORIA.keys()),
        format_func=lambda x: INDICADORES_CATEGORIA[x],
        help="Selecione o indicador específico"
    )

# Determinar se é análise múltipla
is_multiple = False
actual_indicador = selected_indicador_key

# Verificar se o indicador selecionado é uma lista (comparativo)
for cat in CATEGORIAS.values():
    if selected_indicador_key in cat and isinstance(cat[selected_indicador_key], list):
        is_multiple = True
        actual_indicador = cat[selected_indicador_key]
        break

# Obter label amigável
if is_multiple:
    label_indicador = f"📊 Comparativo: {selected_indicador_key}"
else:
    meta_col = getattr(Metadados, actual_indicador, None)
    label_indicador = getattr(meta_col, '_label', INDICADORES_CATEGORIA.get(actual_indicador, actual_indicador))

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
            **Itens:** {', '.join(actual_indicador)}
            """)
        else:
            st.markdown(f"""
            **Label completa:**  
            {label_indicador}
            """)

st.markdown("---")

# Carrega o analisador
analisador = get_analisador_domicilios()

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")

# Informações sobre a base
with st.sidebar.expander("📊 Sobre a Base de Dados", expanded=False):
    st.markdown(f"""
    **Total de Registros:** {len(analisador.df):,}  
    **Ano:** 2025  
    **Fonte:** CETIC.br  
    **Tipo:** TIC Domicílios
    """)

st.sidebar.markdown("---")

def limpar_filtros():
    st.session_state['uf_dom'] = "Brasil"
    st.session_state['area_dom'] = "Todas"
    st.session_state['classe_dom'] = "Todas"
    st.session_state['renda_dom'] = "Todas"
    st.session_state['regiao_dom'] = "Brasil"

# Filtro de UF
ufs = Metadados.COD_UF._map
uf_options = ["Brasil"] + list(ufs.values())
selected_uf_label = st.sidebar.selectbox("UF", uf_options, key='uf_dom')

# Filtro de Área
areas = Metadados.AREA._map
area_options = ["Todas"] + list(areas.values())
selected_area_label = st.sidebar.selectbox("Área", area_options, key='area_dom')

# Filtro de Classe Social
classes = Metadados.CLASSE_2015._map
class_options = ["Todas"] + list(classes.values())
selected_class_label = st.sidebar.selectbox("Classe Social", class_options, key='classe_dom')

# Filtro de Renda Familiar
rendas = Metadados.RENDA_FAMILIAR_2._map
renda_options = ["Todas"] + list(rendas.values())
selected_renda_label = st.sidebar.selectbox("Renda Familiar", renda_options, key='renda_dom')

# Filtro de Região
regioes = Metadados.COD_REGIAO_2._map
regiao_options = ["Brasil"] + list(regioes.values())
selected_regiao_label = st.sidebar.selectbox("Região", regiao_options, key='regiao_dom')

st.sidebar.button("Limpar filtros", on_click=limpar_filtros)

# Preparar filtros para o analisador
filtros = []

def get_meta_value(meta_class, label_map, selected_label):
    if selected_label == "Todas" or selected_label == "Brasil":
        return None
    val = [k for k, v in label_map.items() if v == selected_label][0]
    for attr in dir(meta_class):
        meta_val = getattr(meta_class, attr)
        if isinstance(meta_val, float) and meta_val == val:
            return meta_val
    return None

f_uf = get_meta_value(Metadados.COD_UF, ufs, selected_uf_label)
if f_uf: filtros.append(f_uf)

f_area = get_meta_value(Metadados.AREA, areas, selected_area_label)
if f_area: filtros.append(f_area)

f_class = get_meta_value(Metadados.CLASSE_2015, classes, selected_class_label)
if f_class: filtros.append(f_class)

f_renda = get_meta_value(Metadados.RENDA_FAMILIAR_2, rendas, selected_renda_label)
if f_renda: filtros.append(f_renda)

f_regiao = get_meta_value(Metadados.COD_REGIAO_2, regioes, selected_regiao_label)
if f_regiao: filtros.append(f_regiao)

# Executar análise
# Criamos uma cópia do dataframe para não afetar o original no analisador (que é cacheado)
df_filtrado = analisador.df.copy()
total_original = len(df_filtrado)

# Aplicar os filtros
for f in filtros:
    col = f.column
    df_filtrado = df_filtrado[df_filtrado[col] == f]

# Mostrar informações de filtros de forma mais visual
filtros_ativos = []
if len(filtros) > 0:
    for f in filtros:
        col = f.column
        meta_class = getattr(Metadados, col, None)
        if meta_class and hasattr(meta_class, '_map'):
            label = meta_class._map.get(float(f), str(f))
            col_name = getattr(meta_class, '_label', col)
            filtros_ativos.append(f"**{col_name}:** {label}")

# Layout melhorado com métricas
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.metric("📊 Registros", f"{len(df_filtrado):,}",
              delta=f"{len(df_filtrado) - total_original:,}" if len(filtros) > 0 else None,
              delta_color="off")

with col_info2:
    if len(filtros) > 0:
        st.metric("🔍 Filtros Ativos", len(filtros))
    else:
        st.metric("🔍 Filtros Ativos", "Nenhum")

with col_info3:
    percentual = (len(df_filtrado) / total_original * 100) if total_original > 0 else 0
    st.metric("📈 % da Base", f"{percentual:.1f}%")

# Mostrar filtros ativos em expander
if filtros_ativos:
    with st.expander("🔎 Detalhes dos Filtros Ativos", expanded=False):
        for filtro in filtros_ativos:
            st.markdown(f"- {filtro}")

# Análise do Indicador Selecionado
if len(df_filtrado) > 0:
    res = analisador.analisar_indicador(actual_indicador, df_contexto=df_filtrado)

    if res is not None:
        # Usar tabs para organizar melhor
        tab1, tab2, tab3 = st.tabs(["📊 Resumo", "📈 Gráficos", "📥 Dados"])

        with tab1:
            # Resumo com KPIs principais
            col1, col2, col3 = st.columns(3)

            with col1:
                if not is_multiple:
                    sim_row = res[res['Descrição'] == 'Sim']
                    if not sim_row.empty:
                        st.metric("✅ Sim", sim_row['Percentual'].values[0],
                                 help="Percentual de domicílios que responderam 'Sim'")
                else:
                    chart_data = res.copy()
                    chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                    top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                    st.metric("🏆 Maior", f"{top_row['Indicador']}: {top_row['Percentual']}")

            with col2:
                if not is_multiple:
                    nao_row = res[res['Descrição'] == 'Não']
                    if not nao_row.empty:
                        st.metric("❌ Não", nao_row['Percentual'].values[0],
                                 help="Percentual de domicílios que responderam 'Não'")

            with col3:
                st.metric("📋 Total de Categorias", len(res),
                         help="Número de categorias de resposta")

            st.markdown("---")

            # Tabela formatada
            st.write("### 📊 Tabela Detalhada")
            st.dataframe(res, use_container_width=True, height=300)

        with tab2:
            # Gráficos melhorados
            chart_data = res.copy()
            chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)

            col_g1, col_g2 = st.columns(2)

            with col_g1:
                st.write("### 📊 Gráfico de Barras")
                st.bar_chart(chart_data, x="Descrição", y="Percentual_Num", height=400)

            with col_g2:
                st.write("### 🥧 Distribuição")
                # Criar visualização alternativa
                top_5 = chart_data.nlargest(5, 'Percentual_Num')
                for idx, row in top_5.iterrows():
                    st.progress(row['Percentual_Num'] / 100,
                              text=f"{row['Descrição']}: {row['Percentual']}")

        with tab3:
            # Download dos dados
            st.write("### 📥 Exportar Dados")

            col_d1, col_d2 = st.columns(2)

            with col_d1:
                # Preparar dados para download
                csv = res.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"cetic_domicilios_{selected_indicador_key}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    help="Baixar dados em formato CSV"
                )

            with col_d2:
                # Mostrar informações sobre os dados
                st.info(f"""
                **Informações do Dataset:**
                - Indicador: {selected_indicador_key}
                - Registros: {len(df_filtrado):,}
                - Categorias: {len(res)}
                - Data: {pd.Timestamp.now().strftime('%d/%m/%Y')}
                """)

            st.write("### 📋 Pré-visualização dos Dados")
            st.dataframe(res, use_container_width=True)
else:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.info("💡 **Dica:** Tente remover alguns filtros ou selecionar uma combinação diferente.")

st.markdown("---")
st.caption("Fonte: Microdados da TIC Domicílios 2025 (CETIC.br)")
