"""
Módulo utils - Utilitários para o Observatório de Inclusão Digital
"""
# Data Loader - Funções principais de carregamento
from .data_loader import (
    # CETIC
    carregar_dados_domicilios_cetic,
    carregar_dados_individuos_cetic,
    get_analisador_domicilios,
    get_analisador_individuos,
    # ANATEL
    carregar_dados_anatel,
    carregar_conectividade_escola_anatel,
    carregar_cobertura_movel_anatel,
    carregar_cobertura_movel_5g_uf_anatel,
    carregar_cobertura_movel_4g_uf_anatel,
    get_analisador_anatel,
    get_anos_disponiveis_anatel,
    get_analisador_cobertura_movel,
    # INEP
    carregar_dados_inep,
    carregar_educacao_basica_inep,
    get_analisador_inep,
    get_anos_disponiveis_inep,
)
# HTTP Loader
from .http_loader import HTTPDataLoader
# Filtro Helper
from .filtro_helper import FiltroHelper
# Data Sources
from .data_sources import (
    DATA_SOURCES,
    get_fonte_info,
    get_fonte_urls,
    list_fontes,
    get_anos_disponiveis,
)
__all__ = [
    # Data Loader - CETIC
    'carregar_dados_domicilios_cetic',
    'carregar_dados_individuos_cetic',
    'get_analisador_domicilios',
    'get_analisador_individuos',
    # Data Loader - ANATEL
    'carregar_dados_anatel',
    'carregar_conectividade_escola_anatel',
    'carregar_cobertura_movel_anatel',
    'carregar_cobertura_movel_5g_uf_anatel',
    'carregar_cobertura_movel_4g_uf_anatel',
    'get_analisador_anatel',
    'get_anos_disponiveis_anatel',
    'get_analisador_cobertura_movel',
    # Data Loader - INEP
    'carregar_dados_inep',
    'carregar_educacao_basica_inep',
    'get_analisador_inep',
    'get_anos_disponiveis_inep',
    # HTTP Loader
    'HTTPDataLoader',
    # Filtro Helper
    'FiltroHelper',
    # Data Sources
    'DATA_SOURCES',
    'get_fonte_info',
    'get_fonte_urls',
    'list_fontes',
    'get_anos_disponiveis',
]
