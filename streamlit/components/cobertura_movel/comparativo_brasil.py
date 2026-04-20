"""
Componente de comparativo Brasil, Nordeste e Piauí
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from .config import NE_UF


def renderizar_comparativo_brasil(df: pd.DataFrame, info: dict, col_cobertura_selecionada: str):
    """
    Renderiza a seção de comparativo entre Brasil, Nordeste e Piauí.
    
    Args:
        df: DataFrame com os dados completos
        info: Dicionário com informações do analisador
        col_cobertura_selecionada: Nome da coluna de cobertura selecionada
    """
    st.markdown("## 📊 Comparativo Brasil, Nordeste e Piauí")
    
    if not col_cobertura_selecionada:
        st.info("⚠️ Selecione uma coluna de cobertura na barra lateral para ver as análises.")
        return
    
    try:
        col_uf_info = info['coluna_uf']
        
        # Prepara dados
        df_comp = df.copy()
        
        # Converte cobertura para numérico
        if df_comp[col_cobertura_selecionada].dtype == 'object':
            df_comp['Cobertura_num'] = pd.to_numeric(
                df_comp[col_cobertura_selecionada].astype(str).str.replace('%', '').str.replace(',', '.'),
                errors='coerce'
            )
        else:
            df_comp['Cobertura_num'] = df_comp[col_cobertura_selecionada]
        
        df_comp = df_comp.dropna(subset=['Cobertura_num'])
        
        # Calcula estatísticas
        stats_brasil = _calcular_stats(df_comp, 'Brasil')
        
        # Nordeste
        if col_uf_info and col_uf_info in df_comp.columns:
            df_ne = df_comp[df_comp[col_uf_info].isin(NE_UF)]
            stats_nordeste = _calcular_stats(df_ne, 'Nordeste')
            
            # Piauí
            df_pi = df_comp[df_comp[col_uf_info] == 'PI']
            stats_piaui = _calcular_stats(df_pi, 'Piauí')
        else:
            stats_nordeste = stats_brasil.copy()
            stats_nordeste['Região'] = 'Nordeste (N/D)'
            stats_piaui = stats_brasil.copy()
            stats_piaui['Região'] = 'Piauí (N/D)'
        
        # Renderiza visão geral
        _renderizar_visao_geral(stats_brasil, stats_nordeste, stats_piaui)
        
        # Renderiza gráfico comparativo
        st.markdown("---")
        _renderizar_grafico_comparativo(stats_brasil, stats_nordeste, stats_piaui)
        
    except Exception as e:
        st.error(f"Erro ao processar comparativo: {str(e)}")


def _calcular_stats(df: pd.DataFrame, regiao: str) -> dict:
    """
    Calcula estatísticas de cobertura para uma região.
    """
    return {
        'Região': regiao,
        'Média': df['Cobertura_num'].mean(),
        'Mediana': df['Cobertura_num'].median(),
        'Máxima': df['Cobertura_num'].max(),
        'Mínima': df['Cobertura_num'].min(),
        'Total': len(df)
    }


def _renderizar_visao_geral(stats_brasil: dict, stats_nordeste: dict, stats_piaui: dict):
    """
    Renderiza cards com métricas de visão geral.
    """
    st.markdown("### 🌎 Visão Geral de Cobertura")
    st.caption("💡 Compare os indicadores de cobertura móvel entre Brasil, Nordeste e Piauí")
    
    # Explicação rápida das métricas
    with st.expander("ℹ️ Entenda as métricas", expanded=False):
        st.markdown("""
        **📊 Cobertura Média:** Percentual médio de cobertura de todos os municípios da região
        
        **🎯 Mediana:** Valor central - metade dos municípios tem cobertura acima, metade abaixo
        
        **📈 Delta vs Brasil:** Diferença em relação à média nacional
        - Positivo (+): Região está acima da média nacional
        - Negativo (-): Região está abaixo da média nacional
        
        **📏 Barra de Progresso:** Visualização percentual da cobertura média
        """)
    
    comp_col1, comp_col2, comp_col3 = st.columns(3)
    
    with comp_col1:
        st.markdown("#### 🇧🇷 Brasil")
        st.metric("Cobertura Média", f"{stats_brasil['Média']:.2f}%")
        st.metric("Mediana", f"{stats_brasil['Mediana']:.2f}%")
        st.metric("Registros", f"{stats_brasil['Total']:,}")
        st.progress(stats_brasil['Média'] / 100)
    
    with comp_col2:
        st.markdown("#### 🌵 Nordeste")
        delta_ne = stats_nordeste['Média'] - stats_brasil['Média']
        st.metric("Cobertura Média", f"{stats_nordeste['Média']:.2f}%", 
                 delta=f"{delta_ne:+.2f}% vs Brasil")
        st.metric("Mediana", f"{stats_nordeste['Mediana']:.2f}%")
        st.metric("Registros", f"{stats_nordeste['Total']:,}")
        st.progress(stats_nordeste['Média'] / 100)
    
    with comp_col3:
        st.markdown("#### 🏛️ Piauí")
        delta_pi = stats_piaui['Média'] - stats_brasil['Média']
        st.metric("Cobertura Média", f"{stats_piaui['Média']:.2f}%",
                 delta=f"{delta_pi:+.2f}% vs Brasil")
        st.metric("Mediana", f"{stats_piaui['Mediana']:.2f}%")
        st.metric("Registros", f"{stats_piaui['Total']:,}")
        st.progress(stats_piaui['Média'] / 100)


def _renderizar_grafico_comparativo(stats_brasil: dict, stats_nordeste: dict, stats_piaui: dict):
    """
    Renderiza gráfico de barras comparativo.
    """
    df_comparativo = pd.DataFrame([stats_brasil, stats_nordeste, stats_piaui])
    
    fig_comp = go.Figure()
    
    fig_comp.add_trace(go.Bar(
        name='Média',
        x=df_comparativo['Região'],
        y=df_comparativo['Média'],
        marker=dict(color='#3b82f6'),
        text=df_comparativo['Média'].apply(lambda x: f"{x:.1f}%"),
        textposition='auto'
    ))
    
    fig_comp.add_trace(go.Bar(
        name='Máxima',
        x=df_comparativo['Região'],
        y=df_comparativo['Máxima'],
        marker=dict(color='#10b981'),
        text=df_comparativo['Máxima'].apply(lambda x: f"{x:.1f}%"),
        textposition='auto'
    ))
    
    fig_comp.add_trace(go.Bar(
        name='Mínima',
        x=df_comparativo['Região'],
        y=df_comparativo['Mínima'],
        marker=dict(color='#ef4444'),
        text=df_comparativo['Mínima'].apply(lambda x: f"{x:.1f}%"),
        textposition='auto'
    ))
    
    fig_comp.update_layout(
        barmode='group',
        height=400,
        xaxis_title="Região",
        yaxis_title="Cobertura (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_comp, width='stretch', key="comp_brasil_ne_pi")
