"""
Módulo de estatísticas e análises para dados PCD

Responsabilidade: Calcular estatísticas, agregações e métricas
"""
import pandas as pd
import numpy as np


class EstatisticasPCD:
    """
    Calcula estatísticas e métricas dos dados PCD
    
    Responsabilidades:
    - Calcular percentuais de acesso
    - Comparar com população geral
    - Análises por categorias
    - Tendências temporais
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa com DataFrame
        
        Args:
            df: DataFrame com dados PCD (já filtrado se necessário)
        """
        self.df = df
    
    # === ACESSO À INTERNET ===
    
    def percentual_acesso_internet(self) -> float:
        """Percentual de pessoas com acesso à internet"""
        if 'tem_internet' not in self.df.columns:
            return None
        
        total = len(self.df)
        if total == 0:
            return 0.0
        
        com_internet = self.df['tem_internet'].sum()
        return (com_internet / total) * 100
    
    def acesso_por_tipo_deficiencia(self) -> pd.DataFrame:
        """Percentual de acesso à internet por tipo de deficiência"""
        if 'tipo_deficiencia' not in self.df.columns or 'tem_internet' not in self.df.columns:
            return pd.DataFrame()
        
        resultado = self.df.groupby('tipo_deficiencia').agg({
            'tem_internet': ['sum', 'count']
        })
        
        resultado.columns = ['com_internet', 'total']
        resultado['percentual'] = (resultado['com_internet'] / resultado['total']) * 100
        resultado = resultado.sort_values('percentual', ascending=False)
        
        return resultado.reset_index()
    
    def acesso_por_regiao(self) -> pd.DataFrame:
        """Percentual de acesso à internet por região"""
        if 'regiao' not in self.df.columns or 'tem_internet' not in self.df.columns:
            return pd.DataFrame()
        
        resultado = self.df.groupby('regiao').agg({
            'tem_internet': ['sum', 'count']
        })
        
        resultado.columns = ['com_internet', 'total']
        resultado['percentual'] = (resultado['com_internet'] / resultado['total']) * 100
        resultado = resultado.sort_values('percentual', ascending=False)
        
        return resultado.reset_index()
    
    def acesso_por_area(self) -> pd.DataFrame:
        """Comparação de acesso entre área urbana e rural"""
        if 'area' not in self.df.columns or 'tem_internet' not in self.df.columns:
            return pd.DataFrame()
        
        resultado = self.df.groupby('area').agg({
            'tem_internet': ['sum', 'count']
        })
        
        resultado.columns = ['com_internet', 'total']
        resultado['percentual'] = (resultado['com_internet'] / resultado['total']) * 100
        
        return resultado.reset_index()
    
    # === DISPOSITIVOS ===
    
    def distribuicao_dispositivos(self) -> pd.Series:
        """Distribuição de tipos de dispositivos"""
        dispositivos = {}
        
        if 'tem_computador' in self.df.columns:
            dispositivos['Computador'] = self.df['tem_computador'].sum()
        
        if 'tem_smartphone' in self.df.columns:
            dispositivos['Smartphone'] = self.df['tem_smartphone'].sum()
        
        if 'tem_tablet' in self.df.columns:
            dispositivos['Tablet'] = self.df['tem_tablet'].sum()
        
        return pd.Series(dispositivos)
    
    def percentual_apenas_smartphone(self) -> float:
        """Percentual que acessa internet APENAS via smartphone"""
        if not all(col in self.df.columns for col in ['tem_smartphone', 'tem_computador', 'tem_internet']):
            return None
        
        apenas_smartphone = self.df[
            (self.df['tem_internet'] == True) &
            (self.df['tem_smartphone'] == True) &
            (self.df['tem_computador'] == False)
        ]
        
        total_com_internet = self.df['tem_internet'].sum()
        if total_com_internet == 0:
            return 0.0
        
        return (len(apenas_smartphone) / total_com_internet) * 100
    
    # === BARREIRAS ===
    
    def principais_barreiras(self, top_n: int = 5) -> pd.Series:
        """Top N barreiras mais citadas"""
        if 'tipo_barreira' not in self.df.columns:
            return pd.Series()
        
        barreiras = self.df['tipo_barreira'].value_counts().head(top_n)
        return barreiras
    
    def percentual_com_barreiras(self) -> float:
        """Percentual que encontra barreiras no acesso digital"""
        if 'encontra_barreiras' not in self.df.columns:
            return None
        
        total = len(self.df)
        if total == 0:
            return 0.0
        
        com_barreiras = self.df['encontra_barreiras'].sum()
        return (com_barreiras / total) * 100
    
    # === TECNOLOGIAS ASSISTIVAS ===
    
    def uso_tecnologia_assistiva(self) -> dict:
        """Estatísticas de uso de tecnologias assistivas"""
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
    
    # === DEMOGRAFIA ===
    
    def distribuicao_por_faixa_etaria(self) -> pd.DataFrame:
        """Distribuição por faixa etária com acesso à internet"""
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
        """Distribuição por escolaridade com acesso à internet"""
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
        """Distribuição por faixa de renda com acesso à internet"""
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
    
    # === USO DA INTERNET ===
    
    def atividades_online_mais_comuns(self, top_n: int = 5) -> pd.Series:
        """Top N atividades online mais realizadas"""
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
                label = labels.get(col, col)
                atividades[label] = self.df[col].sum()
        
        serie = pd.Series(atividades).sort_values(ascending=False)
        return serie.head(top_n)
    
    def frequencia_uso_internet(self) -> pd.Series:
        """Distribuição de frequência de uso"""
        if 'frequencia_uso' not in self.df.columns:
            return pd.Series()
        
        return self.df['frequencia_uso'].value_counts()
    
    # === COMPARAÇÕES ===
    
    def comparar_acesso_com_sem_deficiencia(self, df_completo: pd.DataFrame) -> dict:
        """
        Compara acesso entre PCD e população geral
        
        Args:
            df_completo: DataFrame com toda a população (incluindo PCD e não-PCD)
        """
        if 'tem_deficiencia' not in df_completo.columns or 'tem_internet' not in df_completo.columns:
            return {}
        
        # Com deficiência
        pcd = df_completo[df_completo['tem_deficiencia'] == True]
        total_pcd = len(pcd)
        com_internet_pcd = pcd['tem_internet'].sum() if total_pcd > 0 else 0
        
        # Sem deficiência
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
    
    # === RESUMO GERAL ===
    
    def resumo_geral(self) -> dict:
        """Gera resumo estatístico completo"""
        resumo = {
            'total_registros': len(self.df),
            'percentual_acesso_internet': self.percentual_acesso_internet(),
            'percentual_com_barreiras': self.percentual_com_barreiras(),
            'percentual_usa_tecnologia_assistiva': None,
            'dispositivo_mais_comum': None,
            'barreira_principal': None
        }
        
        # Tecnologia assistiva
        if 'usa_tecnologia_assistiva' in self.df.columns:
            total = len(self.df)
            usa = self.df['usa_tecnologia_assistiva'].sum()
            resumo['percentual_usa_tecnologia_assistiva'] = (usa / total * 100) if total > 0 else 0
        
        # Dispositivo mais comum
        dispositivos = self.distribuicao_dispositivos()
        if not dispositivos.empty:
            resumo['dispositivo_mais_comum'] = dispositivos.idxmax()
        
        # Barreira principal
        barreiras = self.principais_barreiras(top_n=1)
        if not barreiras.empty:
            resumo['barreira_principal'] = barreiras.index[0]
        
        return resumo
