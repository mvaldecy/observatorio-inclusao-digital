import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class VisualizadorGeograficoMixin:
    @staticmethod
    def grafico_mapa_brasil(df: pd.DataFrame,
                            location_col: str,
                            value_col: str,
                            titulo: str = "") -> go.Figure:
        fig = px.choropleth(
            df,
            locations=location_col,
            locationmode='country names',
            color=value_col,
            scope='south america',
            title=titulo,
            color_continuous_scale='Blues'
        )

        fig.update_layout(height=500)
        return fig
