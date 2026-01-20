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

from utils.data_loader import get_analisador_individuos
from cetic.individuos.metadados_individuos import MetadadosIndividuos

st.set_page_config(page_title="Cetic Indivíduos", layout="wide")

st.title("📊 CETIC - TIC Indivíduos")

# Categorias de indicadores
CATEGORIAS = {
    "Acesso e Dispositivos": {
        'C1': 'Já acessou a Internet',
        'DISPOSITIVOS': ['C5_A', 'C5_B', 'C5_C', 'C5_D'], # Lista para análise múltipla
        'C5_A': 'Uso de computador de mesa',
        'C5_B': 'Uso de notebook',
        'C5_C': 'Uso de tablet',
        'C5_D': 'Uso de telefone celular',
    },
    "Comunicação": {
        'C7_A': 'Enviar mensagens (WhatsApp, etc.)',
        'C7_B': 'Redes sociais (Instagram, Facebook, etc.)',
        'C7_C': 'Chamadas de voz ou vídeo',
        'C7_F': 'Microblog (X/Twitter)',
    },
    "Comércio e Finanças": {
        'C8_A': 'Procurar informações sobre produtos/serviços',
        'C8_H': 'Transações financeiras (Internet Banking)',
        'C8_I': 'Pagamento por Pix',
        'C9_G': 'Comprar produtos ou serviços',
    },
    "Educação e Trabalho": {
        'C10_A': 'Atividades escolares ou faculdade',
        'C10_F': 'Atividades de trabalho',
        'C8_D': 'Procurar emprego ou enviar currículo',
    },
    "Novas Tecnologias": {
        'C13A': 'Uso de Inteligência Artificial (ChatGPT, etc.)',
    }
}

# Planificar INDICADORES para o selectbox
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

# Determinar se é análise múltipla ou simples
is_multiple = isinstance(selected_indicador_key, str) and selected_indicador_key in [k for cat in CATEGORIAS.values() for k, v in cat.items() if isinstance(v, list)]
actual_indicador = selected_indicador_key
if is_multiple:
    # Encontra a lista de indicadores
    for cat in CATEGORIAS.values():
        if selected_indicador_key in cat and isinstance(cat[selected_indicador_key], list):
            actual_indicador = cat[selected_indicador_key]
            break

# Obter label amigável
if is_multiple:
    label_indicador = f"Comparativo: {selected_indicador_key}"
else:
    meta_col = getattr(MetadadosIndividuos, actual_indicador, None)
    label_indicador = getattr(meta_col, '_label', INDICADORES_FLAT[actual_indicador])

st.subheader(label_indicador)

# Carrega o analisador
analisador = get_analisador_individuos()

# Sidebar - Filtros
st.sidebar.header("Filtros")

def limpar_filtros():
    st.session_state['uf_ind'] = "Brasil"
    st.session_state['area_ind'] = "Todas"
    st.session_state['classe_ind'] = "Todas"
    st.session_state['renda_ind'] = "Todas"
    st.session_state['sexo_ind'] = "Todas"

def get_meta_value(meta_class, label_map, selected_label):
    if selected_label == "Todas" or selected_label == "Brasil":
        return None
    try:
        val = [k for k, v in label_map.items() if v == selected_label][0]
        for attr in dir(meta_class):
            meta_val = getattr(meta_class, attr)
            if isinstance(meta_val, float) and meta_val == val:
                return meta_val
    except Exception:
        pass
    return None

# Filtro de UF
ufs = MetadadosIndividuos.COD_UF._map
uf_options = ["Brasil"] + sorted(list(ufs.values()))
selected_uf_label = st.sidebar.selectbox("UF", uf_options, key='uf_ind')

# Filtro de Área
areas = MetadadosIndividuos.AREA._map
area_options = ["Todas"] + list(areas.values())
selected_area_label = st.sidebar.selectbox("Área", area_options, key='area_ind')

# Filtro de Classe Social
classes = MetadadosIndividuos.CLASSE_2015._map
class_options = ["Todas"] + list(classes.values())
selected_class_label = st.sidebar.selectbox("Classe Social", class_options, key='classe_ind')

# Filtro de Renda Familiar
rendas = MetadadosIndividuos.RENDA_FAMILIAR_2._map
renda_options = ["Todas"] + list(rendas.values())
selected_renda_label = st.sidebar.selectbox("Renda Familiar", renda_options, key='renda_ind')

# Filtro de Sexo
sexos = MetadadosIndividuos.SEXO._map
sexo_options = ["Todas"] + list(sexos.values())
selected_sexo_label = st.sidebar.selectbox("Sexo", sexo_options, key='sexo_ind')

st.sidebar.button("Limpar filtros", on_click=limpar_filtros)

# Preparar filtros para a análise
filtros = []
f_uf = get_meta_value(MetadadosIndividuos.COD_UF, ufs, selected_uf_label)
if f_uf: filtros.append(f_uf)

f_area = get_meta_value(MetadadosIndividuos.AREA, areas, selected_area_label)
if f_area: filtros.append(f_area)

f_class = get_meta_value(MetadadosIndividuos.CLASSE_2015, classes, selected_class_label)
if f_class: filtros.append(f_class)

f_renda = get_meta_value(MetadadosIndividuos.RENDA_FAMILIAR_2, rendas, selected_renda_label)
if f_renda: filtros.append(f_renda)

f_sexo = get_meta_value(MetadadosIndividuos.SEXO, sexos, selected_sexo_label)
if f_sexo: filtros.append(f_sexo)

# Executar análise
# Criamos uma cópia do dataframe para filtragem local
df_filtrado = analisador.df.copy()

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
            # Converte percentual string para float
            chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
            
            # Gráfico de barras
            st.bar_chart(chart_data, x="Descrição", y="Percentual_Num")
            
            # KPI (Apenas se tiver 'Sim' ou 'Sim, nos últimos 3 meses')
            if not is_multiple:
                sim_row = res[res['Descrição'].str.contains('Sim', case=False, na=False)]
                if not sim_row.empty:
                    st.metric(f"{selected_indicador_key} (Positivo)", sim_row['Percentual'].values[0])
            else:
                # Para múltiplo, destaca o maior
                top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                st.metric(f"Maior Uso: {top_row['Indicador']}", top_row['Percentual'])
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

st.markdown("---")
st.caption("Fonte: Microdados da TIC Domicílios/Indivíduos 2025 (CETIC.br)")
