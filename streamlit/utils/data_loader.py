import sys
import os
import streamlit as st

# Adiciona a raiz do projeto ao sys.path para permitir importações dos módulos cetic
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from cetic.domicilios.analisador_domicilios_cetic import AnalisadorDomiciliosCETIC

@st.cache_resource
def get_analisador_domicilios():
    """
    Retorna uma instância única do AnalisadorDomiciliosCETIC.
    O uso de st.cache_resource garante que o arquivo parquet seja carregado apenas uma vez.
    """
    return AnalisadorDomiciliosCETIC()
