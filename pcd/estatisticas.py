"""
Módulo de estatísticas e análises para dados PCD.

Arquivo agregador para manter API estável com implementação modular.
"""

import pandas as pd

from pcd.estatisticas_partes import (
    EstatisticasAcessoBarreirasMixin,
    EstatisticasPerfilComparacoesMixin,
)


class EstatisticasPCD(EstatisticasAcessoBarreirasMixin, EstatisticasPerfilComparacoesMixin):
    """Calcula estatísticas e métricas dos dados PCD."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
