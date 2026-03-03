"""
Funções auxiliares para os componentes de Cobertura Móvel
"""
import pandas as pd


def safe_unique(series: pd.Series) -> list[str]:
    """
    Retorna valores únicos de uma Series, removendo valores nulos e espaços extras.
    """
    return sorted({str(v).strip() for v in series.dropna().unique() if str(v).strip()})
