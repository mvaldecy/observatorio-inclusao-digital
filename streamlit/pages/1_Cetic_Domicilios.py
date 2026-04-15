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

from utils.data_loader import get_analisador_domicilios, get_http_loader
from utils.filtro_helper import FiltroHelper
from cetic.domicilios.metadados import Metadados
from components.categorias_cetic import CATEGORIAS_DOMICILIO
from components.header import render_header, inject_global_css
from components.comparativo_geografico import ComparativoGeografico

st.set_page_config(page_title="Cetic Domicílios", layout="wide")
inject_global_css()

# Configurações de Ano e Cache no Sidebar (antes dos filtros)
st.sidebar.title("⚙️ Configurações")

# Seletor de ano
loader = get_http_loader('cetic')
anos_disponiveis = loader.get_anos_disponiveis('domicilios')

ano_selecionado = st.sidebar.selectbox(
    "📅 Ano da Pesquisa",
    options=anos_disponiveis,
    index=0,
    help="Selecione o ano da pesquisa TIC Domicílios"
)

# Botões de gerenciamento de cache
col_btn1, col_btn2 = st.sidebar.columns(2)

with col_btn1:
    if st.button("🔄 Atualizar", help="Baixar nova versão dos dados", width='stretch'):
        st.cache_data.clear()
        st.cache_resource.clear()
        loader.carregar_dados(ano_selecionado, 'domicilios', force_download=True)
        st.rerun()

with col_btn2:
    if st.button("🗑️ Limpar Cache", help="Remover dados em cache", width='stretch'):
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
    analisador = get_analisador_domicilios(ano=ano_selecionado)
except Exception as e:
    st.error(f"❌ Erro ao carregar dados de {ano_selecionado}: {str(e)}")
    st.info("💡 **Dica:** Verifique sua conexão com a internet ou tente limpar o cache.")
    st.stop()

render_header(f"CETIC - TIC Domicílios {ano_selecionado}", "📊")

# Contar indicadores
total_indicadores = sum(1 for cat in CATEGORIAS_DOMICILIO.values() for k, v in cat.items() if isinstance(v, str))
total_comparativos = sum(1 for cat in CATEGORIAS_DOMICILIO.values() for k, v in cat.items() if isinstance(v, list))

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
        options=list(CATEGORIAS_DOMICILIO.keys()),
        help="Selecione uma categoria de indicadores"
    )

# Planificar INDICADORES da categoria selecionada
INDICADORES_CATEGORIA = {}
for k, v in CATEGORIAS_DOMICILIO[selected_category].items():
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
for cat in CATEGORIAS_DOMICILIO.values():
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


# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")

# Informações sobre a base
with st.sidebar.expander("📊 Sobre a Base de Dados", expanded=False):
    st.markdown(f"""
    **Total de Registros:** {len(analisador.df):,}  
    **Ano:** {ano_selecionado}  
    **Fonte:** CETIC.br  
    **Tipo:** TIC Domicílios  
    **Carregamento:** HTTP + Cache Local
    """)

st.sidebar.markdown("---")

def limpar_filtros():
    st.session_state['uf_dom'] = "Brasil"
    st.session_state['area_dom'] = "Todas"
    st.session_state['classe_dom'] = "Todas"
    st.session_state['renda_dom'] = "Todas"
    st.session_state['regiao_dom'] = "Brasil"

# Criar instância do helper
filtro_helper = FiltroHelper()

# Filtro de UF
if filtro_helper.verificar_metadado_disponivel(Metadados, 'COD_UF'):
    ufs = Metadados.COD_UF._map
    uf_options = filtro_helper.get_opcoes_select(Metadados.COD_UF, "Brasil")
    selected_uf_label = st.sidebar.selectbox("UF", uf_options, key='uf_dom')
else:
    st.sidebar.warning(f"⚠️ Filtro de UF indisponível em {ano_selecionado}")
    selected_uf_label = "Brasil"
    ufs = {}

# Filtro de Área
if filtro_helper.verificar_metadado_disponivel(Metadados, 'AREA'):
    areas = Metadados.AREA._map
    area_options = filtro_helper.get_opcoes_select(Metadados.AREA, "Todas")
    selected_area_label = st.sidebar.selectbox("Área", area_options, key='area_dom')
