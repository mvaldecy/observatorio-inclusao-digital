"""
Dicionário de dados da ANATEL - Conectividade Escolar
Contém descrições de todas as colunas disponíveis nos dados de conectividade escolar

Estrutura similar ao dicionário CETIC para manter padronização
"""

COLUNAS = {
    # Identificação da escola
    'COD_INEP': """Código INEP da escola (Identificador único nacional)""",
    'NO_ENTIDADE': """Nome da entidade/escola""",
    
    # Localização geográfica
    'NO_REGIAO': """Nome da região geográfica (Norte, Nordeste, Sul, etc)""",
    'CO_REGIAO': """Código da região geográfica""",
    'CO_UF': """Código da Unidade Federativa (estado)""",
    'NO_UF': """Nome da Unidade Federativa""",
    'SG_UF': """Sigla da Unidade Federativa (ex: PI, SP, BA)""",
    'NO_MUNICIPIO': """Nome do município""",
    'CO_MUNICIPIO': """Código IBGE do município""",
    
    # Tipo e localização da escola
    'TP_DEPENDENCIA': """Tipo de dependência administrativa (Federal, Estadual, Municipal, Privada)""",
    'TP_LOCALIZACAO': """Tipo de localização (Urbana ou Rural)""",
    'TP_LOCALIZACAO_DIFERENCIADA': """Localização diferenciada (Quilombola, Indígena, Assentamento, etc)""",
    
    # Geolocalização
    'LATITUDE': """Latitude da escola (coordenada geográfica)""",
    'LONGITUDE': """Longitude da escola (coordenada geográfica)""",
    'POSSUI_GEOLOCALIZACAO': """Indica se a escola possui coordenadas geográficas""",
    'GEOLOCALIZACAO_DUPLICATA': """Indica se há duplicação de geolocalização""",
    
    # Dados da escola
    'EXCLUS_INFANTIL': """Indica se é exclusivamente educação infantil""",
    'QT_MAT_BAS': """Quantidade de matrículas na educação básica""",
    'QT_TURMAS_MAIOR_TURNO': """Quantidade de turmas no maior turno""",
    'QT_ALUNOS_MAIOR_TURMA': """Quantidade de alunos na maior turma""",
    'QT_MAT_MAIOR_TURNO': """Quantidade de matrículas no maior turno""",
    'QT_SALAS_UTILIZADAS': """Quantidade de salas de aula utilizadas""",
    'QT_OUTROS_AMBIENTES': """Quantidade de outros ambientes pedagógicos""",
    'QT_DOC_BAS': """Quantidade de docentes na educação básica""",
    
    # Energia elétrica
    'ENERGIA_CENSO_24': """Informação sobre energia no Censo Escolar 2024""",
    'ENERGIA_ADEQUADA': """Indica se a escola possui energia adequada""",
    'IN_ENERGIA_INEXISTENTE': """Indica se não há energia elétrica""",
    'IN_ENERGIA_GERADOR_FOSSIL': """Indica se usa gerador a combustível fóssil""",
    'IN_ENERGIA_RENOVAVEL': """Indica se usa energia renovável""",
    'IN_ENERGIA_REDE_PUBLICA': """Indica se está conectada à rede pública de energia""",
    
    # Conectividade - Acesso
    'CONECT_ACESSO_FIBRA_24': """Indica se possui acesso via fibra óptica em 2024""",
    'CONECT_CLASSIFICACAO_COBERTURA': """Classificação da cobertura de conectividade""",
    'CONECT_CLASSIFICACAO_COBERTURA_10KM': """Classificação de cobertura em raio de 10km""",
    'CONECT_SITUACAO': """Situação atual de conectividade""",
    'CONECT_ADEQUADA': """Indica se possui conectividade adequada""",
    'CONECT_POSSUI_INTERNET': """Indica se possui acesso à internet""",
    
    # Escolas conectadas
    'ESCOLAS_CONECTADAS': """Indica se a escola está conectada à internet""",
    'ESCOLAS_CONECTADAS_ADEQUADAS': """Indica se a escola está conectada de forma adequada""",
    'ESCOLAS_CONECTADAS_NIVEL': """Nível de conectividade da escola""",
    
    # Programas de conectividade
    'ENEC_PREVISTA': """Escola prevista no programa ENEC (Escolas Nordeste Conectadas)""",
    'EACE_PREVISTA': """Escola prevista no programa EACE (Escolas Conectadas)""",
    'EACE_FASE_ETAPA': """Fase/etapa do programa EACE""",
    'EACE_CONECT_ATIVADA': """Indica se a conectividade EACE foi ativada""",
    'EACE_WIFI_ATIVADA': """Indica se o WiFi EACE foi ativado""",
    
    # FUST (Fundo de Universalização dos Serviços de Telecomunicações)
    'FUST_NRO_ATIVADA': """FUST - NRO ativada (Nó de Rede Óptica)""",
    'FUST_REEMB_ATIVADA': """FUST - Reembolso ativado""",
    'FUST_DIR_ATIVADA': """FUST - Direto ativado""",
    
    # Outros programas
    'GESAC_ATIVADA': """Programa GESAC ativado (Governo Eletrônico - Serviço de Atendimento ao Cidadão)""",
    '14172_PREVISTA': """Escola prevista na Lei 14.172 (Lei Aldir Blanc)""",
    'MARAJO': """Indica se a escola está na região do Marajó""",
    'LPT_PREVISTA': """Escola prevista no programa LPT""",
    
    # ODF (Optical Distribution Frame)
    'ODF_ATIVADA': """ODF ativada (ponto de distribuição óptica)""",
    'ODF_WIFI_PREVISTA': """WiFi previsto via ODF""",
    'ODF_WIFI_STATUS': """Status do WiFi ODF""",
    'ODF_CONSENSO': """Consenso ODF""",
    'ODF_CONECT_PREVISTA': """Conectividade ODF prevista""",
    'ODF_CONECT_ATIVADA': """Conectividade ODF ativada""",
    
    # PBLE (Programa Banda Larga nas Escolas)
    'PBLE_PREVISTA': """Escola prevista no PBLE""",
    '4G_RURAL_ATIVADA': """4G Rural ativado""",
    'PBLE_TIPO_OBRIGACAO': """Tipo de obrigação no PBLE""",
    'PBLE_PRESTADORA': """Prestadora do serviço PBLE""",
    'PBLE_TECNOLOGIA': """Tecnologia utilizada no PBLE""",
    
    # PIEC24 (Programa de Inovação Educação Conectada 2024)
    'PIEC24_PAGA': """Indica se o PIEC24 está pago""",
    'PIEC24_STATUS': """Status do programa PIEC24""",
    
    # RNP (Rede Nacional de Ensino e Pesquisa)
    'RNP_PREVISTA': """Escola prevista na RNP""",
    'RNP_ATIVADA': """RNP ativada""",
    'RNP_ACESSO_STATUS': """Status de acesso à RNP""",
    
    # Velocidades de conexão
    'VEL_ADQ': """Velocidade adquirida (contratada total)""",
    'VEL_ADQ_TERRESTRE': """Velocidade adquirida via terrestre""",
    'VEL_MAX': """Velocidade máxima medida""",
    'FONTE_MONITORAMENTO_VEL_MAX': """Fonte de monitoramento da velocidade máxima""",
    'NICBR_VEL_MAX_6M': """Velocidade máxima medida pelo NIC.br nos últimos 6 meses""",
    'PBLE_VEL_CONTRATADA': """Velocidade contratada no PBLE""",
    'EACE_CONECT_VEL_CONTRATADA': """Velocidade contratada no EACE""",
    'ENEC_VEL_CONTRATADA': """Velocidade contratada no ENEC""",
    '14172_CONECT_VEL_CONTRATADA': """Velocidade contratada pela Lei 14.172""",
    'GESAC_VEL_CONTRATADA': """Velocidade contratada no GESAC""",
    'RNP_VELOCIDADE': """Velocidade da conexão RNP""",
    
    # Monitoramento
    'NICBR_MONITORADAS_MEDIDOR': """Indica se é monitorada pelo medidor do NIC.br""",
    
    # Metadados
    'DATA': """Data de referência dos dados""",
    'QT_PROGRAMAS': """Quantidade de programas de conectividade ativos na escola""",
}

