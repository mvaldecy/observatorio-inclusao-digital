"""
Categorias e indicadores do INEP organizados para análise
Estrutura similar ao CATEGORIAS_DOMICILIO do CETIC
"""

CATEGORIAS_INEP = {
    "🌐 Internet e Tecnologia": {
        "Acesso à Internet": "IN_INTERNET",
        "Internet para Alunos": "IN_INTERNET_ALUNOS",
        "Internet para Ensino": "IN_INTERNET_APRENDIZAGEM",
        "Banda Larga": "IN_BANDA_LARGA",
        "Laboratório de Informática": "IN_LABORATORIO_INFORMATICA",
        "Comparativo Internet": ["IN_INTERNET", "IN_BANDA_LARGA", "IN_INTERNET_ALUNOS", "IN_INTERNET_APRENDIZAGEM"],
        "Comparativo Infraestrutura TI": ["IN_LABORATORIO_INFORMATICA", "IN_INTERNET", "IN_BANDA_LARGA"],
    },

    "💻 Equipamentos": {
        "Computadores Desktop (Alunos)": "QT_DESKTOP_ALUNO",
        "Computadores Portáteis (Alunos)": "QT_COMP_PORTATIL_ALUNO",
        "Tablets (Alunos)": "QT_TABLET_ALUNO",
        "Possui Computador": "IN_EQUIP_COMPUTADOR",
        "Projetor Multimídia": "IN_EQUIP_MULTIMIDIA",
        "Impressora": "IN_EQUIP_IMPRESSORA",
        "Comparativo Computadores": ["QT_DESKTOP_ALUNO", "QT_COMP_PORTATIL_ALUNO", "QT_TABLET_ALUNO"],
    },

    "🏫 Caracterização da Escola": {
        "Dependência Administrativa": "TP_DEPENDENCIA",
        "Localização (Urbana/Rural)": "TP_LOCALIZACAO",
        "Categoria Escola Privada": "TP_CATEGORIA_ESCOLA_PRIVADA",
        "Situação de Funcionamento": "TP_SITUACAO_FUNCIONAMENTO",
        "Localização Diferenciada": "TP_LOCALIZACAO_DIFERENCIADA",
    },

    "🏗️ Infraestrutura Básica": {
        "Água - Rede Pública": "IN_AGUA_REDE_PUBLICA",
        "Água Potável": "IN_AGUA_POTAVEL",
        "Energia - Rede Pública": "IN_ENERGIA_REDE_PUBLICA",
        "Esgoto - Rede Pública": "IN_ESGOTO_REDE_PUBLICA",
        "Lixo - Coleta Periódica": "IN_LIXO_COLETA_PERIODICA",
        "Comparativo Saneamento": ["IN_AGUA_REDE_PUBLICA", "IN_ENERGIA_REDE_PUBLICA", "IN_ESGOTO_REDE_PUBLICA", "IN_LIXO_COLETA_PERIODICA"],
    },

    "📚 Espaços e Dependências": {
        "Biblioteca": "IN_BIBLIOTECA",
        "Sala de Leitura": "IN_SALA_LEITURA",
        "Laboratório de Ciências": "IN_LABORATORIO_CIENCIAS",
        "Quadra de Esportes": "IN_QUADRA_ESPORTES",
        "Refeitório": "IN_REFEITORIO",
        "Banheiro PNE": "IN_BANHEIRO_PNE",
        "Sala de Professores": "IN_SALA_PROFESSOR",
        "Comparativo Espaços": ["IN_BIBLIOTECA", "IN_LABORATORIO_INFORMATICA", "IN_LABORATORIO_CIENCIAS", "IN_QUADRA_ESPORTES"],
    },

    "♿ Acessibilidade": {
        "Dependências PNE": "IN_DEPENDENCIAS_PNE",
        "Banheiro PNE": "IN_BANHEIRO_PNE",
        "Sala Atendimento Especial": "IN_SALA_ATENDIMENTO_ESPECIAL",
    },

    "👥 Matrículas e Docentes": {
        "Total de Matrículas": "QT_MAT_BAS",
        "Matrículas - Fundamental": "QT_MAT_FUND",
        "Matrículas - Médio": "QT_MAT_MED",
        "Matrículas - EJA": "QT_MAT_EJA",
        "Total de Docentes": "QT_DOC_BAS",
        "Docentes - Fundamental": "QT_DOC_FUND",
        "Docentes - Médio": "QT_DOC_MED",
        "Comparativo Matrículas": ["QT_MAT_FUND", "QT_MAT_MED", "QT_MAT_EJA"],
        "Comparativo Docentes": ["QT_DOC_FUND", "QT_DOC_MED", "QT_DOC_EJA"],
    },

    "📖 Modalidades de Ensino": {
        "Ensino Regular": "IN_REGULAR",
        "Educação de Jovens e Adultos": "IN_EJA",
        "Educação Profissional": "IN_PROFISSIONALIZANTE",
        "Educação Especial Exclusiva": "IN_ESPECIAL_EXCLUSIVA",
        "Ensino Fundamental - Anos Iniciais": "IN_COMUM_FUND_AI",
        "Ensino Fundamental - Anos Finais": "IN_COMUM_FUND_AF",
        "Ensino Médio": "IN_COMUM_MEDIO_MEDIO",
    },

    "🍽️ Serviços Complementares": {
        "Alimentação Escolar": "IN_ALIMENTACAO",
        "Atendimento Educacional Especializado": "IN_AEE",
        "Atividade Complementar": "IN_ATIVIDADE_COMPLEMENTAR",
    },
}

# Agregadores comuns para análise
AGREGADORES_INEP = {
    "Por Dependência Administrativa": "TP_DEPENDENCIA",
    "Por Localização (Urbana/Rural)": "TP_LOCALIZACAO",
    "Por Região": "CO_REGIAO",
    "Por Estado (UF)": "CO_UF",
    "Por Situação de Funcionamento": "TP_SITUACAO_FUNCIONAMENTO",
    "Por Localização Diferenciada": "TP_LOCALIZACAO_DIFERENCIADA",
}

# UFs para filtros
UFS_BRASIL = {
    11: "Rondônia", 12: "Acre", 13: "Amazonas", 14: "Roraima", 15: "Pará",
    16: "Amapá", 17: "Tocantins", 21: "Maranhão", 22: "Piauí", 23: "Ceará",
    24: "Rio Grande do Norte", 25: "Paraíba", 26: "Pernambuco", 27: "Alagoas",
    28: "Sergipe", 29: "Bahia", 31: "Minas Gerais", 32: "Espírito Santo",
    33: "Rio de Janeiro", 35: "São Paulo", 41: "Paraná", 42: "Santa Catarina",
    43: "Rio Grande do Sul", 50: "Mato Grosso do Sul", 51: "Mato Grosso",
    52: "Goiás", 53: "Distrito Federal"
}

# Regiões
REGIOES_BRASIL = {
    1: "Norte",
    2: "Nordeste",
    3: "Sudeste",
    4: "Sul",
    5: "Centro-Oeste"
}

