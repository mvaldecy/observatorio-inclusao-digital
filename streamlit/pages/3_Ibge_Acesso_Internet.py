"""
Página Streamlit: Análise de Acesso à Internet (IBGE)

Tabela 7336: Pessoas de 10 anos ou mais de idade, por acesso à Internet
Período: 2021-2024

Refatoração: Componentes modulares para melhor manutenibilidade
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functools import lru_cache
import sys
import os

# Adiciona a raiz do projeto e o diretório streamlit ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from utils.data_loader import get_analisador_tabela7336
from components.header import inject_global_css

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

@lru_cache(maxsize=1)
def carregar_dados():
    """Carrega dados da Tabela 7336 com cache"""
    try:
        analisador = get_analisador_tabela7336()
        return analisador.obtener_df()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.stop()

def obter_valor_media(df, localizacao):
    """Calcula a média de acesso para uma localização"""
    d = df[df['LOCALIZACAO'] == localizacao]
    return float(d['PERCENTUAL'].mean()) if not d.empty else None

def criar_heatmap(data, title_prefix=""):
    """Cria um heatmap a partir de um pivot table"""
    fig = go.Figure(data=go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='RdYlGn',
        text=[[f"{val:.1f}%" for val in row] for row in data.values],
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Acesso (%)", thickness=15, len=0.7)
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title='Nível de Instrução',
        yaxis_title='Localização',
        margin=dict(l=150, r=80, t=50, b=100),
        font=dict(size=11),
        xaxis_tickangle=-45
    )
    return fig

def criar_ranking(data, titulo="Ranking", chave_local="LOCALIZACAO", chave_valor="ACESSO"):
    """Cria um gráfico de ranking com barras"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data[chave_local],
        y=data[chave_valor],
        marker=dict(
            color=data[chave_valor],
            colorscale='Viridis',
            showscale=False,
            line=dict(width=1, color='rgba(0,0,0,0.3)')
        ),
        text=[f"{v:.1f}%" for v in data[chave_valor]],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Acesso: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        height=450,
        xaxis_title='',
        yaxis_title='Acesso à Internet (%)',
        margin=dict(l=50, r=50, t=30, b=100),
        font=dict(size=11),
        showlegend=False,
        xaxis_tickangle=-45,
        yaxis=dict(range=[0, 100])
    )
    return fig

def renderizar_insighs_tab1(df_data):
    """Renderiza insights úteis para a Tab 1"""
    col1, col2, col3 = st.columns(3)
    
    media_geral = df_data['PERCENTUAL'].mean()
    max_local = df_data[df_data['LOCALIZACAO'] != 'Brasil'].groupby('LOCALIZACAO')['PERCENTUAL'].mean().max()
    min_local = df_data[df_data['LOCALIZACAO'] != 'Brasil'].groupby('LOCALIZACAO')['PERCENTUAL'].mean().min()
    
    with col1:
        st.metric("📊 Média Geral", f"{media_geral:.1f}%")
    with col2:
        st.metric("🏆 Melhor Local", f"{max_local:.1f}%")
    with col3:
        st.metric("📉 Pior Local", f"{min_local:.1f}%")

# ============================================================================
# Configuração da Página
# ============================================================================

