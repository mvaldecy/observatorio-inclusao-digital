"""
Componente de análise detalhada de municípios
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def renderizar_analise_municipios(df: pd.DataFrame, info: dict, 
                                  col_cobertura_selecionada: str,
                                  selected_uf: str | None):
    """
    Renderiza a seção completa de análise de municípios de um UF.
    
    Args:
        df: DataFrame completo
        info: Informações do analisador
        col_cobertura_selecionada: Coluna de cobertura em uso
        selected_uf: UF selecionada
    """
    if not selected_uf or not info['coluna_municipio']:
        return
    
    st.markdown("---")
    st.markdown(f"## 📊 Municípios do Estado: {selected_uf}")
    st.caption(f"🎯 Mostrando dados de cobertura móvel de todos os municípios de **{selected_uf}**")
    
    try:
        # Prepara dados
        df_uf_analysis = _preparar_dados_uf(df, info, selected_uf, col_cobertura_selecionada)
        
        if len(df_uf_analysis) == 0:
            st.warning(f"⚠️ Nenhum dado encontrado para o estado {selected_uf}")
            return
        
        # Debug info
        _renderizar_debug_info(df_uf_analysis, info, selected_uf)
        
        # Calcula ranking
        df_mun_ranking = _calcular_ranking_municipios(df_uf_analysis, info['coluna_municipio'], selected_uf)
        
        # Estatísticas gerais
        _renderizar_estatisticas_gerais(df_mun_ranking, selected_uf)
        
        st.markdown("---")
        
        # Análise estatística e distribuição
        _renderizar_analise_estatistica(df_mun_ranking, selected_uf)
        
        st.markdown("---")
        
        # Top 10 e Bottom 10
        _renderizar_destaques(df_mun_ranking, selected_uf)
        
        st.markdown("---")
        
        # Tabs com análises detalhadas
        _renderizar_tabs_analise(df_mun_ranking, selected_uf)
    
    except Exception as e:
        st.error(f"Erro ao processar municípios: {str(e)}")
        st.exception(e)


def _preparar_dados_uf(df: pd.DataFrame, info: dict, selected_uf: str, 
                       col_cobertura: str) -> pd.DataFrame:
    """
    Prepara e filtra dados do UF selecionado.
    """
    col_uf = info['coluna_uf']
    
    # Filtra apenas o UF selecionado
    df_uf = df[df[col_uf] == selected_uf].copy()
    
    # Converte cobertura para numérico
    if df_uf[col_cobertura].dtype == 'object':
        df_uf['Cobertura'] = pd.to_numeric(
            df_uf[col_cobertura].astype(str).str.replace('%', '').str.replace(',', '.'),
            errors='coerce'
        )
    else:
        df_uf['Cobertura'] = df_uf[col_cobertura]
    
    df_uf = df_uf.dropna(subset=['Cobertura'])
    
    return df_uf


def _renderizar_debug_info(df_uf: pd.DataFrame, info: dict, selected_uf: str):
    """
    Renderiza informações de debug.
    """
    col_mun = info['coluna_municipio']
    col_uf = info['coluna_uf']
    
    st.info(f"🔍 Coluna de município: **{col_mun}** | Registros encontrados: **{len(df_uf)}**")
    
    with st.expander("🔧 Debug - Ver dados brutos", expanded=False):
        st.write(f"Primeiros 20 registros de {selected_uf}:")
        cols_to_show = [col_mun, 'Cobertura']
        if col_uf not in cols_to_show:
            cols_to_show.insert(1, col_uf)
        st.dataframe(df_uf[cols_to_show].head(20))
        st.write(f"\nMunicípios únicos encontrados: **{df_uf[col_mun].nunique()}**")
        st.write("Lista dos primeiros 30 municípios:")
        st.write(sorted(df_uf[col_mun].unique())[:30])


def _calcular_ranking_municipios(df_uf: pd.DataFrame, col_mun: str, 
                                 selected_uf: str) -> pd.DataFrame:
    """
    Calcula ranking de municípios por cobertura.
    """
    # Agrupa por município
    df_ranking = df_uf.groupby(col_mun, as_index=False)['Cobertura'].mean()
    df_ranking = df_ranking.sort_values('Cobertura', ascending=False)
    
    # Debug: Mostra ranking antes do rename
    with st.expander("🔧 Debug - Ranking calculado", expanded=False):
        st.write("Primeiros 10 municípios no ranking:")
        st.dataframe(df_ranking.head(10))
    
    # Renomeia coluna se necessário
    if col_mun != 'Município':
        df_ranking = df_ranking.rename(columns={col_mun: 'Município'})
    
    df_ranking['Posição'] = range(1, len(df_ranking) + 1)
    df_ranking['UF'] = selected_uf
    
    return df_ranking


def _renderizar_estatisticas_gerais(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza estatísticas gerais dos municípios.
    """
    st.info(f"ℹ️ Analisando **{len(df_ranking)} municípios** do estado de **{selected_uf}**")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("Total de Municípios", f"{len(df_ranking):,}")
    
    with stats_col2:
        st.metric("Cobertura Média", f"{df_ranking['Cobertura'].mean():.2f}%")
    
    with stats_col3:
        st.metric("Melhor Cobertura", f"{df_ranking['Cobertura'].max():.2f}%")
    
    with stats_col4:
        st.metric("Pior Cobertura", f"{df_ranking['Cobertura'].min():.2f}%")


