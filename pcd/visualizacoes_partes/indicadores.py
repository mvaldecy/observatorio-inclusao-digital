import pandas as pd
import plotly.graph_objects as go


class VisualizadorIndicadoresMixin:
    @staticmethod
    def grafico_percentual_acesso(percentual: float, titulo: str = "Acesso à Internet") -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=percentual,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': titulo},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "gray"},
                    {'range': [50, 75], 'color': "lightblue"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        return fig

    @staticmethod
    def metrica_card(valor: float, titulo: str, formato: str = ".1f",
                     subtitulo: str = "", delta: float = None) -> dict:
        if formato.endswith('f'):
            valor_formatado = f"{valor:{formato}}"
        elif formato == '%':
            valor_formatado = f"{valor:.1f}%"
        else:
            valor_formatado = str(valor)

        resultado = {
            'label': titulo,
            'value': valor_formatado
        }

        if delta is not None:
            resultado['delta'] = f"{delta:+.1f}%"

        if subtitulo:
            resultado['help'] = subtitulo

        return resultado

    @staticmethod
    def tabela_formatada(df: pd.DataFrame,
                         colunas_percentual: list = None,
                         colunas_numero: list = None) -> pd.DataFrame:
        df_formatado = df.copy()

        if colunas_percentual:
            for col in colunas_percentual:
                if col in df_formatado.columns:
                    df_formatado[col] = df_formatado[col].apply(lambda x: f"{x:.1f}%")

        if colunas_numero:
            for col in colunas_numero:
                if col in df_formatado.columns:
                    df_formatado[col] = df_formatado[col].apply(lambda x: f"{x:,.0f}")

        return df_formatado
