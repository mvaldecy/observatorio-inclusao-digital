import pandas as pd


class BaseUtilitariosMixin:
    def get_dados_atuais(self) -> pd.DataFrame:
        return self.df.copy()

    def contar_registros(self) -> int:
        return len(self.df)

    def listar_valores_unicos(self, coluna: str) -> list:
        if coluna not in self.df.columns:
            print(f"Coluna '{coluna}' não encontrada")
            return []

        valores = sorted(self.df[coluna].dropna().unique().tolist())
        print(f"Coluna '{coluna}': {len(valores)} valores únicos")
        return valores

    def resumo_dados(self) -> dict:
        resumo = {
            'total_registros': len(self.df),
            'colunas': list(self.df.columns),
            'total_colunas': len(self.df.columns),
            'memoria_mb': self.df.memory_usage(deep=True).sum() / 1024 / 1024
        }

        if 'tem_deficiencia' in self.df.columns:
            resumo['com_deficiencia'] = self.df['tem_deficiencia'].sum()

        if 'tem_internet' in self.df.columns:
            resumo['com_internet'] = self.df['tem_internet'].sum()

        if 'uf' in self.df.columns:
            resumo['total_ufs'] = self.df['uf'].nunique()

        return resumo

    def __repr__(self):
        return f"<AnalisadorPCD: {len(self.df):,} registros, {len(self.df.columns)} colunas>"
