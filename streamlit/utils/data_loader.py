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


