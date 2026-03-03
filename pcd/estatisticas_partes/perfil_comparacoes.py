import pandas as pd


class EstatisticasPerfilComparacoesMixin:
    def distribuicao_por_faixa_etaria(self) -> pd.DataFrame:
        if 'faixa_etaria' not in self.df.columns:
            return pd.DataFrame()

        cols_agg = {'faixa_etaria': 'count'}
        if 'tem_internet' in self.df.columns:
            cols_agg['tem_internet'] = 'sum'

        resultado = self.df.groupby('faixa_etaria').agg(cols_agg)
        resultado.columns = ['total', 'com_internet'] if 'tem_internet' in self.df.columns else ['total']

        if 'com_internet' in resultado.columns:
            resultado['percentual_acesso'] = (resultado['com_internet'] / resultado['total']) * 100

        return resultado.reset_index()

    def distribuicao_por_escolaridade(self) -> pd.DataFrame:
        if 'escolaridade' not in self.df.columns:
            return pd.DataFrame()

        cols_agg = {'escolaridade': 'count'}
        if 'tem_internet' in self.df.columns:
            cols_agg['tem_internet'] = 'sum'

        resultado = self.df.groupby('escolaridade').agg(cols_agg)
        resultado.columns = ['total', 'com_internet'] if 'tem_internet' in self.df.columns else ['total']

        if 'com_internet' in resultado.columns:
            resultado['percentual_acesso'] = (resultado['com_internet'] / resultado['total']) * 100

        return resultado.reset_index()

    def distribuicao_por_renda(self) -> pd.DataFrame:
        if 'renda_familiar' not in self.df.columns:
            return pd.DataFrame()

        cols_agg = {'renda_familiar': 'count'}
        if 'tem_internet' in self.df.columns:
            cols_agg['tem_internet'] = 'sum'

        resultado = self.df.groupby('renda_familiar').agg(cols_agg)
        resultado.columns = ['total', 'com_internet'] if 'tem_internet' in self.df.columns else ['total']

        if 'com_internet' in resultado.columns:
            resultado['percentual_acesso'] = (resultado['com_internet'] / resultado['total']) * 100

        return resultado.reset_index()

    def atividades_online_mais_comuns(self, top_n: int = 5) -> pd.Series:
        atividades = {}
        colunas_atividades = [
            'usa_redes_sociais',
            'usa_servicos_gov',
            'usa_ecommerce',
            'usa_educacao',
            'usa_trabalho'
        ]
        labels = {
            'usa_redes_sociais': 'Redes Sociais',
            'usa_servicos_gov': 'Serviços Governamentais',
            'usa_ecommerce': 'Compras Online',
            'usa_educacao': 'Educação',
            'usa_trabalho': 'Trabalho'
        }

        for col in colunas_atividades:
            if col in self.df.columns:
                atividades[labels.get(col, col)] = self.df[col].sum()

        serie = pd.Series(atividades).sort_values(ascending=False)
        return serie.head(top_n)

    def frequencia_uso_internet(self) -> pd.Series:
        if 'frequencia_uso' not in self.df.columns:
            return pd.Series()
        return self.df['frequencia_uso'].value_counts()

    def comparar_acesso_com_sem_deficiencia(self, df_completo: pd.DataFrame) -> dict:
        if 'tem_deficiencia' not in df_completo.columns or 'tem_internet' not in df_completo.columns:
            return {}

        pcd = df_completo[df_completo['tem_deficiencia'] == True]
        total_pcd = len(pcd)
        com_internet_pcd = pcd['tem_internet'].sum() if total_pcd > 0 else 0

        sem_def = df_completo[df_completo['tem_deficiencia'] == False]
        total_sem_def = len(sem_def)
        com_internet_sem_def = sem_def['tem_internet'].sum() if total_sem_def > 0 else 0

        return {
            'pcd': {
                'total': total_pcd,
                'com_internet': com_internet_pcd,
                'percentual': (com_internet_pcd / total_pcd * 100) if total_pcd > 0 else 0
            },
            'sem_deficiencia': {
                'total': total_sem_def,
                'com_internet': com_internet_sem_def,
                'percentual': (com_internet_sem_def / total_sem_def * 100) if total_sem_def > 0 else 0
            },
            'diferenca_percentual': (
                (com_internet_sem_def / total_sem_def * 100) - (com_internet_pcd / total_pcd * 100)
            ) if total_pcd > 0 and total_sem_def > 0 else 0
        }

    def resumo_geral(self) -> dict:
        resumo = {
            'total_registros': len(self.df),
            'percentual_acesso_internet': self.percentual_acesso_internet(),
            'percentual_com_barreiras': self.percentual_com_barreiras(),
            'percentual_usa_tecnologia_assistiva': None,
            'dispositivo_mais_comum': None,
            'barreira_principal': None
        }

        if 'usa_tecnologia_assistiva' in self.df.columns:
            total = len(self.df)
            usa = self.df['usa_tecnologia_assistiva'].sum()
            resumo['percentual_usa_tecnologia_assistiva'] = (usa / total * 100) if total > 0 else 0

        dispositivos = self.distribuicao_dispositivos()
        if not dispositivos.empty:
            resumo['dispositivo_mais_comum'] = dispositivos.idxmax()

        barreiras = self.principais_barreiras(top_n=1)
        if not barreiras.empty:
            resumo['barreira_principal'] = barreiras.index[0]

        return resumo
