import streamlit as st
import sys
import os

# Adiciona o diretório streamlit ao path
streamlit_path = os.path.dirname(__file__)
if streamlit_path not in sys.path:
    sys.path.append(streamlit_path)

from components.header import render_header

st.set_page_config(
    page_title="Observatório",
    page_icon="🏠",
    layout="wide"
)

# Renderizar header com logo
render_header("Observatório de Inclusão Digital", "🌐")

st.markdown("""
Bem-vindo ao Dashboard do Observatório de Inclusão Digital.

Este projeto visa analisar e visualizar dados sobre o acesso à tecnologia e à internet no Brasil.

### Como navegar:
Utilize o menu lateral para acessar os dashboards específicos:
- **Cetic Domicílios**: Análise de acesso à internet e tecnologia nos domicílios brasileiros.
- **Cetic Indivíduos**: Análise do comportamento e acesso à internet por indivíduos.

---
*Desenvolvido para análise de microdados da TIC Domicílios.*
""")
