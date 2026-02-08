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
st.set_page_config(page_title="Dados Anatel", layout="wide", page_icon="�")

# Título da página
st.markdown("# 📡 Anatel - Conectividade nas Escolas")

# CSS customizado para dark theme
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #333;
    }
    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
    }
    .tag-blue { background-color: #1e40af; color: white; }
    .tag-green { background-color: #166534; color: white; }
    .tag-purple { background-color: #6b21a8; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar - Configurações
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    
    # Seleção de ano usando o sistema real
    anos_disponiveis = get_anos_disponiveis_anatel('conectividade-escola')
    ano_selecionado = st.selectbox(
        "📅 Ano da Pesquisa",
        options=anos_disponiveis,
        index=0 if anos_disponiveis else None
    )
    
    col1, col2 = st.columns(2)
    with col1:
        force_reload = st.button("🔄 Recarregar", use_container_width=True)
    with col2:
        if st.button("🗑️ Limpar Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache limpo!")

# Carrega dados do ano selecionado usando o sistema de cache HTTP
if not ano_selecionado:
    st.warning("⚠️ Nenhum ano disponível. Verifique a configuração.")
    st.stop()

try:
    df = carregar_conectividade_escola_anatel(ano=ano_selecionado, force_download=force_reload)
    
    if df is None:
        st.error(f"❌ Falha ao carregar dados da ANATEL para o ano {ano_selecionado}.")
        st.stop()
    
    st.success(f"✅ Dados de {ano_selecionado} carregados com sucesso! Total de registros: {len(df):,}")
    
except Exception as exc:
    st.error(f"❌ **Erro ao carregar dados**: {exc}")
    st.stop()

# Converter códigos de região/UF para nomes se necessário
for col in df.columns:
    col_lower = col.lower()
    # Se a coluna tem "regiao" ou "co_regiao" e contém códigos numéricos
    if "regiao" in col_lower or "co_regiao" in col_lower:
        if df[col].dtype in ['int64', 'float64'] or df[col].astype(str).str.isnumeric().any():
            df[col] = df[col].astype(str).map(CODIGO_REGIAO_IBGE).fillna(df[col])
    # Se a coluna tem "uf" ou "co_uf" e contém códigos numéricos
    if ("uf" in col_lower or "co_uf" in col_lower) and col_lower not in ["couf", "uf"]:
        if df[col].dtype in ['int64', 'float64'] or (df[col].astype(str).str.isnumeric().any() and df[col].astype(str).str.len().max() == 2):
            df[col] = df[col].astype(str).str.zfill(2).map(CODIGO_UF_IBGE).fillna(df[col])

# Converter códigos binários 0/1 para Não/Sim em todas as colunas
for col in df.columns:
    # Verificar se a coluna tem apenas valores 0, 1 (e possivelmente NaN)
    unique_vals = df[col].dropna().unique()
    if len(unique_vals) <= 2 and set(map(str, unique_vals)).issubset({'0', '1', '0.0', '1.0'}):
        df[col] = df[col].map({0: 'Não', 1: 'Sim', '0': 'Não', '1': 'Sim', 0.0: 'Não', 1.0: 'Sim'}).fillna(df[col])

# Detectar colunas
col_categoria = _find_column(df, ["categoria", "assunto", "tema", "topico"])
col_indicador = _find_column(df, ["indicador", "metrica", "variavel"])
col_uf = _find_column(df, ["uf", "estado", "sigla_uf", "co_uf", "sg_uf", "sigla", "couf"])
col_regiao = _find_column(df, ["regiao", "região", "no_regiao", "nome_regiao", "co_regiao", "coregiao"])
col_area = _find_column(df, ["area", "área", "localizacao", "localização"])
col_localizacao = _find_column(df, ["localizacao", "localização", "loc_diferenciada", "zona", "tipo_localizacao", "tp_localizacao"])
col_classe = _find_column(df, ["classe", "classe_social", "estrato"])
col_renda = _find_column(df, ["renda", "renda_familiar", "faixa_renda"])
col_valor = _find_column(df, ["valor", "percentual", "porcentagem", "total", "quantidade"])

# Debug: mostrar colunas detectadas
with st.expander("🔍 Debug: Colunas Detectadas", expanded=False):
    st.write(f"**Total de colunas no dataset:** {len(df.columns)}")
    st.write(f"**col_uf detectada:** `{col_uf}`")
    st.write(f"**col_regiao detectada:** `{col_regiao}`")
    st.write(f"**col_localizacao detectada:** `{col_localizacao}`")
    st.write("**Primeiras 20 colunas:**")
    st.code("\n".join(df.columns[:20].tolist()))
    if col_uf:
        st.write(f"**Valores únicos em {col_uf}:**")
        st.write(df[col_uf].unique()[:20].tolist())

# Seletor unificado de coluna para análise
all_cols = list(df.columns)
selected_col = None

st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Coluna para Análise")
selected_col = st.sidebar.selectbox(
    "Selecione a coluna para métricas e gráficos",
    ["Nenhuma"] + all_cols,
    index=0
)

if selected_col == "Nenhuma":
    selected_col = None
    col_valor = None
else:
    # Usar a coluna selecionada para ambas análises
    is_numeric = pd.api.types.is_numeric_dtype(df[selected_col])
    col_valor = selected_col if is_numeric else None
    # Sempre analisar a coluna como resposta também
    col_resposta = selected_col

# Filtros no centro da página
st.markdown("---")
st.markdown("## 🎯 Filtros de Dados")

col1, col2, col3 = st.columns(3)

with col1:
    selected_categorias = []
    if col_categoria:
        categorias = _safe_unique(df[col_categoria])
        selected_categorias = st.multiselect("📂 Categoria", categorias, default=categorias[:1] if categorias else [])
    
    selected_ufs = []
    if col_uf:
        uf_options = _safe_unique(df[col_uf])
        selected_ufs = st.multiselect("🗺️ UF", uf_options)

with col2:
    selected_indicadores = []
    if col_indicador:
        indicadores = _safe_unique(df[col_indicador])
        selected_indicadores = st.multiselect("📊 Indicador", indicadores)
    
    selected_regioes = []
    if col_regiao:
        regiao_options = _safe_unique(df[col_regiao])
        selected_regioes = st.multiselect("🌎 Região", regiao_options)

with col3:
    selected_localizacoes = []
    if col_localizacao:
        loc_options = _safe_unique(df[col_localizacao])
        selected_localizacoes = st.multiselect("🏘️ Localização (Urbano/Rural)", loc_options)
    
    st.write("")  # Espaço
    st.write("")  # Espaço
    if st.button("🗑️ Limpar Filtros", use_container_width=True):
        st.rerun()

# Aplicar filtros - Criar máscara booleana sem copiar dados
base_mask = pd.Series([True] * len(df), index=df.index)

if col_categoria and selected_categorias:
    base_mask &= df[col_categoria].astype(str).isin(selected_categorias)

if col_indicador and selected_indicadores:
    base_mask &= df[col_indicador].astype(str).isin(selected_indicadores)

if col_localizacao and selected_localizacoes:
    base_mask &= df[col_localizacao].astype(str).str.strip().str.upper().isin([loc.strip().upper() for loc in selected_localizacoes])

# Aplicar filtros de UF/Região se selecionados (isso afeta todas as visualizações)
if col_uf and selected_ufs:
    base_mask &= df[col_uf].astype(str).str.strip().str.upper().isin([u.strip().upper() for u in selected_ufs])

if col_regiao and selected_regioes:
    base_mask &= df[col_regiao].astype(str).str.strip().str.upper().isin([r.strip().upper() for r in selected_regioes])

# Criar máscaras para Brasil, Nordeste e Piauí
br_mask = base_mask

# Máscara do Nordeste
if col_uf:
    ne_mask = base_mask.copy()
    ne_mask &= _uf_equals(df[col_uf], NE_UF)
elif col_regiao:
    ne_mask = base_mask.copy()
    normalized_region = df[col_regiao].astype(str).str.strip().str.upper()
    ne_mask &= normalized_region.isin({"NORDESTE", "NE"})
else:
    # Se não há coluna UF/Região detectada, mostra dados do Brasil inteiro
    ne_mask = base_mask.copy()

# Máscara do Piauí
if col_uf:
    pi_mask = base_mask.copy()
    pi_mask &= _uf_equals(df[col_uf], {"PI", "PIAUI", "PIAUÍ"})
else:
    # Se não há coluna UF detectada, mostra dados do Brasil inteiro
    pi_mask = base_mask.copy()

# Seção de Resumo dos Filtros Aplicados
if any([selected_categorias, selected_indicadores, selected_ufs, selected_regioes, selected_localizacoes]):
    st.markdown("---")
    st.markdown("## 📊 Dados Selecionados nos Filtros")
    
    # Criar descrição dinâmica do que está sendo mostrado
    filtros_ativos = []
    if selected_regioes:
        filtros_ativos.append(f"{len(selected_regioes)} região(ões)")
    if selected_ufs:
        filtros_ativos.append(f"{len(selected_ufs)} estado(s)")
    if selected_localizacoes:
        filtros_ativos.append(f"localização {'/'.join(selected_localizacoes)}")
    if selected_categorias:
        filtros_ativos.append(f"{len(selected_categorias)} categoria(s)")
    if selected_indicadores:
        filtros_ativos.append(f"{len(selected_indicadores)} indicador(es)")
    
    descricao_filtros = " | ".join(filtros_ativos) if filtros_ativos else "Todos os dados"
    st.caption(f"🔍 **Visualizando dados de:** {descricao_filtros}")
    
    # Calcular métricas dos dados filtrados
    filtrado_total = base_mask.sum()
    total_geral = len(df)
    pct_filtrado = (filtrado_total / total_geral * 100) if total_geral > 0 else 0
    
    # Cards com métricas visuais
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric(
            label="📊 Total Selecionado",
            value=f"{filtrado_total:,} escolas",
            delta=f"{pct_filtrado:.1f}% da base total"
        )
    
    with metric_cols[1]:
        num_ufs = len(selected_ufs) if selected_ufs else (df.loc[base_mask, col_uf].nunique() if col_uf else 0)
        st.metric(
            label="🗺️ Abrangência",
            value=f"{num_ufs} {'estado' if num_ufs == 1 else 'estados'}",
            delta="UFs diferentes" if num_ufs > 0 else None
        )
    
    with metric_cols[2]:
        if col_localizacao and col_localizacao in df.columns:
            urbano_count = df.loc[base_mask, col_localizacao].astype(str).str.upper().str.contains('URBAN').sum()
            rural_count = df.loc[base_mask, col_localizacao].astype(str).str.upper().str.contains('RURAL').sum()
            if urbano_count + rural_count > 0:
                urbano_pct = (urbano_count / (urbano_count + rural_count) * 100)
                st.metric(
                    label="🏙️ Urbano",
                    value=f"{urbano_pct:.1f}%",
                    delta=f"{urbano_count:,} escolas"
                )
    
    with metric_cols[3]:
        if col_localizacao and col_localizacao in df.columns:
            if urbano_count + rural_count > 0:
                rural_pct = (rural_count / (urbano_count + rural_count) * 100)
                st.metric(
                    label="🌾 Rural",
                    value=f"{rural_pct:.1f}%",
                    delta=f"{rural_count:,} escolas"
                )
    
    st.markdown("---")
    
    # Visualizações detalhadas em abas
    tab1, tab2, tab3 = st.tabs(["📍 Distribuição Geográfica", "📊 Análise Rápida", "🏷️ Filtros Ativos"])
    
    with tab1:
        # Gráficos comparativos de regiões selecionadas
        if selected_regioes and col_regiao and col_regiao in df.columns:
            st.markdown("### 🌎 Comparativo entre Regiões Selecionadas")
            
            # Calcular totais por região selecionada
            regiao_data = []
            for regiao in selected_regioes:
                regiao_mask = base_mask & (df[col_regiao].astype(str).str.strip().str.upper() == regiao.upper())
                total = regiao_mask.sum()
                regiao_data.append({'Região': regiao, 'Total': total})
            
            if regiao_data:
                col_reg1, col_reg2 = st.columns(2)
                
                with col_reg1:
                    # Gráfico de barras comparativo
                    st.markdown("**📊 Comparativo de Escolas por Região**")
                    fig_regiao_bar = go.Figure(data=[go.Bar(
                        x=[r['Região'] for r in regiao_data],
                        y=[r['Total'] for r in regiao_data],
                        marker=dict(color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][:len(regiao_data)]),
                        text=[f"{r['Total']:,} escolas" for r in regiao_data],
                        textposition='auto'
                    )])
                    fig_regiao_bar.update_layout(
                        height=350,
                        xaxis_title="Região",
                        yaxis_title="Número de Escolas",
                        showlegend=False
                    )
                    st.plotly_chart(fig_regiao_bar, use_container_width=True, key="filter_regiao_bar")
                
                with col_reg2:
                    # Gráfico de pizza comparativo
                    st.markdown("**📊 Distribuição Percentual**")
                    fig_regiao_pie = go.Figure(data=[go.Pie(
                        labels=[r['Região'] for r in regiao_data],
                        values=[r['Total'] for r in regiao_data],
                        hole=0.4,
                        marker=dict(colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][:len(regiao_data)])
                    )])
                    fig_regiao_pie.update_layout(
                        height=350,
                        showlegend=True
                    )
                    st.plotly_chart(fig_regiao_pie, use_container_width=True, key="filter_regiao_pie")
                
                # Comparativo Urbano x Rural por região
                if col_localizacao and col_localizacao in df.columns:
                    st.markdown("---")
                    st.markdown("**🏙️🌾 Comparativo Urbano x Rural por Região**")
                    
                    regiao_loc_data = []
                    for regiao in selected_regioes:
                        regiao_mask = base_mask & (df[col_regiao].astype(str).str.strip().str.upper() == regiao.upper())
                        urbano = df.loc[regiao_mask, col_localizacao].astype(str).str.upper().str.contains('URBAN').sum()
                        rural = df.loc[regiao_mask, col_localizacao].astype(str).str.upper().str.contains('RURAL').sum()
                        regiao_loc_data.append({
                            'Região': regiao,
                            'Urbano': urbano,
                            'Rural': rural
                        })
                    
                    if regiao_loc_data:
                        fig_loc_comp = go.Figure()
                        
                        fig_loc_comp.add_trace(go.Bar(
                            name='Urbano',
                            x=[r['Região'] for r in regiao_loc_data],
                            y=[r['Urbano'] for r in regiao_loc_data],
                            marker_color='#3b82f6',
                            text=[f"{r['Urbano']:,}" for r in regiao_loc_data],
                            textposition='auto'
                        ))
                        
                        fig_loc_comp.add_trace(go.Bar(
                            name='Rural',
                            x=[r['Região'] for r in regiao_loc_data],
                            y=[r['Rural'] for r in regiao_loc_data],
                            marker_color='#10b981',
                            text=[f"{r['Rural']:,}" for r in regiao_loc_data],
                            textposition='auto'
                        ))
                        
                        fig_loc_comp.update_layout(
                            barmode='group',
                            height=350,
                            xaxis_title="Região",
                            yaxis_title="Número de Escolas",
                            showlegend=True
                        )
                        st.plotly_chart(fig_loc_comp, use_container_width=True, key="filter_regiao_loc")
            
            st.markdown("---")
        
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            # Gráfico de pizza - distribuição por UF
            if col_uf and col_uf in df.columns:
                st.markdown("**📊 Distribuição por Estado**")
                uf_dist = df.loc[base_mask, col_uf].value_counts().head(10)
                if len(uf_dist) > 0:
                    fig_uf = go.Figure(data=[go.Pie(
                        labels=uf_dist.index,
                        values=uf_dist.values,
                        hole=0.4,
                        marker=dict(colors=px.colors.qualitative.Set3)
                    )])
                    fig_uf.update_layout(
                        height=300,
                        margin=dict(l=20, r=20, t=30, b=20),
                        showlegend=True
                    )
                    st.plotly_chart(fig_uf, use_container_width=True, key="filter_uf_pie")
        
        with col_viz2:
            # Gráfico de barras - Top 10 estados
            if col_uf and col_uf in df.columns:
                st.markdown("**📊 Top 10 Estados**")
                uf_top = df.loc[base_mask, col_uf].value_counts().head(10)
                if len(uf_top) > 0:
                    fig_bar = go.Figure(data=[go.Bar(
                        x=uf_top.values,
                        y=uf_top.index,
                        orientation='h',
                        marker=dict(color='#3b82f6'),
                        text=uf_top.values,
                        textposition='auto'
                    )])
                    fig_bar.update_layout(
                        height=300,
                        margin=dict(l=20, r=20, t=30, b=20),
                        xaxis_title="Número de Escolas",
                        yaxis_title="Estado"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True, key="filter_uf_bar")
    
    with tab2:
        st.markdown("**🔍 Insights dos Dados Filtrados**")
        
        insight_cols = st.columns(2)
        
        with insight_cols[0]:
            # Comparação com a média nacional
            if filtrado_total > 0 and total_geral > 0:
                st.info(f"""
                📌 **Representatividade:**
                - Seus filtros selecionaram **{pct_filtrado:.1f}%** de todas as escolas na base
                - Total de {filtrado_total:,} escolas de {total_geral:,}
                """)
                
                # Mostrar distribuição urbano/rural se disponível
                if col_localizacao and col_localizacao in df.columns:
                    if urbano_count + rural_count > 0:
                        st.success(f"""
                        🏘️ **Localização:**
                        - Urbano: {urbano_pct:.1f}% ({urbano_count:,} escolas)
                        - Rural: {rural_pct:.1f}% ({rural_count:,} escolas)
                        """)
        
        with insight_cols[1]:
            # Identificar perguntas com mais "Sim"
            binary_cols_sample = []
            for col in df.columns:
                unique_vals = df.loc[base_mask, col].dropna().astype(str).str.strip().str.upper().unique()
                if 'SIM' in unique_vals or 'NÃO' in unique_vals:
                    binary_cols_sample.append(col)
                    if len(binary_cols_sample) >= 3:
                        break
            
            if binary_cols_sample:
                st.warning(f"""
                ✅ **Perguntas Disponíveis:**
                - Encontradas perguntas do tipo Sim/Não
                - Use os expanders abaixo para ver detalhes
                - Total de {len([c for c in df.columns if 'SIM' in str(df[c].unique()) or 'Sim' in str(df[c].unique())])} perguntas binárias
                """)
    
    with tab3:
        st.markdown("**🏷️ Filtros Aplicados**")
        
        filter_display_cols = st.columns(3)
        
        with filter_display_cols[0]:
            if selected_ufs:
                st.markdown("**🗺️ Estados Selecionados:**")
                for uf in selected_ufs:
                    st.markdown(f"✓ `{uf}`")
            
            if selected_categorias:
                st.markdown("**📂 Categorias:**")
                for cat in selected_categorias:
                    st.markdown(f"✓ `{cat}`")
        
        with filter_display_cols[1]:
            if selected_regioes:
                st.markdown("**🌎 Regiões Selecionadas:**")
                for reg in selected_regioes:
                    st.markdown(f"✓ `{reg}`")
            
            if selected_indicadores:
                st.markdown("**📊 Indicadores:**")
                for ind in selected_indicadores[:5]:
                    st.markdown(f"✓ `{ind}`")
                if len(selected_indicadores) > 5:
                    st.caption(f"... e mais {len(selected_indicadores) - 5} indicadores")
        
        with filter_display_cols[2]:
            if selected_localizacoes:
                st.markdown("**🏘️ Localização:**")
                for loc in selected_localizacoes:
                    st.markdown(f"✓ `{loc}`")

# Análise Detalhada da Coluna Selecionada
if selected_col and selected_col in df.columns:
    st.markdown("---")
    st.markdown(f"## 🔬 Análise Detalhada: **{selected_col}**")
    st.caption(f"💡 Explorando os dados da coluna '{selected_col}' com comparações regionais e insights")
    
    # Verificar tipo de coluna
    is_numeric = pd.api.types.is_numeric_dtype(df[selected_col])
    
    # Tabs para diferentes análises
    analysis_tabs = st.tabs(["📊 Visão Geral", "🌎 Comparação Regional", "🏙️ Urbano x Rural", "📈 Ranking"])
    
    with analysis_tabs[0]:
        # Visão Geral
        col_vis1, col_vis2, col_vis3, col_vis4 = st.columns(4)
        
        with col_vis1:
            total_valores = df.loc[base_mask, selected_col].notna().sum()
            st.metric("📝 Total de Respostas", f"{total_valores:,}")
        
        with col_vis2:
            valores_unicos = df.loc[base_mask, selected_col].nunique()
            st.metric("🎯 Valores Únicos", f"{valores_unicos}")
        
        with col_vis3:
            missing = df.loc[base_mask, selected_col].isna().sum()
            missing_pct = (missing / base_mask.sum() * 100) if base_mask.sum() > 0 else 0
            st.metric("❓ Dados Faltantes", f"{missing:,}", delta=f"{missing_pct:.1f}%")
        
        with col_vis4:
            if is_numeric:
                media = df.loc[base_mask, selected_col].mean()
                st.metric("📊 Média Geral", f"{media:.2f}")
            else:
                mais_comum = df.loc[base_mask, selected_col].mode()[0] if len(df.loc[base_mask, selected_col].mode()) > 0 else "N/A"
                st.metric("⭐ Mais Comum", f"{mais_comum}")
        
        st.markdown("---")
        
        # Gráfico de distribuição
        dist_col1, dist_col2 = st.columns(2)
        
        with dist_col1:
            st.markdown("**📊 Distribuição de Valores**")
            if is_numeric:
                # Histograma para numérico
                fig_hist = go.Figure(data=[go.Histogram(
                    x=df.loc[base_mask, selected_col].dropna(),
                    marker_color='#3b82f6',
                    nbinsx=30
                )])
                fig_hist.update_layout(
                    xaxis_title=selected_col,
                    yaxis_title="Frequência",
                    height=350,
                    showlegend=False
                )
                st.plotly_chart(fig_hist, use_container_width=True, key="col_hist")
            else:
                # Gráfico de barras para categórico
                value_counts = df.loc[base_mask, selected_col].value_counts().head(15)
                fig_bar_cat = go.Figure(data=[go.Bar(
                    x=value_counts.values,
                    y=value_counts.index.astype(str),
                    orientation='h',
                    marker_color='#3b82f6',
                    text=[f"{v:,}" for v in value_counts.values],
                    textposition='auto'
                )])
                fig_bar_cat.update_layout(
                    xaxis_title="Quantidade",
                    yaxis_title=selected_col,
                    height=350,
                    showlegend=False
                )
                st.plotly_chart(fig_bar_cat, use_container_width=True, key="col_bar_cat")
        
        with dist_col2:
            st.markdown("**📊 Top 10 Valores**")
            top_values = df.loc[base_mask, selected_col].value_counts().head(10)
            if len(top_values) > 0:
                fig_pie_top = go.Figure(data=[go.Pie(
                    labels=[str(l) for l in top_values.index],
                    values=top_values.values,
                    hole=0.4,
                    marker=dict(colors=px.colors.qualitative.Set3)
                )])
                fig_pie_top.update_layout(
                    height=350,
                    showlegend=True
                )
                st.plotly_chart(fig_pie_top, use_container_width=True, key="col_pie_top")
    
    with analysis_tabs[1]:
        # Comparação Regional (Brasil, Nordeste, Piauí)
        st.markdown("### 🌎 Comparativo: Brasil vs Nordeste vs Piauí")
        
        comp_col1, comp_col2, comp_col3 = st.columns(3)
        
        with comp_col1:
            st.markdown("**🇧🇷 Brasil**")
            br_data = df.loc[br_mask, selected_col].dropna()
            if len(br_data) > 0:
                if is_numeric:
                    st.metric("Média", f"{br_data.mean():.2f}")
                    st.metric("Mediana", f"{br_data.median():.2f}")
                else:
                    top_br = br_data.value_counts().head(3)
                    for idx, (val, count) in enumerate(top_br.items(), 1):
                        pct = (count / len(br_data) * 100)
                        st.write(f"{idx}º **{val}**: {count:,} ({pct:.1f}%)")
        
        with comp_col2:
            st.markdown("**🌴 Nordeste**")
            ne_data = df.loc[ne_mask, selected_col].dropna()
            if len(ne_data) > 0:
                if is_numeric:
                    st.metric("Média", f"{ne_data.mean():.2f}")
                    st.metric("Mediana", f"{ne_data.median():.2f}")
                else:
                    top_ne = ne_data.value_counts().head(3)
                    for idx, (val, count) in enumerate(top_ne.items(), 1):
                        pct = (count / len(ne_data) * 100)
                        st.write(f"{idx}º **{val}**: {count:,} ({pct:.1f}%)")
        
        with comp_col3:
            st.markdown("**🏴 Piauí**")
            pi_data = df.loc[pi_mask, selected_col].dropna()
            if len(pi_data) > 0:
                if is_numeric:
                    st.metric("Média", f"{pi_data.mean():.2f}")
                    st.metric("Mediana", f"{pi_data.median():.2f}")
                else:
                    top_pi = pi_data.value_counts().head(3)
                    for idx, (val, count) in enumerate(top_pi.items(), 1):
                        pct = (count / len(pi_data) * 100)
                        st.write(f"{idx}º **{val}**: {count:,} ({pct:.1f}%)")
        
        st.markdown("---")
        
        # Gráfico comparativo
        if is_numeric and len(br_data) > 0 and len(ne_data) > 0 and len(pi_data) > 0:
            st.markdown("**📊 Gráfico Comparativo (Box Plot)**")
            fig_box_comp = go.Figure()
            fig_box_comp.add_trace(go.Box(y=br_data, name='Brasil', marker_color='#3b82f6'))
            fig_box_comp.add_trace(go.Box(y=ne_data, name='Nordeste', marker_color='#10b981'))
            fig_box_comp.add_trace(go.Box(y=pi_data, name='Piauí', marker_color='#8b5cf6'))
            fig_box_comp.update_layout(
                yaxis_title=selected_col,
                height=400,
                showlegend=True
            )
            st.plotly_chart(fig_box_comp, use_container_width=True, key="col_box_regional")
        elif not is_numeric:
            # Para categóricos, mostrar gráfico de barras agrupadas
            st.markdown("**📊 Gráfico Comparativo**")
            all_values = df.loc[base_mask, selected_col].value_counts().head(10).index
            
            br_counts = [df.loc[br_mask & (df[selected_col] == val), selected_col].count() for val in all_values]
            ne_counts = [df.loc[ne_mask & (df[selected_col] == val), selected_col].count() for val in all_values]
            pi_counts = [df.loc[pi_mask & (df[selected_col] == val), selected_col].count() for val in all_values]
            
            fig_bar_comp = go.Figure()
            fig_bar_comp.add_trace(go.Bar(name='Brasil', x=[str(v) for v in all_values], y=br_counts, marker_color='#3b82f6'))
            fig_bar_comp.add_trace(go.Bar(name='Nordeste', x=[str(v) for v in all_values], y=ne_counts, marker_color='#10b981'))
            fig_bar_comp.add_trace(go.Bar(name='Piauí', x=[str(v) for v in all_values], y=pi_counts, marker_color='#8b5cf6'))
            fig_bar_comp.update_layout(
                barmode='group',
                xaxis_title=selected_col,
                yaxis_title="Quantidade de Escolas",
                height=400,
                showlegend=True
            )
            st.plotly_chart(fig_bar_comp, use_container_width=True, key="col_bar_regional")
    
    with analysis_tabs[2]:
        # Análise Urbano x Rural
        if col_localizacao and col_localizacao in df.columns:
            st.markdown("### 🏙️🌾 Comparativo: Urbano vs Rural")
            
            urb_rur_col1, urb_rur_col2 = st.columns(2)
            
            # Criar máscaras urbano/rural
            urbano_temp_mask = base_mask & df[col_localizacao].astype(str).str.upper().str.contains('URBAN')
            rural_temp_mask = base_mask & df[col_localizacao].astype(str).str.upper().str.contains('RURAL')
            
            urbano_col_data = df.loc[urbano_temp_mask, selected_col].dropna()
            rural_col_data = df.loc[rural_temp_mask, selected_col].dropna()
            
            with urb_rur_col1:
                st.markdown("**🏙️ Urbano**")
                if len(urbano_col_data) > 0:
                    if is_numeric:
                        st.metric("Média", f"{urbano_col_data.mean():.2f}")
                        st.metric("Mediana", f"{urbano_col_data.median():.2f}")
                        st.metric("Total", f"{len(urbano_col_data):,} escolas")
                    else:
                        top_urb = urbano_col_data.value_counts().head(5)
                        for val, count in top_urb.items():
                            pct = (count / len(urbano_col_data) * 100)
                            st.write(f"**{val}**: {count:,} ({pct:.1f}%)")
            
            with urb_rur_col2:
                st.markdown("**🌾 Rural**")
                if len(rural_col_data) > 0:
                    if is_numeric:
                        st.metric("Média", f"{rural_col_data.mean():.2f}")
                        st.metric("Mediana", f"{rural_col_data.median():.2f}")
                        st.metric("Total", f"{len(rural_col_data):,} escolas")
                    else:
                        top_rur = rural_col_data.value_counts().head(5)
                        for val, count in top_rur.items():
                            pct = (count / len(rural_col_data) * 100)
                            st.write(f"**{val}**: {count:,} ({pct:.1f}%)")
            
            # Gráfico comparativo
            if len(urbano_col_data) > 0 and len(rural_col_data) > 0:
                st.markdown("---")
                st.markdown("**📊 Visualização Comparativa**")
                
                if is_numeric:
                    fig_urb_rur = go.Figure()
                    fig_urb_rur.add_trace(go.Box(y=urbano_col_data, name='Urbano', marker_color='#3b82f6'))
                    fig_urb_rur.add_trace(go.Box(y=rural_col_data, name='Rural', marker_color='#10b981'))
                    fig_urb_rur.update_layout(
                        yaxis_title=selected_col,
                        height=350,
                        showlegend=True
                    )
                    st.plotly_chart(fig_urb_rur, use_container_width=True, key="col_urb_rur_box")
                else:
                    all_vals_ur = df.loc[base_mask, selected_col].value_counts().head(10).index
                    urb_c = [df.loc[urbano_temp_mask & (df[selected_col] == v), selected_col].count() for v in all_vals_ur]
                    rur_c = [df.loc[rural_temp_mask & (df[selected_col] == v), selected_col].count() for v in all_vals_ur]
                    
                    fig_urb_rur_bar = go.Figure()
                    fig_urb_rur_bar.add_trace(go.Bar(name='Urbano', x=[str(v) for v in all_vals_ur], y=urb_c, marker_color='#3b82f6'))
                    fig_urb_rur_bar.add_trace(go.Bar(name='Rural', x=[str(v) for v in all_vals_ur], y=rur_c, marker_color='#10b981'))
                    fig_urb_rur_bar.update_layout(
                        barmode='group',
                        xaxis_title=selected_col,
                        yaxis_title="Quantidade",
                        height=350,
                        showlegend=True
                    )
                    st.plotly_chart(fig_urb_rur_bar, use_container_width=True, key="col_urb_rur_bar")
        else:
            st.info("ℹ️ Coluna de localização não detectada. Não é possível fazer comparação Urbano x Rural.")
    
    with analysis_tabs[3]:
        # Ranking por estado
        if col_uf and col_uf in df.columns:
            st.markdown("### 🏆 Ranking por Estado")
            
            if is_numeric:
                # Para numérico: média por estado
                ranking_data = df.loc[base_mask].groupby(col_uf)[selected_col].agg(['mean', 'count']).reset_index()
                ranking_data.columns = ['Estado', 'Média', 'Quantidade']
                ranking_data = ranking_data.sort_values('Média', ascending=False).head(15)
                
                st.markdown("**📊 Top 15 Estados por Média**")
                fig_ranking = go.Figure(data=[go.Bar(
                    x=ranking_data['Média'],
                    y=ranking_data['Estado'],
                    orientation='h',
                    marker=dict(
                        color=ranking_data['Média'],
                        colorscale='Viridis',
                        showscale=True
                    ),
                    text=[f"{m:.2f}" for m in ranking_data['Média']],
                    textposition='auto'
                )])
                fig_ranking.update_layout(
                    xaxis_title=f"Média de {selected_col}",
                    yaxis_title="Estado",
                    height=500,
                    showlegend=False
                )
                st.plotly_chart(fig_ranking, use_container_width=True, key="col_ranking")
                
                # Tabela detalhada
                st.markdown("**📋 Tabela Detalhada**")
                st.dataframe(
                    ranking_data.style.format({'Média': '{:.2f}', 'Quantidade': '{:,}'}),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                # Para categórico: distribuição por estado
                st.markdown("**📊 Distribuição por Estado (Top 10)**")
                top_ufs = df.loc[base_mask, col_uf].value_counts().head(10).index
                
                state_dist_data = []
                for uf in top_ufs:
                    uf_mask = base_mask & (df[col_uf] == uf)
                    top_val = df.loc[uf_mask, selected_col].mode()[0] if len(df.loc[uf_mask, selected_col].mode()) > 0 else "N/A"
                    top_val_count = (df.loc[uf_mask, selected_col] == top_val).sum()
                    total_uf = df.loc[uf_mask, selected_col].notna().sum()
                    pct = (top_val_count / total_uf * 100) if total_uf > 0 else 0
                    
                    state_dist_data.append({
                        'Estado': uf,
                        'Valor Mais Comum': top_val,
                        'Quantidade': f"{top_val_count:,}",
                        'Percentual': f"{pct:.1f}%"
                    })
                
                st.dataframe(state_dist_data, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Coluna de UF não detectada. Não é possível gerar ranking por estado.")

# Calcular valores médios/agregados usando máscaras
def _calc_metric_from_mask(data_mask: pd.Series) -> tuple[str, str]:
    count_val = data_mask.sum()
    if count_val == 0:
        return "0", "—"
    
    count = f"{count_val:,}"
    
    if col_valor and col_valor in df.columns:
        if pd.api.types.is_numeric_dtype(df[col_valor]):
            avg = df.loc[data_mask, col_valor].mean()
            
            # Verificar se parece ser uma porcentagem
            col_name_lower = str(col_valor).lower()
            is_percentage = 'percent' in col_name_lower or 'porcentagem' in col_name_lower or '%' in col_name_lower
            
            if is_percentage or (0 <= avg <= 100):
                avg_clamped = max(0, min(avg, 100))
                return count, f"{avg_clamped:.2f}%"
            else:
                return count, f"{avg:,.2f}"
        else:
            return count, "N/A"
    return count, "—"


# Área principal
st.markdown("---")
st.markdown("## 📊 Visão Geral dos Dados")

# Métricas comparativas Brasil, Nordeste e Piauí
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🇧🇷 Brasil")
    br_total = br_mask.sum()
    st.metric("Total de Escolas", f"{br_total:,} escolas")
    if br_total > 0:
        br_pct = (br_total / len(df) * 100)
        st.caption(f"📊 Representa {br_pct:.1f}% da base total")

with col2:
    st.markdown("### 🌴 Nordeste")
    ne_total = ne_mask.sum()
    st.metric("Total de Escolas", f"{ne_total:,} escolas")
    if ne_total > 0:
        ne_pct = (ne_total / br_total * 100) if br_total > 0 else 0
        st.caption(f"📊 Representa {ne_pct:.1f}% das escolas do Brasil")

with col3:
    st.markdown("### 🏴 Piauí")
    pi_total = pi_mask.sum()
    st.metric("Total de Escolas", f"{pi_total:,} escolas")
    if pi_total > 0:
        pi_pct = (pi_total / ne_total * 100) if ne_total > 0 else 0
        st.caption(f"📊 Representa {pi_pct:.1f}% das escolas do Nordeste")

# Métricas de filtros
st.markdown("---")
num_filtros = sum([
    len(selected_categorias) > 0,
    len(selected_indicadores) > 0,
    len(selected_ufs) > 0,
    len(selected_regioes) > 0,
    len(selected_localizacoes) > 0
])

if num_filtros > 0:
    st.info(f"🎯 **{num_filtros} filtro(s) ativo(s)** - Os dados exibidos estão filtrados")

# Debug info
if br_mask.sum() == 0:
    st.error("⚠️ Nenhum registro encontrado! Os filtros aplicados não retornaram dados.")
    st.info(f"""
    **Diagnóstico:**
    - Total de registros no arquivo: {len(df):,}
    - Categorias selecionadas: {selected_categorias if selected_categorias else 'Nenhuma'}
    - Indicadores selecionados: {selected_indicadores if selected_indicadores else 'Nenhum'}
    - Áreas selecionadas: {selected_areas if selected_areas else 'Nenhuma'}
    
    **Sugestão:** Clique em "🗑️ Limpar Filtros" na barra lateral para remover os filtros.
    """)
    st.stop()

st.markdown("---")


st.markdown("---")

# Análise de Perguntas com Respostas Sim/Não
st.markdown("## ✅❌ Perguntas com Respostas Sim ou Não")

# Função para identificar colunas com respostas binárias
def _is_binary_column(series: pd.Series) -> bool:
    """Verifica se uma coluna contém respostas binárias tipo Sim/Não"""
    unique_vals = series.dropna().astype(str).str.strip().str.upper().unique()
    if len(unique_vals) == 0 or len(unique_vals) > 5:
        return False
    
    binary_keywords = {
        'SIM', 'NÃO', 'NAO', 'YES', 'NO', 
        'TRUE', 'FALSE', 'VERDADEIRO', 'FALSO',
        'S', 'N', 'Y', 'V', 'F', '1', '0'
    }
    
    return any(val in binary_keywords for val in unique_vals)

# Identificar todas as colunas binárias
binary_columns = []
for col in df.columns:
    if _is_binary_column(df[col]):
        binary_columns.append(col)

if len(binary_columns) == 0:
    st.info("📝 Nenhuma pergunta com respostas Sim/Não foi encontrada nos dados com os filtros aplicados.")
else:
    # Mostrar análise de cada pergunta binária
    for idx, col_name in enumerate(binary_columns, 1):
        with st.expander(f"📊 Pergunta {idx}: {col_name}", expanded=(idx <= 3)):
            st.markdown(f"**❓ Pergunta analisada:** {col_name}")
            st.caption("👇 Veja quantas escolas responderam SIM ou NÃO")
            
            # Análise dos dados Brasil, Nordeste e Piauí
            col1, col2, col3 = st.columns(3)
            
            # Brasil
            with col1:
                st.markdown("### 🇧🇷 Brasil")
                br_counts = df.loc[br_mask, col_name].value_counts()
                br_total = df.loc[br_mask, col_name].notna().sum()
                
                if br_total > 0:
                    for resposta, count in br_counts.items():
                        pct = (count / br_total * 100)
                        st.metric(
                            label=f"{str(resposta).strip()}",
                            value=f"{count:,}",
                            delta=f"{pct:.1f}%"
                        )
                    st.caption(f"Total: {br_total:,}")
                else:
                    st.info("Sem dados")
            
            # Nordeste
            with col2:
                st.markdown("### 🌴 Nordeste")
                ne_counts = df.loc[ne_mask, col_name].value_counts()
                ne_total = df.loc[ne_mask, col_name].notna().sum()
                
                if ne_total > 0:
                    for resposta, count in ne_counts.items():
                        pct = (count / ne_total * 100)
                        st.metric(
                            label=f"{str(resposta).strip()}",
                            value=f"{count:,}",
                            delta=f"{pct:.1f}%"
                        )
                    st.caption(f"Total: {ne_total:,}")
                else:
                    st.info("Sem dados")
            
            # Piauí
            with col3:
                st.markdown("### 🏴 Piauí")
                pi_counts = df.loc[pi_mask, col_name].value_counts()
                pi_total = df.loc[pi_mask, col_name].notna().sum()
                
                if pi_total > 0:
                    for resposta, count in pi_counts.items():
                        pct = (count / pi_total * 100)
                        st.metric(
                            label=f"{str(resposta).strip()}",
                            value=f"{count:,}",
                            delta=f"{pct:.1f}%"
                        )
                    st.caption(f"Total: {pi_total:,}")
                else:
                    st.info("Sem dados")
            
            # Gráfico comparativo
            st.markdown("---")
            st.markdown("**📊 Gráfico Comparativo**")
            
            chart_data = {
                'Resposta': [],
                'Brasil': [],
                'Nordeste': [],
                'Piauí': []
            }
            
            all_responses = df.loc[br_mask, col_name].dropna().unique()
            for resp in all_responses:
                resp_str = str(resp).strip()
                chart_data['Resposta'].append(resp_str)
                
                br_count = (br_mask & (df[col_name].astype(str).str.strip() == resp_str)).sum()
                ne_count = (ne_mask & (df[col_name].astype(str).str.strip() == resp_str)).sum()
                pi_count = (pi_mask & (df[col_name].astype(str).str.strip() == resp_str)).sum()
                
                chart_data['Brasil'].append(br_count)
                chart_data['Nordeste'].append(ne_count)
                chart_data['Piauí'].append(pi_count)
            
            chart_df = pd.DataFrame(chart_data)
            if len(chart_df) > 0:
                fig = go.Figure()
                
                fig.add_trace(go.Bar(name='Brasil', x=chart_df['Resposta'], y=chart_df['Brasil'], marker_color='#3b82f6'))
                fig.add_trace(go.Bar(name='Nordeste', x=chart_df['Resposta'], y=chart_df['Nordeste'], marker_color='#10b981'))
                fig.add_trace(go.Bar(name='Piauí', x=chart_df['Resposta'], y=chart_df['Piauí'], marker_color='#8b5cf6'))
                
                fig.update_layout(
                    barmode='group',
                    xaxis_title="Resposta",
                    yaxis_title="Número de Escolas",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True, key=f"chart_binary_{idx}_{col_name[:20]}")

    # Análise Urbano x Rural
st.markdown("---")
st.markdown("## 🏙️🌾 Análise: Urbano x Rural")
st.caption("💡 **O que é isso?** Compara dados entre escolas localizadas em áreas urbanas e rurais")

if col_localizacao:
    # Identificar valores que representam Urbano e Rural
    def _classify_location(value: str) -> str:
        """Classifica um valor como Urbano, Rural ou Outro"""
        val_normalized = str(value).strip().upper()
        
        urbano_keywords = {'URBANA', 'URBANO', 'URBAN', 'CIDADE', 'CITY'}
        rural_keywords = {'RURAL', 'CAMPO', 'COUNTRYSIDE', 'ROÇA'}
        
        if any(kw in val_normalized for kw in urbano_keywords):
            return 'Urbano'
        elif any(kw in val_normalized for kw in rural_keywords):
            return 'Rural'
        else:
            return 'Outro'
    
    # Criar coluna auxiliar classificada
    df_classified = df.copy()
    df_classified['_loc_classificada'] = df[col_localizacao].apply(_classify_location)
    
    # Contar distribuição
    loc_distribution = df_classified['_loc_classificada'].value_counts()
    
    st.markdown("### 📊 Distribuição Geral")
    col1, col2, col3 = st.columns(3)
    
    urbano_count = loc_distribution.get('Urbano', 0)
    rural_count = loc_distribution.get('Rural', 0)
    outro_count = loc_distribution.get('Outro', 0)
    total_loc = urbano_count + rural_count + outro_count
    
    with col1:
        urbano_pct = (urbano_count / total_loc * 100) if total_loc > 0 else 0
        st.metric("🏙️ Urbano", f"{urbano_count:,}", delta=f"{urbano_pct:.1f}%")
    with col2:
        rural_pct = (rural_count / total_loc * 100) if total_loc > 0 else 0
        st.metric("🌾 Rural", f"{rural_count:,}", delta=f"{rural_pct:.1f}%")
    with col3:
        outro_pct = (outro_count / total_loc * 100) if total_loc > 0 else 0
        st.metric("❓ Outros", f"{outro_count:,}", delta=f"{outro_pct:.1f}%")
    
    # Gráfico de pizza
    if total_loc > 0:
        st.markdown("### 📈 Visualização da Distribuição")
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Urbano', 'Rural', 'Outros'],
            values=[urbano_count, rural_count, outro_count],
            marker=dict(colors=['#3b82f6', '#10b981', '#64748b']),
            hole=0.4
        )])
        fig_pie.update_layout(
            title="Distribuição Urbano x Rural",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="chart_loc_pie")
    
    # Criar máscaras para urbano e rural
    urbano_mask = df_classified['_loc_classificada'] == 'Urbano'
    rural_mask = df_classified['_loc_classificada'] == 'Rural'
    
    st.markdown("---")
    st.markdown("### 📊 Tabela Resumo")
    urbano_total = urbano_mask.sum()
    rural_total = rural_mask.sum()
    total_geral = urbano_total + rural_total
    
    summary_df = pd.DataFrame({
        'Localização': ['Urbano', 'Rural'],
        'Quantidade': [urbano_total, rural_total],
        'Percentual': [
            f"{(urbano_total/total_geral*100):.1f}%" if total_geral > 0 else "0%",
            f"{(rural_total/total_geral*100):.1f}%" if total_geral > 0 else "0%"
        ]
    })
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 📊 Visualizações Comparativas")
    
    # Dois gráficos lado a lado
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**📊 Gráfico de Barras**")
        fig_regional = go.Figure()
        
        fig_regional.add_trace(go.Bar(
            name='Quantidade',
            x=['Urbano', 'Rural'],
            y=[urbano_total, rural_total],
            marker_color=['#3b82f6', '#10b981'],
            text=[f"{urbano_total:,}", f"{rural_total:,}"],
            textposition='auto'
        ))
        
        fig_regional.update_layout(
            xaxis_title="Localização",
            yaxis_title="Número de Escolas",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_regional, use_container_width=True, key="chart_regional_1")
    
    with col_chart2:
        st.markdown("**📊 Distribuição Percentual**")
        fig_pie_urb_rur = go.Figure(data=[go.Pie(
            labels=['Urbano', 'Rural'],
            values=[urbano_total, rural_total],
            marker=dict(colors=['#3b82f6', '#10b981']),
            hole=0.4,
            textinfo='label+percent',
            textposition='inside'
        )])
        fig_pie_urb_rur.update_layout(
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_pie_urb_rur, use_container_width=True, key="chart_pie_urb_rur")

    st.markdown("---")
    st.markdown("### 📊 Comparação Brasil | Nordeste | Piauí")
    
    regions_data = []
    for region_name, region_mask in [('Brasil 🇧🇷', br_mask), ('Nordeste 🌴', ne_mask), ('Piauí 🏴', pi_mask)]:
        urbano_region = (region_mask & urbano_mask).sum()
        rural_region = (region_mask & rural_mask).sum()
        regions_data.append({
            'Região': region_name,
            'Urbano': urbano_region,
            'Rural': rural_region
        })
    
    # Criar gráficos lado a lado
    col_region1, col_region2 = st.columns(2)
    
    with col_region1:
        st.markdown("**📊 Gráfico Agrupado**")
        fig_regional_grouped = go.Figure()
        
        fig_regional_grouped.add_trace(go.Bar(
            name='Urbano',
            x=[r['Região'] for r in regions_data],
            y=[r['Urbano'] for r in regions_data],
            marker_color='#3b82f6',
            text=[f"{r['Urbano']:,}" for r in regions_data],
            textposition='auto'
        ))
        
        fig_regional_grouped.add_trace(go.Bar(
            name='Rural',
            x=[r['Região'] for r in regions_data],
            y=[r['Rural'] for r in regions_data],
            marker_color='#10b981',
            text=[f"{r['Rural']:,}" for r in regions_data],
            textposition='auto'
        ))
        
        fig_regional_grouped.update_layout(
            barmode='group',
            xaxis_title="Região",
            yaxis_title="Número de Escolas",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_regional_grouped, use_container_width=True, key="chart_regional_grouped")
    
    with col_region2:
        st.markdown("**📊 Gráfico Empilhado**")
        fig_regional_stacked = go.Figure()
        
        fig_regional_stacked.add_trace(go.Bar(
            name='Urbano',
            x=[r['Região'] for r in regions_data],
            y=[r['Urbano'] for r in regions_data],
            marker_color='#3b82f6',
            text=[f"{r['Urbano']:,}" for r in regions_data],
            textposition='inside'
        ))
        
        fig_regional_stacked.add_trace(go.Bar(
            name='Rural',
            x=[r['Região'] for r in regions_data],
            y=[r['Rural'] for r in regions_data],
            marker_color='#10b981',
            text=[f"{r['Rural']:,}" for r in regions_data],
            textposition='inside'
        ))
        
        fig_regional_stacked.update_layout(
            barmode='stack',
            xaxis_title="Região",
            yaxis_title="Número de Escolas",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_regional_stacked, use_container_width=True, key="chart_regional_stacked")

