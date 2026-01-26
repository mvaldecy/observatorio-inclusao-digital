import pandas as pd
import sys
import os
import streamlit as st

# Ajuste de Caminhos
current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(current_dir, "../../"))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from anatel.cobertura_movel import AnalisadorAnatel

st.set_page_config(page_title="Anatel Cobertura", layout="wide")

# Funções Auxiliares
@st.cache_resource
def load_data():
    """Carrega dados de cobertura (combina dados de atributos e cobertura)"""
    # Carrega dos arquivos de cobertura
    cobertura_path = os.path.join(root_path, "anatel", "cobertura_movel")
    return AnalisadorAnatel(data_path=cobertura_path)

def format_br(val):
    """Formata número para padrão brasileiro"""
    if pd.isna(val):
        return "N/A"
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Interface Principal
st.title("📡 ANATEL - Monitoramento de Cobertura Móvel")

st.markdown("""
Analise a cobertura de redes móveis (3G, 4G, 5G) por região, estado e município.
""")

analisador = load_data()

if analisador.df.empty:
    st.error("⚠️ Base de dados não encontrada ou está vazia.")
    st.stop()

# --- SIDEBAR: FILTROS ---
st.sidebar.header("🔍 Filtros de Pesquisa")

# 1. Seleção de Tecnologia (filtro principal) - Mudado para Selectbox
st.sidebar.subheader("Tecnologia Móvel")
tecnologias_disponiveis = {
    "3G": "Cobertura_3G",
    "4G": "Cobertura_4G", 
    "5G": "Cobertura_5G",
    "3G + 4G + 5G": "Cobertura_3G4G5G",
    "4G + 5G": "Cobertura_4G5G",
    "Todas": "Cobertura_Todas"
}

tecnologia_selecionada = st.sidebar.selectbox(
    "Escolha a tecnologia:",
    options=list(tecnologias_disponiveis.keys()),
    index=3
)

coluna_tecnologia = tecnologias_disponiveis[tecnologia_selecionada]

# Construir máscara de filtros sem fazer cópias desnecessárias
mask = pd.Series([True] * len(analisador.df), index=analisador.df.index)

    # 2. Filtro de Ano (2023, 2024, 2025)
st.sidebar.subheader("Período")
if 'Período' in analisador.df.columns:
    periodos_raw = analisador.df['Período'].dropna().unique().tolist()
    periodos_str = [str(p) for p in periodos_raw]
    
    # Extrair anos (formato: "09-2024" ou "2024-09")
    anos_set = set()
    for p in periodos_str:
        try:
            # Se contém hífen, pode ser "09-2024" ou "2024-09"
            if '-' in p:
                partes = p.split('-')
                # Tenta encontrar a parte com 4 dígitos (ano)
                for parte in partes:
                    if len(parte) == 4 and parte.isdigit():
                        anos_set.add(int(parte))
        except:
            pass
    
    anos_lista = sorted(list(anos_set), reverse=True)
    ano_selecionado = st.sidebar.selectbox("Selecione o ano:", anos_lista, index=0)
    # Filtrar periodos que terminam com o ano (formato MM-YYYY)
    mask &= (analisador.df['Período'].astype(str).str.endswith(str(ano_selecionado)))

# 3. Operadora (opcional)
if 'Operadora' in analisador.df.columns:
    operadoras = ["Todas"] + sorted(list(set([str(op) for op in analisador.df['Operadora'].dropna().unique().tolist()])))
    operadora_sel = st.sidebar.selectbox("Operadora", operadoras, index=0)
    if operadora_sel != "Todas":
        mask &= (analisador.df['Operadora'].astype(str) == operadora_sel)

# 4. Filtro de Status de Cobertura
st.sidebar.subheader("Status de Cobertura")
status_opcoes = ["Todos", "Com Cobertura Adequada (>50%)", "Com Cobertura Inadequada (1-50%)", "Sem Cobertura (0%)"]
status_filtro = st.sidebar.selectbox("Status de Cobertura", status_opcoes)

