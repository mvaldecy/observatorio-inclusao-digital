from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Adiciona a raiz do projeto ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from utils.data_loader import carregar_conectividade_escola_anatel, get_anos_disponiveis_anatel

NE_UF = {"AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"}

# Mapeamento de códigos IBGE para nomes de regiões
CODIGO_REGIAO_IBGE = {
    "1": "Norte",
    "2": "Nordeste", 
    "3": "Sudeste",
    "4": "Sul",
    "5": "Centro-Oeste"
}

# Mapeamento de códigos UF para siglas
CODIGO_UF_IBGE = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
    "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA",
    "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
    "41": "PR", "42": "SC", "43": "RS",
    "50": "MS", "51": "MT", "52": "GO", "53": "DF"
}

def _normalize(text: str) -> str:
    return "".join(ch for ch in str(text).strip().lower() if ch.isalnum() or ch.isspace())

def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    normalized = {col: _normalize(col) for col in df.columns}
    for col, norm in normalized.items():
        for cand in candidates:
            if _normalize(cand) == norm:
                return col
    for col, norm in normalized.items():
        for cand in candidates:
            if _normalize(cand) in norm:
                return col
    return None

def _safe_unique(series: pd.Series) -> list[str]:
    return sorted({str(v).strip() for v in series.dropna().unique() if str(v).strip()})

def _uf_equals(series: pd.Series, values: set[str]) -> pd.Series:
    normalized = series.astype(str).str.strip().str.upper()
    return normalized.isin({v.upper() for v in values})

# Configuração da página
st.set_page_config(page_title="Conectividade nas Escolas", layout="wide", page_icon="📡")

# Título
st.markdown("# 📡 Anatel - Conectividade nas Escolas")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    
    anos_disponiveis = get_anos_disponiveis_anatel('conectividade-escola')
    if anos_disponiveis:
        ano_selecionado = st.selectbox("📅 Ano", options=anos_disponiveis, index=0)
    else:
        st.warning("Nenhum ano disponível")
        st.stop()
    
    col1, col2 = st.columns(2)
    with col1:
        force_reload = st.button("🔄 Recarregar", use_container_width=True)
    with col2:
        if st.button("🗑️ Limpar Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache limpo!")

# Carrega dados
try:
    df = carregar_conectividade_escola_anatel(ano=ano_selecionado, force_download=force_reload)
    if df is None:
        st.error(f"Falha ao carregar dados")
        st.stop()
except Exception as exc:
    st.error(f"Erro: {exc}")
    st.stop()

# Converter códigos
for col in df.columns:
    col_lower = col.lower()
    if "regiao" in col_lower or "co_regiao" in col_lower:
        if df[col].dtype in ['int64', 'float64'] or df[col].astype(str).str.isnumeric().any():
            df[col] = df[col].astype(str).map(CODIGO_REGIAO_IBGE).fillna(df[col])
    if ("uf" in col_lower or "co_uf" in col_lower) and col_lower not in ["couf", "uf"]:
        if df[col].dtype in ['int64', 'float64'] or (df[col].astype(str).str.isnumeric().any() and df[col].astype(str).str.len().max() == 2):
            df[col] = df[col].astype(str).str.zfill(2).map(CODIGO_UF_IBGE).fillna(df[col])

# Detectar colunas
col_uf = _find_column(df, ["uf", "estado", "sigla_uf", "co_uf", "sg_uf", "sigla", "couf"])
col_regiao = _find_column(df, ["regiao", "região", "no_regiao", "nome_regiao", "co_regiao", "coregiao"])
col_localizacao = _find_column(df, ["localizacao", "localização", "loc_diferenciada", "zona", "tipo_localizacao", "tp_localizacao"])

st.markdown("---")

# ============================================================================
# FILTROS NA PARTE SUPERIOR - PAINEL PRINCIPAL
# ============================================================================

st.markdown("## 🎯 Filtros")

filtro_col1, filtro_col2, filtro_col3, filtro_col4 = st.columns(4)

# Filtro 1: Região
with filtro_col1:
    regioes = ["Total"] + _safe_unique(df[col_regiao]) if col_regiao else ["Total"]
    regiao_sel = st.selectbox("🌎 Região", options=regioes, index=0, key="regiao_filtro")

