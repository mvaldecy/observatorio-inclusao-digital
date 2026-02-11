"""
Componente para visualização de mapas do Brasil com dados por UF
Usa plotly para criar mapas coropléticos (choropleth)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# GeoJSON do Brasil por UF
GEOJSON_BRASIL_UF = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

# Mapeamento de nomes completos para siglas de UF
NOME_PARA_SIGLA_UF = {
    'Acre': 'AC',
    'Alagoas': 'AL',
    'Amapá': 'AP',
    'Amazonas': 'AM',
    'Bahia': 'BA',
    'Ceará': 'CE',
    'Distrito Federal': 'DF',
    'Espírito Santo': 'ES',
    'Goiás': 'GO',
    'Maranhão': 'MA',
    'Mato Grosso': 'MT',
    'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG',
    'Pará': 'PA',
    'Paraíba': 'PB',
    'Paraná': 'PR',
    'Pernambuco': 'PE',
    'Piauí': 'PI',
    'Rio de Janeiro': 'RJ',
    'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO',
    'Roraima': 'RR',
    'Santa Catarina': 'SC',
    'São Paulo': 'SP',
    'Sergipe': 'SE',
    'Tocantins': 'TO'
}

# Siglas para nomes
SIGLA_PARA_NOME_UF = {v: k for k, v in NOME_PARA_SIGLA_UF.items()}


def mapa_cobertura_brasil(
    df: pd.DataFrame,
    coluna_uf: str = 'UF',
    coluna_valor: str = 'Cobertura',
    titulo: str = "Mapa de Cobertura por Estado",
    legenda: str = "Cobertura (%)",
    color_scale: str = "RdYlGn",
    range_color: tuple = (0, 100),
    hover_data: dict = None,
    altura: int = 600
):
    """
    Cria um mapa coroplético do Brasil com dados por UF

    Args:
        df: DataFrame com os dados
        coluna_uf: Nome da coluna que contém as UFs (pode ser sigla ou nome completo)
        coluna_valor: Nome da coluna com os valores a serem mapeados
        titulo: Título do mapa
        legenda: Legenda da escala de cores
        color_scale: Escala de cores do plotly (ex: 'RdYlGn', 'Viridis', 'Blues')
        range_color: Tupla (min, max) para a escala de cores
        hover_data: Dicionário com colunas adicionais para mostrar no hover
        altura: Altura do mapa em pixels

    Returns:
        Figura do plotly
    """
    # Cria uma cópia do DataFrame
    df_map = df.copy()

    # Normaliza a coluna de UF para siglas
    # Converte para string para evitar problemas com categoricals
    df_map[coluna_uf] = df_map[coluna_uf].astype(str)

    # Verifica se a primeira linha é um nome completo ou sigla
    primeiro_valor = df_map[coluna_uf].iloc[0].strip()

    if len(primeiro_valor) > 2 or primeiro_valor in SIGLA_PARA_NOME_UF.values():
        # Se são nomes completos, converte para siglas
        df_map['UF_SIGLA'] = df_map[coluna_uf].map(NOME_PARA_SIGLA_UF)
        # Trata valores que não foram mapeados (mantém original se já for sigla)
        df_map['UF_SIGLA'] = df_map['UF_SIGLA'].fillna(df_map[coluna_uf])
    else:
        # Já são siglas
        df_map['UF_SIGLA'] = df_map[coluna_uf]

    # Garante que o valor está numérico
    if df_map[coluna_valor].dtype == 'object':
        # Remove % e converte
        df_map[coluna_valor] = df_map[coluna_valor].str.replace('%', '').astype(float)

    # Cria o mapa usando plotly express com GeoJSON
    fig = px.choropleth(
        df_map,
        geojson=GEOJSON_BRASIL_UF,
        locations='UF_SIGLA',
        featureidkey="properties.sigla",
        color=coluna_valor,
        hover_name='UF_SIGLA',
        hover_data=hover_data,
        color_continuous_scale=color_scale,
        range_color=range_color,
        labels={coluna_valor: legenda},
        title=titulo
    )

    # Ajusta o layout para focar no Brasil
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=False,
        showcoastlines=False,
        showland=False,
        bgcolor='rgba(0,0,0,0)'
    )

    fig.update_layout(
        height=altura,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        coloraxis_colorbar=dict(
            title=legenda,
            thickness=15,
            len=0.7
        )
    )

    return fig


def mapa_comparativo_4g_5g(
    df_4g: pd.DataFrame,
    df_5g: pd.DataFrame,
    coluna_uf: str = 'UF',
    coluna_valor: str = 'Cobertura',
    altura: int = 500
):
    """
    Cria dois mapas lado a lado comparando cobertura 4G e 5G

    Args:
        df_4g: DataFrame com dados de cobertura 4G
        df_5g: DataFrame com dados de cobertura 5G
        coluna_uf: Nome da coluna que contém as UFs
        coluna_valor: Nome da coluna com os valores de cobertura
        altura: Altura dos mapas em pixels

    Returns:
        Tupla com (figura_4g, figura_5g)
    """
    # Cria mapa 4G
    fig_4g = mapa_cobertura_brasil(
        df_4g,
        coluna_uf=coluna_uf,
        coluna_valor=coluna_valor,
        titulo="📱 Cobertura 4G por Estado",
        legenda="4G (%)",
        color_scale="Blues",
        altura=altura
    )

    # Cria mapa 5G
    fig_5g = mapa_cobertura_brasil(
        df_5g,
        coluna_uf=coluna_uf,
        coluna_valor=coluna_valor,
        titulo="🚀 Cobertura 5G por Estado",
        legenda="5G (%)",
        color_scale="Purples",
        altura=altura
    )

    return fig_4g, fig_5g


def renderizar_mapa_interativo(
    df: pd.DataFrame,
    coluna_uf: str = 'UF',
    coluna_valor: str = 'Cobertura',
    titulo: str = "Mapa de Cobertura",
    config_personalizadas: dict = None
):
    """
    Renderiza um mapa interativo com controles personalizados no Streamlit

    Args:
        df: DataFrame com os dados
        coluna_uf: Nome da coluna com as UFs
        coluna_valor: Nome da coluna com os valores
        titulo: Título do mapa
        config_personalizadas: Configurações personalizadas (opcional)
    """
    # Configurações padrão
    config = {
        'color_scale': 'RdYlGn',
        'range_min': 0,
        'range_max': 100,
        'altura': 600,
        'legenda': 'Cobertura (%)'
    }

    # Atualiza com configurações personalizadas
    if config_personalizadas:
        config.update(config_personalizadas)

    # Sidebar para controles
    with st.sidebar:
        st.markdown("### 🎨 Configurações do Mapa")

        # Seletor de escala de cores
        color_scale = st.selectbox(
            "Escala de Cores:",
            ['RdYlGn', 'Viridis', 'Blues', 'Greens', 'Reds', 'Purples', 'YlOrRd'],
            index=0
        )

        # Ajuste de altura
        altura = st.slider(
            "Altura do Mapa:",
            min_value=400,
            max_value=800,
            value=config['altura'],
            step=50
        )

    # Cria e exibe o mapa
    fig = mapa_cobertura_brasil(
        df,
        coluna_uf=coluna_uf,
        coluna_valor=coluna_valor,
        titulo=titulo,
        legenda=config['legenda'],
        color_scale=color_scale,
        range_color=(config['range_min'], config['range_max']),
        altura=altura
    )

    st.plotly_chart(fig, use_container_width=True)

    # Estatísticas resumidas
    st.markdown("---")
    st.markdown("### 📊 Estatísticas Resumidas")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Média Nacional", f"{df[coluna_valor].mean():.1f}%")

    with col2:
        st.metric("Melhor Estado", f"{df[coluna_valor].max():.1f}%")

    with col3:
        st.metric("Pior Estado", f"{df[coluna_valor].min():.1f}%")

    with col4:
        st.metric("Mediana", f"{df[coluna_valor].median():.1f}%")


def mapa_com_tabs_4g_5g(
    df_4g: pd.DataFrame,
    df_5g: pd.DataFrame,
    coluna_uf: str = 'UF',
    coluna_valor_4g: str = 'Cobertura',
    coluna_valor_5g: str = 'Cobertura'
):
    """
    Renderiza mapas de 4G e 5G em tabs separadas com análise comparativa

    Args:
        df_4g: DataFrame com dados 4G
        df_5g: DataFrame com dados 5G
        coluna_uf: Nome da coluna de UF
        coluna_valor_4g: Nome da coluna de valor no DataFrame 4G
        coluna_valor_5g: Nome da coluna de valor no DataFrame 5G
    """
    # Cria tabs
    tab1, tab2, tab3 = st.tabs(["📱 Cobertura 4G", "🚀 Cobertura 5G", "🔄 Comparação"])

    with tab1:
        st.markdown("### 📱 Mapa de Cobertura 4G por Estado")

        fig_4g = mapa_cobertura_brasil(
            df_4g,
            coluna_uf=coluna_uf,
            coluna_valor=coluna_valor_4g,
            titulo="Cobertura 4G no Brasil",
            legenda="4G (%)",
            color_scale="Blues",
            altura=600
        )

        st.plotly_chart(fig_4g, use_container_width=True, key="mapa_4g")

        # Estatísticas 4G
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🇧🇷 Média Nacional", f"{df_4g[coluna_valor_4g].mean():.1f}%")
        with col2:
            idx_max = df_4g[coluna_valor_4g].idxmax()
            st.metric("🥇 Melhor Estado",
                     f"{df_4g.loc[idx_max, coluna_uf]}: {df_4g.loc[idx_max, coluna_valor_4g]:.1f}%")
        with col3:
            idx_min = df_4g[coluna_valor_4g].idxmin()
            st.metric("⚠️ Pior Estado",
                     f"{df_4g.loc[idx_min, coluna_uf]}: {df_4g.loc[idx_min, coluna_valor_4g]:.1f}%")
        with col4:
            st.metric("📊 Mediana", f"{df_4g[coluna_valor_4g].median():.1f}%")

    with tab2:
        st.markdown("### 🚀 Mapa de Cobertura 5G por Estado")

        fig_5g = mapa_cobertura_brasil(
            df_5g,
            coluna_uf=coluna_uf,
            coluna_valor=coluna_valor_5g,
            titulo="Cobertura 5G no Brasil",
            legenda="5G (%)",
            color_scale="Purples",
            altura=600
        )

        st.plotly_chart(fig_5g, use_container_width=True, key="mapa_5g")

        # Estatísticas 5G
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🇧🇷 Média Nacional", f"{df_5g[coluna_valor_5g].mean():.1f}%")
        with col2:
            idx_max = df_5g[coluna_valor_5g].idxmax()
            st.metric("🥇 Melhor Estado",
                     f"{df_5g.loc[idx_max, coluna_uf]}: {df_5g.loc[idx_max, coluna_valor_5g]:.1f}%")
        with col3:
            idx_min = df_5g[coluna_valor_5g].idxmin()
            st.metric("⚠️ Pior Estado",
                     f"{df_5g.loc[idx_min, coluna_uf]}: {df_5g.loc[idx_min, coluna_valor_5g]:.1f}%")
        with col4:
            st.metric("📊 Mediana", f"{df_5g[coluna_valor_5g].median():.1f}%")

    with tab3:
        st.markdown("### 🔄 Análise Comparativa: 4G vs 5G")

        # Prepara dados para merge (converte para tipos adequados)
        df_4g_merge = df_4g[[coluna_uf, coluna_valor_4g]].copy()
        df_4g_merge[coluna_uf] = df_4g_merge[coluna_uf].astype(str)
        df_4g_merge[coluna_valor_4g] = pd.to_numeric(df_4g_merge[coluna_valor_4g], errors='coerce')

        df_5g_merge = df_5g[[coluna_uf, coluna_valor_5g]].copy()
        df_5g_merge[coluna_uf] = df_5g_merge[coluna_uf].astype(str)
        df_5g_merge[coluna_valor_5g] = pd.to_numeric(df_5g_merge[coluna_valor_5g], errors='coerce')

        # Merge dos dataframes para comparação
        df_comp = pd.merge(
            df_4g_merge.rename(columns={coluna_valor_4g: 'Cobertura_4G'}),
            df_5g_merge.rename(columns={coluna_valor_5g: 'Cobertura_5G'}),
            on=coluna_uf,
            how='outer'
        )

        # Preenche valores nulos com 0 (agora são float, não categorical)
        df_comp['Cobertura_4G'] = df_comp['Cobertura_4G'].fillna(0)
        df_comp['Cobertura_5G'] = df_comp['Cobertura_5G'].fillna(0)

        # Calcula diferença
        df_comp['Diferenca'] = df_comp['Cobertura_4G'] - df_comp['Cobertura_5G']

        # Mapa de diferença
        st.markdown("#### 📊 Gap de Cobertura (4G - 5G)")
        st.caption("Valores positivos indicam que o 4G tem maior cobertura que o 5G")

        fig_diff = mapa_cobertura_brasil(
            df_comp,
            coluna_uf=coluna_uf,
            coluna_valor='Diferenca',
            titulo="Diferença de Cobertura (4G - 5G)",
            legenda="Gap (%)",
            color_scale="RdBu_r",
            range_color=(-10, 100),
            altura=500
        )

        st.plotly_chart(fig_diff, use_container_width=True, key="mapa_diff")

        # Gráfico de barras comparativo
        st.markdown("---")
        st.markdown("#### 📊 Ranking Comparativo por Estado")

        # Ordena por 4G
        df_comp_sorted = df_comp.sort_values('Cobertura_4G', ascending=True)

        fig_bars = go.Figure()

        fig_bars.add_trace(go.Bar(
            name='4G',
            y=df_comp_sorted[coluna_uf],
            x=df_comp_sorted['Cobertura_4G'],
            orientation='h',
            marker=dict(color='#3b82f6'),
            text=df_comp_sorted['Cobertura_4G'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto'
        ))

        fig_bars.add_trace(go.Bar(
            name='5G',
            y=df_comp_sorted[coluna_uf],
            x=df_comp_sorted['Cobertura_5G'],
            orientation='h',
            marker=dict(color='#8b5cf6'),
            text=df_comp_sorted['Cobertura_5G'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto'
        ))

        fig_bars.update_layout(
            barmode='group',
            height=800,
            xaxis_title="Cobertura (%)",
            yaxis_title="Estado",
            showlegend=True,
            margin=dict(l=10, r=10, t=10, b=10)
        )

        st.plotly_chart(fig_bars, use_container_width=True, key="bars_comp")

        # Tabela comparativa
        st.markdown("---")
        st.markdown("#### 📋 Tabela Comparativa Completa")

        df_comp_show = df_comp.sort_values('Cobertura_4G', ascending=False).copy()

        # Garante que são float antes de formatar
        df_comp_show['Cobertura_4G'] = pd.to_numeric(df_comp_show['Cobertura_4G'], errors='coerce')
        df_comp_show['Cobertura_5G'] = pd.to_numeric(df_comp_show['Cobertura_5G'], errors='coerce')
        df_comp_show['Diferenca'] = pd.to_numeric(df_comp_show['Diferenca'], errors='coerce')

        # Formata como string com %
        df_comp_show['Cobertura_4G'] = df_comp_show['Cobertura_4G'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
        df_comp_show['Cobertura_5G'] = df_comp_show['Cobertura_5G'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
        df_comp_show['Diferenca'] = df_comp_show['Diferenca'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")

        st.dataframe(df_comp_show, use_container_width=True, height=400)





