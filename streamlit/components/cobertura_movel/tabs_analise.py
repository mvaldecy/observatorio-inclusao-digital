"""
Tabs de análise detalhada de municípios
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


def renderizar_tab_ranking(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Tab com ranking completo e busca.
    """
    st.markdown("### 📋 Lista Completa - Do Mais ao Menos Conectado")
    
    # Busca e ordenação
    search_col, order_col = st.columns([3, 1])
    
    with search_col:
        busca = st.text_input(
            "🔍 Buscar município:",
            placeholder="Digite o nome do município...",
            key=f"busca_mun_{selected_uf}"
        )
    
    with order_col:
        ordem_ranking = st.selectbox(
            "Ordenar:",
            ["Maior Cobertura", "Menor Cobertura", "Nome A-Z"],
            key=f"ordem_rank_{selected_uf}"
        )
    
    # Aplica filtros
    df_display = df_ranking.copy()
    if busca:
        df_display = df_display[df_display['Município'].str.contains(busca, case=False, na=False)]
    
    if ordem_ranking == "Menor Cobertura":
        df_display = df_display.sort_values('Cobertura', ascending=True)
        df_display['Posição'] = range(1, len(df_display) + 1)
    elif ordem_ranking == "Nome A-Z":
        df_display = df_display.sort_values('Município', ascending=True)
    
    # Formata tabela
    df_show = df_display.copy()
    df_show['Cobertura (%)'] = df_show['Cobertura'].apply(lambda x: f"{x:.2f}%")
    df_show = df_show[['Posição', 'Município', 'Cobertura (%)']]
    
    # Mostra tabela
    st.dataframe(df_show, width='stretch', height=500, hide_index=True)
    
    # Download
    csv_data = df_display[['Município', 'Cobertura', 'Posição']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 Baixar Ranking Completo ({len(df_display)} municípios)",
        data=csv_data,
        file_name=f"ranking_cobertura_{selected_uf}.csv",
        mime="text/csv",
        width='stretch'
    )


