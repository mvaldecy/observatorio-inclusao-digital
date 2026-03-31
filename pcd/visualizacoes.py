"""
Utilitários de visualização para dados PCD

Responsabilidade: Helpers para criar gráficos e visualizações
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pcd.visualizacoes_partes import (
    VisualizadorGeograficoMixin,
    VisualizadorGraficosBasicosMixin,
    VisualizadorIndicadoresMixin,
)


class VisualizadorPCD(
    VisualizadorGraficosBasicosMixin,
    VisualizadorIndicadoresMixin,
    VisualizadorGeograficoMixin,
):
    """
    Cria visualizações para dados PCD
    
    Responsabilidades:
    - Gerar gráficos Plotly
    - Formatações consistentes
    - Templates reutilizáveis
    """
    
    # Cores padrão para visualizações
    CORES = {
        'principal': '#1f77b4',
        'secundaria': '#ff7f0e',
        'sucesso': '#2ca02c',
        'alerta': '#d62728',
        'info': '#9467bd'
    }
    
    PALETA_CATEGORIAS = px.colors.qualitative.Set2


# Funções helper rápidas

def criar_grafico_barras(dados: pd.Series, titulo: str = "") -> go.Figure:
    """Atalho para criar gráfico de barras"""
    return VisualizadorPCD.grafico_barras_simples(dados, titulo)


def criar_grafico_pizza(dados: pd.Series, titulo: str = "") -> go.Figure:
    """Atalho para criar gráfico de pizza"""
    return VisualizadorPCD.grafico_pizza(dados, titulo)


def criar_metrica(valor: float, titulo: str, formato: str = ".1f") -> dict:
    """Atalho para criar métrica"""
    return VisualizadorPCD.metrica_card(valor, titulo, formato)
