"""
Design system centralizado para o Observatório de Inclusão Digital.

Tema claro (fundo branco) com boas práticas de acessibilidade (WCAG AA)
e storytelling de dados.

Uso em cada página, logo após st.set_page_config():

    from components.theme import apply_global_styles
    apply_global_styles()
"""

import streamlit as st

# ============================================================================
# PALETA DE CORES
# ============================================================================

# Cores institucionais
COR_PRIMARIA = "#1B4F8A"        # Azul institucional profundo
COR_PRIMARIA_MEDIA = "#2E86C1"  # Azul médio
COR_PRIMARIA_BG = "#EBF2FA"     # Fundo azul muito suave

# Paleta para visualizações de dados (amigável para daltônicos)
PALETA_DADOS = [
    "#1B4F8A",  # Azul
    "#27AE60",  # Verde
    "#E67E22",  # Laranja
    "#7B2D8B",  # Roxo
    "#C0392B",  # Vermelho
    "#16A085",  # Teal
]

# Cores semânticas
COR_SUCESSO = "#27AE60"
COR_AVISO = "#E67E22"
COR_ERRO = "#C0392B"
COR_INFO = "#2E86C1"

# Cores de interface (UI)
COR_FUNDO = "#FFFFFF"
COR_SUPERFICIE = "#F8FAFC"
COR_BORDA = "#E2E8F0"
COR_TEXTO_PRIMARIO = "#1A202C"
COR_TEXTO_SECUNDARIO = "#718096"

# ============================================================================
# CSS GLOBAL
# ============================================================================

CSS_GLOBAL = """
<style>
    /* ── Base ── */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* ── Cards e containers ── */
    .card-container {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }

    .card-destaque {
        background-color: #EBF2FA;
        border: 1px solid #BDD7EE;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }

    .card-insight {
        background-color: #EAFAF1;
        border-left: 4px solid #27AE60;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }

    .card-aviso {
        background-color: #FEF9E7;
        border-left: 4px solid #E67E22;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }

    /* ── Metric cards ── */
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    /* ── Tags / Badges ── */
    .tag {
        display: inline-block;
        padding: 0.2rem 0.65rem;
        margin: 0.2rem;
        border-radius: 0.25rem;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .tag-blue   { background-color: #DBEAFE; color: #1E40AF; border: 1px solid #BFDBFE; }
    .tag-green  { background-color: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
    .tag-purple { background-color: #EDE9FE; color: #5B21B6; border: 1px solid #DDD6FE; }
    .tag-orange { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .tag-red    { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* ── Inputs ── */
    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="combobox"],
    div[data-baseweb="select"] {
        border: 1px solid #CBD5E0 !important;
        border-radius: 4px !important;
    }

    [data-baseweb="input"]:focus,
    [data-baseweb="select"]:focus,
    input:focus {
        border-color: #1B4F8A !important;
        box-shadow: 0 0 0 1px #1B4F8A !important;
    }

    /* Remove border-bottom laranja do Streamlit em labels */
    label[data-baseweb="label"],
    div[data-baseweb="label"],
    .stSelectbox label,
    .stMultiSelect label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        border: none !important;
        outline: none !important;
    }

    /* ── Main header ── */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1A202C;
        margin-bottom: 1.5rem;
    }

    /* ── Footer ── */
    .footer-obs {
        text-align: center;
        color: #718096;
        padding: 1.5rem;
        font-size: 0.875rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 2rem;
    }
</style>
"""

# ============================================================================
# CONFIGURAÇÕES PADRÃO DE GRÁFICOS PLOTLY (tema claro)
# ============================================================================

PLOTLY_LAYOUT_PADRAO = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="sans-serif", size=12, color="#1A202C"),
    xaxis=dict(
        gridcolor="#E2E8F0",
        linecolor="#CBD5E0",
        tickfont=dict(color="#718096"),
    ),
    yaxis=dict(
        gridcolor="#E2E8F0",
        linecolor="#CBD5E0",
        tickfont=dict(color="#718096"),
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#E2E8F0",
        borderwidth=1,
    ),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E2E8F0",
        font=dict(color="#1A202C"),
    ),
)

# Estilo de anotação para gráficos (legível no fundo claro)
ANOTACAO_PADRAO = dict(
    bgcolor="rgba(255,255,255,0.92)",
    bordercolor="#CBD5E0",
    borderwidth=1,
    borderpad=4,
)


def apply_plotly_layout(fig, height: int = None, title: str = None, extra: dict = None):
    """Aplica layout padrão do tema claro a uma figura Plotly.

    Args:
        fig: Figura plotly a atualizar.
        height: Altura em pixels (opcional).
        title: Título da figura (opcional).
        extra: Dicionário com propriedades adicionais de layout (opcional).

    Returns:
        A mesma figura com layout atualizado.
    """
    layout = dict(PLOTLY_LAYOUT_PADRAO)
    if height:
        layout["height"] = height
    if title:
        layout["title"] = dict(text=title, font=dict(size=14, color="#1A202C"))
    if extra:
        layout.update(extra)
    fig.update_layout(**layout)
    return fig


def apply_global_styles():
    """Injeta o CSS global na página. Chamar logo após st.set_page_config()."""
    st.markdown(CSS_GLOBAL, unsafe_allow_html=True)
