"""
Analisador para Tabela 7336 do IBGE
Dados sobre acesso à Internet - Pessoas de 10 anos ou mais de idade

Responsabilidade: Carregar, filtrar e analisar dados da tabela 7336
"""
import pandas as pd
try:
    from ibge.metadados import get_metadados
    from ibge.utils import normalizar_nomes_colunas
except ImportError:
    from metadados import get_metadados
    from utils import normalizar_nomes_colunas


class AnalisadorTabela7336:
    """
    Analisador especializado em dados de acesso à internet (Tabela 7336)
    
    Responsabilidades:
    - Validar e normalizar dados
    - Filtrar por dimensões (UF, Região, Localização, Período)
    - Agregar dados por diferentes dimensões
    - Calcular percentuais e variações
    """
    
    def __init__(self, df=None, ano: int = 2024):
        """
        Inicializa o analisador
        
        Args:
            df: DataFrame com os dados da tabela 7336
            ano: Ano base para análises (default: 2024)
        """
        self.ano = ano
        
        if df is None:
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_tabela7336()\n"
            )
        
        self.df = df.copy()
        self.df_original = df.copy()
        
        # Normaliza colunas
        self.df = normalizar_nomes_colunas(self.df)
        self.df_original = normalizar_nomes_colunas(self.df_original)
        
        print(f"✓ Tabela 7336 carregada: {len(self.df):,} registros, {len(self.df.columns)} colunas")
    
    def reset_filtros(self):
        """Volta ao DataFrame original sem filtros"""
        self.df = self.df_original.copy()
        print(f"✓ Filtros resetados. Registros: {len(self.df):,}")
        return self.df
    
    def filtrar_por_ano(self, ano: int) -> 'AnalisadorTabela7336':
        """Filtra dados de um ano específico"""
        if 'ANO' not in self.df.columns:
            print("⚠️  Coluna ANO não encontrada")
            return self
        
        self.df = self.df[self.df['ANO'] == ano]
        print(f"✓ Filtrado para ano {ano}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_uf(self, uf: str) -> 'AnalisadorTabela7336':
        """
        Filtra dados de uma UF específica
        
        Args:
            uf: Sigla da UF (ex: 'SP', 'MG')
        """
        if 'UF' not in self.df.columns:
            print("⚠️  Coluna UF não encontrada")
            return self
        
        self.df = self.df[self.df['UF'].str.upper() == uf.upper()]
        print(f"✓ Filtrado para UF {uf.upper()}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_regiao(self, regiao: str) -> 'AnalisadorTabela7336':
        """
        Filtra dados de uma região
        
        Args:
            regiao: Nome da região (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)
        """
        if 'REGIAO' not in self.df.columns:
            print("⚠️  Coluna REGIAO não encontrada")
            return self
        
        self.df = self.df[self.df['REGIAO'].str.lower() == regiao.lower()]
        print(f"✓ Filtrado para Região {regiao}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_localizacao(self, localizacao: str) -> 'AnalisadorTabela7336':
        """
        Filtra por localização (Urbana ou Rural)
        
        Args:
            localizacao: 'Urbana' ou 'Rural'
        """
        if 'LOCALIZACAO' not in self.df.columns:
            print("⚠️  Coluna LOCALIZACAO não encontrada")
            return self
        
        loc = localizacao.lower()
        self.df = self.df[self.df['LOCALIZACAO'].str.lower().str.contains(loc)]
        print(f"✓ Filtrado para {localizacao}: {len(self.df):,} registros")
        return self

    def filtrar_por_instrucao(self, instrucao: str) -> 'AnalisadorTabela7336':
        """
        Filtra pelos níveis de instrução (coluna INSTRUCAO)

        Args:
            instrucao: Nome do nível de instrução (ex: 'Total', 'Médio completo')
        """
        if 'INSTRUCAO' not in self.df.columns:
            print("⚠️  Coluna INSTRUCAO não encontrada")
            return self

        mask = self.df['INSTRUCAO'].astype(str).str.upper() == str(instrucao).upper()
        self.df = self.df[mask]
        print(f"✓ Filtrado para INSTRUCAO={instrucao}: {len(self.df):,} registros")
        return self
    
    def distribucao_por_uf(self) -> pd.DataFrame:
        """
        Distribui dados por UF
        
        Returns:
            DataFrame agrupado por UF
        """
        if 'UF' not in self.df.columns:
            print("⚠️  Coluna UF não encontrada")
            return pd.DataFrame()

        # Agrega PERCENTUAL por UF. Por padrão usa nível 'Total' se existir.
        if 'PERCENTUAL' not in self.df.columns:
            print("⚠️  Coluna PERCENTUAL não encontrada")
            return pd.DataFrame()

        df_work = self.df.copy()
        if 'INSTRUCAO' in df_work.columns and 'TOTAL' in df_work['INSTRUCAO'].str.upper().unique():
            df_work = df_work[df_work['INSTRUCAO'].str.upper() == 'TOTAL']

        resultado = df_work.groupby('UF')['PERCENTUAL'].mean().to_frame('PERCENTUAL')
        return resultado.sort_values(by='PERCENTUAL', ascending=False)
    
    def distribucao_por_regiao(self) -> pd.DataFrame:
        """
        Distribui dados por Região
        
        Returns:
            DataFrame agrupado por Região
        """
        if 'REGIAO' not in self.df.columns:
            print("⚠️  Coluna REGIAO não encontrada")
            return pd.DataFrame()

        if 'PERCENTUAL' not in self.df.columns:
            print("⚠️  Coluna PERCENTUAL não encontrada")
            return pd.DataFrame()

        df_work = self.df.copy()
        if 'INSTRUCAO' in df_work.columns and 'TOTAL' in df_work['INSTRUCAO'].str.upper().unique():
            df_work = df_work[df_work['INSTRUCAO'].str.upper() == 'TOTAL']

        resultado = df_work.groupby('REGIAO')['PERCENTUAL'].mean().to_frame('PERCENTUAL')
        return resultado.sort_values(by='PERCENTUAL', ascending=False)
    
    def distribucao_urbano_rural(self) -> pd.DataFrame:
        """
        Distribui dados entre Urbano e Rural
        
        Returns:
            DataFrame agrupado por Localização
        """
        if 'LOCALIZACAO' not in self.df.columns:
            print("⚠️  Coluna LOCALIZACAO não encontrada")
            return pd.DataFrame()

        if 'PERCENTUAL' not in self.df.columns:
            print("⚠️  Coluna PERCENTUAL não encontrada")
            return pd.DataFrame()

        df_work = self.df.copy()
        if 'INSTRUCAO' in df_work.columns and 'TOTAL' in df_work['INSTRUCAO'].str.upper().unique():
            df_work = df_work[df_work['INSTRUCAO'].str.upper() == 'TOTAL']

        resultado = df_work.groupby('LOCALIZACAO')['PERCENTUAL'].mean().to_frame('PERCENTUAL')
        return resultado
    
    def evolucao_temporal(self, dimensao: str = 'REGIAO') -> pd.DataFrame:
        """
        Mostra evolução temporal por dimensão
        
        Args:
            dimensao: Coluna para agrupar (REGIAO, UF, etc)
            
        Returns:
            DataFrame com evolução temporal
        """
        if 'ANO' not in self.df.columns:
            print("⚠️  Coluna ANO não encontrada")
            return pd.DataFrame()

        if dimensao not in self.df.columns:
            print(f"⚠️  Coluna {dimensao} não encontrada")
            return pd.DataFrame()

        if 'PERCENTUAL' not in self.df.columns:
            print("⚠️  Coluna PERCENTUAL não encontrada")
            return pd.DataFrame()

        df_work = self.df.copy()
        # Prioriza nível 'Total' quando disponível
        if 'INSTRUCAO' in df_work.columns and 'TOTAL' in df_work['INSTRUCAO'].str.upper().unique():
            df_work = df_work[df_work['INSTRUCAO'].str.upper() == 'TOTAL']

        resultado = df_work.groupby(['ANO', dimensao])['PERCENTUAL'].mean().reset_index()
        return resultado.sort_values(['ANO', dimensao])
    
    def obtener_df(self) -> pd.DataFrame:
        """Retorna o DataFrame atual"""
        return self.df.copy()
    
    def resumo_estatistico(self) -> dict:
        """
        Retorna resumo estatístico dos dados
        
        Returns:
            Dicionário com estatísticas
        """
        colunas_num = self.df.select_dtypes(include=['number']).columns

        resumo = {
            'total_registros': len(self.df),
            'total_colunas': len(self.df.columns),
            'anos': sorted(self.df['ANO'].unique()) if 'ANO' in self.df.columns else [],
            'regioes': sorted(self.df['REGIAO'].unique()) if 'REGIAO' in self.df.columns else [],
            'ufs': sorted(self.df['UF'].unique()) if 'UF' in self.df.columns else [],
            'instrucoes': sorted(self.df['INSTRUCAO'].unique()) if 'INSTRUCAO' in self.df.columns else [],
            'estatisticas_numericas': self.df[colunas_num].describe().to_dict()
        }
        
        return resumo