else:
    st.sidebar.warning(f"⚠️ Filtro de Área indisponível em {ano_selecionado}")
    selected_area_label = "Todas"
    areas = {}

# Filtro de Classe Social
if filtro_helper.verificar_metadado_disponivel(Metadados, 'CLASSE_2015'):
    classes = Metadados.CLASSE_2015._map
    class_options = filtro_helper.get_opcoes_select(Metadados.CLASSE_2015, "Todas")
    selected_class_label = st.sidebar.selectbox("Classe Social", class_options, key='classe_dom')
else:
    st.sidebar.warning(f"⚠️ Filtro de Classe Social indisponível em {ano_selecionado}")
    selected_class_label = "Todas"
    classes = {}

# Filtro de Renda Familiar
if filtro_helper.verificar_metadado_disponivel(Metadados, 'RENDA_FAMILIAR_2'):
    rendas = Metadados.RENDA_FAMILIAR_2._map
    renda_options = filtro_helper.get_opcoes_select(Metadados.RENDA_FAMILIAR_2, "Todas")
    selected_renda_label = st.sidebar.selectbox("Renda Familiar", renda_options, key='renda_dom')
else:
    st.sidebar.warning(f"⚠️ Filtro de Renda Familiar indisponível em {ano_selecionado}")
    selected_renda_label = "Todas"
    rendas = {}

# Filtro de Região
if filtro_helper.verificar_metadado_disponivel(Metadados, 'COD_REGIAO_2'):
    regioes = Metadados.COD_REGIAO_2._map
    regiao_options = filtro_helper.get_opcoes_select(Metadados.COD_REGIAO_2, "Brasil")
    selected_regiao_label = st.sidebar.selectbox("Região", regiao_options, key='regiao_dom')
else:
    st.sidebar.warning(f"⚠️ Filtro de Região indisponível em {ano_selecionado}")
    selected_regiao_label = "Brasil"
    regioes = {}

st.sidebar.button("Limpar filtros", on_click=limpar_filtros)

# Preparar filtros para o analisador usando FiltroHelper
filtros = []

f_uf = filtro_helper.get_meta_value(Metadados.COD_UF, ufs, selected_uf_label)
if f_uf: filtros.append(f_uf)

f_area = filtro_helper.get_meta_value(Metadados.AREA, areas, selected_area_label)
if f_area: filtros.append(f_area)

f_class = filtro_helper.get_meta_value(Metadados.CLASSE_2015, classes, selected_class_label)
if f_class: filtros.append(f_class)

f_renda = filtro_helper.get_meta_value(Metadados.RENDA_FAMILIAR_2, rendas, selected_renda_label)
if f_renda: filtros.append(f_renda)

f_regiao = filtro_helper.get_meta_value(Metadados.COD_REGIAO_2, regioes, selected_regiao_label)
if f_regiao: filtros.append(f_regiao)

# Executar análise
# Aplicar filtros usando helper
df_filtrado = filtro_helper.aplicar_filtros(analisador.df, filtros)
total_original = len(analisador.df)

