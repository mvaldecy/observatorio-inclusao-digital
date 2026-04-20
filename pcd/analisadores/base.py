from pcd.analisadores.base_partes import (
    BaseFiltrosPerfilMixin,
    BaseFiltrosPopulacaoMixin,
    BaseUtilitariosMixin,
)


class AnalisadorPCDBase(
    BaseFiltrosPopulacaoMixin,
    BaseFiltrosPerfilMixin,
    BaseUtilitariosMixin,
):
    """Métodos base e filtros gerais do analisador PCD."""

    def __init__(self, df=None, ano: int = 2024):
        self.ano = ano

        if df is None:
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_pcd(ano)\n"
                "do módulo streamlit.utils.data_loader"
            )

        self.df = df.copy()
        self.df_original = df.copy()
        print(f"Analisador PCD carregado: {len(self.df):,} municípios, {len(self.df.columns)} colunas")

    def reset_filtros(self):
        self.df = self.df_original.copy()
        print(f"Filtros resetados. Municípios: {len(self.df):,}")
        return self

    def filtrar_por_municipio(self, municipio: str):
        if 'municipio' not in self.df.columns:
            print("Coluna 'municipio' não encontrada")
            return self

        self.df = self.df[self.df['municipio'].str.contains(municipio, case=False, na=False)]
        print(f"Filtrado para município '{municipio}': {len(self.df):,} registros")
        return self
