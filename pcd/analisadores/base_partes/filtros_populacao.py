import pandas as pd


class BaseFiltrosPopulacaoMixin:
    def filtrar_por_variacao_populacao(self, positiva: bool = True):
        if 'variacao_populacao' not in self.df.columns:
            print("Coluna 'variacao_populacao' não encontrada")
            return self

        if positiva:
            self.df = self.df[self.df['variacao_populacao'] > 0]
            print(f"Filtrado municípios com CRESCIMENTO: {len(self.df):,} municípios")
        else:
            self.df = self.df[self.df['variacao_populacao'] < 0]
            print(f"Filtrado municípios com DECRESCIMENTO: {len(self.df):,} municípios")
        return self

    def filtrar_por_taxa_alfabetizacao(self, min_taxa: float = None, max_taxa: float = None):
        if 'taxa_alfabetizacao_geral' not in self.df.columns:
            print("Coluna 'taxa_alfabetizacao_geral' não encontrada")
            return self

        if min_taxa is not None:
            self.df = self.df[self.df['taxa_alfabetizacao_geral'] >= min_taxa]
        if max_taxa is not None:
            self.df = self.df[self.df['taxa_alfabetizacao_geral'] <= max_taxa]

        print(f"Filtrado por taxa de alfabetização: {len(self.df):,} municípios")
        return self

    def get_maiores_populacoes(self, n: int = 10):
        if 'populacao_2022' not in self.df.columns:
            print("Coluna 'populacao_2022' não encontrada")
            return pd.DataFrame()

        return self.df.nlargest(n, 'populacao_2022')[['municipio', 'populacao_2022', 'taxa_alfabetizacao_geral']]

    def get_menores_taxas_alfabetizacao(self, n: int = 10):
        if 'taxa_alfabetizacao_geral' not in self.df.columns:
            print("Coluna 'taxa_alfabetizacao_geral' não encontrada")
            return pd.DataFrame()

        return self.df.nsmallest(n, 'taxa_alfabetizacao_geral')[['municipio', 'taxa_alfabetizacao_geral', 'populacao_2022']]

    def get_distribuicao_racial(self):
        colunas_pop = ['pop_branca', 'pop_preta', 'pop_amarela', 'pop_parda', 'pop_indigena']

        if not all(col in self.df.columns for col in colunas_pop):
            print("Colunas de população por raça/cor não encontradas")
            return pd.DataFrame()

        return pd.DataFrame({
            'Branca': [self.df['pop_branca'].sum()],
            'Preta': [self.df['pop_preta'].sum()],
            'Amarela': [self.df['pop_amarela'].sum()],
            'Parda': [self.df['pop_parda'].sum()],
            'Indígena': [self.df['pop_indigena'].sum()]
        })

    def get_disparidades_raciais_alfabetizacao(self):
        colunas_taxa = ['taxa_alfa_branca', 'taxa_alfa_preta', 'taxa_alfa_parda']

        if not all(col in self.df.columns for col in colunas_taxa):
            print("Colunas de taxa de alfabetização por raça/cor não encontradas")
            return pd.DataFrame()

        return pd.DataFrame({
            'Raça/Cor': ['Branca', 'Preta', 'Parda'],
            'Taxa Média': [
                self.df['taxa_alfa_branca'].mean(),
                self.df['taxa_alfa_preta'].mean(),
                self.df['taxa_alfa_parda'].mean()
            ],
            'Taxa Mínima': [
                self.df['taxa_alfa_branca'].min(),
                self.df['taxa_alfa_preta'].min(),
                self.df['taxa_alfa_parda'].min()
            ],
            'Taxa Máxima': [
                self.df['taxa_alfa_branca'].max(),
                self.df['taxa_alfa_preta'].max(),
                self.df['taxa_alfa_parda'].max()
            ]
        })
