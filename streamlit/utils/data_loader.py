import sys
import os
import streamlit as st
from .http_loader import HTTPDataLoader

# Adiciona a raiz do projeto ao sys.path para permitir importações dos módulos cetic
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from cetic.domicilios.analisador_domicilios_cetic import AnalisadorDomiciliosCETIC
from cetic.individuos.analisador_individuos_cetic import AnalisadorIndividuosCETIC

@st.cache_data
def carregar_dados_domicilios_cetic(ano: int = 2025, force_download: bool = False):
    """
    Carrega dados de domicílios CETIC via HTTP (com cache local)

    Args:
        ano: Ano da pesquisa (2023, 2024, 2025)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        (DataFrame, metadados) ou (None, None) se falhar
    """
    loader = HTTPDataLoader()
    resultado = loader.carregar_dados(ano, 'domicilios', force_download)

    if resultado:
        return resultado
    return None, None

@st.cache_data
def carregar_dados_individuos_cetic(ano: int = 2025, force_download: bool = False):
    """
    Carrega dados de indivíduos CETIC via HTTP (com cache local)

    Args:
        ano: Ano da pesquisa (2023, 2024, 2025)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        (DataFrame, metadados) ou (None, None) se falhar
    """
    loader = HTTPDataLoader()
    resultado = loader.carregar_dados(ano, 'individuos', force_download)

    if resultado:
        return resultado
    return None, None

@st.cache_resource
def get_analisador_domicilios(ano: int = 2025):
    """
    Retorna uma instância única do AnalisadorDomiciliosCETIC para um ano específico.
    O uso de st.cache_resource garante que seja carregado apenas uma vez por ano.

    Args:
        ano: Ano da pesquisa (default: 2025)
    """
    # Carrega dados via HTTP
    df, meta = carregar_dados_domicilios_cetic(ano)

    if df is None:
        raise ValueError(f"Não foi possível carregar dados de {ano}")

    # Cria analisador passando df e meta (evita importação circular)
    return AnalisadorDomiciliosCETIC(ano=ano, df=df, meta=meta)

@st.cache_resource
def get_analisador_individuos(ano: int = 2025):
    """
    Retorna uma instância única do AnalisadorIndividuosCETIC para um ano específico.
    O uso de st.cache_resource garante que seja carregado apenas uma vez por ano.

    Args:
        ano: Ano da pesquisa (default: 2025)
    """
    # Carrega dados via HTTP
    df, meta = carregar_dados_individuos_cetic(ano)

    if df is None:
        raise ValueError(f"Não foi possível carregar dados de {ano}")

    # Cria analisador passando df e meta (evita importação circular)
    return AnalisadorIndividuosCETIC(ano=ano, df=df, meta=meta)


@st.cache_data
def carregar_dados_anatel(ano: int, tipo: str = 'conectividade-escola', force_download: bool = False):
    """
    Carrega dados da ANATEL de um ano específico do cache (ou baixa se não existir)

    Args:
        ano: Ano específico (2022, 2023, 2024, 2025)
        tipo: Tipo de dado ('conectividade-escola', futuramente outros)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        (DataFrame, None) ou (None, None) se falhar
    """
    loader = HTTPDataLoader(fonte='anatel')
    resultado = loader.carregar_dados(ano, tipo, force_download)

    if resultado:
        return resultado
    return None, None


@st.cache_data
def carregar_conectividade_escola_anatel(ano: int, force_download: bool = False):
    """
    Carrega dados de conectividade escolar da ANATEL de um ano específico
    Equivalente ao carregar_dados_domicilios_cetic/carregar_dados_individuos_cetic

    Args:
        ano: Ano específico (2022, 2023, 2024, 2025)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame do ano específico ou None se falhar
    """
    df, _ = carregar_dados_anatel(ano=ano, tipo='conectividade-escola', force_download=force_download)
    return df


def get_anos_disponiveis_anatel(tipo: str = 'conectividade-escola'):
    """
    Retorna lista de anos disponíveis para um tipo de dado da ANATEL

    Args:
        tipo: Tipo de dado ('conectividade-escola', etc)

    Returns:
        Lista de anos disponíveis (ex: [2025, 2024, 2023, 2022])
    """
    # Anos disponíveis para conectividade escolar
    if tipo == 'conectividade-escola':
        return [2025, 2024, 2023, 2022]

    # Para futuros tipos, adicionar aqui
    return []


def baixar_cobertura_movel_anatel(force_download: bool = False) -> bool:
    """
    Baixa e extrai os arquivos de cobertura móvel da ANATEL
    Os arquivos são salvos em: data/cache/anatel/cobertura-movel/

    Args:
        force_download: Forçar novo download mesmo se já existirem arquivos

    Returns:
        True se sucesso, False caso contrário
    """
    loader = HTTPDataLoader(fonte='anatel')
    return loader.baixar_cobertura_movel(force_download=force_download)


@st.cache_data
def carregar_cobertura_movel_anatel(force_download: bool = False):
    """
    Carrega dados de cobertura móvel da ANATEL
    Os dados são carregados do arquivo parquet em cache

    Args:
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame com os dados de cobertura móvel ou None se falhar
    """
    loader = HTTPDataLoader(fonte='anatel')
    resultado = loader.carregar_dados(ano='consolidado', tipo='cobertura-movel', force_download=force_download)

    if resultado:
        df, _ = resultado
        return df
    return None

