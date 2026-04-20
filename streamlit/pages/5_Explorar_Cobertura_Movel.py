"""
Página de Exploração de Dados de Cobertura Móvel (4G e 5G) da ANATEL
Esta página permite carregar e visualizar a estrutura dos dados
"""
import os
import sys
import streamlit as st

# Adiciona a raiz do projeto ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

# Importação robusta que funciona local e no deploy
try:
    from utils.data_loader import (
        carregar_cobertura_movel_anatel,
        carregar_cobertura_movel_4g_uf_anatel,
        carregar_cobertura_movel_5g_uf_anatel
    )
    from components.explorador_dados import explorador_dados
except ImportError:
    # Fallback para quando rodando do diretório raiz (deploy)
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils.data_loader import (
        carregar_cobertura_movel_anatel,
        carregar_cobertura_movel_4g_uf_anatel,
        carregar_cobertura_movel_5g_uf_anatel
    )
    from components.explorador_dados import explorador_dados

# Configuração da página
st.set_page_config(
    page_title="Explorar Cobertura Móvel - ANATEL",
    layout="wide",
    page_icon="🔍"
)

# Libera memória de outros datasets ao abrir esta página
from utils.memory_manager import set_active_dataset
from components.theme import apply_global_styles
set_active_dataset("anatel_cobertura_movel")
apply_global_styles()

# Configuração dos tipos de dados disponíveis
TIPOS_DADOS = {
    "Cobertura Móvel (Geral)": {
        "loader": carregar_cobertura_movel_anatel,
        "descricao": "Dados consolidados de cobertura móvel em todos os municípios brasileiros"
    },
    "Cobertura 4G por UF": {
        "loader": carregar_cobertura_movel_4g_uf_anatel,
        "descricao": "Dados específicos de cobertura 4G agregados por Unidade Federativa"
    },
    "Cobertura 5G por UF": {
        "loader": carregar_cobertura_movel_5g_uf_anatel,
        "descricao": "Dados específicos de cobertura 5G agregados por Unidade Federativa"
    }
}

# Descrição da página
DESCRICAO = """
### Sobre os Dados de Cobertura Móvel

Esta página permite explorar três tipos de dados da ANATEL:

1. **Cobertura Móvel (Geral)**: Dados consolidados de cobertura móvel em todos os municípios
2. **Cobertura 4G por UF**: Dados específicos de cobertura 4G agregados por Unidade Federativa
3. **Cobertura 5G por UF**: Dados específicos de cobertura 5G agregados por Unidade Federativa
"""

# Usar o componente explorador de dados
explorador_dados(
    tipos_dados=TIPOS_DADOS,
    titulo="🔍 Exploração de Dados de Cobertura Móvel",
    descricao=DESCRICAO,
    fonte="ANATEL - Agência Nacional de Telecomunicações"
)


