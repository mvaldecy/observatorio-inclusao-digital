"""
Componentes do INEP - Censo Escolar
"""

from .categorias_inep import (
    CATEGORIAS_INEP,
    AGREGADORES_INEP,
    UFS_BRASIL,
    REGIOES_BRASIL
)

from .filtro_inep import FiltroINEP
from .comparativo_geografico_inep import ComparativoGeograficoINEP

__all__ = [
    'CATEGORIAS_INEP',
    'AGREGADORES_INEP',
    'UFS_BRASIL',
    'REGIOES_BRASIL',
    'FiltroINEP',
    'ComparativoGeograficoINEP',
]


