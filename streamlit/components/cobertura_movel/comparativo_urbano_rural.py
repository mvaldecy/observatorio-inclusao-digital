"""
Componente de comparativo Urbano x Rural
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def renderizar_comparativo_urbano_rural(df: pd.DataFrame, info: dict, 
                                       col_cobertura_selecionada: str, 
                                       selected_uf: str | None):
    """
    Renderiza a análise comparativa entre áreas urbanas e rurais.
    
    Args:
        df: DataFrame com os dados
        info: Informações do analisador
        col_cobertura_selecionada: Coluna de cobertura em uso
        selected_uf: UF selecionada para análise
    """
    # Verifica se há coluna de localização (urbano/rural)
    col_localizacao = _detectar_coluna_localizacao(df)
    
    # Debug: Mostra colunas disponíveis se não encontrou localização
    if not col_localizacao and selected_uf:
        _renderizar_debug_colunas(df)
    
    if col_localizacao and selected_uf:
        _renderizar_analise_urbano_rural(
            df, info, col_cobertura_selecionada, 
            selected_uf, col_localizacao
        )
    elif not col_localizacao and selected_uf:
        _renderizar_mensagem_nao_disponivel()


def _detectar_coluna_localizacao(df: pd.DataFrame) -> str | None:
    """
    Detecta coluna que contém informação de localização urbano/rural.
    """
    termos_busca = ['LOCALIZA', 'AREA', 'URBANO', 'RURAL', 'TIPO', 'ZONA', 'REGIÃO', 'REGIAO']
    for col in df.columns:
        col_upper = str(col).upper()
        if any(term in col_upper for term in termos_busca):
            return col
    return None


def _renderizar_debug_colunas(df: pd.DataFrame):
    """
    Renderiza expander de debug com colunas disponíveis.
    """
    with st.expander("🔍 Debug - Colunas disponíveis no dataset", expanded=False):
        st.write("**Buscando colunas de localização (urbano/rural)...**")
        termos_busca = ['LOCALIZA', 'AREA', 'URBANO', 'RURAL', 'TIPO', 'ZONA', 'REGIÃO', 'REGIAO']
        st.write(f"Termos de busca: {', '.join(termos_busca)}")
        st.write(f"\n**Todas as colunas disponíveis ({len(df.columns)}):**")
        st.code("\n".join(df.columns.tolist()))
        st.info("💡 Se houver uma coluna de localização com nome diferente, podemos ajustar o código para detectá-la.")


def _renderizar_mensagem_nao_disponivel():
    """
    Renderiza mensagem quando dados urbano/rural não estão disponíveis.
    """
    st.markdown("---")
    st.info(f"""
    ℹ️ **Comparativo Urbano × Rural não disponível**
    
    O dataset de cobertura móvel não contém informações sobre localização urbana/rural dos municípios.
    
    💡 **Dica:** Este tipo de análise está mais disponível em dados de:
    - Conectividade Escolar (que inclui localização das escolas)
    - Dados censitários do IBGE
    - Dados específicos de infraestrutura
    
    Use o expander "Debug" acima para ver todas as colunas disponíveis.
    """)


def _renderizar_analise_urbano_rural(df: pd.DataFrame, info: dict, 
                                     col_cobertura_selecionada: str,
                                     selected_uf: str, col_localizacao: str):
    """
    Renderiza a análise completa urbano x rural.
    """
    st.markdown("---")
    st.markdown(f"## 🏙️ Comparativo Urbano × Rural - {selected_uf}")
    st.caption("Análise comparativa da cobertura móvel entre áreas urbanas e rurais")
    
    try:
        # Prepara dados do UF selecionado
        df_urb_rural = df[df[info['coluna_uf']] == selected_uf].copy()
        
        # Converte cobertura para numérico
        if df_urb_rural[col_cobertura_selecionada].dtype == 'object':
            df_urb_rural['Cobertura_num'] = pd.to_numeric(
                df_urb_rural[col_cobertura_selecionada].astype(str).str.replace('%', '').str.replace(',', '.'),
                errors='coerce'
            )
        else:
            df_urb_rural['Cobertura_num'] = df_urb_rural[col_cobertura_selecionada]
        
        df_urb_rural = df_urb_rural.dropna(subset=['Cobertura_num'])
        
        # Padroniza tipos de área
        df_urb_rural = _padronizar_tipos_area(df_urb_rural, col_localizacao)
        
        if len(df_urb_rural) > 0:
            # Calcula estatísticas
            stats_urb_rural = df_urb_rural.groupby('Tipo_Area')['Cobertura_num'].agg([
                ('Média', 'mean'),
                ('Mediana', 'median'),
                ('Máxima', 'max'),
                ('Mínima', 'min'),
                ('Desvio', 'std'),
                ('Total', 'count')
            ]).round(2)
            
            # Renderiza métricas
            _renderizar_metricas_urbano_rural(stats_urb_rural, selected_uf)
            
            # Renderiza gráficos
            st.markdown("---")
            _renderizar_graficos_urbano_rural(df_urb_rural, stats_urb_rural, selected_uf)
            
            # Tabela estatística
            _renderizar_tabela_estatisticas(stats_urb_rural)
            
            # Interpretação
            _renderizar_interpretacao()
        else:
            st.info(f"ℹ️ Não foram encontrados dados de localização urbano/rural para {selected_uf}")
            st.caption("Os dados podem não conter informação sobre área urbana/rural ou estão em formato não reconhecido.")
    
    except Exception as e:
        st.warning(f"⚠️ Não foi possível processar comparativo urbano/rural: {str(e)}")
        with st.expander("Ver detalhes do erro"):
            st.exception(e)


def _padronizar_tipos_area(df: pd.DataFrame, col_localizacao: str) -> pd.DataFrame:
    """
    Padroniza os valores da coluna de localização para Urbano/Rural.
    """
    df['Tipo_Area'] = df[col_localizacao].astype(str).str.upper()
    
    # Padroniza nomes
    df['Tipo_Area'] = df['Tipo_Area'].replace({
        'URBANA': 'Urbano',
        'URBAN': 'Urbano',
        'U': 'Urbano',
        'RURAL': 'Rural',
        'R': 'Rural'
    })
    
    # Filtra apenas Urbano e Rural
    df = df[df['Tipo_Area'].isin(['Urbano', 'Rural'])]
    
    return df


def _renderizar_metricas_urbano_rural(stats_urb_rural: pd.DataFrame, selected_uf: str):
    """
    Renderiza cards de métricas comparativas.
    """
    urb_col1, urb_col2, urb_col3 = st.columns(3)
    
    urbano_stats = None
    rural_stats = None
    
    if 'Urbano' in stats_urb_rural.index:
        urbano_stats = stats_urb_rural.loc['Urbano']
        with urb_col1:
            st.markdown("### 🏙️ Área Urbana")
            st.metric("Cobertura Média", f"{urbano_stats['Média']:.2f}%")
            st.metric("Mediana", f"{urbano_stats['Mediana']:.2f}%")
            st.metric("Registros", f"{int(urbano_stats['Total']):,}")
    
    if 'Rural' in stats_urb_rural.index:
        rural_stats = stats_urb_rural.loc['Rural']
        with urb_col2:
            st.markdown("### 🌾 Área Rural")
            if urbano_stats is not None:
                delta = rural_stats['Média'] - urbano_stats['Média']
                st.metric("Cobertura Média", f"{rural_stats['Média']:.2f}%", 
                         delta=f"{delta:+.2f}% vs Urbano")
            else:
                st.metric("Cobertura Média", f"{rural_stats['Média']:.2f}%")
            st.metric("Mediana", f"{rural_stats['Mediana']:.2f}%")
            st.metric("Registros", f"{int(rural_stats['Total']):,}")
    
    with urb_col3:
        st.markdown("### 📊 Gap Digital")
        if urbano_stats is not None and rural_stats is not None:
            gap = urbano_stats['Média'] - rural_stats['Média']
            gap_perc = (gap / urbano_stats['Média'] * 100) if urbano_stats['Média'] > 0 else 0
            
            st.metric("Diferença Urbano-Rural", f"{gap:.2f}%")
            st.metric("Gap Relativo", f"{gap_perc:.1f}%")
            
            if gap > 20:
                st.error("🚨 Grande desigualdade!")
            elif gap > 10:
                st.warning("⚠️ Desigualdade moderada")
            else:
                st.success("✅ Desigualdade baixa")


def _renderizar_graficos_urbano_rural(df_urb_rural: pd.DataFrame, 
                                       stats_urb_rural: pd.DataFrame,
                                       selected_uf: str):
    """
    Renderiza gráficos comparativos.
    """
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown("#### 📊 Comparação de Médias")
        
        fig_comp_urb = go.Figure()
        
        fig_comp_urb.add_trace(go.Bar(
            x=['Urbano' if idx == 'Urbano' else 'Rural' for idx in stats_urb_rural.index],
            y=stats_urb_rural['Média'],
            marker=dict(color=['#3b82f6', '#10b981']),
            text=stats_urb_rural['Média'].apply(lambda x: f"{x:.1f}%"),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Cobertura Média: %{y:.2f}%<extra></extra>'
        ))
        
        fig_comp_urb.update_layout(
            height=350,
            yaxis_title="Cobertura Média (%)",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_comp_urb, use_container_width=True, key=f"comp_urb_{selected_uf}")
    
    with comp_col2:
        st.markdown("#### 📈 Box Plot Comparativo")
        
        fig_box_comp = go.Figure()
        
        for tipo in ['Urbano', 'Rural']:
            if tipo in df_urb_rural['Tipo_Area'].values:
                dados_tipo = df_urb_rural[df_urb_rural['Tipo_Area'] == tipo]['Cobertura_num']
                cor = '#3b82f6' if tipo == 'Urbano' else '#10b981'
                
                fig_box_comp.add_trace(go.Box(
                    y=dados_tipo,
                    name=tipo,
                    marker=dict(color=cor),
                    boxmean='sd',
                    hovertemplate='<b>%{fullData.name}</b><br>Cobertura: %{y:.2f}%<extra></extra>'
                ))
        
        fig_box_comp.update_layout(
            height=350,
            yaxis_title="Cobertura (%)",
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_box_comp, use_container_width=True, key=f"box_comp_{selected_uf}")


def _renderizar_tabela_estatisticas(stats_urb_rural: pd.DataFrame):
    """
    Renderiza tabela com estatísticas detalhadas.
    """
    st.markdown("---")
    st.markdown("#### 📋 Estatísticas Detalhadas")
    
    st.dataframe(
        stats_urb_rural.style.format({
            'Média': '{:.2f}%',
            'Mediana': '{:.2f}%',
            'Máxima': '{:.2f}%',
            'Mínima': '{:.2f}%',
            'Desvio': '{:.2f}%',
            'Total': '{:,.0f}'
        }),
        use_container_width=True
    )


def _renderizar_interpretacao():
    """
    Renderiza seção de interpretação dos resultados.
    """
    with st.expander("💡 Como interpretar esta análise", expanded=False):
        st.markdown("""
        **📊 Métricas Principais:**
        - **Cobertura Média**: Percentual médio de cobertura na área
        - **Gap Digital**: Diferença entre urbano e rural (quanto maior, mais desigual)
        - **Desvio Padrão**: Variação interna (quanto maior, mais heterogêneo)
        
        **🎯 Interpretação do Gap:**
        - **< 10%**: Situação equilibrada entre áreas
        - **10-20%**: Desigualdade moderada, requer atenção
        - **> 20%**: Desigualdade crítica, investimento urgente em área rural
        
        **📈 Box Plot:**
        - Compare as caixas: caixa mais alta = maioria com melhor cobertura
        - Compare medianas: linha central de cada caixa
        - Outliers: pontos isolados indicam exceções
        """)