st.set_page_config(
    page_title="IBGE - Acesso à Internet",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_css()

# ============================================================================
# SIDEBAR - Configurações e Filtros
# ============================================================================

with st.sidebar:
    st.title("⚙️ Configurações")
    
    # Carregamento de Dados (antes de carregá-los)
    try:
        with st.spinner("⏳ Carregando dados..."):
            analisador = get_analisador_tabela7336()
            df_original = analisador.obtener_df()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.stop()
    
    # Anos disponíveis
    anos_disponiveis = sorted(df_original['ANO'].unique())
    ano_selecionado = st.selectbox(
        "📅 Ano da Pesquisa",
        options=anos_disponiveis,
        index=len(anos_disponiveis) - 1,
        help="Selecione o ano da pesquisa (2021-2024)"
    )
    
    # Botões de gerenciamento
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🔄 Recarregar", help="Atualizar dados", width='stretch'):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
    
    with col_btn2:
        if st.button("🗑️ Limpar Cache", help="Remover dados em cache", width='stretch'):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.info("✓ Cache limpo!")
            st.rerun()
    
    # Informações sobre a base de dados
    with st.expander("📊 Sobre a Base de Dados", expanded=False):
        st.markdown(f"""
        **Total de Registros:** {len(df_original):,}  
        **Período:** 2021-2024  
        **Fonte:** IBGE - PNAD Contínua  
        **Tabela:** 7336  
        **Indicador:** Acesso à Internet (pessoas 10+ anos)
        """)
    
    st.markdown("---")
    st.markdown("### 🔍 Filtros")
    
    # Regiões e UFs
    regioes_options = sorted(df_original['REGIAO'].unique())
    col_r1, col_r2 = st.columns([3, 1])
    with col_r1:
        regiao_selecionada = st.multiselect(
            "🗺️ Região(ões)",
            options=regioes_options,
            default=["Nordeste"],
            help="Selecione uma ou mais regiões",
            key="regiao_selecionada"
        )
    with col_r2:
        if st.button("✓ Todos", key="btn_todas_regioes", width='stretch'):
            regiao_selecionada = regioes_options
    
    ufs_options = sorted(df_original['UF'].unique())
    col_u1, col_u2 = st.columns([3, 1])
    with col_u1:
        uf_selecionada = st.multiselect(
            "📍 UF(s)",
            options=ufs_options,
            default=["PI"],
            help="Selecione um ou mais estados",
            key="uf_selecionada"
        )
    with col_u2:
        if st.button("✓ Todos", key="btn_todas_ufs", width='stretch'):
            uf_selecionada = ufs_options
    
    # Níveis de instrução disponíveis
    instrucao_options = sorted(df_original['INSTRUCAO'].unique()) if 'INSTRUCAO' in df_original.columns else []
    col_i1, col_i2 = st.columns([3, 1])
    with col_i1:
        instrucao_selecionada = st.multiselect(
            "🎓 Nível(s) de instrução",
            options=instrucao_options,
            default=instrucao_options if instrucao_options else [],
            help="Selecione um ou mais níveis de instrução",
            key='instrucao_selecionada'
        )
    with col_i2:
        if st.button("✓ Todos", key="btn_todas_instrucoes", width='stretch'):
            instrucao_selecionada = instrucao_options

# ============================================================================
# Título Principal
# ============================================================================

st.title("📊 Acesso à Internet - IBGE")
st.markdown("**Tabela 7336:** Pessoas de 10 anos ou mais de idade, por acesso à Internet")
st.markdown("Período: 2021-2024 | Fonte: PNAD Contínua")

# ============================================================================
# Aplicar Filtros
# ============================================================================

# Aplicar filtro inicial por ano
df_ano = df_original[df_original['ANO'] == ano_selecionado].copy()

# Construir máscara a partir do ano e dos filtros da sidebar
base_mask = df_original['ANO'] == ano_selecionado
if regiao_selecionada:
    base_mask &= df_original['REGIAO'].isin(regiao_selecionada)
if uf_selecionada:
    base_mask &= df_original['UF'].isin(uf_selecionada)
if instrucao_selecionada:
    base_mask &= df_original['INSTRUCAO'].isin(instrucao_selecionada)

df_filtrado = df_original[base_mask].copy()
# ============================================================================
# Resumo Executivo
# ============================================================================

st.markdown("### 📈 Resumo dos Filtros Aplicados")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Registros",
        f"{len(df_filtrado):,}",
        help="Total de registros após aplicação dos filtros"
    )

with col2:
    st.metric("📅 Ano", ano_selecionado, help="Ano selecionado para análise")