def _renderizar_analise_estatistica(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza análise estatística completa.
    """
    st.markdown(f"### 📊 Análise Estatística de {selected_uf}")
    st.caption("Entenda como a cobertura está distribuída entre os municípios")
    
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        _renderizar_estatisticas_descritivas(df_ranking)
    
    with stat_col2:
        _renderizar_distribuicao_faixas(df_ranking, selected_uf)


def _renderizar_estatisticas_descritivas(df_ranking: pd.DataFrame):
    """
    Renderiza estatísticas descritivas.
    """
    st.markdown("#### 📈 Estatísticas Descritivas")
    
    media = df_ranking['Cobertura'].mean()
    mediana = df_ranking['Cobertura'].median()
    desvio = df_ranking['Cobertura'].std()
    
    st.markdown(f"""
    **📍 Média:** `{media:.2f}%`  
    → Cobertura média de todos os municípios
    
    **🎯 Mediana:** `{mediana:.2f}%`  
    → Valor central - metade dos municípios tem mais, metade tem menos
    
    **📏 Desvio Padrão:** `{desvio:.2f}%`  
    → Variação dos dados (quanto maior, mais desigual é a cobertura)
    """)
    
    # Interpretação do desvio padrão
    if desvio < 10:
        st.success("✅ **Baixa variação:** Cobertura homogênea entre municípios")
    elif desvio < 20:
        st.info("ℹ️ **Variação moderada:** Alguma desigualdade na cobertura")
    else:
        st.warning("⚠️ **Alta variação:** Grande desigualdade entre municípios")


def _renderizar_distribuicao_faixas(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza distribuição por faixas de cobertura.
    """
    st.markdown("#### 🎚️ Distribuição por Faixas")
    st.caption("Quantidade de municípios em cada nível de cobertura")
    
    # Calcula distribuição
    distribuicao = _calcular_distribuicao_faixas(df_ranking)
    total_mun = len(df_ranking)
    
    # Mostra resumo com emojis
    emojis = {
        'Sem cobertura (0%)': '🔴',
        'Muito Baixa (0-25%)': '🟠',
        'Baixa (25-50%)': '🟡',
        'Média (50-75%)': '🔵',
        'Boa (75-90%)': '🟢',
        'Excelente (90-100%)': '🟢'
    }
    
    for faixa, dados in distribuicao.items():
        emoji = emojis.get(faixa, '⚪')
        qtd = dados['quantidade']
        perc = dados['percentual']
        
        if qtd > 0:
            exemplos = dados['municipios'][:3]
            exemplos_texto = ", ".join(exemplos)
            if qtd > 3:
                exemplos_texto += f" (+{qtd-3} outros)"
            st.markdown(f"{emoji} **{faixa}:** {qtd} ({perc:.1f}%) — *{exemplos_texto}*")
        else:
            st.markdown(f"{emoji} **{faixa}:** {qtd} ({perc:.1f}%)")
    
    # Gráfico de distribuição
    _renderizar_grafico_distribuicao(distribuicao, selected_uf)
    
    # Tabs com municípios por faixa
    _renderizar_tabs_faixas(distribuicao, total_mun, selected_uf)


def _calcular_distribuicao_faixas(df_ranking: pd.DataFrame) -> dict:
    """
    Calcula distribuição de municípios por faixa de cobertura.
    """
    total_mun = len(df_ranking)
    
    faixas = {
        'Sem cobertura (0%)': (0, 0, True),
        'Muito Baixa (0-25%)': (0, 25, False),
        'Baixa (25-50%)': (25, 50, False),
        'Média (50-75%)': (50, 75, False),
        'Boa (75-90%)': (75, 90, False),
        'Excelente (90-100%)': (90, 100, False)
    }
    
    distribuicao = {}
    
    for faixa, (min_val, max_val, igual) in faixas.items():
        if igual:
            mask = df_ranking['Cobertura'] == min_val
        else:
            mask = (df_ranking['Cobertura'] > min_val) & (df_ranking['Cobertura'] <= max_val)
        
        municipios = df_ranking[mask]['Município'].tolist()
        qtd = len(municipios)
        perc = (qtd / total_mun) * 100 if total_mun > 0 else 0
        
        distribuicao[faixa] = {
            'quantidade': qtd,
            'percentual': perc,
            'municipios': municipios
        }
    
    return distribuicao


def _renderizar_grafico_distribuicao(distribuicao: dict, selected_uf: str):
    """
    Renderiza gráfico de barras da distribuição.
    """
    st.markdown("#### 📊 Visualização da Distribuição")
    
    faixas_ordenadas = [
        'Sem cobertura (0%)', 'Muito Baixa (0-25%)', 'Baixa (25-50%)',
        'Média (50-75%)', 'Boa (75-90%)', 'Excelente (90-100%)'
    ]
    
    valores = [distribuicao[f]['quantidade'] for f in faixas_ordenadas]
    percentuais = [distribuicao[f]['percentual'] for f in faixas_ordenadas]
    
    cores = ['#ef4444', '#f97316', '#eab308', '#3b82f6', '#10b981', '#059669']
    
    fig_dist = go.Figure(data=[go.Bar(
        y=faixas_ordenadas,
        x=valores,
        orientation='h',
        marker=dict(color=cores, line=dict(color='rgba(255,255,255,0.2)', width=1)),
        text=[f"{v} ({p:.1f}%)" for v, p in zip(valores, percentuais)],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Municípios: %{x}<br>Percentual: %{text}<extra></extra>'
    )])
    
    fig_dist.update_layout(
        height=350,
        xaxis_title="Quantidade de Municípios",
        yaxis_title="",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_dist, width='stretch', key=f"dist_{selected_uf}")


def _renderizar_tabs_faixas(distribuicao: dict, total_mun: int, selected_uf: str):
    """
    Renderiza tabs com municípios separados por faixas.
    """
    st.markdown("---")
    st.markdown("#### 🔍 Municípios por Faixa de Cobertura")
    
    # Destaca faixas críticas
    faixas_criticas = ['Sem cobertura (0%)', 'Muito Baixa (0-25%)', 'Baixa (25-50%)']
    qtd_criticos = sum(distribuicao[f]['quantidade'] for f in faixas_criticas)
    
    if qtd_criticos > 0:
        st.warning(f"⚠️ **{qtd_criticos} municípios ({(qtd_criticos/total_mun)*100:.1f}%)** com cobertura insuficiente (<50%) precisam de atenção!")
    
    tab_critico, tab_atencao, tab_bom = st.tabs([
        f"🔴 Críticos ({distribuicao['Sem cobertura (0%)']['quantidade'] + distribuicao['Muito Baixa (0-25%)']['quantidade']})",
        f"🟡 Atenção ({distribuicao['Baixa (25-50%)']['quantidade'] + distribuicao['Média (50-75%)']['quantidade']})",
        f"🟢 Bons ({distribuicao['Boa (75-90%)']['quantidade'] + distribuicao['Excelente (90-100%)']['quantidade']})"
    ])
    
    with tab_critico:
        st.caption("Municípios com cobertura crítica (0-25%) que necessitam investimento urgente")
        for faixa in ['Sem cobertura (0%)', 'Muito Baixa (0-25%)']:
            _renderizar_lista_municipios_faixa(faixa, distribuicao[faixa], selected_uf)
    
    with tab_atencao:
        st.caption("Municípios com cobertura moderada (25-75%) que podem melhorar")
        for faixa in ['Baixa (25-50%)', 'Média (50-75%)']:
            _renderizar_lista_municipios_faixa(faixa, distribuicao[faixa], selected_uf)
    
    with tab_bom:
        st.caption("Municípios com boa cobertura (75-100%)")
        for faixa in ['Boa (75-90%)', 'Excelente (90-100%)']:
            _renderizar_lista_municipios_faixa(faixa, distribuicao[faixa], selected_uf)


def _renderizar_lista_municipios_faixa(faixa: str, dados: dict, selected_uf: str):
    """
    Renderiza lista de municípios de uma faixa específica.
    """
    if dados['quantidade'] > 0:
        st.markdown(f"**{faixa}** ({dados['quantidade']} municípios)")
        municipios_text = ", ".join(dados['municipios'])
        st.text_area(
            f"Lista de municípios - {faixa}",
            municipios_text,
            height=100,
            key=f"text_{faixa}_{selected_uf}",
            label_visibility="collapsed"
        )


def _renderizar_destaques(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza top 10 e bottom 10.
    """
    st.markdown(f"### 🎯 Destaques de {selected_uf}")
    
    dest_col1, dest_col2 = st.columns(2)
    
    with dest_col1:
        _renderizar_top10(df_ranking, selected_uf)
    
    with dest_col2:
        _renderizar_bottom10(df_ranking, selected_uf)


def _renderizar_top10(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza top 10 municípios.
    """
    st.markdown("#### 🏆 Top 10 - Mais Conectados")
    st.caption(f"Municípios de {selected_uf} com melhor cobertura")
    
    df_top10 = df_ranking.head(10).copy()
    df_top10_show = df_top10[['Posição', 'Município', 'Cobertura']].copy()
    df_top10_show['Cobertura (%)'] = df_top10_show['Cobertura'].apply(lambda x: f"{x:.2f}%")
    df_top10_show['🥇'] = ['🥇', '🥈', '🥉'] + [''] * 7 if len(df_top10_show) >= 3 else [''] * len(df_top10_show)
    df_top10_show = df_top10_show[['🥇', 'Posição', 'Município', 'Cobertura (%)']]
    
    st.dataframe(df_top10_show, width='stretch', hide_index=True, height=400)
    
    # Gráfico
    fig_top10 = go.Figure(data=[go.Bar(
        y=df_top10['Município'],
        x=df_top10['Cobertura'],
        orientation='h',
        marker=dict(color=df_top10['Cobertura'], colorscale='Greens', showscale=False),
        text=df_top10['Cobertura'].apply(lambda x: f"{x:.1f}%"),
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Cobertura: %{x:.2f}%<extra></extra>'
    )])
    
    fig_top10.update_layout(
        height=400,
        xaxis_title="Cobertura (%)",
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig_top10, width='stretch', key=f"top10_main_{selected_uf}")


def _renderizar_bottom10(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza bottom 10 municípios.
    """
    st.markdown("#### ⚠️ Bottom 10 - Menos Conectados")
    st.caption(f"Municípios de {selected_uf} com pior cobertura")
    
    df_bottom10 = df_ranking.tail(10).sort_values('Cobertura', ascending=True).copy()
    df_bottom10_show = df_bottom10[['Posição', 'Município', 'Cobertura']].copy()
    df_bottom10_show['Posição'] = range(len(df_ranking), len(df_ranking) - 10, -1)
    df_bottom10_show['Cobertura (%)'] = df_bottom10_show['Cobertura'].apply(lambda x: f"{x:.2f}%")
    df_bottom10_show['⚠️'] = ['🚨'] * len(df_bottom10_show)
    df_bottom10_show = df_bottom10_show[['⚠️', 'Posição', 'Município', 'Cobertura (%)']]
    
    st.dataframe(df_bottom10_show, width='stretch', hide_index=True, height=400)
    
    # Gráfico
    fig_bottom10 = go.Figure(data=[go.Bar(
        y=df_bottom10['Município'],
        x=df_bottom10['Cobertura'],
        orientation='h',
        marker=dict(color=df_bottom10['Cobertura'], colorscale='Reds', showscale=False),
        text=df_bottom10['Cobertura'].apply(lambda x: f"{x:.1f}%"),
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Cobertura: %{x:.2f}%<extra></extra>'
    )])
    
    fig_bottom10.update_layout(
        height=400,
        xaxis_title="Cobertura (%)",
        yaxis={'categoryorder': 'total descending'},
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig_bottom10, width='stretch', key=f"bottom10_main_{selected_uf}")


def _renderizar_tabs_analise(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza tabs com análises detalhadas.
    """
    st.markdown("### 📊 Análises Detalhadas")
    
    viz_tab1, viz_tab2, viz_tab3 = st.tabs([
        "📊 Ranking Completo",
        "📈 Gráficos Comparativos",
        "🔝 Personalizar Top/Bottom"
    ])
    
    with viz_tab1:
        from .tabs_analise import renderizar_tab_ranking
        renderizar_tab_ranking(df_ranking, selected_uf)
    
    with viz_tab2:
        from .tabs_analise import renderizar_tab_graficos
        renderizar_tab_graficos(df_ranking, selected_uf)
    
    with viz_tab3:
        from .tabs_analise import renderizar_tab_personalizado
        renderizar_tab_personalizado(df_ranking, selected_uf)
