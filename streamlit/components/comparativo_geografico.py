"""
Componente reutilizável para comparação geográfica (Brasil/Nordeste/Piauí)
"""
import streamlit as st
import pandas as pd
from typing import List, Optional, Dict


class ComparativoGeografico:
    """Componente para comparação Brasil/Nordeste/Piauí"""

    def __init__(self, analisador, meta_class):
        """
        Inicializa o componente

        Args:
            analisador: Instância do analisador (domicílios ou indivíduos)
            meta_class: Classe de metadados (Metadados ou MetadadosIndividuos)
        """
        self.analisador = analisador
        self.meta_class = meta_class

    def renderizar(self, indicador, filtros_extras: List = None, is_multiple: bool = False):
        """
        Renderiza comparativo completo

        Args:
            indicador: Campo ou lista de campos para análise
            filtros_extras: Lista de filtros adicionais a aplicar
            is_multiple: Se é análise múltipla de indicadores
        """
        st.markdown("### 📍 Comparação: Brasil | Nordeste | Piauí")

        # Verificar disponibilidade de COD_UF
        tem_cod_uf = 'COD_UF' in self.analisador.df.columns

        # Analisar regiões
        resultados = self._analisar_regioes(indicador, filtros_extras, tem_cod_uf)

        # Renderizar cards
        self._renderizar_cards(resultados, is_multiple, tem_cod_uf)

        # Renderizar consolidado
        self._renderizar_consolidado(resultados, indicador, tem_cod_uf)

    def _analisar_regioes(self, indicador, filtros_extras, tem_cod_uf) -> Dict[str, Dict]:
        """
        Analisa indicador para Brasil, Nordeste e Piauí

        Returns:
            Dicionário com resultados por região
        """
        resultados = {}

        # Brasil
        df_brasil = self.analisador.df.copy()
        if filtros_extras:
            for f in filtros_extras:
                if f is not None and f.column in df_brasil.columns:
                    df_brasil = df_brasil[df_brasil[f.column] == f]
        resultados['brasil'] = {
            'df': df_brasil,
            'resultado': self.analisador.analisar_indicador(indicador, df_contexto=df_brasil)
        }

        # Nordeste
        df_nordeste = self.analisador.df.copy()
        if 'COD_REGIAO_2' in df_nordeste.columns:
            df_nordeste = df_nordeste[
                df_nordeste['COD_REGIAO_2'] == self.meta_class.COD_REGIAO_2.NORDESTE
            ]
            if filtros_extras:
                for f in filtros_extras:
                    if f is not None and f.column in df_nordeste.columns:
                        df_nordeste = df_nordeste[df_nordeste[f.column] == f]
            resultados['nordeste'] = {
                'df': df_nordeste,
                'resultado': self.analisador.analisar_indicador(indicador, df_contexto=df_nordeste)
            }

        # Piauí (se disponível)
        if tem_cod_uf:
            df_piaui = self.analisador.df.copy()
            df_piaui = df_piaui[df_piaui['COD_UF'] == self.meta_class.COD_UF.PIAUI]
            if filtros_extras:
                for f in filtros_extras:
                    if f is not None and f.column in df_piaui.columns:
                        df_piaui = df_piaui[df_piaui[f.column] == f]
            resultados['piaui'] = {
                'df': df_piaui,
                'resultado': self.analisador.analisar_indicador(indicador, df_contexto=df_piaui)
            }

        return resultados

    def _renderizar_cards(self, resultados: Dict, is_multiple: bool, tem_cod_uf: bool):
        """Renderiza cards individuais para cada região"""
        regioes_config = [
            ('brasil', '🇧🇷 Brasil'),
            ('nordeste', '🌴 Nordeste'),
        ]

        if tem_cod_uf:
            regioes_config.append(('piaui', '🏛️ Piauí'))
            cols = st.columns(3)
        else:
            cols = st.columns(2)
            st.info("ℹ️ Dados por estado disponíveis apenas a partir de 2025")

        for idx, (key, titulo) in enumerate(regioes_config):
            if key in resultados:
                with cols[idx]:
                    self._renderizar_card_regiao(
                        titulo,
                        resultados[key]['df'],
                        resultados[key]['resultado'],
                        is_multiple
                    )

    def _renderizar_card_regiao(self, titulo: str, df: pd.DataFrame,
                                resultado: Optional[pd.DataFrame], is_multiple: bool):
        """Renderiza card individual de uma região"""
        st.markdown(f"#### {titulo}")

        if resultado is not None and len(resultado) > 0:
            st.metric("📊 Registros", f"{len(df):,}")

            # KPI principal
            if not is_multiple:
                sim_row = resultado[resultado['Descrição'].str.lower() == 'sim']
                if not sim_row.empty:
                    st.metric("✅ Sim", sim_row['Percentual'].values[0])
                else:
                    # Mostrar primeira categoria
                    st.metric("📈 Principal", resultado.iloc[0]['Percentual'])
                    st.caption(resultado.iloc[0]['Descrição'])
            else:
                chart_data = resultado.copy()
                chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
                top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                st.metric("🏆 Maior", f"{top_row['Percentual']}")
                st.caption(top_row['Descrição'])

            # Gráfico
            chart_data = resultado.copy()
            chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
            st.bar_chart(chart_data, x="Descrição", y="Percentual_Num", height=300)

            with st.expander("📋 Ver Dados"):
                st.dataframe(resultado, width='stretch')
        else:
            st.warning("⚠️ Sem dados disponíveis")

    def _renderizar_consolidado(self, resultados: Dict, indicador, tem_cod_uf: bool):
        """Renderiza visão consolidada"""
        st.markdown("---")
        st.markdown("### 📊 Visão Consolidada")

        df_comp_list = []

        # Brasil e Nordeste
        for regiao_key, regiao_nome in [('brasil', 'Brasil'), ('nordeste', 'Nordeste')]:
            if regiao_key in resultados:
                resultado = resultados[regiao_key]['resultado']
                if resultado is not None and len(resultado) > 0:
                    for _, row in resultado.iterrows():
                        df_comp_list.append({
                            'Região': regiao_nome,
                            'Categoria': row['Descrição'],
                            'Total': row['Total'],
                            'Percentual': float(row['Percentual'].replace('%', ''))
                        })

        # Piauí
        if tem_cod_uf and 'piaui' in resultados:
            resultado = resultados['piaui']['resultado']
            if resultado is not None and len(resultado) > 0:
                for _, row in resultado.iterrows():
                    df_comp_list.append({
                        'Região': 'Piauí',
                        'Categoria': row['Descrição'],
                        'Total': row['Total'],
                        'Percentual': float(row['Percentual'].replace('%', ''))
                    })

        if df_comp_list:
            df_comparativo = pd.DataFrame(df_comp_list)

            # Criar pivot para visualização
            df_pivot = df_comparativo.pivot(index='Categoria', columns='Região', values='Percentual')

            st.dataframe(df_pivot.style.format("{:.2f}%"), width='stretch')

            # Gráfico comparativo
            st.bar_chart(df_pivot, height=400)

            # Botão download
            csv_comp = df_comparativo.to_csv(index=False).encode('utf-8')
            indicador_str = indicador if isinstance(indicador, str) else '_'.join(indicador[:3])
            st.download_button(
                label="📥 Download Comparativo (CSV)",
                data=csv_comp,
                file_name=f"comparativo_{indicador_str}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Nenhum dado disponível para comparação")

