"""
Analisador principal de dados PCD

Responsabilidade: expor API estável com implementação modular.
"""

from pcd.analisadores.base import AnalisadorPCDBase
from pcd.analisadores.indicadores_2022 import IndicadoresPCDTEA2022Mixin


class AnalisadorPCD(IndicadoresPCDTEA2022Mixin, AnalisadorPCDBase):
    """Analisador principal para dados PCD/TEA com filtros e indicadores."""

    pass