with col3:
    regioes_count = len(regiao_selecionada) if regiao_selecionada else 0
    st.metric("🗺️ Regiões", regioes_count, help="Quantidade de regiões selecionadas")

with col4:
    ufs_count = len(uf_selecionada) if uf_selecionada else 0
    st.metric("📍 Estados", ufs_count, help="Quantidade de estados selecionados")

st.divider()

# ============================================================================
# ANÁLISES DETALHADAS
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Distribuição por Local",
    "🗺️ Comparação por Região",
    "📈 Evolução Temporal",
    "🔢 Dados Brutos"
])

# ============================================================================
# Tab 1: Distribuição por Local (Estado/Região)
# ============================================================================

with tab1:
    st.subheader("Distribuição de Acesso à Internet por Localização")
    
    # Agrupa por localizacao (excluindo Brasil)
    df_por_local = df_filtrado[df_filtrado['LOCALIZACAO'] != 'Brasil'].copy()
    
    if not df_por_local.empty:
        # Insights principais
        renderizar_insighs_tab1(df_filtrado)
        st.divider()
        
        # Criar pivot table para heatmap: LOCALIZACAO x INSTRUCAO
        heatmap_data = df_por_local.pivot_table(
            index='LOCALIZACAO',
            columns='INSTRUCAO',
            values='PERCENTUAL',
            aggfunc='mean'
        )
        
        if not heatmap_data.empty:
            st.markdown("### 🔥 Mapa de Calor - Acesso por Local e Nível de Instrução")
            st.caption("Verde = Alto acesso | Vermelho = Baixo acesso")
            fig_heatmap = criar_heatmap(heatmap_data)
            st.plotly_chart(fig_heatmap, width='stretch', key="heatmap_local_instr")
            st.markdown("---")
        
        # Gráfico comparativo: localidades com melhor e pior acesso
        st.markdown("### 📊 Ranking de Acesso por Localização")
        
        ranking_data = df_por_local.groupby('LOCALIZACAO')['PERCENTUAL'].mean().reset_index()
        ranking_data.columns = ['LOCALIZACAO', 'ACESSO']
        ranking_data = ranking_data.sort_values('ACESSO', ascending=False)
        
        # Mostrar top 5 e bottom 5
        col_top, col_bottom = st.columns(2)
        
        with col_top:
            st.markdown("#### 🏆 Top 5")
            top5 = ranking_data.head(5)
            for idx, row in top5.iterrows():
                st.write(f"**{row['LOCALIZACAO']}**: {row['ACESSO']:.1f}%")
        
        with col_bottom:
            st.markdown("#### 📉 Bottom 5")
            bottom5 = ranking_data.tail(5).iloc[::-1]
            for idx, row in bottom5.iterrows():
                st.write(f"**{row['LOCALIZACAO']}**: {row['ACESSO']:.1f}%")
        
        st.markdown("---")
        
        fig_ranking = criar_ranking(ranking_data, "Ranking de Acesso")
        st.plotly_chart(fig_ranking, width='stretch', key="ranking_local")
        st.markdown("---")
    else:
        st.info("Nenhum dado disponível para a seleção")

# ============================================================================
# Tab 2: Comparação por Região
# ============================================================================

