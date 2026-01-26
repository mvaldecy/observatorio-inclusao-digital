"""
Página Streamlit para análise de Conectividade nas Escolas
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Ajuste de Caminhos
current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(current_dir, "../../"))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from conectividade_escolas.conectividade_escolas import AnalisadorConectividadeEscolas

# Configuração da página
st.set_page_config(
    page_title="Conectividade nas Escolas",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Conectividade nas Escolas Brasileiras")
st.markdown("Análise de conectividade de internet e infraestrutura em escolas públicas e privadas")

# Cache para carregar dados
@st.cache_resource
def load_data():
    conectividade_path = Path(root_path) / "conectividade_escolas"
    return AnalisadorConectividadeEscolas(data_path=conectividade_path)

# Carregar dados
with st.spinner("Carregando dados de conectividade..."):
    analisador = load_data()
    df = analisador.df

if df.empty:
    st.error("Erro ao carregar dados. Verifique se os arquivos estão disponíveis.")
    st.stop()

st.success(f"Dados carregados: {len(df):,} registros de escolas")

# Sidebar com filtros
st.sidebar.header("🔍 Filtros")

# Filtro por Região
regioes = sorted(df['NO_REGIAO'].dropna().unique())
regiao_selecionada = st.sidebar.selectbox("Região", ["Brasil"] + regioes)

# Filtro por UF
if regiao_selecionada == "Brasil":
    ufs = sorted(df['SG_UF'].dropna().unique())
else:
    df_regiao = df[df['NO_REGIAO'] == regiao_selecionada]
    ufs = sorted(df_regiao['SG_UF'].dropna().unique())

uf_selecionada = st.sidebar.selectbox("Estado (UF)", ["Todos"] + list(ufs))

# Filtro por Município
if uf_selecionada == "Todos":
    if regiao_selecionada == "Brasil":
        municipios = sorted(df['NO_MUNICIPIO'].dropna().unique())
    else:
        municipios = sorted(df[df['NO_REGIAO'] == regiao_selecionada]['NO_MUNICIPIO'].dropna().unique())
else:
    df_uf = df[df['SG_UF'] == uf_selecionada]
    municipios = sorted(df_uf['NO_MUNICIPIO'].dropna().unique())

municipio_selecionado = st.sidebar.selectbox("Município", ["Todos"] + list(municipios))

# Filtro por Tipo de Dependência
tipos_dependencia = sorted(df['TP_DEPENDENCIA'].dropna().unique())
tipo_dependencia = st.sidebar.multiselect("Tipo de Dependência", tipos_dependencia, default=tipos_dependencia)

# Novo: Filtro por Localização (Urbano/Rural)
st.sidebar.subheader("Infraestrutura")
if 'TP_LOCALIZACAO' in df.columns:
    localizacoes = sorted(df['TP_LOCALIZACAO'].dropna().unique())
    localizacao_selecionada = st.sidebar.multiselect("Localização", localizacoes, default=localizacoes)
else:
    localizacao_selecionada = []

# Novo: Filtro por Energia
if 'ENERGIA_ADEQUADA' in df.columns:
    energia_opcoes = ["Todas", "Com Energia Adequada", "Sem Energia Adequada"]
    energia_filtro = st.sidebar.selectbox("Energia Adequada", energia_opcoes)
else:
    energia_filtro = "Todas"

# Novo: Filtro por Alunos com Internet
if 'CONECT_POSSUI_INTERNET' in df.columns:
    internet_alunos = ["Todas", "Escolas com Internet", "Escolas sem Internet"]
    internet_alunos_filtro = st.sidebar.selectbox("Internet (Alunos)", internet_alunos)
else:
    internet_alunos_filtro = "Todas"

# Filtro por Conectividade
conectividades = ["Todas", "Com Internet", "Sem Internet"]
conectividade_filtro = st.sidebar.selectbox("Conectividade Geral", conectividades)

# Filtro por Ano (2023, 2024, 2025)
st.sidebar.subheader("Período")
periodos_raw = df['Data'].dropna().unique().tolist()
anos_set = set()
for p in periodos_raw:
    try:
        # Se contém hífen, pode ser "2024-03" ou "03-2024"
        p_str = str(p)
        if '-' in p_str:
            partes = p_str.split('-')
            # Tenta encontrar a parte com 4 dígitos (ano)
            for parte in partes:
                if len(parte) == 4 and parte.isdigit():
                    anos_set.add(int(parte))
    except:
        pass

anos_lista = sorted(list(anos_set), reverse=True)
ano_selecionado = st.sidebar.selectbox("Selecione o ano:", anos_lista, index=0)

# Aplicar filtros com máscara (sem .copy() para economizar memória)
# Filtro de período (por ano)
df_filtrado = df[df['Data'].astype(str).str.contains(str(ano_selecionado))]

# Filtro de região
if regiao_selecionada != "Brasil":
    df_filtrado = df_filtrado[df_filtrado['NO_REGIAO'] == regiao_selecionada]

# Filtro de UF
if uf_selecionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado['SG_UF'] == uf_selecionada]

# Filtro de município
if municipio_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['NO_MUNICIPIO'] == municipio_selecionado]

# Filtro de tipo de dependência
df_filtrado = df_filtrado[df_filtrado['TP_DEPENDENCIA'].isin(tipo_dependencia)]

# Novo: Filtro de localização (urbano/rural)
if localizacao_selecionada:
    df_filtrado = df_filtrado[df_filtrado['TP_LOCALIZACAO'].isin(localizacao_selecionada)]

# Novo: Filtro de energia adequada
if energia_filtro == "Com Energia Adequada":
    df_filtrado = df_filtrado[df_filtrado['ENERGIA_ADEQUADA'] == 'S']
elif energia_filtro == "Sem Energia Adequada":
    df_filtrado = df_filtrado[df_filtrado['ENERGIA_ADEQUADA'] != 'S']

# Novo: Filtro de internet para alunos
if internet_alunos_filtro == "Escolas com Internet":
    df_filtrado = df_filtrado[df_filtrado['CONECT_POSSUI_INTERNET'] == 1]
elif internet_alunos_filtro == "Escolas sem Internet":
    df_filtrado = df_filtrado[df_filtrado['CONECT_POSSUI_INTERNET'] != 1]

# Filtro de conectividade
if conectividade_filtro == "Com Internet":
    df_filtrado = df_filtrado[df_filtrado['CONECT_POSSUI_INTERNET'] == 1]
elif conectividade_filtro == "Sem Internet":
    df_filtrado = df_filtrado[df_filtrado['CONECT_POSSUI_INTERNET'] != 1]

# Exibir resultado da filtragem
st.write(f"**Escolas filtradas:** {len(df_filtrado):,} de {len(df):,}")

# --- SEÇÃO FIXA: DADOS DE IMPORTÂNCIA (Brasil, Nordeste, Piauí) ---
st.divider()
st.subheader("📍 Dados Fixos - Brasil, Nordeste e Piauí")

col_br, col_ne, col_pi = st.columns(3)

# Dados para Brasil (sem .copy() para economizar memória)
if len(df) > 0:
    escolas_internet_br = len(df[df['CONECT_POSSUI_INTERNET'] == 1])
    pct_internet_br = (escolas_internet_br / len(df) * 100) if len(df) > 0 else 0
    with col_br:
        st.metric("🇧🇷 BRASIL", f"{pct_internet_br:.1f}%", "Com Internet")
        st.caption(f"Escolas: {len(df):,}")

# Dados para Nordeste
if 'NO_REGIAO' in df.columns:
    df_nordeste_fix = df[df['NO_REGIAO'] == 'Nordeste']
    if len(df_nordeste_fix) > 0:
        escolas_internet_ne = len(df_nordeste_fix[df_nordeste_fix['CONECT_POSSUI_INTERNET'] == 1])
        pct_internet_ne = (escolas_internet_ne / len(df_nordeste_fix) * 100)
        with col_ne:
            st.metric("🔵 NORDESTE", f"{pct_internet_ne:.1f}%", "Com Internet")
            st.caption(f"Escolas: {len(df_nordeste_fix):,}")
    else:
        with col_ne:
            st.warning("Sem dados para Nordeste")
else:
    with col_ne:
        st.warning("Coluna Região não encontrada")
# Dados para Piauí
if 'SG_UF' in df.columns:
    df_piaui_fix = df[df['SG_UF'] == 'PI']
    if len(df_piaui_fix) > 0:
        escolas_internet_pi = len(df_piaui_fix[df_piaui_fix['CONECT_POSSUI_INTERNET'] == 1])
        pct_internet_pi = (escolas_internet_pi / len(df_piaui_fix) * 100)
        with col_pi:
            st.metric("📍 PIAUÍ", f"{pct_internet_pi:.1f}%", "Com Internet")
            st.caption(f"Escolas: {len(df_piaui_fix):,}")
    else:
        with col_pi:
            st.warning("Sem dados para Piauí")
else:
    with col_pi:
        st.warning("Coluna UF não encontrada")
        st.warning("Sem dados para Piauí")

st.divider()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

# Calcular métricas
total_escolas = len(df_filtrado)
escolas_com_internet = len(df_filtrado[df_filtrado['CONECT_POSSUI_INTERNET'] == 1])
escolas_adequadas = len(df_filtrado[df_filtrado['CONECT_ADEQUADA'] == 1]) if 'CONECT_ADEQUADA' in df_filtrado.columns else 0

if escolas_com_internet > 0:
    velocidade_media = df_filtrado[df_filtrado['VEL_ADQ'].notna()]['VEL_ADQ'].astype(float).mean()
else:
    velocidade_media = 0

with col1:
    st.metric("Total de Escolas", f"{total_escolas:,}")

with col2:
    pct_internet = (escolas_com_internet / total_escolas * 100) if total_escolas > 0 else 0
    st.metric("Com Internet", f"{escolas_com_internet:,}", f"{pct_internet:.1f}%")

with col3:
    pct_adequada = (escolas_adequadas / total_escolas * 100) if total_escolas > 0 else 0
    st.metric("Conectividade Adequada", f"{escolas_adequadas:,}", f"{pct_adequada:.1f}%")

with col4:
    st.metric("Velocidade Média (Mbps)", f"{velocidade_media:.2f}")

# Tabs para diferentes visualizações
tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Conectividade", "Infraestrutura", "Dados"])

with tab1:
    st.subheader("Distribuição por Estado")
    
    if len(df_filtrado) > 0:
        por_estado = df_filtrado.groupby('SG_UF').size().sort_values(ascending=False)
        
        import plotly.express as px
        df_estado = pd.DataFrame({
            'Estado': por_estado.index,
            'Quantidade de Escolas': por_estado.values
        })
        fig = px.bar(df_estado, x='Estado', y='Quantidade de Escolas',
                     labels={'Quantidade de Escolas': 'Escolas'},
                     text='Quantidade de Escolas')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Número total de escolas por estado (UF) nos dados filtrados")
    else:
        st.info("Nenhum dado disponível para os filtros selecionados")

with tab2:
    st.subheader("Conectividade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribuição de conectividade
        if len(df_filtrado) > 0:
            conectividade_dist = df_filtrado['CONECT_SITUACAO'].value_counts()
            st.write("**Situação de Conectividade**")
            st.caption("Classificação geral da situação de conectividade das escolas")
            
            import plotly.express as px
            df_con = pd.DataFrame({
                'Situação': conectividade_dist.index,
                'Quantidade': conectividade_dist.values
            })
            fig = px.pie(df_con, names='Situação', values='Quantidade', 
                        labels={'Quantidade': 'Escolas'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de adequação
        if len(df_filtrado) > 0:
            df_com_adequacao = df_filtrado[df_filtrado['CONECT_ADEQUADA'].isin(['S', 'N'])]
            if len(df_com_adequacao) > 0:
                adequacao_dist = df_com_adequacao['CONECT_ADEQUADA'].value_counts()
                st.write("**Adequação de Conectividade**")
                st.caption("S = Sim (Adequada) | N = Não (Inadequada)")
                
                import plotly.express as px
                df_adeq = pd.DataFrame({
                    'Adequação': ['Adequada' if x == 'S' else 'Inadequada' for x in adequacao_dist.index],
                    'Quantidade': adequacao_dist.values
                })
                fig = px.bar(df_adeq, x='Adequação', y='Quantidade',
                            labels={'Quantidade': 'Escolas'},
                            text='Quantidade')
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Infraestrutura")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Energia
        if len(df_filtrado) > 0:
            energia_dist = df_filtrado['ENERGIA_ADEQUADA'].value_counts()
            st.write("**Energia Adequada**")
            st.caption("S = Sim (Energia adequada) | N = Não (Energia inadequada)")
            
            import plotly.express as px
            df_en = pd.DataFrame({
                'Energia': ['Adequada' if x == 'S' else 'Inadequada' for x in energia_dist.index],
                'Quantidade': energia_dist.values
            })
            fig = px.bar(df_en, x='Energia', y='Quantidade',
                        labels={'Quantidade': 'Escolas'},
                        text='Quantidade')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tipo de Localização
        if len(df_filtrado) > 0:
            localizacao_dist = df_filtrado['TP_LOCALIZACAO'].value_counts()
            st.write("**Localização das Escolas**")
            st.caption("Distribuição entre escolas urbanas e rurais")
            
            import plotly.express as px
            df_loc = pd.DataFrame({
                'Localização': localizacao_dist.index,
                'Quantidade': localizacao_dist.values
            })
            fig = px.pie(df_loc, names='Localização', values='Quantidade')
            st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Dados Detalhados")
    
    # Seletor de colunas para exibição
    colunas_principais = [
        'COD_INEP', 'NO_ENTIDADE', 'NO_MUNICIPIO', 'SG_UF',
        'TP_DEPENDENCIA', 'TP_LOCALIZACAO', 'CONECT_POSSUI_INTERNET', 
        'CONECT_ADEQUADA', 'ENERGIA_ADEQUADA', 'VEL_ADQ', 'QT_MAT_BAS', 'Data'
    ]
    
    colunas_disponiveis = [col for col in colunas_principais if col in df_filtrado.columns]
    
    # Adicionar legenda explicativa
    st.write("**Legenda das Colunas:**")
    col_leg1, col_leg2 = st.columns(2)
    with col_leg1:
        st.caption("**COD_INEP**: Código do Instituto Nacional de Estudos Pedagógicos")
        st.caption("**NO_ENTIDADE**: Nome da escola")
        st.caption("**TP_DEPENDENCIA**: Tipo de administração (Pública/Privada)")
        st.caption("**TP_LOCALIZACAO**: Localização geográfica (Urbana/Rural)")
        st.caption("**CONECT_POSSUI_INTERNET**: Escola possui internet (S/N)")
    with col_leg2:
        st.caption("**CONECT_ADEQUADA**: Conectividade atende os padrões (S/N)")
        st.caption("**ENERGIA_ADEQUADA**: Energia adequada para infraestrutura (S/N)")
        st.caption("**VEL_ADQ**: Velocidade de internet adquirida (Mbps)")
        st.caption("**QT_MAT_BAS**: Quantidade de alunos do ensino básico")
        st.caption("**Data**: Data da coleta dos dados (MM/YYYY)")
    
    st.dataframe(
        df_filtrado[colunas_disponiveis].head(100),
        use_container_width=True,
        height=400
    )
    
    st.write(f"Exibindo 100 primeiros registros de {len(df_filtrado):,}")
    
    # Download dos dados
    csv = df_filtrado.to_csv(index=False)
    st.download_button(
        label="Baixar dados filtrados (CSV)",
        data=csv,
        file_name=f"conectividade_escolas_{ano_selecionado}.csv",
        mime="text/csv"
    )
