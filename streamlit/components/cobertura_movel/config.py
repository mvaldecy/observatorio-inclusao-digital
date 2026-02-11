"""
Configurações e constantes para a página de Cobertura Móvel
"""
import streamlit as st

# Constantes
NE_UF = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']

# CSS customizado para dark theme
CSS_CUSTOM = """
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #333;
    }
    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
    }
    .tag-blue { background-color: #1e40af; color: white; }
    .tag-green { background-color: #166534; color: white; }
    .tag-purple { background-color: #6b21a8; color: white; }
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
    
    # Título da página
    st.markdown("# 📡 Anatel - Cobertura Móvel")
    
    # CSS customizado
    st.markdown(CSS_CUSTOM, unsafe_allow_html=True)
    st.markdown("---")
