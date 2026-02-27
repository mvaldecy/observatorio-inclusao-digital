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


def criar_header(titulo: str, descricao: str = "", icon: str = "🌐"):
    """
    Cria header completo com título e descrição
    
    Args:
        titulo: Título da página
        descricao: Descrição/subtítulo (opcional)
        icon: Ícone emoji (opcional)
    """
    st.title(f"{icon} {titulo}")
    if descricao:
        st.markdown(descricao)
    st.markdown("---")