# Valores categóricos comuns
VALORES = {
    'SG_UF': {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AM': 'Amazonas',
        'AP': 'Amapá',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MG': 'Minas Gerais',
        'MS': 'Mato Grosso do Sul',
        'MT': 'Mato Grosso',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'PR': 'Paraná',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'RS': 'Rio Grande do Sul',
        'SC': 'Santa Catarina',
        'SE': 'Sergipe',
        'SP': 'São Paulo',
        'TO': 'Tocantins',
    },
    'NO_REGIAO': {
        'Norte': 'Região Norte',
        'Nordeste': 'Região Nordeste',
        'Centro-Oeste': 'Região Centro-Oeste',
        'Sudeste': 'Região Sudeste',
        'Sul': 'Região Sul',
    },
    'CO_REGIAO': {
        1: 'Norte',
        2: 'Nordeste',
        3: 'Sudeste',
        4: 'Sul',
        5: 'Centro-Oeste',
    },
    'TP_LOCALIZACAO': {
        'Urbana': 'Área urbana',
        'Rural': 'Área rural',
    },
    'TP_DEPENDENCIA': {
        'Federal': 'Rede federal',
        'Estadual': 'Rede estadual',
        'Municipal': 'Rede municipal',
        'Privada': 'Rede privada',
    },
    # Valores binários (Sim/Não)
    'VALORES_BINARIOS': {
        'Sim': 'Sim',
        'Não': 'Não',
        'S': 'Sim',
        'N': 'Não',
        1: 'Sim',
        0: 'Não',
        True: 'Sim',
        False: 'Não',
    }
}

