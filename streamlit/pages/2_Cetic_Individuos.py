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

st.set_page_config(page_title="Cetic Indivíduos", layout="wide")

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

st.title(f"📊 CETIC - TIC Indivíduos {ano_selecionado}")

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

# Filtro de UF
ufs = MetadadosIndividuos.COD_UF._map
uf_options = ["Brasil"] + list(ufs.values())
selected_uf_label = st.sidebar.selectbox("UF", uf_options, key='uf_ind')

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
sexo_options = ["Todos"] + list(sexos.values())
selected_sexo_label = st.sidebar.selectbox("Sexo", sexo_options, key='sexo_ind')

# Filtro de Região
regioes = MetadadosIndividuos.COD_REGIAO_2._map
regiao_options = ["Brasil"] + list(regioes.values())
selected_regiao_label = st.sidebar.selectbox("Região", regiao_options, key='regiao_ind')

# Filtro de Faixa Etária
faixas_etarias = MetadadosIndividuos.FAIXA_ETARIA._map
faixa_options = ["Todas"] + list(faixas_etarias.values())
selected_faixa_label = st.sidebar.selectbox("Faixa Etária", faixa_options, key='faixa_etaria_ind')

st.sidebar.button("Limpar filtros", on_click=limpar_filtros)

# Preparar filtros para o analisador
filtros = []

def get_meta_value(meta_class, label_map, selected_label):
    if selected_label == "Todas" or selected_label == "Brasil" or selected_label == "Todos":
        return None
    val = [k for k, v in label_map.items() if v == selected_label][0]
    for attr in dir(meta_class):
        meta_val = getattr(meta_class, attr)
        if isinstance(meta_val, float) and meta_val == val:
            return meta_val
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
