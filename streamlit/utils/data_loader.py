import sys
import os

# Adiciona a raiz do projeto ao sys.path para permitir importações dos módulos cetic
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_path not in sys.path:
    sys.path.append(root_path)

# Import condicional do streamlit - só quando estiver realmente rodando no streamlit
try:
    import streamlit as st
    # Verifica qual decorador de cache está disponível
    if hasattr(st, 'cache_data'):
        cache_decorator = st.cache_data
        cache_resource_decorator = st.cache_resource
    elif hasattr(st, 'cache'):
        cache_decorator = lambda func: st.cache(allow_output_mutation=True)(func)
        cache_resource_decorator = lambda func: st.cache(allow_output_mutation=True)(func)
    else:
        # Fallback: sem cache
        cache_decorator = lambda func: func
        cache_resource_decorator = lambda func: func
    STREAMLIT_AVAILABLE = True
except (ImportError, AttributeError):
    # Se streamlit não estiver disponível, usa decoradores dummy
    cache_decorator = lambda func: func
    cache_resource_decorator = lambda func: func
    STREAMLIT_AVAILABLE = False

from .http_loader import HTTPDataLoader
from .ibge_loader import IBGEDataLoader


@cache_resource_decorator
def get_http_loader(fonte: str = 'cetic') -> HTTPDataLoader:
    """
    Retorna uma instância singleton do HTTPDataLoader para a fonte informada.
    Usar cache_resource evita recriar o objeto a cada rerun do Streamlit.

    Args:
        fonte: Fonte de dados ('cetic', 'anatel', 'ibge', 'pcd', etc.)

    Returns:
        Instância compartilhada do HTTPDataLoader
    """
    return HTTPDataLoader(fonte=fonte)

from cetic.domicilios.analisador_domicilios_cetic import AnalisadorDomiciliosCETIC
from cetic.individuos.analisador_individuos_cetic import AnalisadorIndividuosCETIC
from anatel.analisador_anatel import AnalisadorAnatel
from anatel.analisador_cobertura_movel import AnalisadorCoberturaMovel
from ibge.analisador_tabela7336 import AnalisadorTabela7336
from pcd.analisador_pcd import AnalisadorPCD

@cache_decorator
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

@cache_decorator
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

@cache_resource_decorator
def get_analisador_domicilios(ano: int = 2025):
    """
    Retorna uma instância única do AnalisadorDomiciliosCETIC para um ano específico.
    O uso de st.cache_resource garante que o objeto seja mantido em memória sem serialização.

    Args:
        ano: Ano da pesquisa (default: 2025)
    """
    df, meta = carregar_dados_domicilios_cetic(ano)

    if df is None:
        raise ValueError(f"Não foi possível carregar dados de {ano}")

    return AnalisadorDomiciliosCETIC(ano=ano, df=df, meta=meta)

@cache_resource_decorator
def get_analisador_individuos(ano: int = 2025):
    """
    Retorna uma instância única do AnalisadorIndividuosCETIC para um ano específico.
    O uso de st.cache_resource garante que o objeto seja mantido em memória sem serialização.

    Args:
        ano: Ano da pesquisa (default: 2025)
    """
    df, meta = carregar_dados_individuos_cetic(ano)

    if df is None:
        raise ValueError(f"Não foi possível carregar dados de {ano}")

    return AnalisadorIndividuosCETIC(ano=ano, df=df, meta=meta)


@cache_decorator
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


@cache_decorator
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


@cache_resource_decorator
def get_analisador_anatel(ano: int = 2025, tipo: str = 'conectividade-escola'):
    """
    Retorna uma instância única do AnalisadorAnatel para um ano específico.
    O uso de st.cache_resource garante que o objeto seja mantido em memória sem serialização.

    Args:
        ano: Ano da pesquisa (default: 2025)
        tipo: Tipo de dado ('conectividade-escola', etc)

    Returns:
        AnalisadorAnatel configurado com os dados do ano
    """
    df = carregar_conectividade_escola_anatel(ano)

    if df is None:
        raise ValueError(f"Não foi possível carregar dados da ANATEL de {ano}")

    return AnalisadorAnatel(df=df, ano=ano)


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



