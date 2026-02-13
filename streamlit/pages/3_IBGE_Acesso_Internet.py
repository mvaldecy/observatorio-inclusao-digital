"""
Página Streamlit: Análise de Acesso à Internet (IBGE)

Tabela 7336: Pessoas de 10 anos ou mais de idade, por acesso à Internet
Período: 2021-2024
"""

import streamlit as st
import pandas as pd
import sys
import os
import plotly.graph_objects as go
import plotly.express as px

# Adiciona a raiz do projeto e o diretório streamlit ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from utils.data_loader import get_analisador_tabela7336
from ibge.metadados import get_metadados
from components import ibge as ibge_components

# ============================================================================
# Configuração da Página
# ============================================================================

st.set_page_config(
    page_title="IBGE - Acesso à Internet",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para remover bordas laranja/vermelhas e melhorar estética
st.markdown("""
<style>
    /* Remove todas as bordas laranja/vermelhas de labels, headers e títulos */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] label,
    label[data-baseweb="label"],
    div[data-baseweb="label"] {
        border: none !important;
        outline: none !important;
    }
    
    /* Remove bordas em elementos com classe de label */
    .stSelectbox label,
    .stMultiSelect label,
    div[role="option"] {
        border: none !important;
        outline: none !important;
    }
    
    /* Remove borda laranja de inputs e selects */
    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="combobox"],
    div[role="listbox"],
    div[data-baseweb="select"] {
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        outline: none !important;
    }
    
    /* Remove overlay/borda laranja no focus */
    [data-baseweb="input"]:focus,
    [data-baseweb="select"]:focus,
    [data-baseweb="combobox"]:focus,
    input:focus {
        border-color: #0d58ca !important;
        box-shadow: 0 0 0 1px #0d58ca !important;
        outline: none !important;
    }
    
    /* Remove bordas de modal/dropdown */
    div[style*="background"] > div[role="listbox"] {
        border: 1px solid #ccc !important;
        outline: none !important;
    }
    
    /* Melhora multiselect appearance */
    div[data-testid="stMultiSelect"] span {
        color: #262730 !important;
        border: none !important;
    }
    
    /* Melhora elementos de input */
    input {
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        outline: none !important;
    }
    
    /* Remove qualquer borda vermelha de erro */
    input:invalid {
        border-color: #ccc !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Remove bordas em elementos do sidebar */
    [data-testid="stSidebar"] div[data-baseweb] {
        border: none !important;
    }
    
    /* Remove cor de highlight laranja */
    div[style*="rgb(255, 159, 64)"],
    div[style*="#FF9F40"],
    div[style*="#ffb3b3"],
    div[style*="orange"] {
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

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
        if st.button("🔄 Recarregar", help="Atualizar dados", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
    
    with col_btn2:
        if st.button("🗑️ Limpar Cache", help="Remover dados em cache", use_container_width=True):
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
    regiao_selecionada = st.multiselect(
        "🗺️ Região(ões)",
        options=sorted(df_original['REGIAO'].unique()),
        default=["Nordeste"],
        help="Selecione uma ou mais regiões",
        key="regiao_selecionada"
    )
    
    uf_selecionada = st.multiselect(
        "📍 UF(s)",
        options=sorted(df_original['UF'].unique()),
        default=["PI"],
        help="Selecione um ou mais estados",
        key="uf_selecionada"
    )
    
    # Níveis de instrução disponíveis
    instrucao_options = sorted(df_original['INSTRUCAO'].unique()) if 'INSTRUCAO' in df_original.columns else []
    instrucao_selecionada = st.multiselect(
        "🎓 Nível(s) de instrução",
        options=instrucao_options,
        default=instrucao_options if instrucao_options else [],
        help="Selecione um ou mais níveis de instrução",
        key='instrucao_selecionada'
    )

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
    st.subheader("Distribuição de Acesso por Localização")
    
    # Agrupa por localizacao (excluindo Brasil)
    df_por_local = df_filtrado[df_filtrado['LOCALIZACAO'] != 'Brasil'].copy()
    
    if not df_por_local.empty:
        instrs_to_plot = instrucao_selecionada if instrucao_selecionada else sorted(df_por_local['INSTRUCAO'].unique())
        # Renderiza um gráfico por instrução em grid de 2 colunas
        cols_per_row = 2
        # Renderizar todos os gráficos lado-a-lado (uma coluna por instrução)
        if instrs_to_plot:
            cols = st.columns(len(instrs_to_plot))
            for idx, instr in enumerate(instrs_to_plot):
                df_inst = df_por_local[df_por_local['INSTRUCAO'] == instr]
                if df_inst.empty:
                    with cols[idx]:
                        st.markdown(f"### {instr}")
                        st.info("Sem dados")
                    continue

                stats = df_inst.groupby('LOCALIZACAO')['PERCENTUAL'].agg(['mean', 'max', 'min']).reset_index()
                stats = stats.sort_values('mean')
                locais = stats['LOCALIZACAO'].tolist()
                mean_vals = stats['mean'].tolist()
                max_vals = stats['max'].tolist()
                min_vals = stats['min'].tolist()

                with cols[idx]:
                    st.markdown(f"### {instr}")
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='Média', x=locais, y=mean_vals, marker_color='#4F46E5', text=[f"{v:.1f}%" for v in mean_vals], textposition='inside'))
                    fig.add_trace(go.Bar(name='Máxima', x=locais, y=max_vals, marker_color='#10B981', text=[f"{v:.1f}%" for v in max_vals], textposition='inside'))
                    fig.add_trace(go.Bar(name='Mínima', x=locais, y=min_vals, marker_color='#EF4444', text=[f"{v:.1f}%" for v in min_vals], textposition='inside'))

                    fig.update_layout(
                        barmode='group',
                        template='plotly_dark',
                        height=420,
                        margin=dict(l=20, r=10, t=30, b=30),
                        yaxis=dict(title='Percentual (%)', range=[0, 100]),
                        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
                    )

                    st.plotly_chart(fig, use_container_width=True)
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
    col_ano_reg, col_instr_reg = st.columns([1, 2])
    
    with col_ano_reg:
        ano_comp = st.selectbox(
            "Ano",
            options=sorted(df_original['ANO'].unique()),
            index=len(sorted(df_original['ANO'].unique())) - 1,
            key="ano_comp_regioes"
        )
    
    with col_instr_reg:
        instrucoes_disp = sorted(df_original['INSTRUCAO'].unique())
        instrucoes_comp = st.multiselect(
            "Nível(s) de instrução",
            options=instrucoes_disp,
            default=instrucoes_disp,
            key="instrucoes_comp_regioes"
        )
    
    # Preparar dados para as 5 regiões
    df_5regioes = df_original[
        (df_original['ANO'] == ano_comp) &
        (df_original['REGIAO'].isin(['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']))
    ].copy()
    
    if instrucoes_comp:
        df_5regioes = df_5regioes[df_5regioes['INSTRUCAO'].isin(instrucoes_comp)]
    
    if not df_5regioes.empty:
        # Calcular estatísticas por região
        stats_regioes = df_5regioes.groupby('REGIAO')['PERCENTUAL'].agg([
            ('Média', 'mean'),
            ('Mín', 'min'),
            ('Máx', 'max'),
            ('Desvio', 'std'),
            ('N', 'count')
        ]).reset_index()
        
        stats_regioes = stats_regioes.sort_values('Média', ascending=False)
        
        # Gráficos lado a lado
        col_graf1, col_graf2 = st.columns(2)
        
        # Gráfico 1: Barras comparativas
        with col_graf1:
            fig_barras = go.Figure()
            
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
            regioes_ordem = stats_regioes['REGIAO'].tolist()
            medias = stats_regioes['Média'].tolist()
            
            for i, (regiao, media, cor) in enumerate(zip(regioes_ordem, medias, cores)):
                fig_barras.add_trace(go.Bar(
                    x=[regiao],
                    y=[media],
                    name=regiao,
                    marker_color=cor,
                    text=f"{media:.1f}%",
                    textposition='outside',
                    showlegend=False
                ))
            
            fig_barras.update_layout(
                height=350,
                xaxis_title="Região",
                yaxis_title="Acesso à Internet (%)",
                yaxis=dict(range=[0, 105]),
                template='plotly_dark',
                margin=dict(l=50, r=50, t=30, b=50)
            )
            st.plotly_chart(fig_barras, use_container_width=True)
        
        # Gráfico 2: Intervalo (min-max)
        with col_graf2:
            fig_intervalo = go.Figure()
            
            regioes_lista = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
            cores_dict = dict(zip(regioes_lista, ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']))
            
            for _, row in stats_regioes.iterrows():
                regiao = row['REGIAO']
                cor = cores_dict.get(regiao, '#999999')
                
                # Linha min-max
                fig_intervalo.add_trace(go.Scatter(
                    x=[regiao, regiao],
                    y=[row['Mín'], row['Máx']],
                    mode='lines',
                    line=dict(color=cor, width=4),
                    showlegend=False
                ))
                
                # Ponto da média
                fig_intervalo.add_trace(go.Scatter(
                    x=[regiao],
                    y=[row['Média']],
                    mode='markers',
                    marker=dict(size=12, color=cor, symbol='diamond', line=dict(width=2, color='white')),
                    showlegend=False
                ))
            
            fig_intervalo.update_layout(
                height=350,
                xaxis_title="Região",
                yaxis_title="Acesso à Internet (%)",
                yaxis=dict(range=[0, 105]),
                template='plotly_dark',
                margin=dict(l=50, r=50, t=30, b=50)
            )
            st.plotly_chart(fig_intervalo, use_container_width=True)
        
        # Tabela resumida
        st.markdown("---")
        st.markdown("### 📋 Resumo Estatístico")
        
        tabela_exib = stats_regioes[['REGIAO', 'Média', 'Mín', 'Máx', 'Desvio', 'N']].round(2)
        tabela_exib.columns = ['Região', 'Média (%)', 'Mín (%)', 'Máx (%)', 'Desvio Padrão', 'N Registros']
        
        st.dataframe(tabela_exib, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Nenhum dado disponível para os filtros selecionados")

# ============================================================================
# Tab 3: Evolução Temporal
# ============================================================================

with tab3:
    st.subheader("Evolução do Acesso à Internet (2021-2024)")
    
    # Pega o Brasil e as seleções
    df_evolucao = pd.DataFrame()
    
    separar_por_instrucao = st.checkbox('Separar séries por nível de instrução', value=False)
    # Brasil
    df_brasil_tempo = df_original[df_original['LOCALIZACAO'] == 'Brasil'].sort_values('ANO')
    if not df_brasil_tempo.empty:
        if separar_por_instrucao and instrucao_selecionada:
            for instr in instrucao_selecionada:
                df_tmp = df_brasil_tempo[df_brasil_tempo['INSTRUCAO'] == instr][['ANO', 'PERCENTUAL']].copy()
                df_tmp['Série'] = f"Brasil - {instr}"
                df_evolucao = pd.concat([df_evolucao, df_tmp])
        else:
            df_tmp = df_brasil_tempo.copy()
            if 'INSTRUCAO' in df_tmp.columns and instrucao_selecionada:
                df_tmp = df_tmp[df_tmp['INSTRUCAO'].isin(instrucao_selecionada)]
            df_evolucao = pd.concat([df_evolucao, df_tmp[['ANO', 'PERCENTUAL']].assign(Série='Brasil')])
    
    # Média das regiões selecionadas
    df_regiao_tempo = df_original[
        (df_original['LOCALIZACAO'].isin(['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'])) &
        (df_original['REGIAO'].isin(regiao_selecionada if regiao_selecionada else []))
    ]
    if not df_regiao_tempo.empty:
        if separar_por_instrucao and instrucao_selecionada:
            for instr in instrucao_selecionada:
                df_tmp = df_regiao_tempo[df_regiao_tempo['INSTRUCAO'] == instr].groupby('ANO')['PERCENTUAL'].mean().reset_index()
                df_tmp['Série'] = f"Média Regiões - {instr}"
                df_evolucao = pd.concat([df_evolucao, df_tmp])
        else:
            df_tmp = df_regiao_tempo.copy()
            if 'INSTRUCAO' in df_tmp.columns and instrucao_selecionada:
                df_tmp = df_tmp[df_tmp['INSTRUCAO'].isin(instrucao_selecionada)]
            df_media_regiao = df_tmp.groupby('ANO')['PERCENTUAL'].mean().reset_index()
            df_media_regiao['Série'] = 'Média (Regiões Selecionadas)'
            df_evolucao = pd.concat([df_evolucao, df_media_regiao])
    
    # Média das UFs selecionadas
    df_uf_tempo = df_original[
        (df_original['UF'].isin(uf_selecionada if uf_selecionada else [])) &
        (~df_original['LOCALIZACAO'].isin(['Brasil', 'Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']))
    ]
    if not df_uf_tempo.empty:
        if separar_por_instrucao and instrucao_selecionada:
            for instr in instrucao_selecionada:
                df_tmp = df_uf_tempo[df_uf_tempo['INSTRUCAO'] == instr].groupby('ANO')['PERCENTUAL'].mean().reset_index()
                df_tmp['Série'] = f"Média UFs - {instr}"
                df_evolucao = pd.concat([df_evolucao, df_tmp])
        else:
            df_tmp = df_uf_tempo.copy()
            if 'INSTRUCAO' in df_tmp.columns and instrucao_selecionada:
                df_tmp = df_tmp[df_tmp['INSTRUCAO'].isin(instrucao_selecionada)]
            df_media_uf = df_tmp.groupby('ANO')['PERCENTUAL'].mean().reset_index()
            df_media_uf['Série'] = 'Média (UFs Selecionadas)'
            df_evolucao = pd.concat([df_evolucao, df_media_uf])
    
    if not df_evolucao.empty:
        # Pivota para gráfico de linha
        df_pivot = df_evolucao.pivot(index='ANO', columns='Série', values='PERCENTUAL')
        st.line_chart(df_pivot, height=400, use_container_width=True)
        
        st.markdown("**Dados da Série Temporal**")
        st.dataframe(df_pivot, use_container_width=True)
    else:
        st.info("Nenhum dado disponível para evolução temporal")

# ============================================================================
# Tab 4: Dados Brutos
# ============================================================================

with tab4:
    st.subheader("Visualização dos Dados Brutos")
    
    # Opções de coluna para exibição
    all_cols = ['REGIAO', 'UF', 'LOCALIZACAO', 'ANO', 'PERCENTUAL']
    default_cols = ['LOCALIZACAO', 'ANO', 'PERCENTUAL']
    
    cols_shown = st.multiselect(
        "Selecione as colunas para exibir",
        options=all_cols,
        default=default_cols
    )
    
    if cols_shown:
        st.dataframe(
            df_filtrado[cols_shown],
            use_container_width=True,
            height=400
        )
        
        # Download do CSV
        csv = df_filtrado[cols_shown].to_csv(index=False)
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name=f"ibge_tabela7336_{ano_selecionado}.csv",
            mime="text/csv"
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