if status_filtro == "Com Cobertura Adequada (>50%)":
    mask &= (analisador.df[coluna_tecnologia] > 50)
elif status_filtro == "Com Cobertura Inadequada (1-50%)":
    mask &= ((analisador.df[coluna_tecnologia] > 0) & (analisador.df[coluna_tecnologia] <= 50))
elif status_filtro == "Sem Cobertura (0%)":
    mask &= (analisador.df[coluna_tecnologia] == 0) | (analisador.df[coluna_tecnologia].isna())

# 5. Filtro Urbano/Rural
st.sidebar.subheader("Tipo de Localização")
if 'Tipo Localização' in analisador.df.columns:
    tipos_localizacao = ["Todos"] + sorted(list(set([str(t) for t in analisador.df['Tipo Localização'].dropna().unique().tolist() if str(t) != 'nan'])))
    tipo_localizacao_sel = st.sidebar.selectbox("Urbano/Rural", tipos_localizacao, index=0)
    if tipo_localizacao_sel != "Todos":
        mask &= (analisador.df['Tipo Localização'].astype(str) == tipo_localizacao_sel)

# 6. Região (se houver coluna)
st.sidebar.subheader("Localização Geográfica")
if 'Região' in analisador.df.columns:
    regioes = ["Brasil"] + sorted(list(set([str(r) for r in analisador.df['Região'].dropna().unique().tolist() if str(r) != 'nan'])))
    regiao_sel = st.sidebar.selectbox("Região", regioes, index=0)
    if regiao_sel != "Brasil":
        mask &= (analisador.df['Região'].astype(str) == regiao_sel)

# 7. UF (Dependente de Região)
if 'UF' in analisador.df.columns:
    ufs = ["Todas as UFs"] + sorted(list(set([str(uf) for uf in analisador.df[mask]['UF'].dropna().unique().tolist() if str(uf) != 'nan'])))
    uf_sel = st.sidebar.selectbox("UF", ufs, index=0)
    if uf_sel != "Todas as UFs":
        mask &= (analisador.df['UF'].astype(str) == uf_sel)

# 8. Município (Dependente de UF)
if 'Município' in analisador.df.columns:
    municipios = ["Todos os Municípios"] + sorted(list(set([str(m) for m in analisador.df[mask]['Município'].dropna().unique().tolist() if str(m) != 'nan'])))
    municipio_sel = st.sidebar.selectbox("Município", municipios, index=0)
    if municipio_sel != "Todos os Municípios":
        mask &= (analisador.df['Município'].astype(str) == municipio_sel)

# --- PROCESSAMENTO ---
# Verificar se a coluna de tecnologia existe
if coluna_tecnologia not in analisador.df.columns:
    st.error(f"❌ Coluna '{coluna_tecnologia}' não encontrada nos dados carregados!")
    st.info(f"Colunas disponíveis: {', '.join(analisador.df.columns.tolist())}")
    st.stop()

# Aplicar filtros sem fazer cópia completa - usar indexação
df_filtrado = analisador.df.loc[mask & analisador.df[coluna_tecnologia].notna()]

# Converter valores de cobertura para numérico (apenas se houver dados)
if len(df_filtrado) > 0:
    df_filtrado = df_filtrado.copy(deep=False)  # Shallow copy apenas
    df_filtrado[coluna_tecnologia] = pd.to_numeric(
        df_filtrado[coluna_tecnologia].astype(str).str.replace(',', '.'),
        errors='coerce'
    )

# --- DASHBOARD ---
filtros_ativos = f"📡 **Tecnologia:** {tecnologia_selecionada}"
if 'Período' in analisador.df.columns and 'periodo_sel' in locals():
    filtros_ativos += f" | **Período:** {periodo_sel}"
if 'UF' in analisador.df.columns and 'uf_sel' in locals():
    filtros_ativos += f" | **UF:** {uf_sel}"
if 'Município' in analisador.df.columns and 'municipio_sel' in locals():
    filtros_ativos += f" | **Município:** {municipio_sel}"

