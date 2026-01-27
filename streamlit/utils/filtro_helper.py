"""
Helper para gestão de filtros CETIC
Centraliza lógica de filtros para evitar duplicação de código
"""
from typing import Dict, List, Any, Optional
import pandas as pd


class FiltroHelper:
    """Helper para gestão de filtros CETIC"""

    @staticmethod
    def get_meta_value(meta_class, label_map: Dict, selected_label: str) -> Optional[Any]:
        """
        Obtém valor do metadado baseado no label selecionado

        Args:
            meta_class: Classe de metadados (ex: Metadados.COD_UF)
            label_map: Dicionário de mapeamento valor -> label
            selected_label: Label selecionado pelo usuário

        Returns:
            Valor do metadado ou None
        """
        if selected_label in ["Todas", "Brasil", "Todos", "Todas as regiões"]:
            return None
        if not label_map:
            return None

        try:
            # Encontrar valor correspondente ao label
            valores = [k for k, v in label_map.items() if v == selected_label]
            if not valores:
                return None

            valor = valores[0]

            # Buscar atributo da classe que corresponde ao valor
            for attr in dir(meta_class):
                if not attr.startswith('_'):
                    meta_val = getattr(meta_class, attr)
                    if isinstance(meta_val, (int, float)) and meta_val == valor:
                        return meta_val
        except Exception as e:
            print(f"Erro ao obter meta_value: {e}")
            return None

        return None

    @staticmethod
    def verificar_metadado_disponivel(meta_class, nome_campo: str) -> bool:
        """
        Verifica se metadado está disponível e tem dados

        Args:
            meta_class: Classe de metadados completa (ex: Metadados)
            nome_campo: Nome do campo a verificar (ex: 'COD_UF')

        Returns:
            True se disponível, False caso contrário
        """
        try:
            campo = getattr(meta_class, nome_campo, None)
            return campo is not None and hasattr(campo, '_map') and len(campo._map) > 0
        except Exception:
            return False

    @staticmethod
    def aplicar_filtros(df: pd.DataFrame, filtros: List) -> pd.DataFrame:
        """
        Aplica lista de filtros ao DataFrame

        Args:
            df: DataFrame original
            filtros: Lista de valores de metadados para filtrar

        Returns:
            DataFrame filtrado
        """
        df_resultado = df.copy()
        for filtro in filtros:
            if filtro is not None:
                col = filtro.column
                if col in df_resultado.columns:
                    df_resultado = df_resultado[df_resultado[col] == filtro]
        return df_resultado

    @staticmethod
    def criar_descricao_filtros(filtros: List, meta_class) -> List[str]:
        """
        Cria descrições amigáveis dos filtros ativos

        Args:
            filtros: Lista de valores de metadados aplicados
            meta_class: Classe de metadados completa

        Returns:
            Lista de strings descrevendo os filtros
        """
        descricoes = []
        for filtro in filtros:
            if filtro is not None:
                col = filtro.column
                meta_campo = getattr(meta_class, col, None)
                if meta_campo and hasattr(meta_campo, '_map'):
                    label = meta_campo._map.get(float(filtro), str(filtro))
                    col_name = getattr(meta_campo, '_label', col)
                    descricoes.append(f"**{col_name}:** {label}")
        return descricoes

    @staticmethod
    def get_opcoes_select(meta_campo, prefixo_todos: str = "Todas") -> List[str]:
        """
        Obtém opções ordenadas para selectbox

        Args:
            meta_campo: Campo de metadados (ex: Metadados.COD_UF)
            prefixo_todos: Texto para opção "todos" (ex: "Todas", "Todos")

        Returns:
            Lista de labels ordenadas com prefixo_todos no início
        """
        if meta_campo is None or not hasattr(meta_campo, '_map'):
            return [prefixo_todos]

        labels = sorted(meta_campo._map.values())
        return [prefixo_todos] + labels

