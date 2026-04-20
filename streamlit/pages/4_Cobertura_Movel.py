"""
Página de visualização de dados de Cobertura Móvel da ANATEL
Segue o mesmo padrão da página de Dados ANATEL
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
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

# Importação robusta que funciona local e no deploy
try:
    from utils.data_loader import get_analisador_cobertura_movel
except ImportError:
    # Fallback para quando rodando do diretório raiz (deploy)
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils.data_loader import get_analisador_cobertura_movel

# Configuração da página
st.set_page_config(page_title="Cobertura Móvel - ANATEL", layout="wide", page_icon="📡")

# Libera memória de outros datasets ao abrir esta página
from utils.memory_manager import set_active_dataset
from components.theme import apply_global_styles
set_active_dataset("anatel_cobertura_movel")
apply_global_styles()

# Título da página
st.markdown("# 📡 Anatel - Cobertura Móvel")
st.markdown("---")

# Funções auxiliares (mesmo padrão)
def _safe_unique(series: pd.Series) -> list[str]:
    return sorted({str(v).strip() for v in series.dropna().unique() if str(v).strip()})

# Sidebar - Configurações
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

# Carrega dados usando o analisador
try:
    with st.spinner("⏳ Carregando dados de cobertura móvel..."):
        analisador = get_analisador_cobertura_movel(force_download=force_reload)
        df = analisador.df
    
    info = analisador.obter_info_geral()
    
    st.success(f"✅ Dados de cobertura móvel carregados com sucesso! Total de registros: {len(df):,}")
    
    # Verifica se o analisador tem a correção do bug do reset_index
    # Se tiver o bug, avisa para limpar o cache
    try:
        # Testa se o método ranking_cobertura está funcionando corretamente
        # fazendo uma chamada de teste rápida
        import inspect
        source = inspect.getsource(analisador.ranking_cobertura)
        if 'as_index=False' not in source:
            st.warning("⚠️ **Analisador desatualizado detectado!** Clique em 'Limpar Cache' na barra lateral para atualizar.")
    except:
        pass  # Se não conseguir verificar, continua normalmente
    
except Exception as exc:
    st.error(f"❌ **Erro ao carregar dados**: {exc}")
    st.info("💡 Tente limpar o cache na barra lateral se o erro persistir.")
    st.stop()

# Debug: mostrar colunas detectadas
with st.expander("🔍 Debug: Colunas Detectadas", expanded=False):
    st.write(f"**Total de colunas no dataset:** {len(df.columns)}")
    st.write(f"**Coluna de município:** `{info['coluna_municipio']}`")
    st.write(f"**Coluna de UF:** `{info['coluna_uf']}`")
    st.write(f"**Colunas de cobertura:** {info['colunas_cobertura']}")
    st.write(f"**Colunas de tecnologia:** {info['colunas_tecnologia']}")
    st.write("**Todas as colunas disponíveis:**")
    st.code("\n".join(df.columns.tolist()))

# Seletor de coluna para análise
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
        # Tenta definir usando o método se disponível, senão define diretamente
        if hasattr(analisador, 'definir_coluna_municipio'):
            analisador.definir_coluna_municipio(col_municipio_manual)
        else:
            analisador.col_municipio = col_municipio_manual
        st.sidebar.success(f"✓ Usando: {col_municipio_manual}")
        # Atualiza info sem chamar obter_info_geral para evitar problemas
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
        # Tenta definir usando o método se disponível, senão define diretamente
        if hasattr(analisador, 'definir_coluna_uf'):
            analisador.definir_coluna_uf(col_uf_manual)
        else:
            analisador.col_uf = col_uf_manual
        st.sidebar.success(f"✓ Usando: {col_uf_manual}")
        # Atualiza info
        info['coluna_uf'] = col_uf_manual
        info['ufs_disponiveis'] = sorted(df[col_uf_manual].unique().tolist())

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

# ============================================================
# COMPARATIVO BRASIL, NORDESTE E PIAUÍ (FIXO - NÃO FILTRADO)
# ============================================================
st.markdown("---")
st.markdown("## 📊 Comparativo Brasil, Nordeste e Piauí")

if not col_cobertura_selecionada:
    st.info("⚠️ Selecione uma coluna de cobertura na barra lateral para ver as análises.")
    st.stop()

# Processa dados para comparativo
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
    stats_brasil = {
        'Região': 'Brasil',
        'Média': df_comp['Cobertura_num'].mean(),
        'Mediana': df_comp['Cobertura_num'].median(),
        'Máxima': df_comp['Cobertura_num'].max(),
        'Mínima': df_comp['Cobertura_num'].min(),
        'Total': len(df_comp)
    }
    
    # Nordeste
    NE_UF = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    if col_uf_info and col_uf_info in df_comp.columns:
        df_ne = df_comp[df_comp[col_uf_info].isin(NE_UF)]
        stats_nordeste = {
            'Região': 'Nordeste',
            'Média': df_ne['Cobertura_num'].mean(),
            'Mediana': df_ne['Cobertura_num'].median(),
            'Máxima': df_ne['Cobertura_num'].max(),
            'Mínima': df_ne['Cobertura_num'].min(),
            'Total': len(df_ne)
        }
        
        # Piauí
        df_pi = df_comp[df_comp[col_uf_info] == 'PI']
        stats_piaui = {
            'Região': 'Piauí',
            'Média': df_pi['Cobertura_num'].mean(),
            'Mediana': df_pi['Cobertura_num'].median(),
            'Máxima': df_pi['Cobertura_num'].max(),
            'Mínima': df_pi['Cobertura_num'].min(),
            'Total': len(df_pi)
        }
    else:
        stats_nordeste = stats_brasil.copy()
        stats_nordeste['Região'] = 'Nordeste (N/D)'
        stats_piaui = stats_brasil.copy()
        stats_piaui['Região'] = 'Piauí (N/D)'
    
    # Layout do comparativo
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
    
    # Gráfico comparativo
    st.markdown("---")
    
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
    
    st.plotly_chart(fig_comp, use_container_width=True, key="comp_brasil_ne_pi")
    
except Exception as e:
    st.error(f"Erro ao processar comparativo: {str(e)}")

# ============================================================
# FILTROS DE DADOS (ABAIXO DO COMPARATIVO)
# ============================================================
st.markdown("---")
st.markdown("## 🎯 Filtros de Dados")
st.caption("💡 **Atenção:** Estes filtros afetam apenas as análises detalhadas abaixo, não o comparativo acima.")

col1, col2, col3 = st.columns(3)

with col1:
    selected_uf = None
    if info['coluna_uf']:
        uf_options = ["Selecione um estado..."] + info['ufs_disponiveis']
        selected_uf_display = st.selectbox("🗺️ Selecione UF", uf_options)
        if selected_uf_display != "Selecione um estado...":
            selected_uf = selected_uf_display

with col2:
    # Filtro de município - apenas do UF selecionado
    selected_municipio = None
    if info['coluna_municipio'] and selected_uf and info['coluna_uf']:
        # Filtra municípios apenas do UF selecionado
        df_uf = df[df[info['coluna_uf']] == selected_uf]
        municipios_uf = _safe_unique(df_uf[info['coluna_municipio']])
        
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

# Aplicar filtros
df_filtrado = df.copy()

if info['coluna_uf'] and selected_uf:
    df_filtrado = df_filtrado[df_filtrado[info['coluna_uf']] == selected_uf]

if selected_municipio and info['coluna_municipio']:
    df_filtrado = df_filtrado[df_filtrado[info['coluna_municipio']].str.contains(selected_municipio, case=False, na=False)]

# ============================================================
# COMPARATIVO URBANO X RURAL (SE DISPONÍVEL)
# ============================================================

# Verifica se há coluna de localização (urbano/rural)
col_localizacao = None
termos_busca = ['LOCALIZA', 'AREA', 'URBANO', 'RURAL', 'TIPO', 'ZONA', 'REGIÃO', 'REGIAO']
for col in df.columns:
    col_upper = str(col).upper()
    if any(term in col_upper for term in termos_busca):
        col_localizacao = col
        break

# Debug: Mostra colunas disponíveis se não encontrou localização
if not col_localizacao and selected_uf:
    with st.expander("🔍 Debug - Colunas disponíveis no dataset", expanded=False):
        st.write("**Buscando colunas de localização (urbano/rural)...**")
        st.write(f"Termos de busca: {', '.join(termos_busca)}")
        st.write(f"\n**Todas as colunas disponíveis ({len(df.columns)}):**")
        st.code("\n".join(df.columns.tolist()))
        st.info("💡 Se houver uma coluna de localização com nome diferente, podemos ajustar o código para detectá-la.")

if col_localizacao and selected_uf:
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
        
        # Identifica áreas urbanas e rurais
        # Tenta diferentes padrões de nomenclatura
        df_urb_rural['Tipo_Area'] = df_urb_rural[col_localizacao].astype(str).str.upper()
        
        # Padroniza nomes
        df_urb_rural['Tipo_Area'] = df_urb_rural['Tipo_Area'].replace({
            'URBANA': 'Urbano',
            'URBAN': 'Urbano',
            'U': 'Urbano',
            'RURAL': 'Rural',
            'R': 'Rural'
        })
        
        # Filtra apenas Urbano e Rural
        df_urb_rural = df_urb_rural[df_urb_rural['Tipo_Area'].isin(['Urbano', 'Rural'])]
        
        if len(df_urb_rural) > 0:
            # Calcula estatísticas por tipo de área
            stats_urb_rural = df_urb_rural.groupby('Tipo_Area')['Cobertura_num'].agg([
                ('Média', 'mean'),
                ('Mediana', 'median'),
                ('Máxima', 'max'),
                ('Mínima', 'min'),
                ('Desvio', 'std'),
                ('Total', 'count')
            ]).round(2)
            
            # Métricas comparativas
            urb_col1, urb_col2, urb_col3 = st.columns(3)
            
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
                    if 'Urbano' in stats_urb_rural.index:
                        delta = rural_stats['Média'] - urbano_stats['Média']
                        st.metric("Cobertura Média", f"{rural_stats['Média']:.2f}%", 
                                 delta=f"{delta:+.2f}% vs Urbano")
                    else:
                        st.metric("Cobertura Média", f"{rural_stats['Média']:.2f}%")
                    st.metric("Mediana", f"{rural_stats['Mediana']:.2f}%")
                    st.metric("Registros", f"{int(rural_stats['Total']):,}")
            
            with urb_col3:
                st.markdown("### 📊 Gap Digital")
                if 'Urbano' in stats_urb_rural.index and 'Rural' in stats_urb_rural.index:
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
            
            # Gráficos comparativos
            st.markdown("---")
            
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
            
            # Tabela comparativa detalhada
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
            
            # Interpretação
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
        else:
            st.info(f"ℹ️ Não foram encontrados dados de localização urbano/rural para {selected_uf}")
            st.caption("Os dados podem não conter informação sobre área urbana/rural ou estão em formato não reconhecido.")
    
    except Exception as e:
        st.warning(f"⚠️ Não foi possível processar comparativo urbano/rural: {str(e)}")
        with st.expander("Ver detalhes do erro"):
            st.exception(e)
elif not col_localizacao and selected_uf:
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

# ============================================================
# VISUALIZAÇÃO DOS MUNICÍPIOS DO UF SELECIONADO
# ============================================================
if selected_uf and info['coluna_municipio']:
    st.markdown("---")
    st.markdown(f"## 📊 Municípios do Estado: {selected_uf}")
    st.caption(f"🎯 Mostrando dados de cobertura móvel de todos os municípios de **{selected_uf}**")
    
    try:
        # Prepara dados dos municípios APENAS DO UF SELECIONADO
        col_mun = info['coluna_municipio']
        col_uf = info['coluna_uf']
        
        # FILTRO CRUCIAL: Pega apenas registros do UF selecionado
        df_uf_analysis = df[df[col_uf] == selected_uf].copy()
        
        if len(df_uf_analysis) == 0:
            st.warning(f"⚠️ Nenhum dado encontrado para o estado {selected_uf}")
            st.stop()
        
        # Converte cobertura para numérico
        if df_uf_analysis[col_cobertura_selecionada].dtype == 'object':
            df_uf_analysis['Cobertura'] = pd.to_numeric(
                df_uf_analysis[col_cobertura_selecionada].astype(str).str.replace('%', '').str.replace(',', '.'),
                errors='coerce'
            )
        else:
            df_uf_analysis['Cobertura'] = df_uf_analysis[col_cobertura_selecionada]
        
        df_uf_analysis = df_uf_analysis.dropna(subset=['Cobertura'])
        
        # DEBUG: Mostra amostra dos dados com nomes dos municípios
        st.info(f"🔍 Coluna de município: **{col_mun}** | Registros encontrados: **{len(df_uf_analysis)}**")
        with st.expander("🔧 Debug - Ver dados brutos", expanded=False):
            st.write(f"Primeiros 20 registros de {selected_uf}:")
            # Seleciona colunas sem duplicação
            cols_to_show = [col_mun, 'Cobertura']
            if col_uf not in cols_to_show:
                cols_to_show.insert(1, col_uf)
            st.dataframe(df_uf_analysis[cols_to_show].head(20))
            st.write(f"\nMunicípios únicos encontrados: **{df_uf_analysis[col_mun].nunique()}**")
            st.write("Lista dos primeiros 30 municípios:")
            st.write(sorted(df_uf_analysis[col_mun].unique())[:30])
        
        # Agrupa por município do UF selecionado
        df_mun_ranking = df_uf_analysis.groupby(col_mun, as_index=False)['Cobertura'].mean()
        df_mun_ranking = df_mun_ranking.sort_values('Cobertura', ascending=False)
        
        # DEBUG: Mostra ranking antes do rename
        with st.expander("🔧 Debug - Ranking calculado", expanded=False):
            st.write("Primeiros 10 municípios no ranking:")
            st.dataframe(df_mun_ranking.head(10))
        
        # Renomeia coluna de município para 'Município' se necessário
        if col_mun != 'Município':
            df_mun_ranking = df_mun_ranking.rename(columns={col_mun: 'Município'})
        
        df_mun_ranking['Posição'] = range(1, len(df_mun_ranking) + 1)
        df_mun_ranking['UF'] = selected_uf  # Adiciona coluna UF para clareza
        
        # Estatísticas gerais
        st.info(f"ℹ️ Analisando **{len(df_mun_ranking)} municípios** do estado de **{selected_uf}**")
        
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.metric("Total de Municípios", f"{len(df_mun_ranking):,}")
        
        with stats_col2:
            st.metric("Cobertura Média", f"{df_mun_ranking['Cobertura'].mean():.2f}%")
        
        with stats_col3:
            st.metric("Melhor Cobertura", f"{df_mun_ranking['Cobertura'].max():.2f}%")
        
        with stats_col4:
            st.metric("Pior Cobertura", f"{df_mun_ranking['Cobertura'].min():.2f}%")
        
        st.markdown("---")
        
        # ============================================================
        # ANÁLISE ESTATÍSTICA E DISTRIBUIÇÃO
        # ============================================================
        st.markdown(f"### 📊 Análise Estatística de {selected_uf}")
        st.caption("Entenda como a cobertura está distribuída entre os municípios")
        
        # Cria duas colunas para estatísticas e distribuição
        stat_col1, stat_col2 = st.columns(2)
        
        with stat_col1:
            st.markdown("#### 📈 Estatísticas Descritivas")
            
            # Calcula estatísticas
            media = df_mun_ranking['Cobertura'].mean()
            mediana = df_mun_ranking['Cobertura'].median()
            desvio = df_mun_ranking['Cobertura'].std()
            
            # Explica as estatísticas de forma clara
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
        
        with stat_col2:
            st.markdown("#### 🎚️ Distribuição por Faixas")
            st.caption("Quantidade de municípios em cada nível de cobertura")
            
            # Calcula distribuição
            distribuicao_dict = {
                'Sem cobertura (0%)': len(df_mun_ranking[df_mun_ranking['Cobertura'] == 0]),
                'Muito Baixa (0-25%)': len(df_mun_ranking[(df_mun_ranking['Cobertura'] > 0) & (df_mun_ranking['Cobertura'] <= 25)]),
                'Baixa (25-50%)': len(df_mun_ranking[(df_mun_ranking['Cobertura'] > 25) & (df_mun_ranking['Cobertura'] <= 50)]),
                'Média (50-75%)': len(df_mun_ranking[(df_mun_ranking['Cobertura'] > 50) & (df_mun_ranking['Cobertura'] <= 75)]),
                'Boa (75-90%)': len(df_mun_ranking[(df_mun_ranking['Cobertura'] > 75) & (df_mun_ranking['Cobertura'] <= 90)]),
                'Excelente (90-100%)': len(df_mun_ranking[df_mun_ranking['Cobertura'] > 90]),
            }
            
            total_mun = len(df_mun_ranking)
            
            # Prepara dados para gráfico e análise detalhada
            distribuicao_detalhada = {}
            for faixa, qtd in distribuicao_dict.items():
                perc = (qtd/total_mun)*100
                
                # Identifica municípios nesta faixa
                if faixa == 'Sem cobertura (0%)':
                    mask = df_mun_ranking['Cobertura'] == 0
                elif faixa == 'Muito Baixa (0-25%)':
                    mask = (df_mun_ranking['Cobertura'] > 0) & (df_mun_ranking['Cobertura'] <= 25)
                elif faixa == 'Baixa (25-50%)':
                    mask = (df_mun_ranking['Cobertura'] > 25) & (df_mun_ranking['Cobertura'] <= 50)
                elif faixa == 'Média (50-75%)':
                    mask = (df_mun_ranking['Cobertura'] > 50) & (df_mun_ranking['Cobertura'] <= 75)
                elif faixa == 'Boa (75-90%)':
                    mask = (df_mun_ranking['Cobertura'] > 75) & (df_mun_ranking['Cobertura'] <= 90)
                else:  # Excelente
                    mask = df_mun_ranking['Cobertura'] > 90
                
                municipios_faixa = df_mun_ranking[mask]['Município'].tolist()
                
                distribuicao_detalhada[faixa] = {
                    'quantidade': qtd,
                    'percentual': perc,
                    'municipios': municipios_faixa
                }
            
            # Mostra resumo com emojis
            for faixa, dados in distribuicao_detalhada.items():
                emoji = {
                    'Sem cobertura (0%)': '🔴',
                    'Muito Baixa (0-25%)': '🟠',
                    'Baixa (25-50%)': '🟡',
                    'Média (50-75%)': '🔵',
                    'Boa (75-90%)': '🟢',
                    'Excelente (90-100%)': '🟢'
                }.get(faixa, '⚪')
                
                qtd = dados['quantidade']
                perc = dados['percentual']
                
                # Mostra exemplos de municípios se houver
                if qtd > 0:
                    exemplos = dados['municipios'][:3]
                    exemplos_texto = ", ".join(exemplos)
                    if qtd > 3:
                        exemplos_texto += f" (+{qtd-3} outros)"
                    st.markdown(f"{emoji} **{faixa}:** {qtd} ({perc:.1f}%) — *{exemplos_texto}*")
                else:
                    st.markdown(f"{emoji} **{faixa}:** {qtd} ({perc:.1f}%)")
        
        # Gráfico de barras horizontais (melhor que pizza)
        st.markdown("#### 📊 Visualização da Distribuição")
        
        # Ordena do pior para o melhor (ordem lógica)
        faixas_ordenadas = [
            'Sem cobertura (0%)',
            'Muito Baixa (0-25%)',
            'Baixa (25-50%)',
            'Média (50-75%)',
            'Boa (75-90%)',
            'Excelente (90-100%)'
        ]
        
        valores_ordenados = [distribuicao_detalhada[f]['quantidade'] for f in faixas_ordenadas]
        percentuais_ordenados = [distribuicao_detalhada[f]['percentual'] for f in faixas_ordenadas]
        
        # Cores em gradiente lógico (vermelho → amarelo → verde)
        cores = ['#ef4444', '#f97316', '#eab308', '#3b82f6', '#10b981', '#059669']
        
        fig_dist = go.Figure(data=[go.Bar(
            y=faixas_ordenadas,
            x=valores_ordenados,
            orientation='h',
            marker=dict(
                color=cores,
                line=dict(color='rgba(0,0,0,0.08)', width=1)
            ),
            text=[f"{v} ({p:.1f}%)" for v, p in zip(valores_ordenados, percentuais_ordenados)],
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
        
        st.plotly_chart(fig_dist, use_container_width=True, key=f"dist_{selected_uf}")
        
        # Seção expandível com lista completa de municípios por faixa
        st.markdown("---")
        st.markdown("#### 🔍 Municípios por Faixa de Cobertura")
        
        # Destaca faixas problemáticas
        faixas_criticas = ['Sem cobertura (0%)', 'Muito Baixa (0-25%)', 'Baixa (25-50%)']
        qtd_criticos = sum(distribuicao_detalhada[f]['quantidade'] for f in faixas_criticas)
        
        if qtd_criticos > 0:
            st.warning(f"⚠️ **{qtd_criticos} municípios ({(qtd_criticos/total_mun)*100:.1f}%)** com cobertura insuficiente (<50%) precisam de atenção!")
        
        # Tabs por faixa
        tab_critico, tab_atencao, tab_bom = st.tabs([
            f"🔴 Críticos ({distribuicao_detalhada['Sem cobertura (0%)']['quantidade'] + distribuicao_detalhada['Muito Baixa (0-25%)']['quantidade']})",
            f"🟡 Atenção ({distribuicao_detalhada['Baixa (25-50%)']['quantidade'] + distribuicao_detalhada['Média (50-75%)']['quantidade']})",
            f"🟢 Bons ({distribuicao_detalhada['Boa (75-90%)']['quantidade'] + distribuicao_detalhada['Excelente (90-100%)']['quantidade']})"
        ])
        
        with tab_critico:
            st.caption("Municípios com cobertura crítica (0-25%) que necessitam investimento urgente")
            for faixa in ['Sem cobertura (0%)', 'Muito Baixa (0-25%)']:
                dados = distribuicao_detalhada[faixa]
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
        
        with tab_atencao:
            st.caption("Municípios com cobertura moderada (25-75%) que podem melhorar")
            for faixa in ['Baixa (25-50%)', 'Média (50-75%)']:
                dados = distribuicao_detalhada[faixa]
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
        
        with tab_bom:
            st.caption("Municípios com boa cobertura (75-100%)")
            for faixa in ['Boa (75-90%)', 'Excelente (90-100%)']:
                dados = distribuicao_detalhada[faixa]
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
        
        st.markdown("---")
        
        # ============================================================
        # TOP 10 E BOTTOM 10 - DESTAQUE IMEDIATO
        # ============================================================
        st.markdown(f"### 🎯 Destaques de {selected_uf}")
        
        dest_col1, dest_col2 = st.columns(2)
        
        with dest_col1:
            st.markdown("#### 🏆 Top 10 - Mais Conectados")
            st.caption(f"Municípios de {selected_uf} com melhor cobertura")
            df_top10 = df_mun_ranking.head(10).copy()
            df_top10_show = df_top10[['Posição', 'Município', 'Cobertura']].copy()
            df_top10_show['Cobertura (%)'] = df_top10_show['Cobertura'].apply(lambda x: f"{x:.2f}%")
            df_top10_show['🥇'] = ['🥇', '🥈', '🥉'] + [''] * 7 if len(df_top10_show) >= 3 else [''] * len(df_top10_show)
            df_top10_show = df_top10_show[['🥇', 'Posição', 'Município', 'Cobertura (%)']]
            
            st.dataframe(
                df_top10_show,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Gráfico de barras Top 10
            fig_top10 = go.Figure(data=[go.Bar(
                y=df_top10['Município'],
                x=df_top10['Cobertura'],
                orientation='h',
                marker=dict(
                    color=df_top10['Cobertura'],
                    colorscale='Greens',
                    showscale=False
                ),
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
            st.plotly_chart(fig_top10, use_container_width=True, key=f"top10_main_{selected_uf}")
        
        with dest_col2:
            st.markdown("#### ⚠️ Bottom 10 - Menos Conectados")
            st.caption(f"Municípios de {selected_uf} com pior cobertura")
            df_bottom10 = df_mun_ranking.tail(10).sort_values('Cobertura', ascending=True).copy()
            df_bottom10_show = df_bottom10[['Posição', 'Município', 'Cobertura']].copy()
            df_bottom10_show['Posição'] = range(len(df_mun_ranking), len(df_mun_ranking) - 10, -1)
            df_bottom10_show['Cobertura (%)'] = df_bottom10_show['Cobertura'].apply(lambda x: f"{x:.2f}%")
            df_bottom10_show['⚠️'] = ['🚨'] * len(df_bottom10_show)
            df_bottom10_show = df_bottom10_show[['⚠️', 'Posição', 'Município', 'Cobertura (%)']]
            
            st.dataframe(
                df_bottom10_show,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Gráfico de barras Bottom 10
            fig_bottom10 = go.Figure(data=[go.Bar(
                y=df_bottom10['Município'],
                x=df_bottom10['Cobertura'],
                orientation='h',
                marker=dict(
                    color=df_bottom10['Cobertura'],
                    colorscale='Reds',
                    showscale=False
                ),
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
            st.plotly_chart(fig_bottom10, use_container_width=True, key=f"bottom10_main_{selected_uf}")
        
        st.markdown("---")
        
        # ============================================================
        # TABS COM ANÁLISES DETALHADAS
        # ============================================================
        st.markdown("### 📊 Análises Detalhadas")
        
        # Tabs de visualização
        viz_tab1, viz_tab2, viz_tab3 = st.tabs([
            "📊 Ranking Completo",
            "📈 Gráficos Comparativos",
            "🔝 Personalizar Top/Bottom"
        ])
        
        with viz_tab1:
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
            df_display = df_mun_ranking.copy()
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
            st.dataframe(
                df_show,
                use_container_width=True,
                height=500,
                hide_index=True
            )
            
            # Download
            csv_data = df_display[['Município', 'Cobertura', 'Posição']].to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Baixar Ranking Completo ({len(df_display)} municípios)",
                data=csv_data,
                file_name=f"ranking_cobertura_{selected_uf}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with viz_tab2:
            st.markdown("### 📈 Gráficos Comparativos dos Municípios")
            
            # Gráfico de barras horizontais - Top 20 e Bottom 20
            col_graph1, col_graph2 = st.columns(2)
            
            with col_graph1:
                st.markdown("#### 🏆 Top 15 - Melhor Cobertura")
                df_top15 = df_mun_ranking.head(15)
                
                fig_top = go.Figure(data=[go.Bar(
                    y=df_top15['Município'],
                    x=df_top15['Cobertura'],
                    orientation='h',
                    marker=dict(
                        color=df_top15['Cobertura'],
                        colorscale='Greens',
                        showscale=False
                    ),
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
                st.plotly_chart(fig_top, use_container_width=True, key=f"top_graph_{selected_uf}")
            
            with col_graph2:
                st.markdown("#### ⚠️ Bottom 15 - Pior Cobertura")
                df_bottom15 = df_mun_ranking.tail(15).sort_values('Cobertura', ascending=True)
                
                fig_bottom = go.Figure(data=[go.Bar(
                    y=df_bottom15['Município'],
                    x=df_bottom15['Cobertura'],
                    orientation='h',
                    marker=dict(
                        color=df_bottom15['Cobertura'],
                        colorscale='Reds',
                        showscale=False
                    ),
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
                st.plotly_chart(fig_bottom, use_container_width=True, key=f"bottom_graph_{selected_uf}")
            
            # Histograma de distribuição MELHORADO
            st.markdown("---")
            st.markdown("#### 📊 Distribuição de Cobertura nos Municípios")
            st.caption("Visualize como os municípios estão distribuídos ao longo da escala de cobertura")
            
            # Calcula estatísticas para o histograma
            media_hist = df_mun_ranking['Cobertura'].mean()
            mediana_hist = df_mun_ranking['Cobertura'].median()
            
            # Cria histograma com cores em gradiente
            # Divide em bins e atribui cor baseada no valor central do bin
            fig_hist = go.Figure()
            
            # Define bins
            bins = np.linspace(0, 100, 31)  # 30 bins
            hist_values, bin_edges = np.histogram(df_mun_ranking['Cobertura'], bins=bins)
            
            # Calcula centro de cada bin e define cor
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            
            # Função para atribuir cor baseada no valor
            def get_color(value):
                if value <= 25:
                    return '#ef4444'  # Vermelho
                elif value <= 50:
                    return '#f59e0b'  # Laranja
                elif value <= 75:
                    return '#3b82f6'  # Azul
                else:
                    return '#10b981'  # Verde
            
            colors = [get_color(center) for center in bin_centers]
            
            # Adiciona barras do histograma com cores
            fig_hist.add_trace(go.Bar(
                x=bin_centers,
                y=hist_values,
                width=(bin_edges[1] - bin_edges[0]) * 0.9,
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(0,0,0,0.08)', width=1)
                ),
                hovertemplate='Cobertura: %{x:.1f}%<br>Municípios: %{y}<extra></extra>',
                name='Municípios'
            ))
            
            # Adiciona linha vertical para a MÉDIA
            fig_hist.add_vline(
                x=media_hist,
                line_dash="dash",
                line_color="#92400E",
                line_width=3,
                annotation_text=f"Média: {media_hist:.1f}%",
                annotation_position="top",
                annotation_font_size=12,
                annotation_font_color="#92400E"
            )
            
            # Adiciona linha vertical para a MEDIANA
            fig_hist.add_vline(
                x=mediana_hist,
                line_dash="dot",
                line_color="#5B21B6",
                line_width=3,
                annotation_text=f"Mediana: {mediana_hist:.1f}%",
                annotation_position="bottom",
                annotation_font_size=12,
                annotation_font_color="#5B21B6"
            )
            
            # Adiciona áreas de referência
            # Área crítica (0-25%)
            fig_hist.add_vrect(
                x0=0, x1=25,
                fillcolor="red", opacity=0.1,
                layer="below", line_width=0,
                annotation_text="Crítico",
                annotation_position="top left",
                annotation_font_size=10
            )
            
            # Área de atenção (25-50%)
            fig_hist.add_vrect(
                x0=25, x1=50,
                fillcolor="orange", opacity=0.1,
                layer="below", line_width=0,
                annotation_text="Atenção",
                annotation_position="top left",
                annotation_font_size=10
            )
            
            # Área boa (75-100%)
            fig_hist.add_vrect(
                x0=75, x1=100,
                fillcolor="green", opacity=0.1,
                layer="below", line_width=0,
                annotation_text="Bom",
                annotation_position="top right",
                annotation_font_size=10
            )
            
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
            
            st.plotly_chart(fig_hist, use_container_width=True, key=f"hist_{selected_uf}")
            
            # Explicação das linhas de referência
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
                
                **📊 Áreas Sombreadas:**
                - Indicam faixas de qualidade (Crítico, Atenção, Bom)
                - Ajudam a identificar onde a maioria dos municípios está concentrada
                
                **💡 Como usar:**
                - **Barras altas à esquerda** → Muitos municípios com baixa cobertura (problema!)
                - **Barras altas à direita** → Muitos municípios com boa cobertura (positivo!)
                - **Barras espalhadas** → Grande desigualdade entre municípios
                """)
            
            # Box plot MELHORADO
            st.markdown("---")
            st.markdown("#### 📦 Análise Estatística (Box Plot)")
            st.caption("Visualização compacta da distribuição: mediana, quartis e outliers")
            
            # Calcula estatísticas para anotações
            q1 = df_mun_ranking['Cobertura'].quantile(0.25)
            q2 = df_mun_ranking['Cobertura'].quantile(0.50)  # mediana
            q3 = df_mun_ranking['Cobertura'].quantile(0.75)
            
            fig_box = go.Figure()
            
            # Box plot principal
            fig_box.add_trace(go.Box(
                y=df_mun_ranking['Cobertura'],
                name=selected_uf,
                marker=dict(
                    color='#3b82f6',
                    outliercolor='#ef4444',
                    line=dict(color='#1e40af', width=2)
                ),
                boxmean='sd',  # Mostra média e desvio padrão
                boxpoints='outliers',  # Mostra apenas outliers
                hovertemplate='Cobertura: %{y:.2f}%<extra></extra>'
            ))
            
            # Adiciona anotações para os quartis
            annotations = [
                dict(
                    x=0.15, y=q1,
                    text=f'Q1: {q1:.1f}%<br>(25% abaixo)',
                    showarrow=True,
                    arrowhead=2,
                    ax=80, ay=0,
                    font=dict(size=11, color='#92400E'), bgcolor='rgba(255,255,255,0.92)', bordercolor='#E2E8F0', borderwidth=1, borderpad=4),
                dict(
                    x=0.15, y=q2,
                    text=f'Mediana: {q2:.1f}%<br>(50% acima/abaixo)',
                    showarrow=True,
                    arrowhead=2,
                    ax=80, ay=0,
                    font=dict(size=11, color='#5B21B6'), bgcolor='rgba(255,255,255,0.92)', bordercolor='#E2E8F0', borderwidth=1, borderpad=4),
                dict(
                    x=0.15, y=q3,
                    text=f'Q3: {q3:.1f}%<br>(75% abaixo)',
                    showarrow=True,
                    arrowhead=2,
                    ax=80, ay=0,
                    font=dict(size=11, color='#065F46'), bgcolor='rgba(255,255,255,0.92)', bordercolor='#E2E8F0', borderwidth=1, borderpad=4)
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
                st.plotly_chart(fig_box, use_container_width=True, key=f"box_{selected_uf}")
            
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
        
        with viz_tab3:
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
                df_top_dest = df_mun_ranking.head(num_dest).copy()
                df_top_dest['Cobertura (%)'] = df_top_dest['Cobertura'].apply(lambda x: f"{x:.2f}%")
                df_top_dest = df_top_dest[['Posição', 'Município', 'Cobertura (%)']]
                st.dataframe(df_top_dest, use_container_width=True, hide_index=True, height=400)
            
            with dest_col2:
                st.markdown(f"#### ⚠️ Bottom {num_dest}")
                df_bottom_dest = df_mun_ranking.tail(num_dest).sort_values('Cobertura', ascending=True).copy()
                df_bottom_dest['Posição'] = range(len(df_mun_ranking), len(df_mun_ranking) - num_dest, -1)
                df_bottom_dest['Cobertura (%)'] = df_bottom_dest['Cobertura'].apply(lambda x: f"{x:.2f}%")
                df_bottom_dest = df_bottom_dest[['Posição', 'Município', 'Cobertura (%)']]
                st.dataframe(df_bottom_dest, use_container_width=True, hide_index=True, height=400)
    
    except Exception as e:
        st.error(f"Erro ao processar municípios: {str(e)}")
        st.exception(e)

# Seção de Resumo dos Filtros Aplicados
if selected_municipio:
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

# Footer
st.markdown("---")
st.caption("📡 Dados de Cobertura Móvel fornecidos pela ANATEL")
