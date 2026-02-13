"""
Componentes UI reutilizáveis para visualização IBGE (Tabela 7336)
"""
from __future__ import annotations

import streamlit as st
import pandas as pd


def aplicar_configuracoes():
    """Aplicações de configuração (placeholder compatível com outros componentes)"""
    st.set_option('deprecation.showPyplotGlobalUse', False)


def renderizar_filtros(df: pd.DataFrame):
    """Renderiza filtros laterais específicos para IBGE e retorna seleção.

    Retorna: (anos, regioes, ufs, instrucoes)
    """
    st.sidebar.markdown('---')
    st.sidebar.markdown('## 🔎 Filtros IBGE')

    anos = sorted(df['ANO'].unique()) if 'ANO' in df.columns else []
    regioes = sorted(df['REGIAO'].unique()) if 'REGIAO' in df.columns else []
    ufs = sorted(df['UF'].unique()) if 'UF' in df.columns else []
    instrucoes = sorted(df['INSTRUCAO'].unique()) if 'INSTRUCAO' in df.columns else []

    ano = st.sidebar.selectbox('Ano', options=anos, index=len(anos)-1 if anos else 0)
    regioes_sel = st.sidebar.multiselect('Região(ões)', options=regioes, default=['Nordeste'] if 'Nordeste' in regioes else [])
    ufs_sel = st.sidebar.multiselect('UF(s)', options=ufs, default=['PI'] if 'PI' in ufs else [])
    instrucoes_sel = st.sidebar.multiselect('Nível(s) de instrução', options=instrucoes, default=instrucoes if instrucoes else [])

    return ano, regioes_sel, ufs_sel, instrucoes_sel


def renderizar_comparativo_brasil(df: pd.DataFrame, instrucoes_sel: list[str]):
    """Mostra métricas fixas: Brasil, Nordeste, Piauí considerando níveis selecionados."""
    cols = st.columns(4)
    def _valor(local):
        d = df[(df['LOCALIZACAO'] == local)]
        if instrucoes_sel and 'INSTRUCAO' in d.columns:
            d = d[d['INSTRUCAO'].isin(instrucoes_sel)]
        if d.empty:
            return None
        return float(d['PERCENTUAL'].mean())

    v_b = _valor('Brasil')
    v_n = _valor('Nordeste')
    v_pi = _valor('Piauí')

    with cols[0]:
        if v_b is not None:
            st.metric('🇧🇷 Brasil', f"{v_b:.1f}%")
        else:
            st.write('Brasil: —')
    with cols[1]:
        if v_n is not None:
            st.metric('🌎 Nordeste', f"{v_n:.1f}%")
        else:
            st.write('Nordeste: —')
    with cols[2]:
        if v_pi is not None:
            st.metric('📍 Piauí (PI)', f"{v_pi:.1f}%")
        else:
            st.write('Piauí: —')
    with cols[3]:
        st.caption('Filtro aplicado: Níveis de instrução')
        st.write(', '.join(instrucoes_sel) if instrucoes_sel else 'Todos')


def renderizar_analise_instrucao(df: pd.DataFrame):
    """Renderiza uma tabela e gráfico com distribuição por nível de instrução."""
    st.markdown('### Distribuição por Nível de Instrução')
    if 'INSTRUCAO' not in df.columns:
        st.info('Coluna INSTRUCAO não disponível neste dataset')
        return

    # Agrupa por instrução e calcula média do percentual
    resumo = df.groupby('INSTRUCAO')['PERCENTUAL'].mean().sort_values()
    st.bar_chart(resumo.to_frame('PERCENTUAL'), use_container_width=True, height=350)
    st.dataframe(resumo.reset_index().rename(columns={'index':'INSTRUCAO','PERCENTUAL':'PERCENTUAL'}), use_container_width=True)


def renderizar_resumo_filtros(df_original: pd.DataFrame, df_filtrado: pd.DataFrame):
    st.markdown('### Resumo dos Filtros')
    c1, c2, c3 = st.columns(3)
    c1.metric('Registros originais', f"{len(df_original):,}")
    c2.metric('Registros filtrados', f"{len(df_filtrado):,}")
    instr = ', '.join(sorted(df_filtrado['INSTRUCAO'].unique())) if 'INSTRUCAO' in df_filtrado.columns else '—'
    c3.markdown(f"**Níveis de instrução:** {instr}")
