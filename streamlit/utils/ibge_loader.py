"""
Carregador específico para dados do IBGE
Mantido separado do HTTPDataLoader para evitar conflitos de cache
"""
import requests
import pandas as pd
from pathlib import Path
from io import StringIO
from typing import Optional, Tuple
import streamlit as st
from utils.data_sources import get_fonte_urls


# Mapeamento de estados para UF
ESTADOS_UF = {
    'Rondônia': 'RO', 'Acre': 'AC', 'Amazonas': 'AM', 'Roraima': 'RR',
    'Pará': 'PA', 'Amapá': 'AP', 'Tocantins': 'TO',
    'Maranhão': 'MA', 'Piauí': 'PI', 'Ceará': 'CE', 'Rio Grande do Norte': 'RN',
    'Paraíba': 'PB', 'Pernambuco': 'PE', 'Alagoas': 'AL', 'Sergipe': 'SE', 'Bahia': 'BA',
    'Minas Gerais': 'MG', 'Espírito Santo': 'ES', 'Rio de Janeiro': 'RJ', 'São Paulo': 'SP',
    'Paraná': 'PR', 'Santa Catarina': 'SC', 'Rio Grande do Sul': 'RS',
    'Mato Grosso do Sul': 'MS', 'Mato Grosso': 'MT', 'Goiás': 'GO', 'Distrito Federal': 'DF'
}

# Mapeamento de UF para Região
UF_REGIAO = {
    'RO': 'Norte', 'AC': 'Norte', 'AM': 'Norte', 'RR': 'Norte', 'PA': 'Norte', 'AP': 'Norte', 'TO': 'Norte',
    'MA': 'Nordeste', 'PI': 'Nordeste', 'CE': 'Nordeste', 'RN': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'AL': 'Nordeste', 'SE': 'Nordeste', 'BA': 'Nordeste',
    'MG': 'Sudeste', 'ES': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'SC': 'Sul', 'RS': 'Sul',
    'MS': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'DF': 'Centro-Oeste'
}


