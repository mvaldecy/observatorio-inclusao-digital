"""
Módulo INEP - Instituto Nacional de Estudos e Pesquisas Educacionais
Análise de dados do Censo Escolar da Educação Básica
"""

# Importa o dicionário antigo (carregado do Excel)
from .dicionario_educacao_basica import (
    METADADOS_INEP as METADADOS_INEP_ORIGINAL,
    CATEGORIAS_INEP as CATEGORIAS_INEP_ORIGINAL,
    get_metadados,
    get_categorias,
    listar_categorias as listar_categorias_originais,
    listar_variaveis_por_categoria,
    formatar_valor_categorico
)

# Importa o novo dicionário (estilo CETIC)
from .metadados_inep import (
    METADADOS_INEP,
    get_label,
    get_valores,
    formatar_valor,
    listar_categorias,
    listar_variaveis,
    get_categoria_variavel
)

# Importa o analisador
from .analisador_inep import AnalisadorINEP, criar_analisador_inep

__all__ = [
    # Analisador
    'AnalisadorINEP',
    'criar_analisador_inep',

    # Dicionário estilo CETIC (recomendado)
    'METADADOS_INEP',
    'get_label',
    'get_valores',
    'formatar_valor',
    'listar_categorias',
    'listar_variaveis',
    'get_categoria_variavel',

    # Dicionário original (compatibilidade)
    'METADADOS_INEP_ORIGINAL',
    'CATEGORIAS_INEP_ORIGINAL',
    'get_metadados',
    'get_categorias',
    'listar_categorias_originais',
    'listar_variaveis_por_categoria',
    'formatar_valor_categorico'
]