with tab2:
    st.subheader("� Comparação por Região")
    
    # ========== SEÇÃO 1: Comparativo Fixo Brasil, Nordeste e Piauí ==========
    st.markdown("### 🇧🇷 Comparativo Fixo: Brasil | Nordeste | Piauí")
    st.caption("Valores fixos para referência - sem é aplicado filtro de instrução")
    
    # Dados fixos para essa comparação
    df_comp_fixo = df_original[df_original['ANO'] == ano_selecionado].copy()
    
    # Se houver instrução selecionada, applicar filtro
    if instrucao_selecionada:
        df_comp_fixo = df_comp_fixo[df_comp_fixo['INSTRUCAO'].isin(instrucao_selecionada)]
    
    # Função para calcular valor usando LOCALIZACAO
    def obter_valor_regiao(df, localizacao):
        # Sempre buscar por LOCALIZACAO, que pode ser 'Brasil', 'Nordeste', 'Piauí', etc.
        d = df[df['LOCALIZACAO'] == localizacao]
        if d.empty:
            return None
        return float(d['PERCENTUAL'].mean())
    
    # Calcular valores usando LOCALIZACAO
    v_brasil = obter_valor_regiao(df_comp_fixo, 'Brasil')
    v_nordeste = obter_valor_regiao(df_comp_fixo, 'Nordeste')
    v_piaui = obter_valor_regiao(df_comp_fixo, 'Piauí')
    
    # Exibir métricas em 3 colunas
    col_b, col_ne, col_pi = st.columns(3)
    
    with col_b:
        if v_brasil is not None:
            st.metric("🇧🇷 Brasil", f"{v_brasil:.1f}%")
        else:
            st.metric("🇧🇷 Brasil", "—")
    
    with col_ne:
        if v_nordeste is not None:
            delta_ne = v_nordeste - v_brasil if v_brasil else None
            st.metric("🌵 Nordeste", f"{v_nordeste:.1f}%", 
                     delta=f"{delta_ne:+.1f}%" if delta_ne else None)
        else:
            st.metric("🌵 Nordeste", "—")
    
    with col_pi:
        if v_piaui is not None:
            delta_pi = v_piaui - v_brasil if v_brasil else None
            st.metric("🏛️ Piauí", f"{v_piaui:.1f}%",
                     delta=f"{delta_pi:+.1f}%" if delta_pi else None)
        else:
            st.metric("🏛️ Piauí", "—")
    
    st.markdown("---")
    
    # ========== SEÇÃO 2: Comparação das 5 Regiões ==========
    st.markdown("### 📊 Comparação das 5 Regiões")
    
    # Filtros simples em uma linha
    col_ano_reg, col_instr_reg1, col_instr_reg2 = st.columns([1, 2, 0.5])
    
    with col_ano_reg:
        ano_comp = st.selectbox(
            "Ano",
            options=sorted(df_original['ANO'].unique()),
            index=len(sorted(df_original['ANO'].unique())) - 1,
            key="ano_comp_regioes"
        )
    
    with col_instr_reg1:
        instrucoes_disp = sorted(df_original['INSTRUCAO'].unique())
        instrucoes_comp = st.multiselect(
            "Nível(s) de instrução",
            options=instrucoes_disp,
            default=instrucoes_disp,
            key="instrucoes_comp_regioes"
        )
    
    with col_instr_reg2:
        if st.button("✓ Todos", key="btn_todas_instr_comp", width='stretch'):
            instrucoes_comp = instrucoes_disp
    
    # Preparar dados para as 5 regiões
    df_5regioes = df_original[
        (df_original['ANO'] == ano_comp) &
        (df_original['REGIAO'].isin(['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']))
    ].copy()
    
    if instrucoes_comp:
        df_5regioes = df_5regioes[df_5regioes['INSTRUCAO'].isin(instrucoes_comp)]
    
    if not df_5regioes.empty:
        # Calcular estatísticas por região
        stats_regioes = df_5regioes.groupby('REGIAO')['PERCENTUAL'].mean().reset_index()
        stats_regioes.columns = ['REGIAO', 'Média']
        stats_regioes = stats_regioes.sort_values('Média', ascending=False)
        
        st.markdown("### 📊 Comparativo de Acesso - Todas as Regiões")
        st.markdown("---")
        
        # Cores para cada região
        cores_dict = {
            'Norte': '#FF6B6B',
            'Nordeste': '#4ECDC4',
            'Sudeste': '#45B7D1',
            'Sul': '#FFA07A',
            'Centro-Oeste': '#98D8C8'
        }
        
        # Gráfico geral comparativo das 5 regiões
        col_resumo1, col_resumo2 = st.columns(2)
        
        with col_resumo1:
            st.markdown("#### 🏆 Ranking Geral")
            for i, (_, row) in enumerate(stats_regioes.iterrows(), 1):
                medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
                st.write(f"{medal} **{row['REGIAO']}**: {row['Média']:.1f}%")
        
        with col_resumo2:
            st.markdown("#### 📈 Variação")
            max_val = stats_regioes['Média'].max()
            min_val = stats_regioes['Média'].min()
            variacao = max_val - min_val
            st.metric("Diferença (Max-Min)", f"{variacao:.1f}%", delta=None)
            st.metric("Âmbito", f"{min_val:.1f}% a {max_val:.1f}%")
        
        st.divider()
        
        # Gráfico geral de barras das regiões
        fig_geral = go.Figure()
        fig_geral.add_trace(go.Bar(
            x=stats_regioes['REGIAO'],
            y=stats_regioes['Média'],
            marker=dict(
                color=[cores_dict.get(r, '#999999') for r in stats_regioes['REGIAO']],
                line=dict(width=2, color='rgba(0,0,0,0.1)')
            ),
            text=[f"{v:.1f}%" for v in stats_regioes['Média']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Acesso: %{y:.1f}%<extra></extra>'
        ))
        
        fig_geral.update_layout(
            height=400,
            title="<b>Acesso à Internet por Região</b>",
            xaxis_title='Região',
            yaxis_title='Acesso à Internet (%)',
            yaxis=dict(range=[0, 100]),
            margin=dict(l=50, r=50, t=70, b=50),
            font=dict(size=12),
            showlegend=False
        )
        
        st.plotly_chart(fig_geral, width='stretch', key="bar_regioes_geral")
        st.markdown("---")
        
        # Gráficos de barras lado a lado por nível de instrução
        st.markdown("### 📊 Detalhamento por Nível de Instrução")
        
        # Preparar dados com breakdown por instrução
        df_regioes_instr = df_5regioes.groupby(['REGIAO', 'INSTRUCAO'])['PERCENTUAL'].mean().reset_index()
        
        for idx, instr in enumerate(sorted(df_regioes_instr['INSTRUCAO'].unique())):
            df_instr = df_regioes_instr[df_regioes_instr['INSTRUCAO'] == instr].sort_values('PERCENTUAL', ascending=True)
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                y=df_instr['REGIAO'],
                x=df_instr['PERCENTUAL'],
                orientation='h',
                marker=dict(
                    color=[cores_dict.get(r, '#999999') for r in df_instr['REGIAO']],
                    line=dict(width=1, color='rgba(0,0,0,0.2)')
                ),
                text=[f"{v:.1f}%" for v in df_instr['PERCENTUAL']],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>' + instr + ': %{x:.1f}%<extra></extra>'
            ))
            
            fig_bar.update_layout(
                height=350,
                title=f"<b>{instr}</b>",
                xaxis_title='Acesso à Internet (%)',
                yaxis_title='Região',
                xaxis=dict(range=[0, 100]),
                margin=dict(l=120, r=50, t=50, b=30),
                font=dict(size=11),
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, width='stretch', key=f"bar_regiao_{instr}")
        
        st.markdown("---")
        st.markdown("### 📋 Resumo Estatístico")
        
        tabela_exib = stats_regioes[['REGIAO', 'Média']].round(2)
        tabela_exib.columns = ['Região', 'Acesso à Internet (%)']
        tabela_exib = tabela_exib.sort_values('Acesso à Internet (%)', ascending=False)
        
        st.dataframe(tabela_exib, width='stretch', hide_index=True)
    else:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados")

