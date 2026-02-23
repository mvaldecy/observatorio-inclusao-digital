"""
Componente de Filtros para INEP
"""
import streamlit as st
from .categorias_inep import UFS_BRASIL, REGIOES_BRASIL
from inep import get_valores, formatar_valor


class FiltroINEP:
    """Helper para construir filtros do INEP no sidebar"""

    def __init__(self, analisador):
        self.analisador = analisador
        self.filtros_aplicados = {}

        # Inicializar contador de reset no session_state
        if 'filtro_inep_reset_counter' not in st.session_state:
            st.session_state.filtro_inep_reset_counter = 0

    def render_filtros_geograficos(self):
        """Renderiza filtros geográficos"""
        st.sidebar.markdown("### 🗺️ Filtros Geográficos")

        # Filtro por Região
        regiao = st.sidebar.selectbox(
            "Região",
            options=[None] + list(REGIOES_BRASIL.keys()),
            format_func=lambda x: "Todas as regiões" if x is None else REGIOES_BRASIL[x],
            help="Filtre por região geográfica",
            key=f"regiao_{st.session_state.filtro_inep_reset_counter}"
        )

        if regiao:
            self.filtros_aplicados['CO_REGIAO'] = regiao

        # Filtro por UF
        uf = st.sidebar.selectbox(
            "Estado (UF)",
            options=[None] + list(UFS_BRASIL.keys()),
            format_func=lambda x: "Todos os estados" if x is None else f"{UFS_BRASIL[x]} ({x})",
            help="Filtre por estado",
            key=f"uf_{st.session_state.filtro_inep_reset_counter}"
        )

        if uf:
            self.filtros_aplicados['CO_UF'] = uf

    def render_filtros_caracterizacao(self):
        """Renderiza filtros de caracterização"""
        st.sidebar.markdown("### 🏫 Caracterização")

        # Dependência Administrativa
        dependencias = get_valores('TP_DEPENDENCIA')
        dep = st.sidebar.multiselect(
            "Dependência Administrativa",
            options=list(dependencias.keys()),
            format_func=lambda x: dependencias[x],
            help="Tipo de gestão da escola",
            key=f"dependencia_{st.session_state.filtro_inep_reset_counter}"
        )

        if dep:
            self.filtros_aplicados['TP_DEPENDENCIA'] = [int(d) for d in dep]

        # Localização
        localizacoes = get_valores('TP_LOCALIZACAO')
        loc = st.sidebar.selectbox(
            "Localização",
            options=[None] + list(localizacoes.keys()),
            format_func=lambda x: "Todas" if x is None else localizacoes[x],
            help="Localização da escola",
            key=f"localizacao_{st.session_state.filtro_inep_reset_counter}"
        )

        if loc:
            self.filtros_aplicados['TP_LOCALIZACAO'] = int(loc)

        # Localização Diferenciada (Território)
        loc_dif = get_valores('TP_LOCALIZACAO_DIFERENCIADA')
        territorio = st.sidebar.selectbox(
            "Território",
            options=[None] + list(loc_dif.keys()),
            format_func=lambda x: "Todos" if x is None else loc_dif[x],
            help="Localização diferenciada (indígena, quilombola, etc)",
            key=f"territorio_{st.session_state.filtro_inep_reset_counter}"
        )

        if territorio:
            self.filtros_aplicados['TP_LOCALIZACAO_DIFERENCIADA'] = int(territorio)

    def render_filtros_infraestrutura(self):
        """Renderiza filtros de infraestrutura"""
        with st.sidebar.expander("🌐 Infraestrutura", expanded=False):

            # Internet
            internet = st.checkbox(
                "Apenas com Internet",
                key=f"filtro_internet_{st.session_state.filtro_inep_reset_counter}"
            )
            if internet:
                self.filtros_aplicados['IN_INTERNET'] = 1

            # Laboratório
            lab = st.checkbox(
                "Apenas com Lab. de Informática",
                key=f"filtro_lab_{st.session_state.filtro_inep_reset_counter}"
            )
            if lab:
                self.filtros_aplicados['IN_LABORATORIO_INFORMATICA'] = 1

            # Banda Larga
            banda = st.checkbox(
                "Apenas com Banda Larga",
                key=f"filtro_banda_{st.session_state.filtro_inep_reset_counter}"
            )
            if banda:
                self.filtros_aplicados['IN_BANDA_LARGA'] = 1

    def render_filtros_situacao(self):
        """Renderiza filtros de situação"""
        with st.sidebar.expander("📊 Situação", expanded=False):

            situacoes = get_valores('TP_SITUACAO_FUNCIONAMENTO')
            sit = st.selectbox(
                "Situação de Funcionamento",
                options=[None] + list(situacoes.keys()),
                format_func=lambda x: "Todas" if x is None else situacoes[x],
                key=f"filtro_situacao_{st.session_state.filtro_inep_reset_counter}"
            )

            if sit:
                self.filtros_aplicados['TP_SITUACAO_FUNCIONAMENTO'] = int(sit)

    def aplicar_filtros(self):
        """Aplica todos os filtros ao analisador"""
        if self.filtros_aplicados:
            self.analisador.filtrar_dados(**self.filtros_aplicados)
            return True
        return False

    def mostrar_resumo_filtros(self):
        """Mostra resumo dos filtros aplicados"""
        if not self.filtros_aplicados:
            st.info("ℹ️ Nenhum filtro aplicado - mostrando todas as escolas")
            return

        st.markdown("### 🔍 Filtros Aplicados")

        cols = st.columns(len(self.filtros_aplicados))

        for i, (chave, valor) in enumerate(self.filtros_aplicados.items()):
            with cols[i]:
                # Obter label amigável
                from inep import get_label
                label = get_label(chave)

                # Formatar valor
                if isinstance(valor, list):
                    valor_str = ", ".join([formatar_valor(chave, v) for v in valor])
                else:
                    valor_str = formatar_valor(chave, valor)

                st.metric(label, valor_str)

    def render_todos_filtros(self):
        """Renderiza todos os grupos de filtros"""
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 🔍 Filtros")

        # Botão para limpar filtros no topo
        if st.sidebar.button("🗑️ Limpar Filtros", use_container_width=True, key="limpar_filtros_inep"):
            # Incrementar contador para resetar todos os widgets
            st.session_state.filtro_inep_reset_counter += 1

            # Limpar dicionário de filtros aplicados
            self.filtros_aplicados.clear()

            # Resetar DataFrame do analisador
            self.analisador.resetar_filtros()

            # Recarregar página
            st.rerun()

        st.sidebar.markdown("---")

        self.render_filtros_geograficos()
        self.render_filtros_caracterizacao()
        self.render_filtros_infraestrutura()
        self.render_filtros_situacao()

        st.sidebar.markdown("---")


        # Aplicar filtros
        filtros_ativos = self.aplicar_filtros()

        return filtros_ativos

