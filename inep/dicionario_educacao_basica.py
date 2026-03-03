"""
Dicionário de dados do INEP - Censo Escolar da Educação Básica
Gerado automaticamente a partir do arquivo Excel fornecido pelo INEP

Estrutura:
- METADADOS_INEP: dicionário com informações de cada variável (nome, descrição, tipo, categorias)
- CATEGORIAS_INEP: organização das variáveis por categoria temática
"""

# =============================================================================
# METADADOS DAS VARIÁVEIS
# =============================================================================

METADADOS_INEP = {}

def _parse_categorias(categoria_str):
    """
    Parse da string de categorias para um dicionário

    Args:
        categoria_str: String com categorias no formato "1 - Descrição\n2 - Descrição"

    Returns:
        Dicionário {codigo: descrição} ou None se não houver categorias
    """
    if not categoria_str or str(categoria_str) == 'nan':
        return None

    categorias = {}
    linhas = str(categoria_str).strip().split('\n')

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha == '':
            continue

        # Tenta fazer split por " - " ou apenas "-"
        if ' - ' in linha:
            partes = linha.split(' - ', 1)
        elif '-' in linha:
            partes = linha.split('-', 1)
        else:
            continue

        if len(partes) == 2:
            try:
                codigo = partes[0].strip()
                descricao = partes[1].strip()
                categorias[codigo] = descricao
            except:
                continue

    return categorias if categorias else None


def carregar_metadados():
    """
    Carrega metadados do arquivo Excel do dicionário de dados
    """
    import pandas as pd
    from pathlib import Path

    arquivo = Path(__file__).parent / 'dicionário_dados_educação_básica.xlsx'

    if not arquivo.exists():
        print(f"⚠️  Arquivo não encontrado: {arquivo}")
        return {}

    # Lê o arquivo
    df = pd.read_excel(arquivo, sheet_name='microdados_unidade_coleta', header=6)

    # Remove linhas vazias (baseado na coluna 1 - Nome da Variável)
    df = df[df.iloc[:, 1].notna()].copy()

    # Usa índices ao invés de nomes de colunas (evita problemas com encoding)
    # Colunas: 0=N, 1=Nome, 2=Descrição, 3=Tipo, 4=Tamanho, 5=Categoria
    metadados = {}

    for idx, row in df.iterrows():
        nome = row.iloc[1]  # Nome da Variável
        if pd.isna(nome):
            continue

        nome = str(nome).strip()
        descricao = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else nome  # Descrição
        tipo = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else 'Unknown'  # Tipo
        tamanho = int(row.iloc[4]) if pd.notna(row.iloc[4]) else None  # Tamanho

        # Parse das categorias (coluna 5)
        categorias = None
        if pd.notna(row.iloc[5]):
            categorias = _parse_categorias(row.iloc[5])

        metadados[nome] = {
            'label': descricao,
            'tipo': tipo,
            'tamanho': tamanho,
            'categorias': categorias
        }

    return metadados


# Carrega os metadados ao importar o módulo
try:
    METADADOS_INEP = carregar_metadados()
except Exception as e:
    print(f"⚠️  Erro ao carregar metadados do INEP: {e}")
    METADADOS_INEP = {}


# =============================================================================
# CATEGORIZAÇÃO DAS VARIÁVEIS
# =============================================================================