# ============================================================================
# Tab 3: Comparativo por Município
# ============================================================================

with tab3:
    st.subheader("Comparativo de Acesso à Internet por Município")
    
    # Filtros para a Tab 3
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        regioes_t3 = sorted(df_original['REGIAO'].unique())
        regiao_t3 = st.selectbox(
            "🗺️ Região",
            options=regioes_t3,
            index=list(regioes_t3).index("Nordeste") if "Nordeste" in regioes_t3 else 0,
            key="regiao_t3"
        )
    
    with col_f2:
        ufs_disponiveis_t3 = sorted(df_original[df_original['REGIAO'] == regiao_t3]['UF'].unique())
        uf_t3 = st.selectbox(
            "📍 Estado",
            options=ufs_disponiveis_t3,
            index=list(ufs_disponiveis_t3).index("PI") if "PI" in ufs_disponiveis_t3 else 0,
            key="uf_t3"
        )
    
    st.markdown("---")
    
    # Pegar automaticamente todos os municípios do estado selecionado
    municipios_t3 = sorted(df_original[
        (df_original['REGIAO'] == regiao_t3) & 
        (df_original['UF'] == uf_t3) &
        (df_original['LOCALIZACAO'] != 'Brasil')
    ]['LOCALIZACAO'].unique())
    
    if municipios_t3:
        st.markdown(f"### 📊 {uf_t3} - {len(municipios_t3)} município(s)")
        
        # Filtrar dados para todos os municípios do estado
        df_municipios = df_original[
            (df_original['REGIAO'] == regiao_t3) &
            (df_original['UF'] == uf_t3) &
            (df_original['LOCALIZACAO'].isin(municipios_t3))
        ].copy()
        
        # Resumo geral dos municípios
        col_s1, col_s2, col_s3 = st.columns(3)
        media_estado = df_municipios.groupby('LOCALIZACAO')['PERCENTUAL'].mean().mean()
        melhor_mun = df_municipios.groupby('LOCALIZACAO')['PERCENTUAL'].mean().max()
        pior_mun = df_municipios.groupby('LOCALIZACAO')['PERCENTUAL'].mean().min()
        
        with col_s1:
            st.metric("📊 Média do Estado", f"{media_estado:.1f}%")
        with col_s2:
            st.metric("🏆 Melhor Município", f"{melhor_mun:.1f}%")
        with col_s3:
            st.metric("📉 Pior Município", f"{pior_mun:.1f}%")
        
        # Ranking dos municípios
        ranking_mun = df_municipios.groupby('LOCALIZACAO')['PERCENTUAL'].mean().reset_index()
        ranking_mun.columns = ['MUNICIPIO', 'ACESSO']
        ranking_mun = ranking_mun.sort_values('ACESSO', ascending=False)
        
        st.divider()
        st.markdown("### 📈 Ranking de Municípios")
        
        col_top, col_bottom = st.columns(2)
        with col_top:
            st.markdown("#### 🏆 Top 5")
            for i, (_, row) in enumerate(ranking_mun.head(5).iterrows(), 1):
                medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
                st.write(f"{medal} **{row['MUNICIPIO']}**: {row['ACESSO']:.1f}%")
        
        with col_bottom:
            st.markdown("#### 📉 Últimos 5")
            for i, (_, row) in enumerate(ranking_mun.tail(5).iloc[::-1].iterrows(), 1):
                st.write(f"{i}. **{row['MUNICIPIO']}**: {row['ACESSO']:.1f}%")
        
        st.divider()
        st.markdown("### 📊 Gráficos Comparativos")
        
        # Renderizar gráficos em 2 colunas
        for idx in range(0, len(municipios_t3), 2):
            cols = st.columns(2)
            
            for col_idx in range(2):
                if idx + col_idx < len(municipios_t3):
                    municipio = municipios_t3[idx + col_idx]
                    
                    with cols[col_idx]:
                        # Filtrar dados do município
                        df_mun = df_municipios[df_municipios['LOCALIZACAO'] == municipio].copy()
                        
                        if df_mun.empty:
                            st.info(f"Sem dados para {municipio}")
                            continue
                        
                        # Agrupar por instrução e pegar a média
                        stats_mun = df_mun.groupby('INSTRUCAO')['PERCENTUAL'].mean().reset_index()
                        stats_mun = stats_mun.sort_values('PERCENTUAL', ascending=True)
                        
                        instrs = stats_mun['INSTRUCAO'].tolist()
                        vals = stats_mun['PERCENTUAL'].tolist()
                        
                        media_mun = stats_mun['PERCENTUAL'].mean()
                        st.markdown(f"### {municipio} | {media_mun:.1f}%")
                        
                        # Gráfico de barras horizontal
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            y=instrs,
                            x=vals,
                            orientation='h',
                            marker=dict(
                                color=vals,
                                colorscale='Viridis',
                                showscale=False
                            ),
                            text=[f"{v:.1f}%" for v in vals],
                            textposition='outside',
                            hovertemplate='<b>%{y}</b><br>Acesso: %{x:.1f}%<extra></extra>'
                        ))
                        
                        fig.update_layout(
                            height=400,
                            xaxis_title='Acesso à Internet (%)',
                            yaxis_title='Nível de Instrução',
                            margin=dict(l=150, r=50, t=30, b=50),
                            font=dict(size=11),
                            showlegend=False,
                            xaxis=dict(range=[0, 100])
                        )
                        
                        st.plotly_chart(fig, width='stretch', key=f"mun_bar_{municipio}")
    else:
        st.warning(f"⚠️ Nenhum município encontrado para {uf_t3}")

