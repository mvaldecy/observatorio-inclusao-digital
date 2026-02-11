"""
Página de visualização de dados de Cobertura Móvel da ANATEL
Refatorada com componentes modulares
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Adiciona a raiz do projeto ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

# Importação robusta que funciona local e no deploy
try:
    from utils.data_loader import get_analisador_cobertura_movel
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils.data_loader import get_analisador_cobertura_movel

# Importa componentes
from components.cobertura_movel import (
    aplicar_configuracoes,
    renderizar_filtros,
    renderizar_comparativo_brasil,
    renderizar_comparativo_urbano_rural,
    renderizar_analise_municipios
)
from components.cobertura_movel.filtros import aplicar_filtros, renderizar_resumo_filtros

# =============================================================================
# CONFIGURAÇÃO INICIAL
# =============================================================================
aplicar_configuracoes()

# =============================================================================
# SIDEBAR - CONFIGURAÇÕES
# =============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    
    col1, col2 = st.columns(2)
    with col1:
        force_reload = st.button("🔄 Recarregar", use_container_width=True)
    with col2:
        if st.button("🗑️ Limpar Cache", use_container_width=True):
            with st.spinner("Limpando cache..."):
                st.cache_data.clear()
                st.cache_resource.clear()
            st.info("✓ Cache limpo! Recarregando página...")
            st.rerun()
    
    st.markdown("---")
    st.caption("💡 **Limpar Cache:** Use quando houver erros ou para atualizar o analisador")
    st.caption("🔄 **Recarregar:** Baixa novamente os dados da fonte")

# =============================================================================
# CARREGAMENTO DE DADOS
# =============================================================================
try:
    with st.spinner("⏳ Carregando dados de cobertura móvel..."):
        analisador = get_analisador_cobertura_movel(force_download=force_reload)
        df = analisador.df
    
    info = analisador.obter_info_geral()
    
    st.success(f"✅ Dados de cobertura móvel carregados com sucesso! Total de registros: {len(df):,}")
    
    # Verifica se o analisador tem a correção do bug do reset_index
    try:
        import inspect
        source = inspect.getsource(analisador.ranking_cobertura)
        if 'as_index=False' not in source:
            st.warning("⚠️ **Analisador desatualizado detectado!** Clique em 'Limpar Cache' na barra lateral para atualizar.")
    except:
        pass
    
except Exception as exc:
    st.error(f"❌ **Erro ao carregar dados**: {exc}")
    st.info("💡 Tente limpar o cache na barra lateral se o erro persistir.")
    st.stop()

# =============================================================================
# DEBUG: COLUNAS DETECTADAS
# =============================================================================
with st.expander("🔍 Debug: Colunas Detectadas", expanded=False):
    st.write(f"**Total de colunas no dataset:** {len(df.columns)}")
    st.write(f"**Coluna de município:** `{info['coluna_municipio']}`")
    st.write(f"**Coluna de UF:** `{info['coluna_uf']}`")
    st.write(f"**Colunas de cobertura:** {info['colunas_cobertura']}")
    st.write(f"**Colunas de tecnologia:** {info['colunas_tecnologia']}")
    st.write("**Todas as colunas disponíveis:**")
    st.code("\n".join(df.columns.tolist()))

# =============================================================================
# SELEÇÃO MANUAL DE COLUNAS (SE NECESSÁRIO)
# =============================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Configuração de Colunas")

# Permitir seleção manual de coluna de município se não foi detectada
if not info['coluna_municipio']:
    st.sidebar.warning("⚠️ Coluna de município não detectada automaticamente")
    col_municipio_manual = st.sidebar.selectbox(
        "Selecione a coluna de município:",
        options=[""] + list(df.columns),
        index=0,
        key="col_mun_select",
        help="Selecione manualmente a coluna que contém o nome dos municípios"
    )
    if col_municipio_manual:
        if hasattr(analisador, 'definir_coluna_municipio'):
            analisador.definir_coluna_municipio(col_municipio_manual)
        else:
            analisador.col_municipio = col_municipio_manual
        st.sidebar.success(f"✓ Usando: {col_municipio_manual}")
        info['coluna_municipio'] = col_municipio_manual

# Permitir seleção manual de coluna de UF se não foi detectada
if not info['coluna_uf']:
    st.sidebar.warning("⚠️ Coluna de UF não detectada automaticamente")
    col_uf_manual = st.sidebar.selectbox(
        "Selecione a coluna de UF:",
        options=[""] + list(df.columns),
        index=0,
        key="col_uf_select",
        help="Selecione manualmente a coluna que contém a sigla do estado"
    )
    if col_uf_manual:
        if hasattr(analisador, 'definir_coluna_uf'):
            analisador.definir_coluna_uf(col_uf_manual)
        else:
            analisador.col_uf = col_uf_manual
        st.sidebar.success(f"✓ Usando: {col_uf_manual}")
        info['coluna_uf'] = col_uf_manual
        info['ufs_disponiveis'] = sorted(df[col_uf_manual].unique().tolist())

# =============================================================================
# SELEÇÃO DE COLUNA DE COBERTURA
# =============================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Coluna de Cobertura")

col_cobertura_selecionada = None
if info['colunas_cobertura']:
    col_cobertura_selecionada = st.sidebar.selectbox(
        "Selecione a coluna de cobertura",
        options=info['colunas_cobertura'],
        index=0
    )
else:
    st.warning("⚠️ Nenhuma coluna de cobertura identificada automaticamente.")

# =============================================================================
# COMPARATIVO BRASIL, NORDESTE E PIAUÍ (NÃO FILTRADO)
# =============================================================================
st.markdown("---")
renderizar_comparativo_brasil(df, info, col_cobertura_selecionada)

# =============================================================================
# FILTROS DE DADOS
# =============================================================================
st.markdown("---")
selected_uf, selected_municipio = renderizar_filtros(df, info)

# Aplicar filtros
df_filtrado = aplicar_filtros(df, info, selected_uf, selected_municipio)

# =============================================================================
# COMPARATIVO URBANO X RURAL
# =============================================================================
renderizar_comparativo_urbano_rural(df, info, col_cobertura_selecionada, selected_uf)

# =============================================================================
# ANÁLISE DETALHADA DE MUNICÍPIOS
# =============================================================================
renderizar_analise_municipios(df, info, col_cobertura_selecionada, selected_uf)

# =============================================================================
# RESUMO DOS FILTROS APLICADOS
# =============================================================================
renderizar_resumo_filtros(df, df_filtrado, info, selected_uf, selected_municipio, col_cobertura_selecionada)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("📡 Dados de Cobertura Móvel fornecidos pela ANATEL")
