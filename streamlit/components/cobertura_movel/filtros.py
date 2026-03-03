"""
Componente de filtros para a página de Cobertura Móvel
"""
import streamlit as st
import pandas as pd
from .utils import safe_unique


def renderizar_filtros(df: pd.DataFrame, info: dict) -> tuple[str | None, str | None]:
    """
    Renderiza os filtros de UF e município.
    
    Args:
        df: DataFrame com os dados
        info: Dicionário com informações do analisador (colunas, etc)
    
    Returns:
        Tupla (selected_uf, selected_municipio)
    """
    st.markdown("## 🎯 Filtros de Dados")
    st.caption("💡 **Atenção:** Estes filtros afetam apenas as análises detalhadas abaixo, não o comparativo acima.")
    
    col1, col2, col3 = st.columns(3)
    
    selected_uf = None
    selected_municipio = None
    
    with col1:
        if info['coluna_uf']:
            uf_options = ["Selecione um estado..."] + info['ufs_disponiveis']
            selected_uf_display = st.selectbox("🗺️ Selecione UF", uf_options)
            if selected_uf_display != "Selecione um estado...":
                selected_uf = selected_uf_display
    
    with col2:
        # Filtro de município - apenas do UF selecionado
        if info['coluna_municipio'] and selected_uf and info['coluna_uf']:
            # Filtra municípios apenas do UF selecionado
            df_uf = df[df[info['coluna_uf']] == selected_uf]
            municipios_uf = safe_unique(df_uf[info['coluna_municipio']])
            
            if len(municipios_uf) > 0:
                selected_municipio = st.selectbox(
                    f"🏙️ Município de {selected_uf}",
                    ["Todos os municípios"] + municipios_uf,
                    index=0
                )
                if selected_municipio == "Todos os municípios":
                    selected_municipio = None
        elif info['coluna_municipio'] and not selected_uf:
            st.info("👈 Selecione um UF primeiro")
    
    with col3:
        st.write("")
        st.write("")
        if st.button("🗑️ Limpar Filtros", use_container_width=True):
            st.rerun()
    
    return selected_uf, selected_municipio


def aplicar_filtros(df: pd.DataFrame, info: dict, selected_uf: str | None, 
                    selected_municipio: str | None) -> pd.DataFrame:
    """
    Aplica os filtros selecionados ao DataFrame.
    
    Args:
        df: DataFrame original
        info: Informações do analisador
        selected_uf: UF selecionada (ou None)
        selected_municipio: Município selecionado (ou None)
    
    Returns:
        DataFrame filtrado
    """
    df_filtrado = df.copy()
    
    if info['coluna_uf'] and selected_uf:
        df_filtrado = df_filtrado[df_filtrado[info['coluna_uf']] == selected_uf]
    
    if selected_municipio and info['coluna_municipio']:
        df_filtrado = df_filtrado[df_filtrado[info['coluna_municipio']].str.contains(
            selected_municipio, case=False, na=False
        )]
    
    return df_filtrado


def renderizar_resumo_filtros(df: pd.DataFrame, df_filtrado: pd.DataFrame, 
                              info: dict, selected_uf: str | None, 
                              selected_municipio: str | None, 
                              col_cobertura_selecionada: str | None):
    """
    Renderiza um resumo dos filtros aplicados e métricas dos dados filtrados.
    
    Args:
        df: DataFrame original (sem filtros)
        df_filtrado: DataFrame com filtros aplicados
        info: Informações do analisador
        selected_uf: UF selecionada
        selected_municipio: Município selecionado
        col_cobertura_selecionada: Coluna de cobertura em uso
    """
    if not selected_municipio:
        return
    
    st.markdown("---")
    st.markdown("#### 📊 Resumo dos Filtros Aplicados")
    
    # Descrição dos filtros
    st.info(f"🔍 **UF:** {selected_uf} | **Município:** {selected_municipio}")
    
    # Métricas dos dados filtrados
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        total_filtrado = len(df_filtrado)
        pct_filtrado = (total_filtrado / len(df) * 100) if len(df) > 0 else 0
        st.metric(
            label="📊 Registros Filtrados",
            value=f"{total_filtrado:,}",
            delta=f"{pct_filtrado:.1f}% do total"
        )
    
    with metric_cols[1]:
        if info['coluna_municipio']:
            num_municipios = df_filtrado[info['coluna_municipio']].nunique()
            st.metric(
                label="🏙️ Municípios",
                value=f"{num_municipios:,}"
            )
    
    with metric_cols[2]:
        if col_cobertura_selecionada and col_cobertura_selecionada in df_filtrado.columns:
            # Calcula cobertura média
            df_cob = df_filtrado[col_cobertura_selecionada].copy()
            if df_cob.dtype == 'object':
                df_cob = pd.to_numeric(
                    df_cob.astype(str).str.replace('%', '').str.replace(',', '.'),
                    errors='coerce'
                )
            media_cob = df_cob.mean()
            st.metric(
                label="📡 Cobertura Média",
                value=f"{media_cob:.2f}%"
            )
    
    with metric_cols[3]:
        if info['coluna_uf']:
            num_ufs = df_filtrado[info['coluna_uf']].nunique()
            st.metric(
                label="🗺️ Estados",
                value=f"{num_ufs}"
            )