# Análise cruzada com coluna selecionada
    if selected_col and selected_col in df.columns:
        st.markdown("---")
        st.markdown(f"### 🔍 Análise Cruzada: {selected_col} x Localização")
        st.caption(f"Como os valores de '{selected_col}' variam entre áreas urbanas e rurais?")
        
        # Verificar se é numérica
        if pd.api.types.is_numeric_dtype(df[selected_col]):
            # Análise numérica
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏙️ Urbano")
                urbano_data = df.loc[urbano_mask, selected_col].dropna()
                if len(urbano_data) > 0:
                    st.metric("Média", f"{urbano_data.mean():.2f}")
                    st.metric("Mediana", f"{urbano_data.median():.2f}")
                    st.metric("Total de Registros", f"{len(urbano_data):,}")
                else:
                    st.info("Sem dados")
            
            with col2:
                st.markdown("#### 🌾 Rural")
                rural_data = df.loc[rural_mask, selected_col].dropna()
                if len(rural_data) > 0:
                    st.metric("Média", f"{rural_data.mean():.2f}")
                    st.metric("Mediana", f"{rural_data.median():.2f}")
                    st.metric("Total de Registros", f"{len(rural_data):,}")
                else:
                    st.info("Sem dados")
            
            # Boxplot comparativo
            if len(urbano_data) > 0 or len(rural_data) > 0:
                st.markdown("#### 📊 Distribuição Comparativa (Boxplot)")
                
                plot_data = []
                if len(urbano_data) > 0:
                    plot_data.append(go.Box(y=urbano_data, name='Urbano', marker_color='#3b82f6'))
                if len(rural_data) > 0:
                    plot_data.append(go.Box(y=rural_data, name='Rural', marker_color='#10b981'))
                
                fig_box = go.Figure(data=plot_data)
                fig_box.update_layout(
                    yaxis_title=selected_col,
                    height=400,
                    showlegend=True
                )
                st.plotly_chart(fig_box, use_container_width=True, key="chart_boxplot_numeric")
                
                # Interpretação
                if len(urbano_data) > 0 and len(rural_data) > 0:
                    diff_mean = urbano_data.mean() - rural_data.mean()
                    diff_pct = (diff_mean / rural_data.mean() * 100) if rural_data.mean() != 0 else 0
                    
                    if abs(diff_pct) > 5:
                        if diff_mean > 0:
                            st.info(f"📊 **Observação:** Em média, áreas urbanas têm valores {abs(diff_pct):.1f}% maiores que áreas rurais para '{selected_col}'")
                        else:
                            st.info(f"📊 **Observação:** Em média, áreas rurais têm valores {abs(diff_pct):.1f}% maiores que áreas urbanas para '{selected_col}'")
                    else:
                        st.success(f"📊 **Observação:** Os valores são similares entre áreas urbanas e rurais (diferença menor que 5%)")
        
        else:
            # Análise categórica
            st.markdown("#### 📊 Distribuição de Respostas por Localização")
            
            # Criar tabela comparativa
            all_responses_loc = df[selected_col].dropna().unique()
            
            comparison_loc_data = []
            for resposta in sorted([str(r) for r in all_responses_loc]):
                urbano_count_resp = (urbano_mask & (df[selected_col].astype(str) == resposta)).sum()
                rural_count_resp = (rural_mask & (df[selected_col].astype(str) == resposta)).sum()
                
                urbano_total_resp = (urbano_mask & df[selected_col].notna()).sum()
                rural_total_resp = (rural_mask & df[selected_col].notna()).sum()
                
                urbano_pct_resp = (urbano_count_resp / urbano_total_resp * 100) if urbano_total_resp > 0 else 0
                rural_pct_resp = (rural_count_resp / rural_total_resp * 100) if rural_total_resp > 0 else 0
                
                comparison_loc_data.append({
                    'Resposta': resposta,
                    'Urbano (Qtd)': f"{urbano_count_resp:,}",
                    'Urbano (%)': f"{urbano_pct_resp:.1f}%",
                    'Rural (Qtd)': f"{rural_count_resp:,}",
                    'Rural (%)': f"{rural_pct_resp:.1f}%"
                })
            
            comparison_loc_df = pd.DataFrame(comparison_loc_data)
            st.dataframe(comparison_loc_df, use_container_width=True, hide_index=True)
            
            # Gráfico de barras agrupadas
            st.markdown("#### 📊 Visualização Comparativa")
            fig_cat = go.Figure()
            
            responses_list = [item['Resposta'] for item in comparison_loc_data]
            urbano_counts = [int(item['Urbano (Qtd)'].replace(',', '')) for item in comparison_loc_data]
            rural_counts = [int(item['Rural (Qtd)'].replace(',', '')) for item in comparison_loc_data]
            
            fig_cat.add_trace(go.Bar(
                name='Urbano',
                x=responses_list,
                y=urbano_counts,
                marker_color='#3b82f6'
            ))
            
            fig_cat.add_trace(go.Bar(
                name='Rural',
                x=responses_list,
                y=rural_counts,
                marker_color='#10b981'
            ))
            
            fig_cat.update_layout(
                barmode='group',
                xaxis_title=selected_col,
                yaxis_title="Número de Escolas",
                height=450,
                showlegend=True
            )
            
            st.plotly_chart(fig_cat, use_container_width=True, key="chart_cat_bars")
    
    # Análise por Estado do Nordeste (Urbano x Rural)
    if col_uf:
        st.markdown("---")
        st.markdown("### 🌴 Análise por Estado do Nordeste: Urbano x Rural")
        st.caption("Distribuição urbano/rural em cada estado nordestino")
        
        ne_states_loc = []
        for uf in sorted(NE_UF):
            uf_mask = base_mask & _uf_equals(df[col_uf], {uf})
            if uf_mask.sum() > 0:
                urbano_uf = (uf_mask & urbano_mask).sum()
                rural_uf = (uf_mask & rural_mask).sum()
                total_uf = uf_mask.sum()
                
                if total_uf > 0:
                    urbano_pct_uf = (urbano_uf / total_uf * 100)
                    rural_pct_uf = (rural_uf / total_uf * 100)
                    
                    ne_states_loc.append({
                        'Estado': uf,
                        'Urbano': urbano_uf,
                        'Urbano %': f"{urbano_pct_uf:.1f}%",
                        'Rural': rural_uf,
                        'Rural %': f"{rural_pct_uf:.1f}%",
                        'Total': total_uf
                    })
        
        if ne_states_loc:
            ne_states_df = pd.DataFrame(ne_states_loc)
            st.dataframe(ne_states_df, use_container_width=True, hide_index=True)
            
            # Dois gráficos lado a lado
            col_ne1, col_ne2 = st.columns(2)
            
            with col_ne1:
                st.markdown("**📊 Gráfico Agrupado por Estado**")
                fig_grouped_ne = go.Figure()
                
                fig_grouped_ne.add_trace(go.Bar(
                    name='Urbano',
                    x=[s['Estado'] for s in ne_states_loc],
                    y=[s['Urbano'] for s in ne_states_loc],
                    marker_color='#3b82f6',
                    text=[f"{s['Urbano']:,}" for s in ne_states_loc],
                    textposition='auto'
                ))
                
                fig_grouped_ne.add_trace(go.Bar(
                    name='Rural',
                    x=[s['Estado'] for s in ne_states_loc],
                    y=[s['Rural'] for s in ne_states_loc],
                    marker_color='#10b981',
                    text=[f"{s['Rural']:,}" for s in ne_states_loc],
                    textposition='auto'
                ))
                
                fig_grouped_ne.update_layout(
                    barmode='group',
                    xaxis_title="Estado",
                    yaxis_title="Número de Escolas",
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig_grouped_ne, use_container_width=True, key="chart_grouped_ne")
            
            with col_ne2:
                st.markdown("**📊 Gráfico Empilhado por Estado**")
                fig_stacked = go.Figure()
                
                fig_stacked.add_trace(go.Bar(
                    name='Urbano',
                    x=[s['Estado'] for s in ne_states_loc],
                    y=[s['Urbano'] for s in ne_states_loc],
                    marker_color='#3b82f6',
                    text=[f"{s['Urbano']:,}" for s in ne_states_loc],
                    textposition='inside'
                ))
                
                fig_stacked.add_trace(go.Bar(
                    name='Rural',
                    x=[s['Estado'] for s in ne_states_loc],
                    y=[s['Rural'] for s in ne_states_loc],
                    marker_color='#10b981',
                    text=[f"{s['Rural']:,}" for s in ne_states_loc],
                    textposition='inside'
                ))
                
                fig_stacked.update_layout(
                    barmode='stack',
                    xaxis_title="Estado",
                    yaxis_title="Número de Escolas",
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig_stacked, use_container_width=True, key="chart_stacked_advanced")
            
            # Destacar estado com maior proporção rural
            max_rural_pct = 0
            max_rural_state = None
            for state in ne_states_loc:
                rural_pct = float(state['Rural %'].replace('%', ''))
                if rural_pct > max_rural_pct:
                    max_rural_pct = rural_pct
                    max_rural_state = state['Estado']
            
            if max_rural_state:
                st.success(f"🌾 **Estado mais rural:** {max_rural_state} com {max_rural_pct:.1f}% de escolas em área rural")
        else:
            st.info("Sem dados disponíveis para análise por estado")

