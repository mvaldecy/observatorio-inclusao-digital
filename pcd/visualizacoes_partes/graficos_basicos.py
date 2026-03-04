import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class VisualizadorGraficosBasicosMixin:
    @staticmethod
    def grafico_barras_simples(dados: pd.Series, titulo: str = "",
                               xlabel: str = "", ylabel: str = "") -> go.Figure:
        fig = px.bar(
            x=dados.index,
            y=dados.values,
            labels={'x': xlabel, 'y': ylabel},
            title=titulo
        )
        fig.update_layout(showlegend=False, height=400)
        return fig

    @staticmethod
    def grafico_barras_horizontais(dados: pd.Series, titulo: str = "",
                                   xlabel: str = "", ylabel: str = "") -> go.Figure:
        fig = px.bar(
            x=dados.values,
            y=dados.index,
            orientation='h',
            labels={'x': xlabel, 'y': ylabel},
            title=titulo
        )
        fig.update_layout(showlegend=False, height=max(300, len(dados) * 40))
        return fig

    @staticmethod
    def grafico_pizza(dados: pd.Series, titulo: str = "") -> go.Figure:
        fig = px.pie(values=dados.values, names=dados.index, title=titulo)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        return fig

    @staticmethod
    def grafico_comparacao_barras(df: pd.DataFrame,
                                  x_col: str,
                                  y_cols: list,
                                  titulo: str = "",
                                  labels: dict = None) -> go.Figure:
        fig = go.Figure()
        for y_col in y_cols:
            fig.add_trace(go.Bar(x=df[x_col], y=df[y_col], name=y_col))

        fig.update_layout(
            title=titulo,
            barmode='group',
            height=400,
            xaxis_title=labels.get('x', x_col) if labels else x_col,
            yaxis_title=labels.get('y', '') if labels else ''
        )
        return fig

    @staticmethod
    def grafico_linha_temporal(df: pd.DataFrame,
                               x_col: str,
                               y_col: str,
                               titulo: str = "",
                               labels: dict = None) -> go.Figure:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            title=titulo,
            labels=labels or {},
            markers=True
        )
        fig.update_layout(height=400)
        return fig

    @staticmethod
    def grafico_heatmap(df: pd.DataFrame,
                        x_col: str,
                        y_col: str,
                        value_col: str,
                        titulo: str = "") -> go.Figure:
        pivot = df.pivot_table(index=y_col, columns=x_col, values=value_col)

        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='Blues'
        ))

        fig.update_layout(title=titulo, height=400)
        return fig

    @staticmethod
    def grafico_funil(dados: pd.Series, titulo: str = "") -> go.Figure:
        fig = go.Figure(go.Funnel(
            y=dados.index,
            x=dados.values,
            textinfo="value+percent initial"
        ))
        fig.update_layout(title=titulo, height=400)
        return fig