st.info(f"{filtros_ativos} | **Setores:** {len(df_filtrado):,}")

# --- SEÇÃO FIXA: DADOS DE IMPORTÂNCIA (Brasil, Nordeste, Piauí) ---
st.divider()
st.subheader("📍 Dados Fixos - Brasil, Nordeste e Piauí")

col_br, col_ne, col_pi = st.columns(3)

# Dados para Brasil
df_brasil = analisador.df[analisador.df[coluna_tecnologia].notna()].copy(deep=False)
if len(df_brasil) > 0:
    df_brasil[coluna_tecnologia] = pd.to_numeric(
        df_brasil[coluna_tecnologia].astype(str).str.replace(',', '.'),
        errors='coerce'
    )
    cobertura_brasil = df_brasil[coluna_tecnologia].mean()
    with col_br:
        st.metric("🇧🇷 BRASIL", f"{cobertura_brasil:.2f}%", "Cobertura Média")
        st.caption(f"Setores: {len(df_brasil):,}")

# Dados para Nordeste
df_nordeste = analisador.df[
    (analisador.df['Região'] == 'Nordeste') & 
    (analisador.df[coluna_tecnologia].notna())
].copy(deep=False) if 'Região' in analisador.df.columns else pd.DataFrame()

if len(df_nordeste) > 0:
    df_nordeste[coluna_tecnologia] = pd.to_numeric(
        df_nordeste[coluna_tecnologia].astype(str).str.replace(',', '.'),
        errors='coerce'
    )
    cobertura_nordeste = df_nordeste[coluna_tecnologia].mean()
    with col_ne:
        st.metric("🔵 NORDESTE", f"{cobertura_nordeste:.2f}%", "Cobertura Média")
        st.caption(f"Setores: {len(df_nordeste):,}")
else:
    with col_ne:
        st.warning("Sem dados para Nordeste")

# Dados para Piauí
df_piaui = analisador.df[
    (analisador.df['UF'] == 'PI') & 
    (analisador.df[coluna_tecnologia].notna())
].copy(deep=False) if 'UF' in analisador.df.columns else pd.DataFrame()

if len(df_piaui) > 0:
    df_piaui[coluna_tecnologia] = pd.to_numeric(
        df_piaui[coluna_tecnologia].astype(str).str.replace(',', '.'),
        errors='coerce'
    )
    cobertura_piaui = df_piaui[coluna_tecnologia].mean()
    with col_pi:
        st.metric("📍 PIAUÍ", f"{cobertura_piaui:.2f}%", "Cobertura Média")
        st.caption(f"Setores: {len(df_piaui):,}")
else:
    with col_pi:
        st.warning("Sem dados para Piauí")

