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

# Categorias de indicadores
CATEGORIAS = {
    "Infraestrutura": {
        'A4': 'Acesso à Internet',
        'A1_A': 'Possui Computador de mesa',
        'A1_B': 'Possui Notebook',
        'A1_C': 'Possui Tablet',
        'A1_AGREG': 'Possui algum tipo de computador',
        'A1A4': 'Presença de computador e Internet',
    },
    "Conexão": {
        'A7': 'Principal tipo de conexão',
        'A7A': 'Possui WiFi',
        'A8A': 'Velocidade da Internet',
        'A9_FAIXA': 'Valor pago pela conexão',
    },
    "Barreiras (Motivo principal)": {
        'A5A': 'Principal motivo de falta de Internet',
    },
    "Barreiras (Múltipla escolha)": {
        'A5_A': 'Falta de computador',
        'A5_B': 'Falta de necessidade',
        'A5_C': 'Falta de interesse',
        'A5_E': 'Muito caro',
        'A5_F': 'Não sabem usar',
        'BARREIRAS': ['A5_A', 'A5_B', 'A5_C', 'A5_E', 'A5_F'],
    }
}

# Planificar INDICADORES
INDICADORES_FLAT = {}
for cat, inds in CATEGORIAS.items():
    for k, v in inds.items():
        if isinstance(v, str):
            INDICADORES_FLAT[k] = f"[{cat}] {v}"
        else:
            INDICADORES_FLAT[k] = f"[{cat}] COMPARATIVO: {k}"

selected_indicador_key = st.selectbox("Selecione o Indicador para Análise", 
                                      options=list(INDICADORES_FLAT.keys()),
                                      format_func=lambda x: INDICADORES_FLAT[x])

# Determinar se é análise múltipla
is_multiple = isinstance(selected_indicador_key, str) and selected_indicador_key in [k for cat in CATEGORIAS.values() for k, v in cat.items() if isinstance(v, list)]
actual_indicador = selected_indicador_key
if is_multiple:
    for cat in CATEGORIAS.values():
        if selected_indicador_key in cat and isinstance(cat[selected_indicador_key], list):
            actual_indicador = cat[selected_indicador_key]
            break

# Obter label amigável
if is_multiple:
    label_indicador = f"Comparativo: {selected_indicador_key}"
else:
    meta_col = getattr(Metadados, actual_indicador, None)
    label_indicador = getattr(meta_col, '_label', INDICADORES_FLAT[actual_indicador])

st.subheader(label_indicador)

# Carrega o analisador
analisador = get_analisador_domicilios()

# Sidebar - Filtros
st.sidebar.header("Filtros")

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

# O analisador.filtrar_dados modifica self.df, então vamos instanciar um novo ou usar o método de forma isolada
# Para simplificar aqui e garantir que o cache funcione bem, vamos usar o analisar_indicador passando o df filtrado manualmente
for f in filtros:
    col = f.column
    df_filtrado = df_filtrado[df_filtrado[col] == f]

st.info(f"Registros encontrados: {len(df_filtrado)}")

# Análise do Indicador Selecionado
if len(df_filtrado) > 0:
    res = analisador.analisar_indicador(actual_indicador, df_contexto=df_filtrado)
    
    if res is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("### Tabela de Resultados")
            st.dataframe(res, use_container_width=True)
            
        with col2:
            st.write("### Visualização")
            chart_data = res.copy()
            chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
            
            # Gráfico de barras
            st.bar_chart(chart_data, x="Descrição", y="Percentual_Num")
            
            # KPI (Apenas se tiver 'Sim')
            if not is_multiple:
                sim_row = res[res['Descrição'] == 'Sim']
                if not sim_row.empty:
                    st.metric(f"{selected_indicador_key} (Sim)", sim_row['Percentual'].values[0])
            else:
                top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                st.metric(f"Maior: {top_row['Indicador']}", top_row['Percentual'])
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

st.markdown("---")
st.caption("Fonte: Microdados da TIC Domicílios 2025 (CETIC.br)")