else:
    st.info("📝 Coluna de localização (Urbano/Rural) não foi detectada automaticamente nos dados.")
    st.caption("💡 **Dica:** Para ver esta análise, certifique-se de que há uma coluna chamada 'localizacao', 'localização', 'loc_diferenciada' ou 'zona' nos dados.")

    # Análise por Estado do Nordeste
    if col_uf:
        st.markdown("---")
        st.markdown("### 🌴 Análise Detalhada: Estados do Nordeste")
        st.caption("💡 Comparação entre todos os estados do Nordeste para cada pergunta")
        
        # Criar máscara para cada estado do Nordeste
        ne_states = {}
        for uf in NE_UF:
            uf_mask = base_mask & _uf_equals(df[col_uf], {uf})
            if uf_mask.sum() > 0:
                ne_states[uf] = uf_mask
        
        if len(ne_states) > 0:
            for idx, col_name in enumerate(binary_columns, 1):
                with st.expander(f"📊 {col_name} - Comparação por Estado", expanded=(idx == 1)):
                    st.markdown(f"**Pergunta:** {col_name}")
                    
                    # Criar tabela comparativa por estado
                    state_comparison = []
                    
                    for state_code, state_mask in sorted(ne_states.items()):
                        state_counts = df.loc[state_mask, col_name].value_counts()
                        state_total = df.loc[state_mask, col_name].notna().sum()
                        
                        if state_total > 0:
                            # Contar Sim e Não
                            sim_count = 0
                            nao_count = 0
                            
                            for resp, count in state_counts.items():
                                resp_upper = str(resp).strip().upper()
                                if resp_upper in {'SIM', 'YES', 'Y', 'S', 'TRUE', 'VERDADEIRO', '1'}:
                                    sim_count += count
                                elif resp_upper in {'NÃO', 'NAO', 'NO', 'N', 'FALSE', 'FALSO', '0'}:
                                    nao_count += count
                            
                            sim_pct = (sim_count / state_total * 100) if state_total > 0 else 0
                            nao_pct = (nao_count / state_total * 100) if state_total > 0 else 0
                            
                            state_comparison.append({
                                "Estado": state_code,
                                "Total Escolas": f"{state_total:,}",
                                "SIM": f"{sim_count:,} ({sim_pct:.1f}%)",
                                "NÃO": f"{nao_count:,} ({nao_pct:.1f}%)",
                                "% SIM": sim_pct
                            })
                    
                    if state_comparison:
                        # Ordenar por % de SIM (decrescente)
                        state_comparison.sort(key=lambda x: x["% SIM"], reverse=True)
                        
                        # Remover coluna % SIM (era só para ordenação)
                        for item in state_comparison:
                            del item["% SIM"]
                        
                        comp_df = pd.DataFrame(state_comparison)
                        st.dataframe(comp_df, use_container_width=True, hide_index=True)
                        
                        # Calcular média do Nordeste