# Filtro 2: Estado
with filtro_col2:
    if col_uf:
        if regiao_sel == "Total":
            ufs = ["Total"] + _safe_unique(df[col_uf])
        else:
            regiao_mask = df[col_regiao].astype(str).str.strip() == regiao_sel
            ufs = ["Total"] + _safe_unique(df.loc[regiao_mask, col_uf])
        estado_sel = st.selectbox("🗺️ Estado", options=ufs, index=0, key="estado_filtro")
    else:
        estado_sel = "Total"

# Filtro 3: Localização
with filtro_col3:
    if col_localizacao:
        locs = ["Total"] + _safe_unique(df[col_localizacao])
        localizacao_sel = st.selectbox("🏘️ Localização", options=locs, index=0, key="localizacao_filtro")
    else:
        localizacao_sel = "Total"

# Filtro 4: Tipo de Educação
with filtro_col4:
    tipos_educacao = [
        "Total",
        "Fundamental Completo",
        "Fundamental Incompleto", 
        "Médio Completo",
        "Médio Incompleto",
        "Sem Instrução e Fundamental Incompleto",
        "Superior Completo",
        "Superior Incompleto"
    ]
    tipo_edu_sel = st.selectbox("🎓 Tipo Educação", options=tipos_educacao, index=0, key="educacao_filtro")

# Aplicar filtros
mask = pd.Series([True] * len(df), index=df.index)

if regiao_sel != "Total" and col_regiao:
    mask &= df[col_regiao].astype(str).str.strip() == regiao_sel

if estado_sel != "Total" and col_uf:
    mask &= df[col_uf].astype(str).str.strip().str.upper() == estado_sel.upper()

if localizacao_sel != "Total" and col_localizacao:
    mask &= df[col_localizacao].astype(str).str.strip() == localizacao_sel

df_filtro = df[mask].copy()

st.markdown("---")

# Resumo
st.markdown("## 📊 Dados Selecionados")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Total Escolas", f"{mask.sum():,}")
with col_m2:
    st.metric("Região", regiao_sel if regiao_sel != "Total" else "Brasil")
with col_m3:
    st.metric("Estado", estado_sel if estado_sel != "Total" else "Todos")
with col_m4:
    st.metric("Localização", localizacao_sel if localizacao_sel != "Total" else "Todas")

st.markdown("---")

# ============================================================================
# GRÁFICOS - MUITO GRANDES, UM POR LINHA
# ============================================================================

# Gráfico 1: Distribuição por Região
st.markdown("## 📊 Distribuição por Região")

if col_regiao and len(df_filtro) > 0:
    regiao_counts = df_filtro[col_regiao].value_counts().reset_index()
    regiao_counts.columns = ['Região', 'Quantidade']
    regiao_counts = regiao_counts.sort_values('Quantidade', ascending=True)
    
    fig_regiao = go.Figure(data=[go.Bar(
        y=regiao_counts['Região'],
        x=regiao_counts['Quantidade'],
        orientation='h',
        marker=dict(
            color=regiao_counts['Quantidade'],
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Qtd")
        ),
        text=[f"{v:,}" for v in regiao_counts['Quantidade']],
        textposition='auto'
    )])
    
    fig_regiao.update_layout(
        height=800,
        xaxis_title="Quantidade de Escolas",
        yaxis_title="Região",
        margin=dict(l=150, r=50, t=50, b=50),
        font=dict(size=14)
    )
    
    st.plotly_chart(fig_regiao, use_container_width=True, key="grafico_regiao_grande")
else:
    st.info("Sem dados de região")

st.markdown("---")

# Gráfico 2: Distribuição por Estado
st.markdown("## 📊 Distribuição por Estado")

if col_uf and len(df_filtro) > 0:
    estado_counts = df_filtro[col_uf].value_counts().reset_index()
    estado_counts.columns = ['Estado', 'Quantidade']
    estado_counts = estado_counts.sort_values('Quantidade', ascending=True).tail(20)
    
    fig_estado = go.Figure(data=[go.Bar(
        y=estado_counts['Estado'],
        x=estado_counts['Quantidade'],
        orientation='h',
        marker=dict(
            color=estado_counts['Quantidade'],
            colorscale='Greens',
            showscale=True,
            colorbar=dict(title="Qtd")
        ),
        text=[f"{v:,}" for v in estado_counts['Quantidade']],
        textposition='auto'
    )])
    
    fig_estado.update_layout(
        height=800,
        xaxis_title="Quantidade de Escolas",
        yaxis_title="Estado",
        margin=dict(l=100, r=50, t=50, b=50),
        font=dict(size=14)
    )
    
    st.plotly_chart(fig_estado, use_container_width=True, key="grafico_estado_grande")