# ============================================================================
# Tab 4: Dados Brutos
# ============================================================================

with tab4:
    st.subheader("Visualização dos Dados Brutos")
    
    # Opções de coluna para exibição
    all_cols = ['REGIAO', 'UF', 'LOCALIZACAO', 'ANO', 'PERCENTUAL']
    default_cols = ['LOCALIZACAO', 'ANO', 'PERCENTUAL']
    
    col_opt1, col_opt2 = st.columns([3, 1])
    
    with col_opt1:
        cols_shown = st.multiselect(
            "Selecione as colunas para exibir",
            options=all_cols,
            default=default_cols,
            key="cols_shown_raw"
        )
    
    with col_opt2:
        # Download do CSV
        if cols_shown:
            csv = df_filtrado[cols_shown].to_csv(index=False)
            st.download_button(
                label="📥 CSV",
                data=csv,
                file_name=f"ibge_tabela7336_{ano_selecionado}.csv",
                mime="text/csv",
                width='stretch'
            )
    
    if cols_shown:
        # Exibir dados em layout de 2 colunas (lado a lado)
        df_display = df_filtrado[cols_shown].reset_index(drop=True)
        
        cols_layout = st.columns(2)
        
        for idx, row in df_display.iterrows():
            col_idx = idx % 2
            
            with cols_layout[col_idx]:
                # Criar um container visual para cada registro
                with st.container(border=True):
                    for col in cols_shown:
                        valor = row[col]
                        if col == 'PERCENTUAL':
                            st.metric(col, f"{valor:.1f}%")
                        else:
                            st.write(f"**{col}:** {valor}")
        
        st.divider()
        st.markdown("### 📊 Vista em Tabela")
        st.dataframe(
            df_display,
            width='stretch',
            height=300
        )

# ============================================================================
# Footer
# ============================================================================

st.divider()

footer_cols = st.columns(4)

with footer_cols[0]:
    st.caption("📊 **Fonte:** IBGE - PNAD Contínua")

with footer_cols[1]:
    st.caption(f"📅 **Período:** 2021-2024")

with footer_cols[2]:
    st.caption("🔖 **Tabela:** 7336")

with footer_cols[3]:
    st.caption("📈 **Atualizado:** Fevereiro 2026")