CATEGORIAS_INEP = {
    'identificacao': {
        'label': 'Identificação e Localização',
        'variaveis': [
            'NU_ANO_CENSO',
            'NO_REGIAO', 'CO_REGIAO',
            'NO_UF', 'SG_UF', 'CO_UF',
            'NO_MUNICIPIO', 'CO_MUNICIPIO',
            'NO_REGIAO_GEOG_INTERM', 'CO_REGIAO_GEOG_INTERM',
            'NO_REGIAO_GEOG_IMED', 'CO_REGIAO_GEOG_IMED',
            'NO_MESORREGIAO', 'CO_MESORREGIAO',
            'NO_MICRORREGIAO', 'CO_MICRORREGIAO',
            'NO_DISTRITO', 'CO_DISTRITO',
            'CO_ENTIDADE', 'CO_ESCOLA_SEDE_VINCULADA',
            'NO_ENTIDADE',
        ]
    },

    'caracterizacao': {
        'label': 'Caracterização da Escola',
        'variaveis': [
            'TP_DEPENDENCIA',
            'TP_CATEGORIA_ESCOLA_PRIVADA',
            'TP_LOCALIZACAO',
            'TP_LOCALIZACAO_DIFERENCIADA',
            'TP_SITUACAO_FUNCIONAMENTO',
            'DT_ANO_LETIVO_INICIO',
            'DT_ANO_LETIVO_TERMINO',
        ]
    },

    'infraestrutura_basica': {
        'label': 'Infraestrutura Básica',
        'variaveis': [
            'IN_LOCAL_FUNC_PREDIO_ESCOLAR',
            'IN_PREDIO_COMPARTILHADO',
            'IN_AGUA_POTAVEL',
            'IN_AGUA_FILTRADA',
            'IN_AGUA_REDE_PUBLICA',
            'IN_AGUA_POCO_ARTESIANO',
            'IN_AGUA_CACIMBA',
            'IN_AGUA_FONTE_RIO',
            'IN_AGUA_INEXISTENTE',
            'IN_ENERGIA_REDE_PUBLICA',
            'IN_ENERGIA_GERADOR_FOSSIL',
            'IN_ENERGIA_RENOVAVEL',
            'IN_ENERGIA_INEXISTENTE',
            'IN_ESGOTO_REDE_PUBLICA',
            'IN_ESGOTO_FOSSA_SEPTICA',
            'IN_ESGOTO_FOSSA_COMUM',
            'IN_ESGOTO_INEXISTENTE',
            'IN_LIXO_COLETA_PERIODICA',
            'IN_LIXO_QUEIMA',
            'IN_LIXO_JOGA_OUTRA_AREA',
            'IN_LIXO_RECICLA',
            'IN_LIXO_ENTERRA',
            'IN_LIXO_OUTROS',
        ]
    },

    'infraestrutura_espacos': {
        'label': 'Espaços e Instalações',
        'variaveis': [
            'IN_SALA_DIRETORIA',
            'IN_SALA_PROFESSOR',
            'IN_LABORATORIO_INFORMATICA',
            'IN_LABORATORIO_CIENCIAS',
            'IN_SALA_ATENDIMENTO_ESPECIAL',
            'IN_QUADRA_ESPORTES',
            'IN_QUADRA_ESPORTES_COBERTA',
            'IN_QUADRA_ESPORTES_DESCOBERTA',
            'IN_COZINHA',
            'IN_BIBLIOTECA',
            'IN_BIBLIOTECA_SALA_LEITURA',
            'IN_SALA_LEITURA',
            'IN_PARQUE_INFANTIL',
            'IN_BERCARIO',
            'IN_BANHEIRO',
            'IN_BANHEIRO_INFANTIL',
            'IN_BANHEIRO_PNE',
            'IN_DEPENDENCIAS_PNE',
            'IN_SECRETARIA',
            'IN_REFEITORIO',
            'IN_DESPENSA',
            'IN_ALMOXARIFADO',
            'IN_AUDITORIO',
            'IN_PATIO_COBERTO',
            'IN_PATIO_DESCOBERTO',
            'IN_ALOJAMENTO_ALUNO',
            'IN_ALOJAMENTO_PROFESSOR',
            'IN_AREA_VERDE',
            'IN_LAVANDERIA',
            'IN_DEPENDENCIAS_OUTRAS',
        ]
    },

    'equipamentos': {
        'label': 'Equipamentos e Recursos',
        'variaveis': [
            'IN_EQUIP_TV',
            'IN_EQUIP_VIDEOCASSETE',
            'IN_EQUIP_DVD',
            'IN_EQUIP_PARAB',
            'IN_EQUIP_COPIADORA',
            'IN_EQUIP_RETROPROJETOR',
            'IN_EQUIP_IMPRESSORA',
            'IN_EQUIP_IMPRESSORA_MULT',
            'IN_EQUIP_SOM',
            'IN_EQUIP_MULTIMIDIA',
            'IN_EQUIP_FAX',
            'IN_EQUIP_FOTO',
            'IN_EQUIP_COMPUTADOR',
            'IN_EQUIP_PARQUE_INFANTIL',
            'QT_EQUIP_TV',
            'QT_EQUIP_VIDEOCASSETE',
            'QT_EQUIP_DVD',
            'QT_EQUIP_PARAB',
            'QT_EQUIP_COPIADORA',
            'QT_EQUIP_RETROPROJETOR',
            'QT_EQUIP_IMPRESSORA',
            'QT_EQUIP_IMPRESSORA_MULT',
            'QT_EQUIP_SOM',
            'QT_EQUIP_MULTIMIDIA',
            'QT_EQUIP_FAX',
            'QT_EQUIP_FOTO',
        ]
    },

    'internet_computadores': {
        'label': 'Internet e Computadores',
        'variaveis': [
            'IN_INTERNET',
            'IN_INTERNET_ALUNOS',
            'IN_INTERNET_ADMINISTRATIVO',
            'IN_INTERNET_APRENDIZAGEM',
            'IN_INTERNET_COMUNIDADE',
            'IN_ACESSO_INTERNET_COMPUTADOR',
            'IN_ACESSO_INTERNET_DISPOSITIVO',
            'IN_ACES_INTERNET_COMP_MESA',
            'IN_ACES_INTERNET_COMP_PORT',
            'IN_ACES_INTERNET_DISP_PESS',
            'IN_REDE_LOCAL',
            'IN_BANDA_LARGA',
            'QT_DESKTOP_ALUNO',
            'QT_COMP_PORTATIL_ALUNO',
            'QT_TABLET_ALUNO',
            'QT_DESKTOP_ADMINISTRATIVO',
            'QT_COMP_PORTATIL_ADMINISTRATIVO',
            'QT_TABLET_ADMINISTRATIVO',
        ]
    },

    'acessibilidade': {
        'label': 'Acessibilidade e Inclusão',
        'variaveis': [
            'IN_MATERIAL_PED_LACIONAL',
            'IN_MATERIAL_ESPECIFICO',
            'IN_MATERIAL_ESP_QUILOMBOLA',
            'IN_MATERIAL_ESP_INDIGENA',
            'IN_EDUCACAO_INDIGENA',
            'CO_LINGUA_INDIGENA',
            'CO_LINGUA_INDIGENA_2',
            'CO_LINGUA_INDIGENA_3',
        ]
    },

    'organizacao_ensino': {
        'label': 'Organização do Ensino',
        'variaveis': [
            'IN_REGULAR',
            'IN_EJA',
            'IN_ESPECIAL_EXCLUSIVA',
            'IN_COMUM_CRECHE',
            'IN_COMUM_PRE',
            'IN_COMUM_FUND_AI',
            'IN_COMUM_FUND_AF',
            'IN_COMUM_MEDIO_MEDIO',
            'IN_ESP_EXCLUSIVA_CRECHE',
            'IN_ESP_EXCLUSIVA_PRE',
            'IN_ESP_EXCLUSIVA_FUND_AI',
            'IN_ESP_EXCLUSIVA_FUND_AF',
            'IN_ESP_EXCLUSIVA_MEDIO_MEDIO',
            'IN_COMUM_EJA_FUND',
            'IN_COMUM_EJA_MEDIO',
            'IN_ESP_EXCLUSIVA_EJA_FUND',
            'IN_ESP_EXCLUSIVA_EJA_MEDIO',
        ]
    },

    'modalidades': {
        'label': 'Modalidades de Ensino',
        'variaveis': [
            'IN_PROFISSIONALIZANTE',
            'IN_EDUCACAO_INDIGENA',
            'IN_BRASILEIRA_EXTERIOR',
        ]
    },

    'alunos_matriculas': {
        'label': 'Alunos e Matrículas',
        'variaveis': [
            'QT_MAT_BAS',
            'QT_MAT_INF',
            'QT_MAT_FUND',
            'QT_MAT_MED',
            'QT_MAT_PROF',
            'QT_MAT_EJA',
            'QT_MAT_ESP',
        ]
    },

    'profissionais': {
        'label': 'Profissionais',
        'variaveis': [
            'QT_DOC_BAS',
            'QT_DOC_INF',
            'QT_DOC_FUND',
            'QT_DOC_MED',
            'QT_DOC_PROF',
            'QT_DOC_EJA',
            'QT_DOC_ESP',
        ]
    },

    'alimentacao_transporte': {
        'label': 'Alimentação e Transporte',
        'variaveis': [
            'IN_ALIMENTACAO',
            'IN_AEE',
            'IN_ATIVIDADE_COMPLEMENTAR',
            'IN_FUNDAMENTAL_CICLOS',
        ]
    }
}


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def get_metadados(variavel: str) -> dict:
    """
    Retorna metadados de uma variável específica

    Args:
        variavel: Nome da variável

    Returns:
        Dicionário com label, tipo, tamanho e categorias
    """
    return METADADOS_INEP.get(variavel, {
        'label': variavel,
        'tipo': 'Unknown',
        'tamanho': None,
        'categorias': None
    })


