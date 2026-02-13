"""
Funções utilitárias para análise de dados IBGE
"""
import pandas as pd
from pathlib import Path


def normalizar_nomes_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nomes de colunas: maiúsculas, remove espaços extras
    
    Args:
        df: DataFrame para normalizar
        
    Returns:
        DataFrame com colunas normalizadas
    """
    df.columns = [str(col).strip().upper() for col in df.columns]
    return df


def filtrar_por_regex(df: pd.DataFrame, coluna: str, padrao: str) -> pd.DataFrame:
    """
    Filtra DataFrame usando regex em uma coluna
    
    Args:
        df: DataFrame a filtrar
        coluna: Nome da coluna
        padrao: Padrão regex
        
    Returns:
        DataFrame filtrado
    """
    return df[df[coluna].str.contains(padrao, case=False, na=False, regex=True)]


def agrupar_por_coluna(df: pd.DataFrame, coluna: str, agregacao: str = 'sum') -> pd.DataFrame:
    """
    Agrupa dados por uma coluna específica
    
    Args:
        df: DataFrame a agrupar
        coluna: Coluna para agrupar
        agregacao: Tipo de agregação (sum, mean, count, etc)
        
    Returns:
        DataFrame agrupado
    """
    colunas_numericas = df.select_dtypes(include=['number']).columns
    return df.groupby(coluna)[colunas_numericas].agg(agregacao)


def get_cache_dir() -> Path:
    """
    Retorna o diretório de cache para dados IBGE
    Cria o diretório se não existir
    """
    cache_dir = Path(__file__).parent.parent / 'data' / 'cache' / 'ibge'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def salvar_cache(df: pd.DataFrame, arquivo: str):
    """
    Salva DataFrame em cache como parquet
    
    Args:
        df: DataFrame a salvar
        arquivo: Nome do arquivo (sem extensão)
    """
    cache_dir = get_cache_dir()
    caminho = cache_dir / f'{arquivo}.parquet'
    df.to_parquet(caminho, index=False)
    print(f"✓ Cache salvo: {caminho}")


def carregar_cache(arquivo: str) -> pd.DataFrame:
    """
    Carrega DataFrame do cache
    
    Args:
        arquivo: Nome do arquivo (sem extensão)
        
    Returns:
        DataFrame carregado ou None se não existe
    """
    cache_dir = get_cache_dir()
    caminho = cache_dir / f'{arquivo}.parquet'
    
    if caminho.exists():
        return pd.read_parquet(caminho)
    return None
