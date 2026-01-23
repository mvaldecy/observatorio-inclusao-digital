"""
Componente de Header sem logo
"""
import streamlit as st


def render_header(title: str, icon: str = "🌐"):
    """
    Renderiza o header padrão com título

    Args:
        title: Título da página
        icon: Ícone emoji para o título (opcional)
    """
    st.title(f"{icon} {title}")
    st.markdown("---")