def renderizar_tab_graficos(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Tab com gráficos comparativos.
    """
    st.markdown("### 📈 Gráficos Comparativos dos Municípios")
    
    # Gráficos Top 15 e Bottom 15
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.markdown("#### 🏆 Top 15 - Melhor Cobertura")
        df_top15 = df_ranking.head(15)
        
        fig_top = go.Figure(data=[go.Bar(
            y=df_top15['Município'],
            x=df_top15['Cobertura'],
            orientation='h',
            marker=dict(color=df_top15['Cobertura'], colorscale='Greens', showscale=False),
            text=df_top15['Cobertura'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Cobertura: %{x:.2f}%<extra></extra>'
        )])
        
        fig_top.update_layout(
            height=500,
            xaxis_title="Cobertura (%)",
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_top, width='stretch', key=f"top_graph_{selected_uf}")
    
    with col_graph2:
        st.markdown("#### ⚠️ Bottom 15 - Pior Cobertura")
        df_bottom15 = df_ranking.tail(15).sort_values('Cobertura', ascending=True)
        
        fig_bottom = go.Figure(data=[go.Bar(
            y=df_bottom15['Município'],
            x=df_bottom15['Cobertura'],
            orientation='h',
            marker=dict(color=df_bottom15['Cobertura'], colorscale='Reds', showscale=False),
            text=df_bottom15['Cobertura'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Cobertura: %{x:.2f}%<extra></extra>'
        )])
        
        fig_bottom.update_layout(
            height=500,
            xaxis_title="Cobertura (%)",
            yaxis={'categoryorder': 'total descending'},
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_bottom, width='stretch', key=f"bottom_graph_{selected_uf}")
    
    # Histograma
    st.markdown("---")
    _renderizar_histograma(df_ranking, selected_uf)
    
    # Box plot
    st.markdown("---")
    _renderizar_boxplot(df_ranking, selected_uf)


def _renderizar_histograma(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza histograma de distribuição.
    """
    st.markdown("#### 📊 Distribuição de Cobertura nos Municípios")
    st.caption("Visualize como os municípios estão distribuídos ao longo da escala de cobertura")
    
    media_hist = df_ranking['Cobertura'].mean()
    mediana_hist = df_ranking['Cobertura'].median()
    
    # Cria histograma com cores
    bins = np.linspace(0, 100, 31)
    hist_values, bin_edges = np.histogram(df_ranking['Cobertura'], bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    def get_color(value):
        if value <= 25:
            return '#ef4444'
        elif value <= 50:
            return '#f59e0b'
        elif value <= 75:
            return '#3b82f6'
        else:
            return '#10b981'
    
    colors = [get_color(center) for center in bin_centers]
    
    fig_hist = go.Figure()
    
    fig_hist.add_trace(go.Bar(
        x=bin_centers,
        y=hist_values,
        width=(bin_edges[1] - bin_edges[0]) * 0.9,
        marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.3)', width=1)),
        hovertemplate='Cobertura: %{x:.1f}%<br>Municípios: %{y}<extra></extra>',
        name='Municípios'
    ))
    
    # Linhas de referência
    fig_hist.add_vline(
        x=media_hist, line_dash="dash", line_color="#fbbf24", line_width=3,
        annotation_text=f"Média: {media_hist:.1f}%", annotation_position="top",
        annotation_font_size=12, annotation_font_color="#fbbf24"
    )
    
    fig_hist.add_vline(
        x=mediana_hist, line_dash="dot", line_color="#8b5cf6", line_width=3,
        annotation_text=f"Mediana: {mediana_hist:.1f}%", annotation_position="bottom",
        annotation_font_size=12, annotation_font_color="#8b5cf6"
    )
    
    # Áreas de referência
    fig_hist.add_vrect(x0=0, x1=25, fillcolor="red", opacity=0.1, layer="below", line_width=0,
                       annotation_text="Crítico", annotation_position="top left", annotation_font_size=10)
    fig_hist.add_vrect(x0=25, x1=50, fillcolor="orange", opacity=0.1, layer="below", line_width=0,
                       annotation_text="Atenção", annotation_position="top left", annotation_font_size=10)
    fig_hist.add_vrect(x0=75, x1=100, fillcolor="green", opacity=0.1, layer="below", line_width=0,
                       annotation_text="Bom", annotation_position="top right", annotation_font_size=10)
    
    fig_hist.update_layout(
        title=f"Distribuição de Cobertura nos Municípios de {selected_uf}",
        xaxis_title="Cobertura (%)",
        yaxis_title="Quantidade de Municípios",
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        xaxis=dict(range=[0, 105], dtick=10)
    )
    
    st.plotly_chart(fig_hist, width='stretch', key=f"hist_{selected_uf}")
    
    # Explicação
    with st.expander("ℹ️ Como interpretar o histograma", expanded=False):
        st.markdown(f"""
        **🎨 Cores das Barras:**
        - 🔴 **Vermelho** (0-25%): Cobertura crítica
        - 🟠 **Laranja** (25-50%): Cobertura insuficiente  
        - 🔵 **Azul** (50-75%): Cobertura razoável
        - 🟢 **Verde** (75-100%): Boa cobertura
        
        **📍 Linhas de Referência:**
        - 🟡 **Linha tracejada (Média: {media_hist:.1f}%)**: Cobertura média de todos os municípios
        - 🟣 **Linha pontilhada (Mediana: {mediana_hist:.1f}%)**: Metade tem mais, metade tem menos
        
        **💡 Como usar:**
        - **Barras altas à esquerda** → Muitos municípios com baixa cobertura (problema!)
        - **Barras altas à direita** → Muitos municípios com boa cobertura (positivo!)
        - **Barras espalhadas** → Grande desigualdade entre municípios
        """)


def _renderizar_boxplot(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Renderiza box plot estatístico.
    """
    st.markdown("#### 📦 Análise Estatística (Box Plot)")
    st.caption("Visualização compacta da distribuição: mediana, quartis e outliers")
    
    q1 = df_ranking['Cobertura'].quantile(0.25)
    q2 = df_ranking['Cobertura'].quantile(0.50)
    q3 = df_ranking['Cobertura'].quantile(0.75)
    
    fig_box = go.Figure()
    
    fig_box.add_trace(go.Box(
        y=df_ranking['Cobertura'],
        name=selected_uf,
        marker=dict(color='#3b82f6', outliercolor='#ef4444', line=dict(color='#1e40af', width=2)),
        boxmean='sd',
        boxpoints='outliers',
        hovertemplate='Cobertura: %{y:.2f}%<extra></extra>'
    ))
    
    # Anotações dos quartis
    annotations = [
        dict(x=0.15, y=q1, text=f'Q1: {q1:.1f}%<br>(25% abaixo)', showarrow=True, arrowhead=2,
             ax=80, ay=0, font=dict(size=11, color='#f59e0b'), bgcolor='rgba(0,0,0,0.7)', borderpad=4),
        dict(x=0.15, y=q2, text=f'Mediana: {q2:.1f}%<br>(50% acima/abaixo)', showarrow=True, arrowhead=2,
             ax=80, ay=0, font=dict(size=11, color='#8b5cf6'), bgcolor='rgba(0,0,0,0.7)', borderpad=4),
        dict(x=0.15, y=q3, text=f'Q3: {q3:.1f}%<br>(75% abaixo)', showarrow=True, arrowhead=2,
             ax=80, ay=0, font=dict(size=11, color='#10b981'), bgcolor='rgba(0,0,0,0.7)', borderpad=4)
    ]
    
    fig_box.update_layout(
        height=400,
        yaxis_title="Cobertura (%)",
        showlegend=False,
        annotations=annotations,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(range=[-5, 105])
    )
    
    col_box1, col_box2 = st.columns([2, 1])
    
    with col_box1:
        st.plotly_chart(fig_box, width='stretch', key=f"box_{selected_uf}")
    
    with col_box2:
        st.markdown("**📊 Interpretação:**")
        st.markdown(f"""
        **Quartis:**
        - 🟠 **Q1 ({q1:.1f}%)**: 25% dos municípios tem menos
        - 🟣 **Mediana ({q2:.1f}%)**: Valor central
        - 🟢 **Q3 ({q3:.1f}%)**: 75% dos municípios tem menos
        
        **Amplitude Interquartil:**
        - **{q3-q1:.1f}%** (Q3 - Q1)
        - 50% central dos dados
        
        **Outliers (🔴):**
        - Municípios fora do padrão
        - Podem ser excepcionalmente bons ou ruins
        """)
    
    # Explicação do Box Plot
    with st.expander("ℹ️ Como ler um Box Plot", expanded=False):
        st.markdown("""
        **📦 Elementos do Box Plot:**
        
        1. **Caixa (retângulo azul)**: 
           - Contém 50% dos municípios (do meio)
           - Base = Q1 (25% abaixo)
           - Linha central = Mediana (50% acima/abaixo)
           - Topo = Q3 (75% abaixo)
        
        2. **Bigodes (linhas)**:
           - Linha inferior: valor mínimo (sem outliers)
           - Linha superior: valor máximo (sem outliers)
        
        3. **Pontos vermelhos**:
           - Outliers (valores extremos)
           - Municípios muito diferentes da maioria
        
        **💡 Interpretação rápida:**
        - **Caixa pequena** → Municípios similares (baixa variação)
        - **Caixa grande** → Municípios muito diferentes (alta variação)
        - **Mediana perto do topo** → Maioria tem valores altos
        - **Mediana perto da base** → Maioria tem valores baixos
        """)


def renderizar_tab_personalizado(df_ranking: pd.DataFrame, selected_uf: str):
    """
    Tab com destaques personalizados.
    """
    st.markdown("### 🔝 Destaques - Top e Bottom")
    
    num_dest = st.slider(
        "Quantidade de municípios nos destaques:",
        min_value=5,
        max_value=30,
        value=10,
        step=5,
        key=f"slider_dest_{selected_uf}"
    )
    
    dest_col1, dest_col2 = st.columns(2)
    
    with dest_col1:
        st.markdown(f"#### 🏆 Top {num_dest}")
        df_top_dest = df_ranking.head(num_dest).copy()
        df_top_dest['Cobertura (%)'] = df_top_dest['Cobertura'].apply(lambda x: f"{x:.2f}%")
        df_top_dest = df_top_dest[['Posição', 'Município', 'Cobertura (%)']]
        st.dataframe(df_top_dest, width='stretch', hide_index=True, height=400)
    
    with dest_col2:
        st.markdown(f"#### ⚠️ Bottom {num_dest}")
        df_bottom_dest = df_ranking.tail(num_dest).sort_values('Cobertura', ascending=True).copy()
        df_bottom_dest['Posição'] = range(len(df_ranking), len(df_ranking) - num_dest, -1)
        df_bottom_dest['Cobertura (%)'] = df_bottom_dest['Cobertura'].apply(lambda x: f"{x:.2f}%")
        df_bottom_dest = df_bottom_dest[['Posição', 'Município', 'Cobertura (%)']]
        st.dataframe(df_bottom_dest, width='stretch', hide_index=True, height=400)
