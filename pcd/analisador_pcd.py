"""
Analisador principal de dados PCD

Responsabilidade: Filtrar e preparar dados para análise
"""
import pandas as pd
try:
    from pcd.metadados import get_todos_campos
except ImportError:
    from metadados import get_todos_campos


class AnalisadorPCD:
    """
    Analisador principal dos dados de inclusão digital para PCD
    Dados: Municípios do Piauí - População, Alfabetização e Raça/Cor
    
    Responsabilidades:
    - Validar e normalizar dados
    - Filtrar por municípios e características
    - Preparar dados para análises específicas
    """
    
    def __init__(self, df=None, ano: int = 2024):
        """
        Inicializa o analisador
        
        Args:
            df: DataFrame com os dados PCD (municípios do Piauí)
            ano: Ano base para análises (default: 2024)
        """
        self.ano = ano
        
        if df is None:
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_pcd(ano)\n"
                "do módulo streamlit.utils.data_loader"
            )
        
        self.df = df.copy()
        self.df_original = df.copy()
        
        print(f"✓ Analisador PCD carregado: {len(self.df):,} municípios, {len(self.df.columns)} colunas")
    
    def reset_filtros(self):
        """Reseta todos os filtros, voltando aos dados originais"""
        self.df = self.df_original.copy()
        print(f"✓ Filtros resetados. Municípios: {len(self.df):,}")
        return self
    
    # === FILTROS ESPECÍFICOS PARA OS DADOS REAIS ===
    
    def filtrar_por_municipio(self, municipio: str):
        """Filtra por município específico"""
        if 'municipio' not in self.df.columns:
            print("⚠️  Coluna 'municipio' não encontrada")
            return self
        
        self.df = self.df[self.df['municipio'].str.contains(municipio, case=False, na=False)]
        print(f"✓ Filtrado para município '{municipio}': {len(self.df):,} registros")
        return self
    
    def filtrar_por_variacao_populacao(self, positiva: bool = True):
        """Filtra municípios com crescimento ou decrescimento populacional"""
        if 'variacao_populacao' not in self.df.columns:
            print("⚠️  Coluna 'variacao_populacao' não encontrada")
            return self
        
        if positiva:
            self.df = self.df[self.df['variacao_populacao'] > 0]
            print(f"✓ Filtrado municípios com CRESCIMENTO: {len(self.df):,} municípios")
        else:
            self.df = self.df[self.df['variacao_populacao'] < 0]
            print(f"✓ Filtrado municípios com DECRESCIMENTO: {len(self.df):,} municípios")
        return self
    
    def filtrar_por_taxa_alfabetizacao(self, min_taxa: float = None, max_taxa: float = None):
        """Filtra municípios por taxa de alfabetização geral"""
        if 'taxa_alfabetizacao_geral' not in self.df.columns:
            print("⚠️  Coluna 'taxa_alfabetizacao_geral' não encontrada")
            return self
        
        if min_taxa is not None:
            self.df = self.df[self.df['taxa_alfabetizacao_geral'] >= min_taxa]
        if max_taxa is not None:
            self.df = self.df[self.df['taxa_alfabetizacao_geral'] <= max_taxa]
        
        print(f"✓ Filtrado por taxa de alfabetização: {len(self.df):,} municípios")
        return self
    
    def get_maiores_populacoes(self, n: int = 10):
        """Retorna os N municípios com maior população (2022)"""
        if 'populacao_2022' not in self.df.columns:
            print("⚠️  Coluna 'populacao_2022' não encontrada")
            return pd.DataFrame()
        
        return self.df.nlargest(n, 'populacao_2022')[['municipio', 'populacao_2022', 'taxa_alfabetizacao_geral']]
    
    def get_menores_taxas_alfabetizacao(self, n: int = 10):
        """Retorna os N municípios com menor taxa de alfabetização"""
        if 'taxa_alfabetizacao_geral' not in self.df.columns:
            print("⚠️  Coluna 'taxa_alfabetizacao_geral' não encontrada")
            return pd.DataFrame()
        
        return self.df.nsmallest(n, 'taxa_alfabetizacao_geral')[['municipio', 'taxa_alfabetizacao_geral', 'populacao_2022']]
    
    def get_distribuicao_racial(self):
        """Retorna estatísticas da distribuição racial nos municípios"""
        colunas_pop = ['pop_branca', 'pop_preta', 'pop_amarela', 'pop_parda', 'pop_indigena']
        
        if not all(col in self.df.columns for col in colunas_pop):
            print("⚠️  Colunas de população por raça/cor não encontradas")
            return pd.DataFrame()
        
        return pd.DataFrame({
            'Branca': [self.df['pop_branca'].sum()],
            'Preta': [self.df['pop_preta'].sum()],
            'Amarela': [self.df['pop_amarela'].sum()],
            'Parda': [self.df['pop_parda'].sum()],
            'Indígena': [self.df['pop_indigena'].sum()]
        })
    
    def get_disparidades_raciais_alfabetizacao(self):
        """Analisa disparidades nas taxas de alfabetização por raça/cor"""
        colunas_taxa = ['taxa_alfa_branca', 'taxa_alfa_preta', 'taxa_alfa_parda']
        
        if not all(col in self.df.columns for col in colunas_taxa):
            print("⚠️  Colunas de taxa de alfabetização por raça/cor não encontradas")
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
    
    # === FILTROS GEOGRÁFICOS ===
    
    def filtrar_por_uf(self, uf: str):
        """Filtra dados de uma UF específica"""
        if 'uf' not in self.df.columns:
            print("⚠️  Coluna 'uf' não encontrada")
            return self
        
        self.df = self.df[self.df['uf'].str.upper() == uf.upper()]
        print(f"✓ Filtrado para UF {uf.upper()}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_regiao(self, regiao: str):
        """Filtra dados de uma região"""
        if 'regiao' not in self.df.columns:
            print("⚠️  Coluna 'regiao' não encontrada")
            return self
        
        self.df = self.df[self.df['regiao'].str.lower() == regiao.lower()]
        print(f"✓ Filtrado para Região {regiao}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_area(self, area: str):
        """Filtra por área (Urbana ou Rural)"""
        if 'area' not in self.df.columns:
            print("⚠️  Coluna 'area' não encontrada")
            return self
        
        self.df = self.df[self.df['area'].str.lower() == area.lower()]
        print(f"✓ Filtrado para Área {area}: {len(self.df):,} registros")
        return self
    
    # === FILTROS DE DEFICIÊNCIA ===
    
    def filtrar_por_tipo_deficiencia(self, tipo: str):
        """Filtra por tipo de deficiência"""
        if 'tipo_deficiencia' not in self.df.columns:
            print("⚠️  Coluna 'tipo_deficiencia' não encontrada")
            return self
        
        self.df = self.df[self.df['tipo_deficiencia'].str.lower() == tipo.lower()]
        print(f"✓ Filtrado para Deficiência {tipo}: {len(self.df):,} registros")
        return self
    
    def filtrar_com_deficiencia(self, tem: bool = True):
        """Filtra pessoas com ou sem deficiência"""
        if 'tem_deficiencia' not in self.df.columns:
            print("⚠️  Coluna 'tem_deficiencia' não encontrada")
            return self
        
        self.df = self.df[self.df['tem_deficiencia'] == tem]
        texto = "COM deficiência" if tem else "SEM deficiência"
        print(f"✓ Filtrado pessoas {texto}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_grau_deficiencia(self, grau: str):
        """Filtra por grau da deficiência"""
        if 'grau_deficiencia' not in self.df.columns:
            print("⚠️  Coluna 'grau_deficiencia' não encontrada")
            return self
        
        self.df = self.df[self.df['grau_deficiencia'].str.lower() == grau.lower()]
        print(f"✓ Filtrado por grau {grau}: {len(self.df):,} registros")
        return self
    
    # === FILTROS DEMOGRÁFICOS ===
    
    def filtrar_por_faixa_etaria(self, faixa: str):
        """Filtra por faixa etária"""
        if 'faixa_etaria' not in self.df.columns:
            print("⚠️  Coluna 'faixa_etaria' não encontrada")
            return self
        
        self.df = self.df[self.df['faixa_etaria'] == faixa]
        print(f"✓ Filtrado para faixa etária {faixa}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_sexo(self, sexo: str):
        """Filtra por sexo"""
        if 'sexo' not in self.df.columns:
            print("⚠️  Coluna 'sexo' não encontrada")
            return self
        
        self.df = self.df[self.df['sexo'].str.lower() == sexo.lower()]
        print(f"✓ Filtrado por sexo {sexo}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_escolaridade(self, escolaridade: str):
        """Filtra por nível de escolaridade"""
        if 'escolaridade' not in self.df.columns:
            print("⚠️  Coluna 'escolaridade' não encontrada")
            return self
        
        self.df = self.df[self.df['escolaridade'] == escolaridade]
        print(f"✓ Filtrado por escolaridade {escolaridade}: {len(self.df):,} registros")
        return self
    
    def filtrar_por_renda(self, faixa_renda: str):
        """Filtra por faixa de renda familiar"""
        if 'renda_familiar' not in self.df.columns:
            print("⚠️  Coluna 'renda_familiar' não encontrada")
            return self
        
        self.df = self.df[self.df['renda_familiar'] == faixa_renda]
        print(f"✓ Filtrado por renda {faixa_renda}: {len(self.df):,} registros")
        return self
    
    # === FILTROS DE ACESSO ===
    
    def filtrar_com_internet(self, tem: bool = True):
        """Filtra por acesso à internet"""
        if 'tem_internet' not in self.df.columns:
            print("⚠️  Coluna 'tem_internet' não encontrada")
            return self
        
        self.df = self.df[self.df['tem_internet'] == tem]
        texto = "COM" if tem else "SEM"
        print(f"✓ Filtrado pessoas {texto} internet: {len(self.df):,} registros")
        return self
    
    def filtrar_por_frequencia_uso(self, frequencia: str):
        """Filtra por frequência de uso da internet"""
        if 'frequencia_uso' not in self.df.columns:
            print("⚠️  Coluna 'frequencia_uso' não encontrada")
            return self
        
        self.df = self.df[self.df['frequencia_uso'].str.lower() == frequencia.lower()]
        print(f"✓ Filtrado por frequência {frequencia}: {len(self.df):,} registros")
        return self
    
    # === MÉTODOS AUXILIARES ===
    
    def get_dados_atuais(self) -> pd.DataFrame:
        """Retorna DataFrame com filtros aplicados"""
        return self.df.copy()
    
    def contar_registros(self) -> int:
        """Retorna número de registros após filtros"""
        return len(self.df)
    
    def listar_valores_unicos(self, coluna: str) -> list:
        """Lista valores únicos de uma coluna"""
        if coluna not in self.df.columns:
            print(f"⚠️  Coluna '{coluna}' não encontrada")
            return []
        
        valores = sorted(self.df[coluna].dropna().unique().tolist())
        print(f"✓ Coluna '{coluna}': {len(valores)} valores únicos")
        return valores
    
    def resumo_dados(self) -> dict:
        """Retorna resumo estatístico dos dados atuais"""
        resumo = {
            'total_registros': len(self.df),
            'colunas': list(self.df.columns),
            'total_colunas': len(self.df.columns),
            'memoria_mb': self.df.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        # Adiciona contagens específicas se colunas existirem
        if 'tem_deficiencia' in self.df.columns:
            resumo['com_deficiencia'] = self.df['tem_deficiencia'].sum()
        
        if 'tem_internet' in self.df.columns:
            resumo['com_internet'] = self.df['tem_internet'].sum()
        
        if 'uf' in self.df.columns:
            resumo['total_ufs'] = self.df['uf'].nunique()
        
        return resumo
    
    def __repr__(self):
        return f"<AnalisadorPCD: {len(self.df):,} registros, {len(self.df.columns)} colunas>"
