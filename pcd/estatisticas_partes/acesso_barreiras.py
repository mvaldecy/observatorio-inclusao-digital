import pandas as pd


class EstatisticasAcessoBarreirasMixin:
    def percentual_acesso_internet(self) -> float:
        if 'tem_internet' not in self.df.columns:
            return None

        total = len(self.df)
        if total == 0:
            return 0.0

        com_internet = self.df['tem_internet'].sum()
        return (com_internet / total) * 100

    def acesso_por_tipo_deficiencia(self) -> pd.DataFrame:
        if 'tipo_deficiencia' not in self.df.columns or 'tem_internet' not in self.df.columns:
            return pd.DataFrame()

        resultado = self.df.groupby('tipo_deficiencia').agg({'tem_internet': ['sum', 'count']})
        resultado.columns = ['com_internet', 'total']
        resultado['percentual'] = (resultado['com_internet'] / resultado['total']) * 100
        return resultado.sort_values('percentual', ascending=False).reset_index()

    def acesso_por_regiao(self) -> pd.DataFrame:
        if 'regiao' not in self.df.columns or 'tem_internet' not in self.df.columns:
            return pd.DataFrame()

        resultado = self.df.groupby('regiao').agg({'tem_internet': ['sum', 'count']})
        resultado.columns = ['com_internet', 'total']
        resultado['percentual'] = (resultado['com_internet'] / resultado['total']) * 100
        return resultado.sort_values('percentual', ascending=False).reset_index()

    def acesso_por_area(self) -> pd.DataFrame:
        if 'area' not in self.df.columns or 'tem_internet' not in self.df.columns:
            return pd.DataFrame()

        resultado = self.df.groupby('area').agg({'tem_internet': ['sum', 'count']})
        resultado.columns = ['com_internet', 'total']
        resultado['percentual'] = (resultado['com_internet'] / resultado['total']) * 100
        return resultado.reset_index()

    def distribuicao_dispositivos(self) -> pd.Series:
        dispositivos = {}

        if 'tem_computador' in self.df.columns:
            dispositivos['Computador'] = self.df['tem_computador'].sum()
        if 'tem_smartphone' in self.df.columns:
            dispositivos['Smartphone'] = self.df['tem_smartphone'].sum()
        if 'tem_tablet' in self.df.columns:
            dispositivos['Tablet'] = self.df['tem_tablet'].sum()

        return pd.Series(dispositivos)

    def percentual_apenas_smartphone(self) -> float:
        if not all(col in self.df.columns for col in ['tem_smartphone', 'tem_computador', 'tem_internet']):
            return None

        apenas_smartphone = self.df[
            (self.df['tem_internet'] == True)
            & (self.df['tem_smartphone'] == True)
            & (self.df['tem_computador'] == False)
        ]

        total_com_internet = self.df['tem_internet'].sum()
        if total_com_internet == 0:
            return 0.0

        return (len(apenas_smartphone) / total_com_internet) * 100

    def principais_barreiras(self, top_n: int = 5) -> pd.Series:
        if 'tipo_barreira' not in self.df.columns:
            return pd.Series()
        return self.df['tipo_barreira'].value_counts().head(top_n)

    def percentual_com_barreiras(self) -> float:
        if 'encontra_barreiras' not in self.df.columns:
            return None

        total = len(self.df)
        if total == 0:
            return 0.0

        com_barreiras = self.df['encontra_barreiras'].sum()
        return (com_barreiras / total) * 100

    def uso_tecnologia_assistiva(self) -> dict:
        stats = {}

        if 'usa_tecnologia_assistiva' in self.df.columns:
            total = len(self.df)
            usa = self.df['usa_tecnologia_assistiva'].sum()
            stats['percentual_usa'] = (usa / total) * 100 if total > 0 else 0
            stats['total_usa'] = usa
            stats['total'] = total

        if 'tipo_tecnologia_assistiva' in self.df.columns:
            stats['tipos_mais_usados'] = self.df['tipo_tecnologia_assistiva'].value_counts().to_dict()

        return stats
