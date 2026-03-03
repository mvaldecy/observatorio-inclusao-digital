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
from utils.http_loader import HTTPDataLoader
from cetic.individuos.metadados_individuos import MetadadosIndividuos
from components.categorias_cetic import CATEGORIAS_INDIVIDUOS
from components.header import render_header

st.set_page_config(page_title="Cetic Indivíduos", layout="wide")

# CSS customizado para remover bordas laranja/vermelhas e melhorar estética
st.markdown("""
<style>
    /* Remove todas as bordas laranja/vermelhas de labels, headers e títulos */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] label,
    label[data-baseweb="label"],
    div[data-baseweb="label"] {
        border: none !important;
        outline: none !important;
    }
    
    /* Remove bordas em elementos com classe de label */
    .stSelectbox label,
    .stMultiSelect label,
    div[role="option"] {
        border: none !important;
        outline: none !important;
    }
    
    /* Remove borda laranja de inputs e selects */
    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="combobox"],
    div[role="listbox"],
    div[data-baseweb="select"] {
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        outline: none !important;
    }
    
    /* Remove overlay/borda laranja no focus */
    [data-baseweb="input"]:focus,
    [data-baseweb="select"]:focus,
    [data-baseweb="combobox"]:focus,
    input:focus {
        border-color: #0d58ca !important;
        box-shadow: 0 0 0 1px #0d58ca !important;
        outline: none !important;
    }
    
    /* Remove bordas de modal/dropdown */
    div[style*="background"] > div[role="listbox"] {
        border: 1px solid #ccc !important;
        outline: none !important;
    }
    
    /* Melhora multiselect appearance */
    div[data-testid="stMultiSelect"] span {
        color: #262730 !important;
        border: none !important;
    }
    
    /* Melhora elementos de input */
    input {
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        outline: none !important;
    }
    
    /* Remove qualquer borda vermelha de erro */
    input:invalid {
        border-color: #ccc !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Remove bordas em elementos do sidebar */
    [data-testid="stSidebar"] div[data-baseweb] {
        border: none !important;
    }
    
    /* Remove cor de highlight laranja */
    div[style*="rgb(255, 159, 64)"],
    div[style*="#FF9F40"],
    div[style*="#ffb3b3"],
    div[style*="orange"] {
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Configurações de Ano e Cache no Sidebar (antes dos filtros)
st.sidebar.title("⚙️ Configurações")

# Seletor de ano
loader = HTTPDataLoader()
anos_disponiveis = loader.get_anos_disponiveis('individuos')

ano_selecionado = st.sidebar.selectbox(
    "📅 Ano da Pesquisa",
    options=anos_disponiveis,
    index=0,  # Usa 2024 como padrão (primeiro da lista, já que 2025 indivíduos ainda não disponível)
    help="Selecione o ano da pesquisa TIC Indivíduos",
)

# Botões de gerenciamento de cache
col_btn1, col_btn2 = st.sidebar.columns(2)

with col_btn1:
    if st.button("🔄 Atualizar", help="Baixar nova versão dos dados", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        loader.carregar_dados(ano_selecionado, 'individuos', force_download=True)
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

# Carrega analisador (com cache por ano)
try:
    analisador = get_analisador_individuos(ano=ano_selecionado)
except Exception as e:
    st.error(f"❌ Erro ao carregar dados de {ano_selecionado}: {str(e)}")
    st.info("💡 **Dica:** Verifique sua conexão com a internet ou tente limpar o cache.")
    st.stop()

render_header(f"CETIC - TIC Indivíduos {ano_selecionado}", "📊")

# Usa categorias importadas do arquivo centralizado
CATEGORIAS = CATEGORIAS_INDIVIDUOS

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
    meta_col = getattr(MetadadosIndividuos, actual_indicador, None)
    label_indicador = getattr(meta_col, '_label', INDICADORES_CATEGORIA.get(actual_indicador, actual_indicador))

st.subheader(label_indicador)


# Sidebar - Filtros
st.sidebar.header("Filtros")

def limpar_filtros():
    st.session_state['uf_ind'] = "Brasil"
    st.session_state['classe_ind'] = "Todas"
    st.session_state['renda_ind'] = "Todas"
    st.session_state['sexo_ind'] = "Todos"
    st.session_state['regiao_ind'] = "Brasil"
    st.session_state['faixa_etaria_ind'] = "Todas"

# Função auxiliar para verificar disponibilidade de metadados
def verificar_metadado_disponivel(nome_campo):
    try:
        campo = getattr(MetadadosIndividuos, nome_campo, None)
        return campo is not None and hasattr(campo, '_map') and len(campo._map) > 0
    except:
        return False

# Filtro de UF
if verificar_metadado_disponivel('COD_UF'):
    ufs = MetadadosIndividuos.COD_UF._map
    uf_options = ["Brasil"] + list(ufs.values())
    selected_uf_label = st.sidebar.selectbox("UF", uf_options, key='uf_ind')
else:
    st.sidebar.warning(f"⚠️ Filtro de UF indisponível em {ano_selecionado}")
    selected_uf_label = "Brasil"
    ufs = {}

# Filtro de Classe Social
if verificar_metadado_disponivel('CLASSE_2015'):
    classes = MetadadosIndividuos.CLASSE_2015._map
    class_options = ["Todas"] + list(classes.values())
    selected_class_label = st.sidebar.selectbox("Classe Social", class_options, key='classe_ind')
else:
    st.sidebar.warning(f"⚠️ Filtro de Classe Social indisponível em {ano_selecionado}")
    selected_class_label = "Todas"
    classes = {}

# Filtro de Renda Familiar
if verificar_metadado_disponivel('RENDA_FAMILIAR_2'):
    rendas = MetadadosIndividuos.RENDA_FAMILIAR_2._map
    renda_options = ["Todas"] + list(rendas.values())
    selected_renda_label = st.sidebar.selectbox("Renda Familiar", renda_options, key='renda_ind')
else:
    st.sidebar.warning(f"⚠️ Filtro de Renda Familiar indisponível em {ano_selecionado}")
    selected_renda_label = "Todas"
    rendas = {}

# Filtro de Sexo
if verificar_metadado_disponivel('SEXO'):
    sexos = MetadadosIndividuos.SEXO._map
    sexo_options = ["Todos"] + list(sexos.values())
    selected_sexo_label = st.sidebar.selectbox("Sexo", sexo_options, key='sexo_ind')
else:
    st.sidebar.warning(f"⚠️ Filtro de Sexo indisponível em {ano_selecionado}")
    selected_sexo_label = "Todos"
    sexos = {}

# Filtro de Região
if verificar_metadado_disponivel('COD_REGIAO_2'):
    regioes = MetadadosIndividuos.COD_REGIAO_2._map
    regiao_options = ["Brasil"] + list(regioes.values())
    selected_regiao_label = st.sidebar.selectbox("Região", regiao_options, key='regiao_ind')
else:
    st.sidebar.warning(f"⚠️ Filtro de Região indisponível em {ano_selecionado}")
    selected_regiao_label = "Brasil"
    regioes = {}

# Filtro de Faixa Etária
if verificar_metadado_disponivel('FAIXA_ETARIA'):
    faixas_etarias = MetadadosIndividuos.FAIXA_ETARIA._map
    faixa_options = ["Todas"] + list(faixas_etarias.values())
    selected_faixa_label = st.sidebar.selectbox("Faixa Etária", faixa_options, key='faixa_etaria_ind')
else:
    st.sidebar.warning(f"⚠️ Filtro de Faixa Etária indisponível em {ano_selecionado}")
    selected_faixa_label = "Todas"
    faixas_etarias = {}

st.sidebar.button("Limpar filtros", on_click=limpar_filtros)

# Preparar filtros para o analisador
filtros = []

def get_meta_value(meta_class, label_map, selected_label):
    if selected_label == "Todas" or selected_label == "Brasil" or selected_label == "Todos":
        return None
    if not label_map:  # Se o mapa está vazio, retorna None
        return None
    try:
        val = [k for k, v in label_map.items() if v == selected_label]
        if not val:
            return None
        val = val[0]
        for attr in dir(meta_class):
            meta_val = getattr(meta_class, attr)
            if isinstance(meta_val, float) and meta_val == val:
                return meta_val
    except:
        return None
    return None

f_uf = get_meta_value(MetadadosIndividuos.COD_UF, ufs, selected_uf_label)
if f_uf: filtros.append(f_uf)

f_class = get_meta_value(MetadadosIndividuos.CLASSE_2015, classes, selected_class_label)
if f_class: filtros.append(f_class)

f_renda = get_meta_value(MetadadosIndividuos.RENDA_FAMILIAR_2, rendas, selected_renda_label)
if f_renda: filtros.append(f_renda)

f_sexo = get_meta_value(MetadadosIndividuos.SEXO, sexos, selected_sexo_label)
if f_sexo: filtros.append(f_sexo)

f_regiao = get_meta_value(MetadadosIndividuos.COD_REGIAO_2, regioes, selected_regiao_label)
if f_regiao: filtros.append(f_regiao)

f_faixa = get_meta_value(MetadadosIndividuos.FAIXA_ETARIA, faixas_etarias, selected_faixa_label)
if f_faixa: filtros.append(f_faixa)

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
        meta_class = getattr(MetadadosIndividuos, col, None)
        if meta_class and hasattr(meta_class, '_map'):
            label = meta_class._map.get(float(f), str(f))
            col_name = getattr(meta_class, '_label', col)
            filtros_ativos.append(f"**{col_name}:** {label}")

# Layout melhorado com métricas
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.metric("📊 Registros", f"{len(df_filtrado):,}")

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
    # Criar abas principais
    tab_comparativo, tab_agregadores, tab_customizado = st.tabs(["🗺️ Comparativo Geográfico", "📊 Agregadores", "🔍 Análise Customizada"])

    with tab_comparativo:
        st.markdown("### 📍 Comparação: Brasil | Nordeste | Piauí")
        st.markdown("Visualização fixa das três regiões de interesse. Você pode aplicar filtros adicionais abaixo.")

        # Sub-filtros para o comparativo geográfico
        st.markdown("---")
        col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)

        with col_f1:
            # Filtro de Classe para comparativo
            class_comp_options = ["Todas"] + list(classes.values())
            selected_class_comp = st.selectbox("💼 Classe Social", class_comp_options, key='classe_comp')

        with col_f2:
            # Filtro de Renda para comparativo
            renda_comp_options = ["Todas"] + list(rendas.values())
            selected_renda_comp = st.selectbox("💰 Renda Familiar", renda_comp_options, key='renda_comp')

        with col_f3:
            # Filtro de Sexo para comparativo
            sexo_comp_options = ["Todos"] + list(sexos.values())
            selected_sexo_comp = st.selectbox("👤 Sexo", sexo_comp_options, key='sexo_comp')

        with col_f4:
            # Filtro de Faixa Etária para comparativo
            faixa_comp_options = ["Todas"] + list(faixas_etarias.values())
            selected_faixa_comp = st.selectbox("🎂 Faixa Etária", faixa_comp_options, key='faixa_comp')

        with col_f5:
            if st.button("🔄 Resetar Filtros Comparativo", key='reset_comp'):
                st.rerun()

        # Aplicar filtros adicionais ao comparativo
        filtros_comp = []

        f_class_comp = get_meta_value(MetadadosIndividuos.CLASSE_2015, classes, selected_class_comp)
        if f_class_comp: filtros_comp.append(f_class_comp)

        f_renda_comp = get_meta_value(MetadadosIndividuos.RENDA_FAMILIAR_2, rendas, selected_renda_comp)
        if f_renda_comp: filtros_comp.append(f_renda_comp)

        f_sexo_comp = get_meta_value(MetadadosIndividuos.SEXO, sexos, selected_sexo_comp)
        if f_sexo_comp: filtros_comp.append(f_sexo_comp)

        f_faixa_comp = get_meta_value(MetadadosIndividuos.FAIXA_ETARIA, faixas_etarias, selected_faixa_comp)
        if f_faixa_comp: filtros_comp.append(f_faixa_comp)

        st.markdown("---")

        # Verificar se COD_UF existe no dataset (só existe em 2025+)
        tem_cod_uf = 'COD_UF' in analisador.df.columns

        # Análises para Brasil, Nordeste e Piauí (se disponível)
        if tem_cod_uf:
            col_brasil, col_nordeste, col_piaui = st.columns(3)
        else:
            col_brasil, col_nordeste = st.columns(2)
            st.info("ℹ️ Dados por estado (Piauí) disponíveis apenas a partir de 2025")

        # BRASIL
        with col_brasil:
            st.markdown("#### 🇧🇷 Brasil")
            df_brasil = analisador.df.copy()
            for f in filtros_comp:
                col = f.column
                df_brasil = df_brasil[df_brasil[col] == f]

            res_brasil = analisador.analisar_indicador(actual_indicador, df_contexto=df_brasil)

            if res_brasil is not None and len(res_brasil) > 0:
                st.metric("📊 Registros", f"{len(df_brasil):,}")

                # Mostrar KPI principal
                if not is_multiple:
                    sim_row = res_brasil[res_brasil['Descrição'] == 'Sim']
                    if not sim_row.empty:
                        st.metric("✅ Sim", sim_row['Percentual'].values[0])
                else:
                    chart_data = res_brasil.copy()
                    chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                    top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                    st.metric("🏆 Maior", f"{top_row['Percentual']}")
                    st.caption(top_row['Descrição'])

                # Gráfico de barras
                chart_data = res_brasil.copy()
                chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                st.bar_chart(chart_data, x="Descrição", y="Percentual_Num", height=300)

                with st.expander("📋 Ver Dados Completos"):
                    st.dataframe(res_brasil, use_container_width=True)
            else:
                st.warning("Sem dados")

        # NORDESTE
        with col_nordeste:
            st.markdown("#### 🌴 Nordeste")
            df_nordeste = analisador.df.copy()
            df_nordeste = df_nordeste[df_nordeste['COD_REGIAO_2'] == MetadadosIndividuos.COD_REGIAO_2.NORDESTE]
            for f in filtros_comp:
                col = f.column
                df_nordeste = df_nordeste[df_nordeste[col] == f]

            res_nordeste = analisador.analisar_indicador(actual_indicador, df_contexto=df_nordeste)

            if res_nordeste is not None and len(res_nordeste) > 0:
                st.metric("�� Registros", f"{len(df_nordeste):,}")

                # Mostrar KPI principal
                if not is_multiple:
                    sim_row = res_nordeste[res_nordeste['Descrição'] == 'Sim']
                    if not sim_row.empty:
                        st.metric("✅ Sim", sim_row['Percentual'].values[0])
                else:
                    chart_data = res_nordeste.copy()
                    chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                    top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                    st.metric("🏆 Maior", f"{top_row['Percentual']}")
                    st.caption(top_row['Descrição'])

                # Gráfico de barras
                chart_data = res_nordeste.copy()
                chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                st.bar_chart(chart_data, x="Descrição", y="Percentual_Num", height=300)

                with st.expander("📋 Ver Dados Completos"):
                    st.dataframe(res_nordeste, use_container_width=True)
            else:
                st.warning("Sem dados")

        # PIAUÍ (apenas se COD_UF existir - 2025+)
        res_piaui = None
        if tem_cod_uf:
            with col_piaui:
                st.markdown("#### 🏛️ Piauí")
                df_piaui = analisador.df.copy()
                df_piaui = df_piaui[df_piaui['COD_UF'] == MetadadosIndividuos.COD_UF.PIAUI]
                for f in filtros_comp:
                    col = f.column
                    df_piaui = df_piaui[df_piaui[col] == f]

                res_piaui = analisador.analisar_indicador(actual_indicador, df_contexto=df_piaui)

                if res_piaui is not None and len(res_piaui) > 0:
                    st.metric("📊 Registros", f"{len(df_piaui):,}")

                    # Mostrar KPI principal
                    if not is_multiple:
                        sim_row = res_piaui[res_piaui['Descrição'] == 'Sim']
                        if not sim_row.empty:
                            st.metric("✅ Sim", sim_row['Percentual'].values[0])
                    else:
                        chart_data = res_piaui.copy()
                        chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                        top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                        st.metric("🏆 Maior", f"{top_row['Percentual']}")
                        st.caption(top_row['Descrição'])

                    # Gráfico de barras
                    chart_data = res_piaui.copy()
                    chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                    st.bar_chart(chart_data, x="Descrição", y="Percentual_Num", height=300)

                    with st.expander("📋 Ver Dados Completos"):
                        st.dataframe(res_piaui, use_container_width=True)
                else:
                    st.warning("Sem dados")

        # Gráfico comparativo consolidado
        st.markdown("---")
        st.markdown("### 📊 Visão Consolidada")

        # Verificar quais resultados estão disponíveis
        tem_brasil = res_brasil is not None and len(res_brasil) > 0
        tem_nordeste = res_nordeste is not None and len(res_nordeste) > 0
        tem_piaui = res_piaui is not None and len(res_piaui) > 0

        if tem_brasil and tem_nordeste:
            # Criar dataframe comparativo
            df_comp_list = []

            for idx, row in res_brasil.iterrows():
                df_comp_list.append({
                    'Região': 'Brasil',
                    'Categoria': row['Descrição'],
                    'Percentual': float(row['Percentual'].replace('%', ''))
                })

            for idx, row in res_nordeste.iterrows():
                df_comp_list.append({
                    'Região': 'Nordeste',
                    'Categoria': row['Descrição'],
                    'Percentual': float(row['Percentual'].replace('%', ''))
                })

            if tem_piaui:
                for idx, row in res_piaui.iterrows():
                    df_comp_list.append({
                        'Região': 'Piauí',
                        'Categoria': row['Descrição'],
                        'Percentual': float(row['Percentual'].replace('%', ''))
                    })

            df_comparativo = pd.DataFrame(df_comp_list)

            # Criar gráfico de barras agrupadas usando pivot
            df_pivot = df_comparativo.pivot(index='Categoria', columns='Região', values='Percentual')

            # Tabela comparativa (sempre visível)
            st.dataframe(df_pivot, use_container_width=True)

            # Exportar comparativo
            st.markdown("---")
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                csv_comp = df_comparativo.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Comparativo (CSV)",
                    data=csv_comp,
                    file_name=f"comparativo_br_ne_pi_{selected_indicador_key}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Dados insuficientes para comparação")

    with tab_agregadores:
        st.markdown("### 📊 Análise por Agregadores")
        st.markdown("Visualize o indicador agregado por diferentes dimensões demográficas e geográficas.")

        # Verificar disponibilidade de campos para agregação
        tem_cod_uf = 'COD_UF' in analisador.df.columns

        # Seletor de agregador
        agregadores_disponiveis = []
        agregadores_map = {}

        # AGREGADORES GEOGRÁFICOS
        if verificar_metadado_disponivel('COD_REGIAO_2'):
            agregadores_disponiveis.append("Região")
            agregadores_map["Região"] = ('COD_REGIAO_2', MetadadosIndividuos.COD_REGIAO_2)

        if tem_cod_uf:
            agregadores_disponiveis.append("UF (Estado)")
            agregadores_map["UF (Estado)"] = ('COD_UF', MetadadosIndividuos.COD_UF)

        if verificar_metadado_disponivel('AREA'):
            agregadores_disponiveis.append("Área (Urbana/Rural)")
            agregadores_map["Área (Urbana/Rural)"] = ('AREA', MetadadosIndividuos.AREA)

        # AGREGADORES SOCIOECONÔMICOS
        if verificar_metadado_disponivel('CLASSE_2015'):
            agregadores_disponiveis.append("Classe Social")
            agregadores_map["Classe Social"] = ('CLASSE_2015', MetadadosIndividuos.CLASSE_2015)

        if verificar_metadado_disponivel('RENDA_FAMILIAR_2'):
            agregadores_disponiveis.append("Renda Familiar")
            agregadores_map["Renda Familiar"] = ('RENDA_FAMILIAR_2', MetadadosIndividuos.RENDA_FAMILIAR_2)

        if verificar_metadado_disponivel('RENDA_PESSOAL'):
            agregadores_disponiveis.append("Renda Pessoal")
            agregadores_map["Renda Pessoal"] = ('RENDA_PESSOAL', MetadadosIndividuos.RENDA_PESSOAL)

        # AGREGADORES DEMOGRÁFICOS
        if verificar_metadado_disponivel('SEXO'):
            agregadores_disponiveis.append("Sexo")
            agregadores_map["Sexo"] = ('SEXO', MetadadosIndividuos.SEXO)

        if verificar_metadado_disponivel('IDADE'):
            agregadores_disponiveis.append("Idade")
            agregadores_map["Idade"] = ('IDADE', MetadadosIndividuos.IDADE)

        if verificar_metadado_disponivel('FAIXA_ETARIA'):
            agregadores_disponiveis.append("Faixa Etária")
            agregadores_map["Faixa Etária"] = ('FAIXA_ETARIA', MetadadosIndividuos.FAIXA_ETARIA)

        if verificar_metadado_disponivel('RACA'):
            agregadores_disponiveis.append("Raça/Cor")
            agregadores_map["Raça/Cor"] = ('RACA', MetadadosIndividuos.RACA)

        # AGREGADORES EDUCACIONAIS
        if verificar_metadado_disponivel('GRAU_INSTRUCAO_1'):
            agregadores_disponiveis.append("Grau de Instrução")
            agregadores_map["Grau de Instrução"] = ('GRAU_INSTRUCAO_1', MetadadosIndividuos.GRAU_INSTRUCAO_1)

        # AGREGADORES DE TRABALHO
        if verificar_metadado_disponivel('PEA'):
            agregadores_disponiveis.append("Condição de Atividade (PEA)")
            agregadores_map["Condição de Atividade (PEA)"] = ('PEA', MetadadosIndividuos.PEA)

        if verificar_metadado_disponivel('OCUP_12'):
            agregadores_disponiveis.append("Tipo de Ocupação")
            agregadores_map["Tipo de Ocupação"] = ('OCUP_12', MetadadosIndividuos.OCUP_12)

        if verificar_metadado_disponivel('APOSENT'):
            agregadores_disponiveis.append("Aposentado")
            agregadores_map["Aposentado"] = ('APOSENT', MetadadosIndividuos.APOSENT)

        if not agregadores_disponiveis:
            st.warning("⚠️ Nenhum agregador disponível para este ano")
        else:
            col_agg1, col_agg2 = st.columns([2, 1])

            with col_agg1:
                selected_agregador = st.selectbox(
                    "📂 Selecione o agregador",
                    options=agregadores_disponiveis,
                    help="Escolha a dimensão pela qual deseja agregar os dados"
                )

            with col_agg2:
                mostrar_grafico = st.checkbox("📈 Mostrar Gráfico", value=True)

            st.markdown("---")

            # Obter campo e metadados do agregador selecionado
            campo_agregador, meta_agregador = agregadores_map[selected_agregador]

            # Criar análise agregada
            df_trabalho = analisador.df.copy()

            # Aplicar filtros da sidebar (exceto o próprio agregador)
            filtros_agg = []

            # Adicionar filtros que não sejam o agregador atual
            if campo_agregador != 'CLASSE_2015':
                f_class = get_meta_value(MetadadosIndividuos.CLASSE_2015, classes, selected_class_label)
                if f_class: filtros_agg.append(f_class)

            if campo_agregador != 'RENDA_FAMILIAR_2':
                f_renda = get_meta_value(MetadadosIndividuos.RENDA_FAMILIAR_2, rendas, selected_renda_label)
                if f_renda: filtros_agg.append(f_renda)

            if campo_agregador != 'SEXO':
                f_sexo = get_meta_value(MetadadosIndividuos.SEXO, sexos, selected_sexo_label)
                if f_sexo: filtros_agg.append(f_sexo)

            if campo_agregador != 'FAIXA_ETARIA':
                f_faixa = get_meta_value(MetadadosIndividuos.FAIXA_ETARIA, faixas_etarias, selected_faixa_label)
                if f_faixa: filtros_agg.append(f_faixa)

            if campo_agregador != 'COD_REGIAO_2':
                f_regiao = get_meta_value(MetadadosIndividuos.COD_REGIAO_2, regioes, selected_regiao_label)
                if f_regiao: filtros_agg.append(f_regiao)

            # Aplicar filtros
            for f in filtros_agg:
                col = f.column
                df_trabalho = df_trabalho[df_trabalho[col] == f]

            # Criar resultado agregado
            resultados_agregados = []

            # Obter valores únicos do agregador
            valores_agregador = sorted(df_trabalho[campo_agregador].unique())

            for valor in valores_agregador:
                # Filtrar por este valor
                df_grupo = df_trabalho[df_trabalho[campo_agregador] == valor]

                # Analisar indicador para este grupo
                res_grupo = analisador.analisar_indicador(actual_indicador, df_contexto=df_grupo)

                if res_grupo is not None and len(res_grupo) > 0:
                    # Obter label do valor
                    label_valor = meta_agregador._map.get(valor, str(valor))

                    # Para cada linha do resultado
                    for idx, row in res_grupo.iterrows():
                        resultados_agregados.append({
                            selected_agregador: label_valor,
                            'Categoria': row['Descrição'],
                            'Total': row['Total'],
                            'Percentual': row['Percentual'],
                            'Percentual_Num': float(row['Percentual'].replace('%', ''))
                        })

            if resultados_agregados:
                df_agregado = pd.DataFrame(resultados_agregados)

                # Mostrar métricas resumidas
                st.markdown(f"#### 📈 Análise por {selected_agregador}")

                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("🔢 Grupos", len(valores_agregador))
                with col_m2:
                    st.metric("📊 Total de Registros", f"{len(df_trabalho):,}")
                with col_m3:
                    categorias_unicas = df_agregado['Categoria'].nunique()
                    st.metric("📋 Categorias", categorias_unicas)

                st.markdown("---")

                # Criar visualizações
                if mostrar_grafico:
                    # Para indicadores binários (Sim/Não), mostrar apenas "Sim"
                    if not is_multiple and 'Sim' in df_agregado['Categoria'].values:
                        df_grafico = df_agregado[df_agregado['Categoria'] == 'Sim'].copy()
                        df_grafico = df_grafico.sort_values('Percentual_Num', ascending=False)

                        st.markdown("##### 📊 Percentual de 'Sim' por " + selected_agregador)
                        st.bar_chart(df_grafico, x=selected_agregador, y='Percentual_Num', height=400)
                    else:
                        # Para indicadores múltiplos, mostrar gráfico agrupado
                        st.markdown("##### 📊 Distribuição por Categoria")
                        df_pivot_grafico = df_agregado.pivot(
                            index=selected_agregador,
                            columns='Categoria',
                            values='Percentual_Num'
                        )
                        st.bar_chart(df_pivot_grafico, height=400)

                # Tabela detalhada
                st.markdown("##### 📋 Dados Detalhados")

                # Criar tabela pivotada para melhor visualização
                df_pivot_tabela = df_agregado.pivot_table(
                    index=selected_agregador,
                    columns='Categoria',
                    values='Percentual',
                    aggfunc='first'
                )

                st.dataframe(df_pivot_tabela, use_container_width=True)

                # Botão de download
                st.markdown("---")
                csv_agregado = df_agregado.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Download Análise por {selected_agregador} (CSV)",
                    data=csv_agregado,
                    file_name=f"agregado_{selected_agregador.lower().replace(' ', '_')}_{selected_indicador_key}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

                # Insights automáticos
                with st.expander("💡 Insights"):
                    if not is_multiple and 'Sim' in df_agregado['Categoria'].values:
                        df_sim = df_agregado[df_agregado['Categoria'] == 'Sim'].copy()
                        df_sim = df_sim.sort_values('Percentual_Num', ascending=False)

                        maior = df_sim.iloc[0]
                        menor = df_sim.iloc[-1]

                        st.markdown(f"""
                        - **Maior percentual:** {maior[selected_agregador]} com {maior['Percentual']}
                        - **Menor percentual:** {menor[selected_agregador]} com {menor['Percentual']}
                        - **Diferença:** {maior['Percentual_Num'] - menor['Percentual_Num']:.1f} pontos percentuais
                        """)
                    else:
                        st.markdown(f"Análise detalhada disponível para {len(valores_agregador)} grupos de {selected_agregador}")
            else:
                st.warning("Nenhum dado disponível para agregação com os filtros selecionados")

    with tab_customizado:
        st.markdown("### 🔍 Análise com Filtros Personalizados")
        st.markdown("Use os filtros da barra lateral para criar sua própria análise.")

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
                                 help="Percentual de indivíduos que responderam 'Sim'")
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
                                 help="Percentual de indivíduos que responderam 'Não'")

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
                    file_name=f"cetic_individuos_{selected_indicador_key}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
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
st.caption(f"Fonte: Microdados da TIC Indivíduos {ano_selecionado} (CETIC.br)")
