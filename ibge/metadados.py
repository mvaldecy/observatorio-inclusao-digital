"""
Informações sobre os dados da tabela 7336 do IBGE
Tabela: Pessoas de 10 anos ou mais de idade, por acesso à Internet
"""

METADADOS_TABELA7336 = {
    'nome': 'Pessoas de 10 anos ou mais de idade, por acesso à Internet',
    'codigo': 7336,
    'descricao': 'Dados sobre acesso à internet por pessoa, localização geográfica e período',
    'periodos_disponiveis': [2021, 2022, 2023, 2024],
    'variaveis_principais': [
        'Pessoas de 10 anos ou mais de idade',
        'Com acesso à Internet',
        'Sem acesso à Internet',
        'Acesso por smartphone',
        'Acesso por computador'
    ],
    'dimensoes': [
        'Unidade da Federação (UF)',
        'Região',
        'Localização (Urbana/Rural)',
        'Período'
    ],
    'fonte': 'PNAD Contínua',
    'website': 'https://www.ibge.gov.br'
}


def get_metadados() -> dict:
    """Retorna os metadados da tabela 7336"""
    return METADADOS_TABELA7336


def descricao_colunas() -> dict:
    """
    Descrição das colunas esperadas no CSV
    """
    return {
        'Brasil': 'Nível agregado Brasil',
        'Região': 'Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)',
        'UF': 'Unidade da Federação (Estado)',
        'Localização': 'Rural ou Urbana',
        'Ano': 'Período da pesquisa',
        'Valor': 'Número de pessoas (em mil)',
        'Percentual': 'Porcentagem relativa'
    }
