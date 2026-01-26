import pandas as pd
import sys
import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Ajuste de Caminhos
current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(current_dir, "../../"))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from anatel.cobertura_movel import AnalisadorRodovias

st.set_page_config(page_title="Cobertura em Rodovias", layout="wide")

# Funções Auxiliares
@st.cache_resource
def load_data_federais():
    """Carrega dados de rodovias federais"""
    return AnalisadorRodovias(tipo_rodovia="federais")

@st.cache_resource
def load_data_estaduais():
    """Carrega dados de rodovias estaduais"""
    return AnalisadorRodovias(tipo_rodovia="estaduais")

def format_br(val):
    """Formata número para padrão brasileiro"""
    if pd.isna(val):
        return "N/A"
    return f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Interface Principal
st.title("🛣️ Cobertura Móvel em Rodovias")

st.markdown("""
Analise a cobertura de redes móveis (3G, 4G, 5G) em rodovias federais e estaduais.
Dados baseados em monitoramento ANATEL de extensão de rodovia coberta por tecnologia e operadora.
""")

# --- ABAS: FEDERAIS vs ESTADUAIS ---
tab_federais, tab_estaduais = st.tabs(["🏛️ Rodovias Federais", "🗺️ Rodovias Estaduais"])

# ============ RODOVIAS FEDERAIS ============
with tab_federais:
    st.subheader("Rodovias Federais")
    
    analisador_fed = load_data_federais()
    
    if analisador_fed.df.empty:
        st.error("⚠️ Base de dados de rodovias federais não encontrada ou está vazia.")
    else:
        # SIDEBAR: FILTROS FEDERAIS
        with st.sidebar:
            st.markdown("### 🏛️ Filtros - Rodovias Federais")
            
            # Filtro por UF
            if 'UF' in analisador_fed.df.columns:
                ufs_fed = ["Todas as UFs"] + sorted(list(set([str(uf) for uf in analisador_fed.df['UF'].dropna().unique().tolist() if str(uf) != 'nan'])))
                uf_sel_fed = st.selectbox("UF (Federais)", ufs_fed, index=0)
                mask_fed = analisador_fed.df['UF'].astype(str) == uf_sel_fed if uf_sel_fed != "Todas as UFs" else pd.Series([True] * len(analisador_fed.df), index=analisador_fed.df.index)
            else:
                mask_fed = pd.Series([True] * len(analisador_fed.df), index=analisador_fed.df.index)
            
            # Filtro por Rodovia
            if 'Rodovia' in analisador_fed.df.columns:
                rodovias_fed = ["Todas as Rodovias"] + sorted(list(set([str(r) for r in analisador_fed.df[mask_fed]['Rodovia'].dropna().unique().tolist() if str(r) != 'nan'])))
                rodovia_sel_fed = st.selectbox("Rodovia (Federais)", rodovias_fed, index=0)
                if rodovia_sel_fed != "Todas as Rodovias":
                    mask_fed &= (analisador_fed.df['Rodovia'].astype(str) == rodovia_sel_fed)
            
            # Filtro por Tecnologia
            if 'Tecnologia' in analisador_fed.df.columns:
                tecnologias_fed = ["Todas"] + sorted(list(set([str(t) for t in analisador_fed.df[mask_fed]['Tecnologia'].dropna().unique().tolist() if str(t) != 'nan'])))
                tecnologia_sel_fed = st.selectbox("Tecnologia (Federais)", tecnologias_fed, index=0)
                if tecnologia_sel_fed != "Todas":
                    mask_fed &= (analisador_fed.df['Tecnologia'].astype(str) == tecnologia_sel_fed)
            
            # Filtro por Operadora
            if 'Operadora' in analisador_fed.df.columns:
                operadoras_fed = ["Todas"] + sorted(list(set([str(op) for op in analisador_fed.df[mask_fed]['Operadora'].dropna().unique().tolist() if str(op) != 'nan'])))
                operadora_sel_fed = st.selectbox("Operadora (Federais)", operadoras_fed, index=0)
                if operadora_sel_fed != "Todas":
                    mask_fed &= (analisador_fed.df['Operadora'].astype(str) == operadora_sel_fed)
        
        # Aplicar filtros
        df_filtrado_fed = analisador_fed.df.loc[mask_fed].copy()
        
        # Métricas principais
        if len(df_filtrado_fed) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            extensao_total = pd.to_numeric(df_filtrado_fed['Extensão (km)'], errors='coerce').sum()
            extensao_coberta = pd.to_numeric(df_filtrado_fed['Extensão coberta (km)'], errors='coerce').sum()
            cobertura_pct = (extensao_coberta / extensao_total * 100) if extensao_total > 0 else 0
            
            with col1:
                st.metric("📏 Extensão Total", f"{extensao_total:,.1f} km", "Total de rodovia")
            with col2:
                st.metric("📡 Extensão Coberta", f"{extensao_coberta:,.1f} km", "Com cobertura")
            with col3:
                st.metric("📊 Cobertura Geral", f"{cobertura_pct:.2f}%", "Percentual coberto")
            with col4:
                num_trechos = len(df_filtrado_fed)
                st.metric("🔢 Trechos", f"{num_trechos}", "Quantidade")
            
            st.divider()
            
            # Análise por Tecnologia
            if 'Tecnologia' in df_filtrado_fed.columns:
                st.subheader("Cobertura por Tecnologia")
                
                df_por_tec = df_filtrado_fed.groupby('Tecnologia').agg({
                    'Extensão (km)': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'Extensão coberta (km)': lambda x: pd.to_numeric(x, errors='coerce').sum()
                }).reset_index()
                
                df_por_tec['Cobertura (%)'] = (df_por_tec['Extensão coberta (km)'] / df_por_tec['Extensão (km)'] * 100).round(2)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.dataframe(df_por_tec, use_container_width=True)
                
                with col2:
                    fig = px.bar(df_por_tec, x='Tecnologia', y='Cobertura (%)', 
                                title='Cobertura por Tecnologia (%)',
                                color='Cobertura (%)', color_continuous_scale='RdYlGn', range_color=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
            
            # Análise por Operadora
            if 'Operadora' in df_filtrado_fed.columns:
                st.subheader("Cobertura por Operadora")
                
                df_por_op = df_filtrado_fed.groupby('Operadora').agg({
                    'Extensão (km)': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'Extensão coberta (km)': lambda x: pd.to_numeric(x, errors='coerce').sum()
                }).reset_index()
                
                df_por_op['Cobertura (%)'] = (df_por_op['Extensão coberta (km)'] / df_por_op['Extensão (km)'] * 100).round(2)
                df_por_op = df_por_op.sort_values('Cobertura (%)', ascending=False)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.dataframe(df_por_op, use_container_width=True)
                
                with col2:
                    fig = px.bar(df_por_op, x='Operadora', y='Cobertura (%)', 
                                title='Cobertura por Operadora (%)',
                                color='Cobertura (%)', color_continuous_scale='RdYlGn', range_color=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            st.subheader("📋 Detalhamento por Trecho")
            
            df_display = df_filtrado_fed.copy()
            if 'Extensão coberta (km)' in df_display.columns and 'Extensão (km)' in df_display.columns:
                df_display['Cobertura (%)'] = (
                    pd.to_numeric(df_display['Extensão coberta (km)'], errors='coerce') / 
                    pd.to_numeric(df_display['Extensão (km)'], errors='coerce') * 100
                ).round(2)
            
            # Paginação para não sobrecarregar com muitos dados
            rows_per_page = 50
            total_rows = len(df_display)
            total_pages = (total_rows + rows_per_page - 1) // rows_per_page
            
            if total_pages > 1:
                page = st.slider("Página", 1, total_pages, 1)
                start_idx = (page - 1) * rows_per_page
                end_idx = start_idx + rows_per_page
                df_pagina = df_display.iloc[start_idx:end_idx]
                st.caption(f"Mostrando {start_idx + 1} a {min(end_idx, total_rows)} de {total_rows} trechos")
            else:
                df_pagina = df_display
            
            st.dataframe(df_pagina, use_container_width=True, height=400)

# ============ RODOVIAS ESTADUAIS ============
with tab_estaduais:
    st.subheader("Rodovias Estaduais")
    
    analisador_est = load_data_estaduais()
    
    if analisador_est.df.empty:
        st.error("⚠️ Base de dados de rodovias estaduais não encontrada ou está vazia.")
    else:
        # SIDEBAR: FILTROS ESTADUAIS
        with st.sidebar:
            st.markdown("### 🗺️ Filtros - Rodovias Estaduais")
            
            # Filtro por UF
            if 'UF' in analisador_est.df.columns:
                ufs_est = ["Todas as UFs"] + sorted(list(set([str(uf) for uf in analisador_est.df['UF'].dropna().unique().tolist() if str(uf) != 'nan'])))
                uf_sel_est = st.selectbox("UF (Estaduais)", ufs_est, index=0, key="uf_est")
                mask_est = analisador_est.df['UF'].astype(str) == uf_sel_est if uf_sel_est != "Todas as UFs" else pd.Series([True] * len(analisador_est.df), index=analisador_est.df.index)
            else:
                mask_est = pd.Series([True] * len(analisador_est.df), index=analisador_est.df.index)
            
            # Filtro por Rodovia
            if 'Rodovia' in analisador_est.df.columns:
                rodovias_est = ["Todas as Rodovias"] + sorted(list(set([str(r) for r in analisador_est.df[mask_est]['Rodovia'].dropna().unique().tolist() if str(r) != 'nan'])))
                rodovia_sel_est = st.selectbox("Rodovia (Estaduais)", rodovias_est, index=0, key="rod_est")
                if rodovia_sel_est != "Todas as Rodovias":
                    mask_est &= (analisador_est.df['Rodovia'].astype(str) == rodovia_sel_est)
            
            # Filtro por Tecnologia
            if 'Tecnologia' in analisador_est.df.columns:
                tecnologias_est = ["Todas"] + sorted(list(set([str(t) for t in analisador_est.df[mask_est]['Tecnologia'].dropna().unique().tolist() if str(t) != 'nan'])))
                tecnologia_sel_est = st.selectbox("Tecnologia (Estaduais)", tecnologias_est, index=0, key="tec_est")
                if tecnologia_sel_est != "Todas":
                    mask_est &= (analisador_est.df['Tecnologia'].astype(str) == tecnologia_sel_est)
            
            # Filtro por Operadora
            if 'Operadora' in analisador_est.df.columns:
                operadoras_est = ["Todas"] + sorted(list(set([str(op) for op in analisador_est.df[mask_est]['Operadora'].dropna().unique().tolist() if str(op) != 'nan'])))
                operadora_sel_est = st.selectbox("Operadora (Estaduais)", operadoras_est, index=0, key="op_est")
                if operadora_sel_est != "Todas":
                    mask_est &= (analisador_est.df['Operadora'].astype(str) == operadora_sel_est)
        
        # Aplicar filtros
        df_filtrado_est = analisador_est.df.loc[mask_est].copy()
        
        # Métricas principais
        if len(df_filtrado_est) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            extensao_total_est = pd.to_numeric(df_filtrado_est['Extensão (km)'], errors='coerce').sum()
            extensao_coberta_est = pd.to_numeric(df_filtrado_est['Extensão coberta (km)'], errors='coerce').sum()
            cobertura_pct_est = (extensao_coberta_est / extensao_total_est * 100) if extensao_total_est > 0 else 0
            
            with col1:
                st.metric("📏 Extensão Total", f"{extensao_total_est:,.1f} km", "Total de rodovia")
            with col2:
                st.metric("📡 Extensão Coberta", f"{extensao_coberta_est:,.1f} km", "Com cobertura")
            with col3:
                st.metric("📊 Cobertura Geral", f"{cobertura_pct_est:.2f}%", "Percentual coberto")
            with col4:
                num_trechos_est = len(df_filtrado_est)
                st.metric("🔢 Trechos", f"{num_trechos_est}", "Quantidade")
            
            st.divider()
            
            # Análise por Tecnologia
            if 'Tecnologia' in df_filtrado_est.columns:
                st.subheader("Cobertura por Tecnologia")
                
                df_por_tec_est = df_filtrado_est.groupby('Tecnologia').agg({
                    'Extensão (km)': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'Extensão coberta (km)': lambda x: pd.to_numeric(x, errors='coerce').sum()
                }).reset_index()
                
                df_por_tec_est['Cobertura (%)'] = (df_por_tec_est['Extensão coberta (km)'] / df_por_tec_est['Extensão (km)'] * 100).round(2)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.dataframe(df_por_tec_est, use_container_width=True)
                
                with col2:
                    fig = px.bar(df_por_tec_est, x='Tecnologia', y='Cobertura (%)', 
                                title='Cobertura por Tecnologia (%)',
                                color='Cobertura (%)', color_continuous_scale='RdYlGn', range_color=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
            
            # Análise por Operadora
            if 'Operadora' in df_filtrado_est.columns:
                st.subheader("Cobertura por Operadora")
                
                df_por_op_est = df_filtrado_est.groupby('Operadora').agg({
                    'Extensão (km)': lambda x: pd.to_numeric(x, errors='coerce').sum(),
                    'Extensão coberta (km)': lambda x: pd.to_numeric(x, errors='coerce').sum()
                }).reset_index()
                
                df_por_op_est['Cobertura (%)'] = (df_por_op_est['Extensão coberta (km)'] / df_por_op_est['Extensão (km)'] * 100).round(2)
                df_por_op_est = df_por_op_est.sort_values('Cobertura (%)', ascending=False)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.dataframe(df_por_op_est, use_container_width=True)
                
                with col2:
                    fig = px.bar(df_por_op_est, x='Operadora', y='Cobertura (%)', 
                                title='Cobertura por Operadora (%)',
                                color='Cobertura (%)', color_continuous_scale='RdYlGn', range_color=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            st.subheader("📋 Detalhamento por Trecho")
            
            df_display_est = df_filtrado_est.copy()
            if 'Extensão coberta (km)' in df_display_est.columns and 'Extensão (km)' in df_display_est.columns:
                df_display_est['Cobertura (%)'] = (
                    pd.to_numeric(df_display_est['Extensão coberta (km)'], errors='coerce') / 
                    pd.to_numeric(df_display_est['Extensão (km)'], errors='coerce') * 100
                ).round(2)
            
            # Paginação para não sobrecarregar com muitos dados
            rows_per_page_est = 50
            total_rows_est = len(df_display_est)
            total_pages_est = (total_rows_est + rows_per_page_est - 1) // rows_per_page_est
            
            if total_pages_est > 1:
                page_est = st.slider("Página", 1, total_pages_est, 1, key="page_est")
                start_idx_est = (page_est - 1) * rows_per_page_est
                end_idx_est = start_idx_est + rows_per_page_est
                df_pagina_est = df_display_est.iloc[start_idx_est:end_idx_est]
                st.caption(f"Mostrando {start_idx_est + 1} a {min(end_idx_est, total_rows_est)} de {total_rows_est} trechos")
            else:
                df_pagina_est = df_display_est
            
            st.dataframe(df_pagina_est, use_container_width=True, height=400)