class IBGEDataLoader:
    """Carregador especializado para dados do IBGE"""
    
    def __init__(self, cache_dir: str = None):
        """
        Inicializa o loader do IBGE
        
        Args:
            cache_dir: Diretório de cache (opcional)
        """
        if cache_dir is None:
            project_root = Path(__file__).parent.parent.parent
            cache_dir = project_root / "data" / "cache"
        
        self.cache_dir = Path(cache_dir) / "ibge" / "consolidado"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _transformar_tabela7336(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma Tabela 7336 de formato 'wide' para 'long' estruturado
        Mantém todos os níveis de instrução
        
        Args:
            df: DataFrame no formato wide do IBGE
            
        Returns:
            DataFrame reorganizado com colunas: REGIAO, UF, LOCALIZACAO, ANO, INSTRUCAO, PERCENTUAL
        """
        # Remove linhas inválidas (rodapé do arquivo)
        df = df[df.iloc[:, 0].notna()]
        df = df[~df.iloc[:, 0].str.contains(r'Fonte:|Notas|Legenda|Símbolo|^-$|^0$|^X$|^\.\.$|^\.\.\.', na=False, regex=True)]
        
        # Filtra apenas Brasil e regiões/estados válidos
        df_limpo = df[df.iloc[:, 0].isin(list(ESTADOS_UF.keys()) + list(ESTADOS_UF.values()) + ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste', 'Brasil'])].copy()
        
        # Renomeia primeira coluna como LOCALIZACAO (região/estado/Brasil)
        df_limpo.columns = ['LOCALIZACAO'] + [col for col in df_limpo.columns[1:]]
        
        # Converte valores numéricos (substituir vírgula por ponto)
        for col in df_limpo.columns[1:]:
            df_limpo[col] = df_limpo[col].astype(str).str.replace(',', '.').apply(pd.to_numeric, errors='coerce')
        
        # Nomes dos níveis de instrução (ordem no arquivo IBGE)
        niveis_instrucao = [
            'Total',
            'Sem instrução e fundamental incompleto',
            'Fundamental completo',
            'Médio incompleto',
            'Médio completo',
            'Superior incompleto',
            'Superior completo'
        ]
        
        # Anos: 2021, 2022, 2023, 2024 (7 colunas por ano)
        anos = [2021, 2022, 2023, 2024]
        cols_por_ano = 7
        
        registros = []
        for idx, row in df_limpo.iterrows():
            localizacao = row['LOCALIZACAO']
            regiao = None
            uf = None
            
            # Detecta se é região ou estado
            if localizacao in ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']:
                regiao = localizacao
                uf = localizacao  # Usa nome da região
            elif localizacao == 'Brasil':
                regiao = 'Brasil'
                uf = 'BR'
            else:
                uf = ESTADOS_UF.get(localizacao, localizacao)
                regiao = UF_REGIAO.get(uf, 'Brasil')
            
            # Extrai dados para cada ano e cada nível de instrução
            col_idx = 1
            for ano in anos:
                for nivel_idx, nivel in enumerate(niveis_instrucao):
                    if col_idx < len(row):
                        percentual = row.iloc[col_idx]
                        if pd.notna(percentual):
                            registros.append({
                                'REGIAO': regiao,
                                'UF': uf,
                                'LOCALIZACAO': localizacao,
                                'ANO': ano,
                                'INSTRUCAO': nivel,
                                'PERCENTUAL': percentual
                            })
                        col_idx += 1
        
        df_long = pd.DataFrame(registros)
        return df_long
    
    def carregar_tabela7336(self, force_download: bool = False) -> Optional[pd.DataFrame]:
        """
        Carrega Tabela 7336 do IBGE (Acesso à Internet)
        
        Args:
            force_download: Forçar novo download mesmo se existir cache
            
        Returns:
            DataFrame com os dados ou None se erro
        """
        # Busca URL configurada em streamlit/utils/data_sources.py
        urls = get_fonte_urls('ibge')
        url = urls.get('consolidado', {}).get('tabela-7336', '') or 'https://github.com/mvaldecy/observatorio-inclusao-digital/releases/download/dados-ibge-2021-2024/tabela7336.csv'
        parquet_path = self.cache_dir / 'tabela-7336.parquet'
        
        # Tenta carregar do cache primeiro
        if parquet_path.exists() and not force_download:
            try:
                df = pd.read_parquet(str(parquet_path))
                return df
            except Exception as e:
                print(f"⚠️ Erro ao carregar cache: {e}")
        
        # Baixa e processa
        try:
            print(f"📥 Baixando Tabela 7336 do IBGE... URL={url}")

            # Se a fonte apontar para o site SIDRA, usamos a API pública de valores
            if 'sidra.ibge.gov.br' in url or 'apisidra.ibge.gov.br' in url:
                api_url = 'https://apisidra.ibge.gov.br/values/t/7336/n1/all/v/all/p/all?formato=csv'
                response = requests.get(api_url, timeout=30)
                response.raise_for_status()
                text = response.text
                # Tentativa de parse: primeiro com ponto-e-vírgula, depois com vírgula
                try:
                    df_raw = pd.read_csv(StringIO(text), sep=';', encoding='utf-8')
                except Exception:
                    df_raw = pd.read_csv(StringIO(text), sep=',', encoding='utf-8')
            else:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                # Lê em memória (formato do release do repositório usa header e 4 linhas iniciais, Brasil está na 5ª linha)
                try:
                    df_raw = pd.read_csv(StringIO(response.text), sep=';', encoding='utf-8', skiprows=4)
                except Exception:
                    df_raw = pd.read_csv(StringIO(response.text), sep=';', encoding='utf-8')
            
            # Transforma de wide para long
            df = self._transformar_tabela7336(df_raw)
            
            # Salva em cache
            df.to_parquet(str(parquet_path), index=False)
            print(f"✅ Tabela 7336 carregada: {len(df)} registros")
            print(f"   Colunas: {list(df.columns)}")
            
            return df
            
        except Exception as e:
            print(f"❌ Erro ao carregar Tabela 7336: {e}")
            import traceback
            traceback.print_exc()
            return None

