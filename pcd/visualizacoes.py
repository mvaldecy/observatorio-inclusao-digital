"""
Utilitários de visualização para dados PCD

Responsabilidade: Helpers para criar gráficos e visualizações
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class VisualizadorPCD:
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
    
    @staticmethod
    def grafico_barras_simples(dados: pd.Series, titulo: str = "", 
                                xlabel: str = "", ylabel: str = "") -> go.Figure:
        """Cria gráfico de barras simples"""
        fig = px.bar(
            x=dados.index,
            y=dados.values,
            labels={'x': xlabel, 'y': ylabel},
            title=titulo
        )
        
        fig.update_layout(
            showlegend=False,
            height=400
        )
        
        return fig
    
    @staticmethod
    def grafico_barras_horizontais(dados: pd.Series, titulo: str = "",
                                    xlabel: str = "", ylabel: str = "") -> go.Figure:
        """Cria gráfico de barras horizontais"""
        fig = px.bar(
            x=dados.values,
            y=dados.index,
            orientation='h',
            labels={'x': xlabel, 'y': ylabel},
            title=titulo
        )
        
        fig.update_layout(
            showlegend=False,
            height=max(300, len(dados) * 40)
        )
        
        return fig
    
    @staticmethod
    def grafico_pizza(dados: pd.Series, titulo: str = "") -> go.Figure:
        """Cria gráfico de pizza"""
        fig = px.pie(
            values=dados.values,
            names=dados.index,
            title=titulo
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        return fig
    
    @staticmethod
    def grafico_comparacao_barras(df: pd.DataFrame, 
                                   x_col: str, 
                                   y_cols: list,
                                   titulo: str = "",
                                   labels: dict = None) -> go.Figure:
        """Cria gráfico de barras com múltiplas séries"""
        fig = go.Figure()
        
        for y_col in y_cols:
            fig.add_trace(go.Bar(
                x=df[x_col],
                y=df[y_col],
                name=y_col
            ))
        
        fig.update_layout(
            title=titulo,
            barmode='group',
            height=400,
            xaxis_title=labels.get('x', x_col) if labels else x_col,
            yaxis_title=labels.get('y', '') if labels else ''
        )
        
        return fig
    
    @staticmethod
    def grafico_percentual_acesso(percentual: float, titulo: str = "Acesso à Internet") -> go.Figure:
        """Cria gráfico de gauge para percentual"""
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
    def grafico_linha_temporal(df: pd.DataFrame, 
                                x_col: str, 
                                y_col: str,
                                titulo: str = "",
                                labels: dict = None) -> go.Figure:
        """Cria gráfico de linha para séries temporais"""
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
    def grafico_mapa_brasil(df: pd.DataFrame,
                            location_col: str,
                            value_col: str,
                            titulo: str = "") -> go.Figure:
        """Cria mapa coroplético do Brasil por UF"""
        fig = px.choropleth(
            df,
            locations=location_col,
            locationmode='country names',  # ou 'USA-states' para UFs
            color=value_col,
            scope='south america',
            title=titulo,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(height=500)
        return fig
    
    @staticmethod
    def metrica_card(valor: float, titulo: str, formato: str = ".1f",
                     subtitulo: str = "", delta: float = None) -> dict:
        """
        Retorna dados formatados para card de métrica (para uso com st.metric)
        
        Returns:
            dict com 'value', 'label', 'delta'
        """
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
        """
        Formata DataFrame para exibição
        
        Args:
            df: DataFrame a formatar
            colunas_percentual: Colunas que são percentuais (adiciona % e formata)
            colunas_numero: Colunas numéricas (adiciona separador de milhares)
        """
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
    
    @staticmethod
    def grafico_heatmap(df: pd.DataFrame, 
                        x_col: str, 
                        y_col: str, 
                        value_col: str,
                        titulo: str = "") -> go.Figure:
        """Cria heatmap/mapa de calor"""
        # Pivot para formato de matriz
        pivot = df.pivot_table(index=y_col, columns=x_col, values=value_col)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='Blues'
        ))
        
        fig.update_layout(
            title=titulo,
            height=400
        )
        
        return fig
    
    @staticmethod
    def grafico_funil(dados: pd.Series, titulo: str = "") -> go.Figure:
        """Cria gráfico de funil"""
        fig = go.Figure(go.Funnel(
            y=dados.index,
            x=dados.values,
            textinfo="value+percent initial"
        ))
        
        fig.update_layout(
            title=titulo,
            height=400
        )
        
        return fig


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
