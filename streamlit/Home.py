import streamlit as st

st.set_page_config(
    page_title="Observatório de Inclusão Digital",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Observatório de Inclusão Digital")

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