st.divider()

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    # Métricas principais
    m1, m2, m3, m4 = st.columns(4)
    
    cobertura_media = df_filtrado[coluna_tecnologia].mean()
    cobertura_min = df_filtrado[coluna_tecnologia].min()
    cobertura_max = df_filtrado[coluna_tecnologia].max()
    
    with m1:
        st.metric(
            "Cobertura Média (%)",
            f"{cobertura_media:.2f}%"
        )
    with m2:
        st.metric(
            "Cobertura Mínima (%)",
            f"{cobertura_min:.2f}%"
        )
    with m3:
        st.metric(
            "Cobertura Máxima (%)",
            f"{cobertura_max:.2f}%"
        )
    with m4:
        st.metric(
            "Total de Setores",
            f"{len(df_filtrado):,}"
        )

    # Visualizações
    st.subheader("📊 Análise de Cobertura")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Distribuição de Cobertura (%)**")
        hist_data = pd.cut(df_filtrado[coluna_tecnologia], bins=10)
        hist_counts = hist_data.value_counts().sort_index()
        # Converter índices de interval para strings
        hist_counts.index = hist_counts.index.astype(str)
        
        # Criar gráfico com valores nos topos das barras
        import plotly.express as px
        df_hist = pd.DataFrame({
            'Faixa de Cobertura': [str(idx) for idx in hist_counts.index],
            'Quantidade de Setores': hist_counts.values
        })
        fig = px.bar(df_hist, x='Faixa de Cobertura', y='Quantidade de Setores',
                     labels={'Quantidade de Setores': 'Setores'},
                     text='Quantidade de Setores')
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.write("**Setores por Faixa de Cobertura**")
        st.caption("Cada faixa mostra a quantidade de setores com cobertura naquele intervalo")
        faixas = {
            "0-25%": (0, 25),
            "25-50%": (25, 50),
            "50-75%": (50, 75),
            "75-100%": (75, 100)
        }
        dados_faixa = {}
        for faixa, (min_val, max_val) in faixas.items():
            count = len(df_filtrado[
                (df_filtrado[coluna_tecnologia] >= min_val) &
                (df_filtrado[coluna_tecnologia] < max_val)
            ])
            dados_faixa[faixa] = count
        
        df_faixa = pd.DataFrame({
            'Faixa': list(dados_faixa.keys()),
            'Setores': list(dados_faixa.values())
        })
        fig2 = px.bar(df_faixa, x='Faixa', y='Setores', 
                      labels={'Setores': 'Quantidade de Setores'},
                      text='Setores')
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Legenda explicativa
        st.info("""
        **Legenda:**
        - **0-25%**: Setores com cobertura baixa (≤25%)
        - **25-50%**: Setores com cobertura média-baixa
        - **50-75%**: Setores com cobertura média-alta
        - **75-100%**: Setores com cobertura plena (≥75%)
        """)
    
    # ANÁLISE DE COMBINAÇÕES IMPORTANTES
    st.subheader("🔄 Comparação de Tecnologias")
    st.caption("Análise de cobertura entre diferentes tecnologias e suas combinações")
    
    col_comp1, col_comp2, col_comp3 = st.columns(3)
    
    # Comparação de cobertura por tecnologia
    tecnologias_comparacao = {
        "3G": "Cobertura_3G",
        "4G": "Cobertura_4G",
        "5G": "Cobertura_5G",
        "4G + 5G": "Cobertura_4G5G",
        "Todas (3G+4G+5G)": "Cobertura_3G4G5G"
    }
    
    comparacao_dados = []
    for tech_nome, tech_col in tecnologias_comparacao.items():
        if tech_col in analisador.df.columns:
            # Aplicar mesmos filtros
            df_tech = analisador.df.loc[mask & analisador.df[tech_col].notna()].copy()
            if len(df_tech) > 0:
                df_tech[tech_col] = pd.to_numeric(
                    df_tech[tech_col].astype(str).str.replace(',', '.'),
                    errors='coerce'
                )
                media_cobertura = df_tech[tech_col].mean()
                setores_com_cobertura = len(df_tech[df_tech[tech_col] > 0])
                
                comparacao_dados.append({
                    'Tecnologia': tech_nome,
                    'Cobertura Média (%)': media_cobertura,
                    'Setores com Cobertura': setores_com_cobertura,
                    'Total de Setores': len(df_tech)
                })
    
    if comparacao_dados:
        df_comparacao = pd.DataFrame(comparacao_dados)
        
        with col_comp1:
            st.metric(
                "Maior Cobertura",
                df_comparacao.loc[df_comparacao['Cobertura Média (%)'].idxmax(), 'Tecnologia'],
                f"{df_comparacao['Cobertura Média (%)'].max():.2f}%"
            )
        
        with col_comp2:
            tech_5g = df_comparacao[df_comparacao['Tecnologia'] == '5G']
            if not tech_5g.empty:
                st.metric(
                    "Cobertura 5G",
                    f"{tech_5g['Cobertura Média (%)'].values[0]:.2f}%",
                    "Tecnologia mais recente"
                )
        
        with col_comp3:
            diferenca = df_comparacao[df_comparacao['Tecnologia'] == 'Todas (3G+4G+5G)']['Cobertura Média (%)'].values
            if len(diferenca) > 0:
                st.metric(
                    "Cobertura Total",
                    f"{diferenca[0]:.2f}%",
                    "Qualquer tecnologia"
                )
        
        # Gráfico de comparação
        st.write("**Comparação de Cobertura Média por Tecnologia**")
        
        import plotly.express as px
        fig_comp = px.bar(
            df_comparacao,
            x='Tecnologia',
            y='Cobertura Média (%)',
            labels={'Cobertura Média (%)': 'Cobertura Média (%)'},
            text='Cobertura Média (%)',
            color='Cobertura Média (%)',
            color_continuous_scale='Blues'
        )
        fig_comp.update_traces(textposition='outside', texttemplate='%{text:.2f}%')
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # Tabela de comparação
        st.write("**Detalhes da Comparação**")
        df_comparacao_display = df_comparacao.copy()
        df_comparacao_display['Cobertura Média (%)'] = df_comparacao_display['Cobertura Média (%)'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(df_comparacao_display, use_container_width=True)
    
    # ANÁLISE: OPERADORA POR REGIÃO
    if 'Operadora' in analisador.df.columns and 'Região' in analisador.df.columns:
        st.subheader("🗺️ Análise Operadora vs Região")
        st.caption("Comparação de cobertura da tecnologia selecionada por operadora em cada região")
        
        # Preparar dados para análise
        df_operadora_regiao = analisador.df.loc[mask].copy()
        if len(df_operadora_regiao) > 0:
            df_operadora_regiao[coluna_tecnologia] = pd.to_numeric(
                df_operadora_regiao[coluna_tecnologia].astype(str).str.replace(',', '.'),
                errors='coerce'
            )
            
            # Criar pivot table
            pivot_data = df_operadora_regiao.groupby(['Operadora', 'Região'])[coluna_tecnologia].mean().unstack(fill_value=0)
            
            if not pivot_data.empty:
                # Gráfico de heatmap
                import plotly.graph_objects as go
                
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=pivot_data.values,
                    x=pivot_data.columns,
                    y=pivot_data.index,
                    colorscale='Viridis',
                    text=pivot_data.values.round(2),
                    texttemplate='%{text:.1f}%',
                    textfont={"size": 10},
                    hovertemplate='<b>%{y}</b><br>%{x}<br>Cobertura: %{z:.2f}%<extra></extra>'
                ))
                
                fig_heatmap.update_layout(
                    title=f"Cobertura {tecnologia_selecionada} por Operadora e Região",
                    xaxis_title="Região",
                    yaxis_title="Operadora",
                    height=400
                )
                
                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                # Tabela de detalhes
                st.write("**Matriz de Cobertura (%)**")
                df_pivot_display = pivot_data.round(2)
                st.dataframe(df_pivot_display, use_container_width=True)

    # Tabela de detalhes
    st.subheader("📋 Detalhes por Setor")
    
    colunas_exibir = [col for col in df_filtrado.columns 
                      if col in ['Período', 'Operadora', 'Código Setor Censitário', coluna_tecnologia]]
    
    if colunas_exibir:
        df_exibir = df_filtrado[colunas_exibir].copy()
        df_exibir[coluna_tecnologia] = df_exibir[coluna_tecnologia].apply(lambda x: f"{x:.2f}%")
        
        # Adicionar legenda explicativa
        st.write("**Colunas:**")
        col_legenda1, col_legenda2 = st.columns(2)
        with col_legenda1:
            st.caption("**Período**: Data de coleta dos dados")
            st.caption("**Operadora**: Empresa de telecomunicações")
        with col_legenda2:
            st.caption("**Código Setor Censitário**: Identificador único do setor geográfico")
            st.caption(f"**{coluna_tecnologia}**: Percentual de cobertura da tecnologia naquele setor")
        
        st.dataframe(df_exibir.head(100), use_container_width=True)
        st.caption(f"Exibindo 100 primeiros registros de {len(df_exibir):,} setores encontrados")

st.markdown("---")
st.caption("Fonte: Microdados ANATEL. Dados de cobertura por setor censitário e operadora.")