def get_label(variavel: str) -> str:
    """
    Retorna o label (descrição) de uma variável

    Args:
        variavel: Nome da variável

    Returns:
        String com a descrição da variável
    """
    return get_metadados(variavel).get('label', variavel)


def get_categorias(variavel: str) -> dict:
    """
    Retorna as categorias/valores possíveis de uma variável

    Args:
        variavel: Nome da variável

    Returns:
        Dicionário {codigo: descrição} ou None
    """
    return get_metadados(variavel).get('categorias')


def listar_variaveis_por_categoria(categoria: str) -> list:
    """
    Lista todas as variáveis de uma categoria temática

    Args:
        categoria: Nome da categoria (ex: 'internet_computadores')

    Returns:
        Lista de nomes de variáveis
    """
    if categoria in CATEGORIAS_INEP:
        return CATEGORIAS_INEP[categoria]['variaveis']
    return []


def listar_categorias() -> list:
    """
    Lista todas as categorias temáticas disponíveis

    Returns:
        Lista de tuplas (categoria, label)
    """
    return [(cat, info['label']) for cat, info in CATEGORIAS_INEP.items()]


def formatar_valor_categorico(variavel: str, valor) -> str:
    """
    Formata um valor categórico para exibição

    Args:
        variavel: Nome da variável
        valor: Valor a ser formatado

    Returns:
        String formatada com código e descrição
    """
    categorias = get_categorias(variavel)
    if not categorias:
        return str(valor)

    valor_str = str(int(valor) if isinstance(valor, float) and valor.is_integer() else valor)

    if valor_str in categorias:
        return f"{valor_str} - {categorias[valor_str]}"
    return str(valor)


