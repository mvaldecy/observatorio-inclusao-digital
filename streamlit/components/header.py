"""
Componente de Header sem logo
"""
import streamlit as st

_CSS_GLOBAL = """
<style>
    /* Remove bordas laranja/vermelhas de labels, headers e títulos */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] label,
    label[data-baseweb="label"],
    div[data-baseweb="label"] {
        border: none !important;
        outline: none !important;
    }
    .stSelectbox label,
    .stMultiSelect label,
    div[role="option"] {
        border: none !important;
        outline: none !important;
    }
    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="combobox"],
    div[role="listbox"],
    div[data-baseweb="select"] {
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        outline: none !important;
    }
    [data-baseweb="input"]:focus,
    [data-baseweb="select"]:focus,
    [data-baseweb="combobox"]:focus,
    input:focus {
        border-color: #0d58ca !important;
        box-shadow: 0 0 0 1px #0d58ca !important;
        outline: none !important;
    }
    div[style*="background"] > div[role="listbox"] {
        border: 1px solid #ccc !important;
        outline: none !important;
    }
    div[data-testid="stMultiSelect"] span {
        color: #262730 !important;
        border: none !important;
    }
    input {
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        outline: none !important;
    }
    input:invalid {
        border-color: #ccc !important;
        box-shadow: none !important;
        outline: none !important;
    }
    [data-testid="stSidebar"] div[data-baseweb] {
        border: none !important;
    }
    div[style*="rgb(255, 159, 64)"],
    div[style*="#FF9F40"],
    div[style*="#ffb3b3"],
    div[style*="orange"] {
        border: none !important;
        box-shadow: none !important;
    }
</style>
"""


def inject_global_css():
    """Injeta o CSS global compartilhado entre todas as páginas."""
    st.markdown(_CSS_GLOBAL, unsafe_allow_html=True)


def render_header(title: str, icon: str = "🌐"):
    """
    Renderiza o header padrão com título e injeta o CSS global.

    Args:
        title: Título da página
        icon: Ícone emoji para o título (opcional)
    """
    inject_global_css()
    st.title(f"{icon} {title}")
    st.markdown("---")


def criar_header(titulo: str, descricao: str = "", icon: str = "🌐"):
    """
    Cria header completo com título, descrição e injeta o CSS global.

    Args:
        titulo: Título da página
        descricao: Descrição/subtítulo (opcional)
        icon: Ícone emoji (opcional)
    """
    inject_global_css()
    st.title(f"{icon} {titulo}")
    if descricao:
        st.markdown(descricao)
    st.markdown("---")