else:
    st.info("Sem dados de estado")

st.markdown("---")

# Gráfico 3: Distribuição por Localização
st.markdown("## 📊 Distribuição por Localização")

if col_localizacao and len(df_filtro) > 0:
    loc_counts = df_filtro[col_localizacao].value_counts().reset_index()
    loc_counts.columns = ['Localização', 'Quantidade']
    loc_counts = loc_counts.sort_values('Quantidade', ascending=True)
    
    fig_loc = go.Figure(data=[go.Bar(
        y=loc_counts['Localização'],
        x=loc_counts['Quantidade'],
        orientation='h',
        marker=dict(
            color=['#3b82f6', '#10b981', '#f59e0b'],
            showscale=False
        ),
        text=[f"{v:,}" for v in loc_counts['Quantidade']],
        textposition='auto'
    )])
    
    fig_loc.update_layout(
        height=800,
        xaxis_title="Quantidade de Escolas",
        yaxis_title="Localização",
        margin=dict(l=150, r=50, t=50, b=50),
        font=dict(size=14)
    )
    
    st.plotly_chart(fig_loc, use_container_width=True, key="grafico_loc_grande")
else:
    st.info("Sem dados de localização")

st.markdown("---")

# Gráfico 4: Comparativo Urbano x Rural (Pie Chart)
st.markdown("## 📊 Proporção Urbano x Rural")

if col_localizacao and len(df_filtro) > 0:
    def classify_loc(val):
        v = str(val).upper()
        if 'URBAN' in v:
            return 'Urbano'
        elif 'RURAL' in v:
            return 'Rural'
        return 'Outro'
    
    df_filtro_loc = df_filtro.copy()
    df_filtro_loc['_tipo_loc'] = df_filtro_loc[col_localizacao].apply(classify_loc)
    
    loc_pie = df_filtro_loc['_tipo_loc'].value_counts().reset_index()
    loc_pie.columns = ['Tipo', 'Quantidade']
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=loc_pie['Tipo'],
        values=loc_pie['Quantidade'],
        marker=dict(colors=['#3b82f6', '#10b981', '#64748b']),
        hole=0.3,
        textinfo='label+percent+value'
    )])
    
    fig_pie.update_layout(
        height=800,
        font=dict(size=14)
    )
    
    st.plotly_chart(fig_pie, use_container_width=True, key="grafico_pie_grande")
else:
    st.info("Sem dados para gráfico de pizza")

st.markdown("---")

# Gráfico 5: Top 10 Estados
st.markdown("## 📊 Top 10 Estados com Mais Escolas")

if col_uf and len(df_filtro) > 0:
    top10 = df_filtro[col_uf].value_counts().head(10).reset_index()
    top10.columns = ['Estado', 'Quantidade']
    
    fig_top10 = go.Figure(data=[go.Bar(
        x=top10['Estado'],
        y=top10['Quantidade'],
        marker=dict(
            color=top10['Quantidade'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Qtd")
        ),
        text=[f"{v:,}" for v in top10['Quantidade']],
        textposition='outside'
    )])
    
    fig_top10.update_layout(
        height=800,
        xaxis_title="Estado",
        yaxis_title="Quantidade de Escolas",
        xaxis_tickangle=-45,
        margin=dict(l=50, r=50, t=50, b=100),
        font=dict(size=14)
    )
    
    st.plotly_chart(fig_top10, use_container_width=True, key="grafico_top10_grande")
else:
    st.info("Sem dados para top 10")

st.markdown("---")

# Tabela de Dados
st.markdown("## 📋 Dados Brutos")

if len(df_filtro) > 0:
    st.dataframe(df_filtro, use_container_width=True, height=600)
else:
    st.info("Nenhum dado para exibir")