@cache_decorator
def carregar_cobertura_movel_anatel(force_download: bool = False):
    """
    Carrega dados de cobertura móvel da ANATEL (geral)
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


@cache_resource_decorator
def get_analisador_cobertura_movel(force_download: bool = False):
    """
    Retorna uma instância única do AnalisadorCoberturaMovel.
    O uso de st.cache_resource garante que o objeto seja mantido em memória sem serialização.

    Args:
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        AnalisadorCoberturaMovel configurado com os dados
    """
    df = carregar_cobertura_movel_anatel(force_download)

    if df is None:
        raise ValueError("Não foi possível carregar dados de cobertura móvel da ANATEL")

    return AnalisadorCoberturaMovel(df=df)



@cache_decorator
def carregar_cobertura_movel_5g_uf_anatel(force_download: bool = False):
    """
    Carrega dados de cobertura móvel 5G por UF da ANATEL
    Os dados são carregados do arquivo parquet em cache

    Args:
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame com os dados de cobertura 5G por UF ou None se falhar
    """
    loader = HTTPDataLoader(fonte='anatel')
    resultado = loader.carregar_dados(ano='consolidado', tipo='cobertura-movel-5g-uf', force_download=force_download)

    if resultado:
        df, _ = resultado
        return df
    return None


@cache_decorator
def carregar_cobertura_movel_4g_uf_anatel(force_download: bool = False):
    """
    Carrega dados de cobertura móvel 4G por UF da ANATEL
    Os dados são carregados do arquivo parquet em cache

    Args:
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame com os dados de cobertura 4G por UF ou None se falhar
    """
    loader = HTTPDataLoader(fonte='anatel')
    resultado = loader.carregar_dados(ano='consolidado', tipo='cobertura-movel-4g-uf', force_download=force_download)

    if resultado:
        df, _ = resultado
        return df
    return None


# =============================================================================
# FUNÇÕES DE CARREGAMENTO DO INEP
# =============================================================================

@st.cache_data
def carregar_dados_inep(ano: int, tipo: str = 'educacao-basica', force_download: bool = False):
    """
    Carrega dados do INEP (Censo Escolar) de um ano específico

    Args:
        ano: Ano dos dados (2022, 2023, 2024)
        tipo: Tipo de dado ('educacao-basica')
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        (DataFrame, None) ou (None, None) se falhar
    """
    loader = HTTPDataLoader(fonte='inep')
    resultado = loader.carregar_dados(ano, tipo, force_download)

    if resultado:
        return resultado
    return None, None


@st.cache_data
def carregar_educacao_basica_inep(ano: int, force_download: bool = False):
    """
    Carrega dados de educação básica do INEP de um ano específico
    Equivalente ao carregar_conectividade_escola_anatel

    Args:
        ano: Ano específico (2022, 2023, 2024)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame do ano específico ou None se falhar
    """
    df, _ = carregar_dados_inep(ano=ano, tipo='educacao-basica', force_download=force_download)
    return df


def get_anos_disponiveis_inep(tipo: str = 'educacao-basica'):
    """
    Retorna lista de anos disponíveis para um tipo de dado do INEP

    Args:
        tipo: Tipo de dado ('educacao-basica')

    Returns:
        Lista de anos disponíveis (ex: [2024, 2023, 2022])
    """
    loader = HTTPDataLoader(fonte='inep')
    return loader.get_anos_disponiveis(tipo=tipo)


@st.cache_resource
def get_analisador_inep(ano: int, force_download: bool = False):
    """
    Retorna um analisador de dados do INEP para um ano específico
    Similar ao get_analisador_domicilios para manter interface consistente

    Args:
        ano: Ano dos dados (2022, 2023, 2024)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        AnalisadorINEP inicializado com os dados do ano
    """
    from inep.analisador_inep import AnalisadorINEP

    df = carregar_educacao_basica_inep(ano=ano, force_download=force_download)

    if df is None:
        st.error(f"❌ Não foi possível carregar dados do INEP para o ano {ano}")
        return None

    return AnalisadorINEP(df=df, ano=ano)
# ============================================================================
# IBGE - Instituto Brasileiro de Geografia e Estatística
# ============================================================================

@cache_decorator
def carregar_dados_ibge_tabela7336(force_download: bool = False):
    """
    Carrega dados da Tabela 7336 do IBGE (Acesso à Internet)
    
    Args:
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame com os dados da tabela 7336 ou None se falhar
    """
    loader = IBGEDataLoader()
    df = loader.carregar_tabela7336(force_download=force_download)
    return df


@cache_resource_decorator
def get_analisador_tabela7336(force_download: bool = False):
    """
    Retorna uma instância única do AnalisadorTabela7336.
    O uso de st.cache_resource garante que o objeto seja mantido em memória sem serialização.

    Args:
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        AnalisadorTabela7336 configurado com os dados
    """
    df = carregar_dados_ibge_tabela7336(force_download)

    if df is None:
        raise ValueError("Não foi possível carregar dados de acesso à Internet (Tabela 7336) do IBGE")

    return AnalisadorTabela7336(df=df)


# ============================================================================
# PCD - Pessoas com Deficiência
# ============================================================================

@cache_decorator
def carregar_dados_pcd(ano: int = 2024, force_download: bool = False):
    """
    Carrega dados PCD (Pessoas com Deficiência) via HTTP (GitHub Releases)
    
    Args:
        ano: Ano dos dados (default: 2024)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame com os dados PCD ou None se falhar
    """
    loader = HTTPDataLoader(fonte='pcd')
    
    # Tenta carregar dados
    resultado = loader.carregar_dados(ano, 'dados-pcd', force_download)
    
    if resultado:
        df, _ = resultado
        return df
    
    return None


@cache_decorator
def carregar_dados_pcd_brasil_nordeste(ano: int = 2024, force_download: bool = False):
    """
    Carrega dados agregados PCD (Brasil e Nordeste) via HTTP (GitHub Releases)

    Args:
        ano: Ano dos dados (default: 2024)
        force_download: Forçar novo download mesmo se existir cache

    Returns:
        DataFrame com os dados agregados ou None se falhar
    """
    loader = HTTPDataLoader(fonte='pcd')

    resultado = loader.carregar_dados(ano, 'dados-pcd-br-ne', force_download)

    if resultado:
        df, _ = resultado
        return df

    return None


@cache_resource_decorator
def get_analisador_pcd(ano: int = 2024):
    """
    Retorna uma instância única do AnalisadorPCD.
    O uso de st.cache_resource garante que o objeto seja mantido em memória sem serialização.

    Args:
        ano: Ano dos dados (default: 2024)

    Returns:
        AnalisadorPCD configurado com os dados
    """
    df = carregar_dados_pcd(ano)

    if df is None:
        raise ValueError(f"Não foi possível carregar dados PCD de {ano}")

    return AnalisadorPCD(df=df, ano=ano)


def get_anos_disponiveis_pcd():
    """
    Retorna lista de anos disponíveis para dados PCD baseado nas pastas em cache

    Returns:
        Lista de anos disponíveis (ex: [2024, 2023, 2022])
    """
    from pathlib import Path
    from utils.data_sources import DATA_SOURCES
    
    cache_dir = Path(__file__).parent.parent.parent / 'data' / 'cache' / 'pcd'
    
    # Primeiro verifica se há anos configurados em DATA_SOURCES
    anos_configurados = []
    pcd_config = DATA_SOURCES.get('pcd', {})
    if 'urls' in pcd_config:
        anos_configurados = [ano for ano in pcd_config['urls'].keys() if isinstance(ano, int)]
    
    # Se DATA_SOURCES tem anos configurados, retorna eles
    if anos_configurados:
        return sorted(anos_configurados, reverse=True)
    
    # Caso contrário, busca por pastas de anos no cache
    if not cache_dir.exists():
        return []
    
    anos = []
    for item in cache_dir.iterdir():
        if item.is_dir() and item.name.isdigit() and len(item.name) == 4:
            ano = int(item.name)
            # Verifica se tem arquivo parquet dentro
            if any(item.glob('*.parquet')):
                anos.append(ano)
    
    return sorted(anos, reverse=True) if anos else []