# Mostrar informações de filtros usando helper
filtros_ativos = filtro_helper.criar_descricao_filtros(filtros, Metadados)

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
    # Criar abas principais
    tab_comparativo, tab_agregadores, tab_customizado = st.tabs(["🗺️ Comparativo Geográfico", "📊 Agregadores", "🔍 Análise Customizada"])

    with tab_comparativo:
        st.markdown("Visualização fixa das três regiões de interesse. Você pode aplicar filtros adicionais abaixo.")

        # Sub-filtros para o comparativo geográfico
        st.markdown("---")
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)

        with col_f1:
            # Filtro de Área para comparativo
            area_comp_options = filtro_helper.get_opcoes_select(Metadados.AREA, "Todas")
            selected_area_comp = st.selectbox("🏘️ Área", area_comp_options, key='area_comp')

        with col_f2:
            # Filtro de Classe para comparativo
            class_comp_options = filtro_helper.get_opcoes_select(Metadados.CLASSE_2015, "Todas")
            selected_class_comp = st.selectbox("💼 Classe Social", class_comp_options, key='classe_comp')

        with col_f3:
            # Filtro de Renda para comparativo
            renda_comp_options = filtro_helper.get_opcoes_select(Metadados.RENDA_FAMILIAR_2, "Todas")
            selected_renda_comp = st.selectbox("💰 Renda Familiar", renda_comp_options, key='renda_comp')

        with col_f4:
            if st.button("🔄 Resetar Filtros Comparativo", key='reset_comp'):
                st.rerun()

        # Aplicar filtros adicionais ao comparativo usando FiltroHelper
        filtros_comp = []

        f_area_comp = filtro_helper.get_meta_value(Metadados.AREA, areas, selected_area_comp)
        if f_area_comp: filtros_comp.append(f_area_comp)

        f_class_comp = filtro_helper.get_meta_value(Metadados.CLASSE_2015, classes, selected_class_comp)
        if f_class_comp: filtros_comp.append(f_class_comp)

        f_renda_comp = filtro_helper.get_meta_value(Metadados.RENDA_FAMILIAR_2, rendas, selected_renda_comp)
        if f_renda_comp: filtros_comp.append(f_renda_comp)

        st.markdown("---")

        # Usar o componente reutilizável para o comparativo
        comparativo = ComparativoGeografico(analisador, Metadados)
        comparativo.renderizar(actual_indicador, filtros_comp, is_multiple)

    with tab_agregadores:
        st.markdown("### 📊 Análise por Agregadores")
        st.markdown("Visualize o indicador agregado por diferentes dimensões demográficas e geográficas.")

        # Verificar disponibilidade de campos para agregação
        tem_cod_uf = 'COD_UF' in analisador.df.columns

        # Seletor de agregador
        agregadores_disponiveis = []
        agregadores_map = {}

        if filtro_helper.verificar_metadado_disponivel(Metadados, 'CLASSE_2015'):
            agregadores_disponiveis.append("Classe Social")
            agregadores_map["Classe Social"] = ('CLASSE_2015', Metadados.CLASSE_2015)

        if filtro_helper.verificar_metadado_disponivel(Metadados, 'AREA'):
            agregadores_disponiveis.append("Área")
            agregadores_map["Área"] = ('AREA', Metadados.AREA)

        if filtro_helper.verificar_metadado_disponivel(Metadados, 'RENDA_FAMILIAR_2'):
            agregadores_disponiveis.append("Renda Familiar")
            agregadores_map["Renda Familiar"] = ('RENDA_FAMILIAR_2', Metadados.RENDA_FAMILIAR_2)

        if filtro_helper.verificar_metadado_disponivel(Metadados, 'COD_REGIAO_2'):
            agregadores_disponiveis.append("Região")
            agregadores_map["Região"] = ('COD_REGIAO_2', Metadados.COD_REGIAO_2)

        if tem_cod_uf:
            agregadores_disponiveis.append("UF (Estado)")
            agregadores_map["UF (Estado)"] = ('COD_UF', Metadados.COD_UF)

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
            df_trabalho = analisador.df

            # Aplicar filtros da sidebar (exceto o próprio agregador)
            filtros_agg = []

            # Adicionar filtros que não sejam o agregador atual
            if campo_agregador != 'AREA':
                f_area = filtro_helper.get_meta_value(Metadados.AREA, areas, selected_area_label)
                if f_area: filtros_agg.append(f_area)

            if campo_agregador != 'CLASSE_2015':
                f_class = filtro_helper.get_meta_value(Metadados.CLASSE_2015, classes, selected_class_label)
                if f_class: filtros_agg.append(f_class)

            if campo_agregador != 'RENDA_FAMILIAR_2':
                f_renda = filtro_helper.get_meta_value(Metadados.RENDA_FAMILIAR_2, rendas, selected_renda_label)
                if f_renda: filtros_agg.append(f_renda)

            if campo_agregador != 'COD_REGIAO_2':
                f_regiao = filtro_helper.get_meta_value(Metadados.COD_REGIAO_2, regioes, selected_regiao_label)
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

                st.dataframe(df_pivot_tabela, width='stretch')

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
            st.dataframe(res, width='stretch', height=300)

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
            st.dataframe(res, width='stretch')
else:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.info("💡 **Dica:** Tente remover alguns filtros ou selecionar uma combinação diferente.")

st.markdown("---")
st.caption("Fonte: Microdados da TIC Domicílios 2025 (CETIC.br)")
