"""
Componente de Comparativo Geográfico para INEP
Análise: Brasil | Nordeste | Piauí
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List, Optional, Dict


class ComparativoGeograficoINEP:
    """Componente para comparação geográfica de dados do INEP"""

    def __init__(self, analisador):
        """
        Inicializa o componente

        Args:
            analisador: Instância do AnalisadorINEP
        """
        self.analisador = analisador

    def renderizar(self, indicador, filtros_extras: Dict = None, is_multiple: bool = False):
        """
        Renderiza comparativo completo Brasil/Nordeste/Piauí

        Args:
            indicador: Campo ou lista de campos para análise
            filtros_extras: Dicionário de filtros adicionais (ex: {'TP_DEPENDENCIA': 3})
            is_multiple: Se é análise múltipla de indicadores
        """
        st.markdown("### 📍 Comparação Geográfica: Brasil | Nordeste | Piauí")

        # Analisar regiões
        resultados = self._analisar_regioes(indicador, filtros_extras)

        # Renderizar cards
        self._renderizar_cards(resultados, is_multiple)

        # Renderizar consolidado
        self._renderizar_consolidado(resultados, indicador, is_multiple)

    def _analisar_regioes(self, indicador, filtros_extras) -> Dict[str, Dict]:
        """
        Analisa indicador para Brasil, Nordeste e Piauí

        Returns:
            Dicionário com resultados por região
        """
        resultados = {}

        # Brasil (todos os dados)
        df_brasil = self.analisador.df.copy()
        if filtros_extras:
            for col, valor in filtros_extras.items():
                if col in df_brasil.columns:
                    if isinstance(valor, list):
                        df_brasil = df_brasil[df_brasil[col].isin(valor)]
                    else:
                        df_brasil = df_brasil[df_brasil[col] == valor]

        resultados['brasil'] = {
            'df': df_brasil,
            'label': '🇧🇷 Brasil',
            'total': len(df_brasil)
        }

        # Nordeste (CO_REGIAO == 2)
        df_nordeste = self.analisador.df.copy()
        if 'CO_REGIAO' in df_nordeste.columns:
            df_nordeste = df_nordeste[df_nordeste['CO_REGIAO'] == 2]
            if filtros_extras:
                for col, valor in filtros_extras.items():
                    if col in df_nordeste.columns:
                        if isinstance(valor, list):
                            df_nordeste = df_nordeste[df_nordeste[col].isin(valor)]
                        else:
                            df_nordeste = df_nordeste[df_nordeste[col] == valor]

            resultados['nordeste'] = {
                'df': df_nordeste,
                'label': '🌴 Nordeste',
                'total': len(df_nordeste)
            }
        else:
            resultados['nordeste'] = None

        # Piauí (CO_UF == 22)
        df_piaui = self.analisador.df.copy()
        if 'CO_UF' in df_piaui.columns:
            df_piaui = df_piaui[df_piaui['CO_UF'] == 22]
            if filtros_extras:
                for col, valor in filtros_extras.items():
                    if col in df_piaui.columns:
                        if isinstance(valor, list):
                            df_piaui = df_piaui[df_piaui[col].isin(valor)]
                        else:
                            df_piaui = df_piaui[df_piaui[col] == valor]

            resultados['piaui'] = {
                'df': df_piaui,
                'label': '🏛️ Piauí',
                'total': len(df_piaui)
            }
        else:
            resultados['piaui'] = None

        # Analisar indicador para cada região
        from inep.analisador_inep import AnalisadorINEP

        for regiao_key, dados in resultados.items():
            if dados is not None:
                # Criar analisador temporário para cada região
                ano = self.analisador.ano
                analisador_temp = AnalisadorINEP(df=dados['df'], ano=ano)
                resultado = analisador_temp.analisar_indicador(indicador)
                dados['resultado'] = resultado

        return resultados

    def _renderizar_cards(self, resultados: Dict, is_multiple: bool):
        """Renderiza cards individuais para cada região"""
        # Verificar quais regiões estão disponíveis
        regioes_disponiveis = [k for k, v in resultados.items() if v is not None]

        if len(regioes_disponiveis) == 0:
            st.warning("⚠️ Nenhuma região disponível para comparação")
            return

        # Criar colunas dinamicamente
        cols = st.columns(len(regioes_disponiveis))

        for idx, regiao_key in enumerate(regioes_disponiveis):
            dados = resultados[regiao_key]
            with cols[idx]:
                self._renderizar_card_regiao(
                    dados['label'],
                    dados['df'],
                    dados.get('resultado'),
                    is_multiple
                )

    def _renderizar_card_regiao(self, titulo: str, df: pd.DataFrame,
                                resultado: Optional[pd.DataFrame], is_multiple: bool):
        """Renderiza card individual de uma região"""
        st.markdown(f"#### {titulo}")

        if resultado is not None and not resultado.empty:
            st.metric("🏫 Total de Escolas", f"{len(df):,}")

            # KPI principal
            if not is_multiple:
                # Tentar encontrar "Sim"
                if 'Descrição' in resultado.columns:
                    sim_row = resultado[resultado['Descrição'].str.contains('Sim', case=False, na=False)]
                    if not sim_row.empty and 'Percentual' in sim_row.columns:
                        st.metric("✅ Sim", sim_row['Percentual'].values[0])
                    else:
                        # Mostrar primeira categoria
                        if 'Percentual' in resultado.columns:
                            st.metric("📈 Principal", resultado.iloc[0]['Percentual'])
                            if 'Descrição' in resultado.columns:
                                st.caption(resultado.iloc[0]['Descrição'])
            else:
                # Análise múltipla - mostrar o maior valor
                if 'Percentual' in resultado.columns:
                    chart_data = resultado.copy()
                    chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                    top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                    st.metric("🏆 Maior", f"{top_row['Percentual']}")
                    if 'Descrição' in top_row:
                        st.caption(top_row['Descrição'])

            # Gráfico de barras
            if 'Descrição' in resultado.columns and 'Percentual' in resultado.columns:
                chart_data = resultado.copy()
                chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)

                fig = px.bar(
                    chart_data,
                    x='Descrição',
                    y='Percentual_Num',
                    text='Percentual',
                    color='Percentual_Num',
                    color_continuous_scale='Viridis'
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    showlegend=False,
                    height=250,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title="",
                    yaxis_title="Percentual (%)"
                )
                st.plotly_chart(fig, width='stretch')

            # Tabela de dados (expandível)
            with st.expander("📋 Ver Detalhes"):
                st.dataframe(resultado, width='stretch', hide_index=True)
        else:
            st.warning("Sem dados disponíveis")

    def _renderizar_consolidado(self, resultados: Dict, indicador, is_multiple: bool):
        """Renderiza comparativo consolidado entre as regiões"""
        st.markdown("---")
        st.markdown("### 📊 Comparativo Consolidado")

        # Verificar quais regiões têm dados
        regioes_com_dados = {k: v for k, v in resultados.items()
                            if v is not None and v.get('resultado') is not None
                            and not v['resultado'].empty}

        if not regioes_com_dados:
            st.info("ℹ️ Nenhum dado disponível para comparação")
            return

        # Criar DataFrame consolidado
        dados_consolidados = []

        for regiao_key, dados in regioes_com_dados.items():
            resultado = dados['resultado']

            if is_multiple:
                # Análise múltipla - agregar por indicador
                for _, row in resultado.iterrows():
                    dados_consolidados.append({
                        'Região': dados['label'],
                        'Indicador': row.get('Descrição', row.get('Indicador', '')),
                        'Total': row.get('Total', 0),
                        'Percentual': row.get('Percentual', '0%'),
                        'Percentual_Num': float(str(row.get('Percentual', '0%')).replace('%', ''))
                    })
            else:
                # Análise simples - agregar por categoria
                for _, row in resultado.iterrows():
                    dados_consolidados.append({
                        'Região': dados['label'],
                        'Categoria': row.get('Descrição', ''),
                        'Total': row.get('Total', 0),
                        'Percentual': row.get('Percentual', '0%'),
                        'Percentual_Num': float(str(row.get('Percentual', '0%')).replace('%', ''))
                    })

        if dados_consolidados:
            df_consolidado = pd.DataFrame(dados_consolidados)

            # Tabela comparativa
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("#### 📋 Tabela Comparativa")
                st.dataframe(df_consolidado, width='stretch', hide_index=True)

            with col2:
                st.markdown("#### 📈 Resumo")
                for regiao_key, dados in regioes_com_dados.items():
                    st.metric(
                        dados['label'],
                        f"{dados['total']:,} escolas"
                    )

            # Gráfico comparativo
            st.markdown("#### 📊 Visualização Comparativa")

            if is_multiple:
                # Gráfico agrupado por indicador
                fig = px.bar(
                    df_consolidado,
                    x='Região',
                    y='Percentual_Num',
                    color='Indicador',
                    barmode='group',
                    text='Percentual',
                    title='Comparação entre Regiões por Indicador',
                    labels={'Percentual_Num': 'Percentual (%)'}
                )
            else:
                # Gráfico agrupado por categoria
                fig = px.bar(
                    df_consolidado,
                    x='Região',
                    y='Percentual_Num',
                    color='Categoria',
                    barmode='group',
                    text='Percentual',
                    title='Comparação entre Regiões por Categoria',
                    labels={'Percentual_Num': 'Percentual (%)'}
                )

            fig.update_traces(textposition='outside')
            fig.update_layout(height=500, xaxis_tickangle=-45)
            st.plotly_chart(fig, width='stretch')

            # Download
            csv = df_consolidado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar Comparativo (CSV)",
                data=csv,
                file_name=f"comparativo_geografico_inep.csv",
                mime="text/csv"
            )
        else:
            st.info("ℹ️ Nenhum dado disponível para consolidação")

