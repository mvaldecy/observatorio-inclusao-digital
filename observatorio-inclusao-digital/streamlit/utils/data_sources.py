"""
Configuração de URLs das fontes de dados
Centralizadas em um único arquivo para facilitar manutenção
"""

DATA_SOURCES = {
    'cetic': {
        'name': 'CETIC.br - Centro de Estudos sobre as TIC',
        'description': 'Pesquisa TIC Domicílios e Indivíduos',
        'website': 'https://cetic.br',
        'urls': {
            2025: {
                'domicilios': 'https://cetic.br/media/microdados/983/tic_domicilios_2025_domicilios_base_de_microdados_v1.0.sav',
                'individuos': 'https://cetic.br/media/microdados/988/tic_domicilios_2025_individuos_base_de_microdados_v1.0.sav'
            },
            2024: {
                'domicilios': 'https://cetic.br/media/microdados/863/tic_domicilios_2024_domicilios_base_de_microdados_v1.0.sav',
                'individuos': 'https://cetic.br/media/microdados/861/tic_domicilios_2024_individuos_base_de_microdados_v1.0.sav'
            },
            2023: {
                'domicilios': 'https://cetic.br/media/microdados/758/tic_domicilios_2023_domicilios_base_de_microdados_v1.0.sav',
                'individuos': 'https://cetic.br/media/microdados/754/tic_domicilios_2023_individuos_base_de_microdados_v1.0.sav'
            }
        }
    },
    # Futuramente outras fontes:
    # 'anatel': {
    #     'name': 'ANATEL - Agência Nacional de Telecomunicações',
    #     'description': 'Dados de telecomunicações e telefonia',
    #     'website': 'https://www.gov.br/anatel',
    #     'urls': {
    #         2024: {...}
    #     }
    # },
    # 'ibge': {
    #     'name': 'IBGE - Instituto Brasileiro de Geografia e Estatística',
    #     'description': 'Dados demográficos e socioeconômicos',
    #     'website': 'https://www.ibge.gov.br',
    #     'urls': {
    #         2024: {...}
    #     }
    # }
}


def get_fonte_info(fonte: str) -> dict:
    """
    Retorna informações sobre uma fonte de dados

    Args:
        fonte: Nome da fonte ('cetic', 'anatel', 'ibge', etc.)

    Returns:
        Dicionário com informações da fonte ou None se não encontrada
    """
    return DATA_SOURCES.get(fonte)


def get_fonte_urls(fonte: str) -> dict:
    """
    Retorna apenas as URLs de uma fonte

    Args:
        fonte: Nome da fonte ('cetic', 'anatel', 'ibge', etc.)

    Returns:
        Dicionário com URLs organizadas por ano e tipo
    """
    fonte_data = DATA_SOURCES.get(fonte)
    if fonte_data:
        return fonte_data.get('urls', {})
    return {}


def list_fontes() -> list:
    """
    Lista todas as fontes de dados disponíveis

    Returns:
        Lista com nomes das fontes
    """
    return list(DATA_SOURCES.keys())


def get_anos_disponiveis(fonte: str, tipo: str = None) -> list:
    """
    Retorna lista de anos disponíveis para uma fonte

    Args:
        fonte: Nome da fonte
        tipo: Tipo de dado (opcional) - 'domicilios' ou 'individuos'

    Returns:
        Lista de anos disponíveis (ordenada decrescente)
    """
    urls = get_fonte_urls(fonte)

    if tipo:
        # Retorna apenas anos que têm o tipo especificado
        anos = [ano for ano, tipos in urls.items() if tipo in tipos]
        return sorted(anos, reverse=True)

    return sorted(urls.keys(), reverse=True)

