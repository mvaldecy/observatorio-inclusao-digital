"""
Componentes para a página de Cobertura Móvel
"""
from .config import aplicar_configuracoes
from .filtros import renderizar_filtros
from .comparativo_brasil import renderizar_comparativo_brasil
from .comparativo_urbano_rural import renderizar_comparativo_urbano_rural
from .analise_municipios import renderizar_analise_municipios
from .utils import safe_unique

__all__ = [
    'aplicar_configuracoes',
    'renderizar_filtros',
    'renderizar_comparativo_brasil',
    'renderizar_comparativo_urbano_rural',
    'renderizar_analise_municipios',
    'safe_unique'
]
