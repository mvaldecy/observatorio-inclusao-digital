"""
Configurações e constantes para a página de Cobertura Móvel
"""
import streamlit as st
import sys
import os

# Garante que components/ está no path para importar theme
_comp_dir = os.path.dirname(os.path.dirname(__file__))
if _comp_dir not in sys.path:
    sys.path.insert(0, _comp_dir)

from components.theme import apply_global_styles

# Constantes
NE_UF = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']

# CSS específico para componentes de Cobertura Móvel (complementa o tema global)
CSS_COBERTURA = """
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1A202C;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
    }
    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .tag-blue   { background-color: #DBEAFE; color: #1E40AF; border: 1px solid #BFDBFE; }
    .tag-green  { background-color: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
    .tag-purple { background-color: #EDE9FE; color: #5B21B6; border: 1px solid #DDD6FE; }
</style>
"""


def aplicar_configuracoes():
    """
    Aplica configurações iniciais da página (título, CSS, etc.)
    """
    # Configuração da página
    st.set_page_config(
        page_title="Cobertura Móvel - ANATEL",
        layout="wide",
        page_icon="📡"
    )

    # Aplica tema global claro
    apply_global_styles()

    # CSS adicional específico da página
    st.markdown(CSS_COBERTURA, unsafe_allow_html=True)

    # Título da página
    st.markdown("# 📡 Anatel - Cobertura Móvel")
    st.markdown("---")