# Lista de colunas binárias (respostas Sim/Não)
COLUNAS_BINARIAS = [
    'POSSUI_GEOLOCALIZACAO',
    'GEOLOCALIZACAO_DUPLICATA',
    'EXCLUS_INFANTIL',
    'ENERGIA_ADEQUADA',
    'IN_ENERGIA_INEXISTENTE',
    'IN_ENERGIA_GERADOR_FOSSIL',
    'IN_ENERGIA_RENOVAVEL',
    'IN_ENERGIA_REDE_PUBLICA',
    'CONECT_ACESSO_FIBRA_24',
    'CONECT_ADEQUADA',
    'CONECT_POSSUI_INTERNET',
    'ESCOLAS_CONECTADAS',
    'ESCOLAS_CONECTADAS_ADEQUADAS',
    'ENEC_PREVISTA',
    'EACE_PREVISTA',
    'EACE_CONECT_ATIVADA',
    'EACE_WIFI_ATIVADA',
    'FUST_NRO_ATIVADA',
    'FUST_REEMB_ATIVADA',
    'FUST_DIR_ATIVADA',
    'GESAC_ATIVADA',
    '14172_PREVISTA',
    'MARAJO',
    'LPT_PREVISTA',
    'ODF_ATIVADA',
    'ODF_WIFI_PREVISTA',
    'ODF_CONECT_PREVISTA',
    'ODF_CONECT_ATIVADA',
    'PBLE_PREVISTA',
    '4G_RURAL_ATIVADA',
    'PIEC24_PAGA',
    'RNP_PREVISTA',
    'RNP_ATIVADA',
    'NICBR_MONITORADAS_MEDIDOR',
]

# Colunas numéricas (quantidades, velocidades)
COLUNAS_NUMERICAS = [
    'QT_MAT_BAS',
    'QT_TURMAS_MAIOR_TURNO',
    'QT_ALUNOS_MAIOR_TURMA',
    'QT_MAT_MAIOR_TURNO',
    'QT_SALAS_UTILIZADAS',
    'QT_OUTROS_AMBIENTES',
    'QT_DOC_BAS',
    'VEL_ADQ',
    'VEL_ADQ_TERRESTRE',
    'VEL_MAX',
    'NICBR_VEL_MAX_6M',
    'PBLE_VEL_CONTRATADA',
    'EACE_CONECT_VEL_CONTRATADA',
    'ENEC_VEL_CONTRATADA',
    '14172_CONECT_VEL_CONTRATADA',
    'GESAC_VEL_CONTRATADA',
    'RNP_VELOCIDADE',
    'QT_PROGRAMAS',
]

# Colunas de coordenadas
COLUNAS_COORDENADAS = [
    'LATITUDE',
    'LONGITUDE',
]


def obter_label(coluna: str) -> str:
    """
    Retorna a label descritiva de uma coluna
    
    Args:
        coluna: Nome da coluna
        
    Returns:
        Label descritiva ou o próprio nome da coluna se não encontrada
    """
    return COLUNAS.get(coluna, coluna)


def obter_valor_label(coluna: str, valor) -> str:
    """
    Retorna a label descritiva de um valor em uma coluna
    
    Args:
        coluna: Nome da coluna
        valor: Valor a ser traduzido
        
    Returns:
        Label descritiva do valor ou o próprio valor se não encontrada
    """
    if coluna in VALORES:
        return VALORES[coluna].get(valor, str(valor))
    
    # Para colunas binárias, usa o dicionário genérico
    if coluna in COLUNAS_BINARIAS:
        return VALORES['VALORES_BINARIOS'].get(valor, str(valor))
    
    return str(valor)


def eh_coluna_binaria(coluna: str) -> bool:
    """
    Verifica se uma coluna é binária (Sim/Não)
    
    Args:
        coluna: Nome da coluna
        
    Returns:
        True se for coluna binária, False caso contrário
    """
    return coluna in COLUNAS_BINARIAS


def eh_coluna_numerica(coluna: str) -> bool:
    """
    Verifica se uma coluna é numérica
    
    Args:
        coluna: Nome da coluna
        
    Returns:
        True se for coluna numérica, False caso contrário
    """
    return coluna in COLUNAS_NUMERICAS


def listar_colunas_por_tipo(tipo: str = 'todas') -> list:
    """
    Lista colunas por tipo
    
    Args:
        tipo: Tipo de colunas ('todas', 'binarias', 'numericas', 'coordenadas')
        
    Returns:
        Lista de nomes de colunas
    """
    if tipo == 'binarias':
        return COLUNAS_BINARIAS
    elif tipo == 'numericas':
        return COLUNAS_NUMERICAS
    elif tipo == 'coordenadas':
        return COLUNAS_COORDENADAS
    else:
        return list(COLUNAS.keys())
