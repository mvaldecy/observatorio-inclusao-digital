"""
Metadados do INEP - Censo Escolar da Educação Básica
Estrutura similar ao metadados.py do CETIC
"""

# =============================================================================
# METADADOS COMPLETOS DAS VARIÁVEIS DO INEP
# Estrutura: categoria -> variavel -> {'label': str, 'valores': {codigo: descricao}}
# =============================================================================

METADADOS_INEP = {
    'identificacao': {
        'NU_ANO_CENSO': {
            'label': 'Ano do Censo',
            'valores': None
        },
        'NO_REGIAO': {
            'label': 'Nome da Região Geográfica',
            'valores': None
        },
        'CO_REGIAO': {
            'label': 'Código da Região Geográfica',
            'valores': {
                '1': 'Norte',
                '2': 'Nordeste',
                '3': 'Sudeste',
                '4': 'Sul',
                '5': 'Centro-Oeste'
            }
        },
        'NO_UF': {
            'label': 'Nome da Unidade da Federação',
            'valores': None
        },
        'SG_UF': {
            'label': 'Sigla da Unidade da Federação',
            'valores': None
        },
        'CO_UF': {
            'label': 'Código da Unidade da Federação',
            'valores': None
        },
        'NO_MUNICIPIO': {
            'label': 'Nome do Município',
            'valores': None
        },
        'CO_MUNICIPIO': {
            'label': 'Código do Município',
            'valores': None
        },
        'NO_DISTRITO': {
            'label': 'Nome do Distrito',
            'valores': None
        },
        'CO_DISTRITO': {
            'label': 'Código do Distrito',
            'valores': None
        },
        'CO_ENTIDADE': {
            'label': 'Código da Entidade/Escola',
            'valores': None
        },
        'NO_ENTIDADE': {
            'label': 'Nome da Entidade/Escola',
            'valores': None
        },
    },

    'caracterizacao': {
        'TP_DEPENDENCIA': {
            'label': 'Dependência Administrativa',
            'valores': {
                '1': 'Federal',
                '2': 'Estadual',
                '3': 'Municipal',
                '4': 'Privada'
            }
        },
        'TP_CATEGORIA_ESCOLA_PRIVADA': {
            'label': 'Categoria da Escola Privada',
            'valores': {
                '1': 'Particular',
                '2': 'Comunitária',
                '3': 'Confessional',
                '4': 'Filantrópica'
            }
        },
        'TP_LOCALIZACAO': {
            'label': 'Localização',
            'valores': {
                '1': 'Urbana',
                '2': 'Rural'
            }
        },
        'TP_LOCALIZACAO_DIFERENCIADA': {
            'label': 'Localização Diferenciada',
            'valores': {
                '0': 'Não está em área de localização diferenciada',
                '1': 'Área de assentamento',
                '2': 'Terra indígena',
                '3': 'Área remanescente de quilombos',
                '4': 'Área onde se localiza comunidade em área de exclusão e de vulnerabilidade social',
                '5': 'Área em que se encontra a escola está situada em área de itinerantes'
            }
        },
        'TP_SITUACAO_FUNCIONAMENTO': {
            'label': 'Situação de Funcionamento',
            'valores': {
                '1': 'Em atividade',
                '2': 'Paralisada',
                '3': 'Extinta (ano do censo)',
                '4': 'Extinta (anos anteriores)'
            }
        },
    },

    'infraestrutura_agua': {
        'IN_AGUA_POTAVEL': {
            'label': 'Possui água potável',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AGUA_FILTRADA': {
            'label': 'Abastecimento de água - Água filtrada',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AGUA_REDE_PUBLICA': {
            'label': 'Abastecimento de água - Rede pública',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AGUA_POCO_ARTESIANO': {
            'label': 'Abastecimento de água - Poço artesiano',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AGUA_CACIMBA': {
            'label': 'Abastecimento de água - Cacimba/Cisterna/Poço',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AGUA_FONTE_RIO': {
            'label': 'Abastecimento de água - Fonte/Rio/Igarapé/Riacho/Córrego',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AGUA_INEXISTENTE': {
            'label': 'Abastecimento de água - Inexistente',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
    },

    'infraestrutura_energia': {
        'IN_ENERGIA_REDE_PUBLICA': {
            'label': 'Fonte de energia elétrica - Rede pública',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ENERGIA_GERADOR_FOSSIL': {
            'label': 'Fonte de energia elétrica - Gerador movido a combustível fóssil',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ENERGIA_RENOVAVEL': {
            'label': 'Fonte de energia elétrica - Fontes de energia renováveis ou alternativas',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ENERGIA_INEXISTENTE': {
            'label': 'Fonte de energia elétrica - Inexistente',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
    },

    'infraestrutura_esgoto': {
        'IN_ESGOTO_REDE_PUBLICA': {
            'label': 'Esgotamento sanitário - Rede pública',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ESGOTO_FOSSA_SEPTICA': {
            'label': 'Esgotamento sanitário - Fossa séptica',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ESGOTO_FOSSA_COMUM': {
            'label': 'Esgotamento sanitário - Fossa comum',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ESGOTO_INEXISTENTE': {
            'label': 'Esgotamento sanitário - Inexistente',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
    },

    'infraestrutura_lixo': {
        'IN_LIXO_COLETA_PERIODICA': {
            'label': 'Destinação do lixo - Coleta periódica',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LIXO_QUEIMA': {
            'label': 'Destinação do lixo - Queima',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LIXO_JOGA_OUTRA_AREA': {
            'label': 'Destinação do lixo - Joga em outra área',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LIXO_RECICLA': {
            'label': 'Destinação do lixo - Recicla',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LIXO_ENTERRA': {
            'label': 'Destinação do lixo - Enterra',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LIXO_OUTROS': {
            'label': 'Destinação do lixo - Outros',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
    },

    'espacos_ambientes': {
        'IN_LOCAL_FUNC_PREDIO_ESCOLAR': {
            'label': 'Local de funcionamento - Prédio escolar',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_PREDIO_COMPARTILHADO': {
            'label': 'Prédio compartilhado com outra escola',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_SALA_DIRETORIA': {
            'label': 'Dependências - Sala de diretoria',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_SALA_PROFESSOR': {
            'label': 'Dependências - Sala de professores',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LABORATORIO_INFORMATICA': {
            'label': 'Dependências - Laboratório de informática',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LABORATORIO_CIENCIAS': {
            'label': 'Dependências - Laboratório de ciências',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_SALA_ATENDIMENTO_ESPECIAL': {
            'label': 'Dependências - Sala de atendimento especial',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_QUADRA_ESPORTES': {
            'label': 'Dependências - Quadra de esportes',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_QUADRA_ESPORTES_COBERTA': {
            'label': 'Dependências - Quadra de esportes coberta',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_QUADRA_ESPORTES_DESCOBERTA': {
            'label': 'Dependências - Quadra de esportes descoberta',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_COZINHA': {
            'label': 'Dependências - Cozinha',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_BIBLIOTECA': {
            'label': 'Dependências - Biblioteca',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_BIBLIOTECA_SALA_LEITURA': {
            'label': 'Dependências - Biblioteca ou sala de leitura',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_SALA_LEITURA': {
            'label': 'Dependências - Sala de leitura',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_PARQUE_INFANTIL': {
            'label': 'Dependências - Parque infantil',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_BERCARIO': {
            'label': 'Dependências - Berçário',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_BANHEIRO': {
            'label': 'Dependências - Banheiro',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_BANHEIRO_INFANTIL': {
            'label': 'Dependências - Banheiro infantil',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_BANHEIRO_PNE': {
            'label': 'Dependências - Banheiro adequado para pessoas com necessidades especiais',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_DEPENDENCIAS_PNE': {
            'label': 'Dependências - Dependências acessíveis para pessoas com necessidades especiais',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_SECRETARIA': {
            'label': 'Dependências - Secretaria',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_REFEITORIO': {
            'label': 'Dependências - Refeitório',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_DESPENSA': {
            'label': 'Dependências - Despensa',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ALMOXARIFADO': {
            'label': 'Dependências - Almoxarifado',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AUDITORIO': {
            'label': 'Dependências - Auditório',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_PATIO_COBERTO': {
            'label': 'Dependências - Pátio coberto',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_PATIO_DESCOBERTO': {
            'label': 'Dependências - Pátio descoberto',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ALOJAMENTO_ALUNO': {
            'label': 'Dependências - Alojamento de aluno',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ALOJAMENTO_PROFESSOR': {
            'label': 'Dependências - Alojamento de professor',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AREA_VERDE': {
            'label': 'Dependências - Área verde',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_LAVANDERIA': {
            'label': 'Dependências - Lavanderia',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
    },

    'equipamentos': {
        'IN_EQUIP_TV': {
            'label': 'Equipamento - Aparelho de televisão',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_VIDEOCASSETE': {
            'label': 'Equipamento - Videocassete',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_DVD': {
            'label': 'Equipamento - DVD',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_PARAB': {
            'label': 'Equipamento - Antena parabólica',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_COPIADORA': {
            'label': 'Equipamento - Copiadora',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_RETROPROJETOR': {
            'label': 'Equipamento - Retroprojetor',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_IMPRESSORA': {
            'label': 'Equipamento - Impressora',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_IMPRESSORA_MULT': {
            'label': 'Equipamento - Impressora multifuncional',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_SOM': {
            'label': 'Equipamento - Aparelho de som',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_MULTIMIDIA': {
            'label': 'Equipamento - Projetor multimídia (datashow)',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_FAX': {
            'label': 'Equipamento - Fax',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_FOTO': {
            'label': 'Equipamento - Máquina fotográfica/Filmadora',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EQUIP_COMPUTADOR': {
            'label': 'Equipamento - Computador',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'QT_EQUIP_TV': {
            'label': 'Quantidade de aparelhos de televisão',
            'valores': None
        },
        'QT_EQUIP_DVD': {
            'label': 'Quantidade de aparelhos de DVD',
            'valores': None
        },
        'QT_EQUIP_SOM': {
            'label': 'Quantidade de aparelhos de som',
            'valores': None
        },
        'QT_EQUIP_MULTIMIDIA': {
            'label': 'Quantidade de projetores multimídia',
            'valores': None
        },
    },

    'internet_computadores': {
        'IN_INTERNET': {
            'label': 'Acesso à Internet',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_INTERNET_ALUNOS': {
            'label': 'Acesso à Internet - Para uso dos alunos',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_INTERNET_ADMINISTRATIVO': {
            'label': 'Acesso à Internet - Para uso administrativo',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_INTERNET_APRENDIZAGEM': {
            'label': 'Acesso à Internet - Para uso nos processos de ensino e aprendizagem',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_INTERNET_COMUNIDADE': {
            'label': 'Acesso à Internet - Para uso da comunidade',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ACESSO_INTERNET_COMPUTADOR': {
            'label': 'Acesso à internet através de computadores, portáteis e tablets da escola',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ACESSO_INTERNET_DISPOSITIVO': {
            'label': 'Acesso à internet através de dispositivo pessoal (computadores portáteis, celulares, tablets e similares)',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_BANDA_LARGA': {
            'label': 'Acesso à internet - Banda larga',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'QT_DESKTOP_ALUNO': {
            'label': 'Quantidade de computadores de mesa (desktop) em uso pelos alunos',
            'valores': None
        },
        'QT_COMP_PORTATIL_ALUNO': {
            'label': 'Quantidade de computadores portáteis em uso pelos alunos',
            'valores': None
        },
        'QT_TABLET_ALUNO': {
            'label': 'Quantidade de tablets em uso pelos alunos',
            'valores': None
        },
        'QT_DESKTOP_ADMINISTRATIVO': {
            'label': 'Quantidade de computadores de mesa (desktop) para uso administrativo',
            'valores': None
        },
        'QT_COMP_PORTATIL_ADMINISTRATIVO': {
            'label': 'Quantidade de computadores portáteis para uso administrativo',
            'valores': None
        },
        'QT_TABLET_ADMINISTRATIVO': {
            'label': 'Quantidade de tablets para uso administrativo',
            'valores': None
        },
    },

    'educacao_indigena': {
        'IN_EDUCACAO_INDIGENA': {
            'label': 'Escola de educação escolar indígena',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'CO_LINGUA_INDIGENA': {
            'label': 'Código da língua indígena 1',
            'valores': None
        },
        'CO_LINGUA_INDIGENA_2': {
            'label': 'Código da língua indígena 2',
            'valores': None
        },
        'CO_LINGUA_INDIGENA_3': {
            'label': 'Código da língua indígena 3',
            'valores': None
        },
    },

    'modalidades_ensino': {
        'IN_REGULAR': {
            'label': 'Oferece ensino regular',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_EJA': {
            'label': 'Oferece EJA - Educação de Jovens e Adultos',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ESPECIAL_EXCLUSIVA': {
            'label': 'Oferece educação especial exclusivamente',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_COMUM_CRECHE': {
            'label': 'Ensino regular - Creche',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_COMUM_PRE': {
            'label': 'Ensino regular - Pré-escola',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_COMUM_FUND_AI': {
            'label': 'Ensino regular - Anos iniciais do ensino fundamental',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_COMUM_FUND_AF': {
            'label': 'Ensino regular - Anos finais do ensino fundamental',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_COMUM_MEDIO_MEDIO': {
            'label': 'Ensino regular - Ensino médio',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_PROFISSIONALIZANTE': {
            'label': 'Oferece educação profissional',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
    },

    'matriculas': {
        'QT_MAT_BAS': {
            'label': 'Número de matrículas na educação básica',
            'valores': None
        },
        'QT_MAT_INF': {
            'label': 'Número de matrículas na educação infantil',
            'valores': None
        },
        'QT_MAT_FUND': {
            'label': 'Número de matrículas no ensino fundamental',
            'valores': None
        },
        'QT_MAT_MED': {
            'label': 'Número de matrículas no ensino médio',
            'valores': None
        },
        'QT_MAT_PROF': {
            'label': 'Número de matrículas na educação profissional',
            'valores': None
        },
        'QT_MAT_EJA': {
            'label': 'Número de matrículas na EJA',
            'valores': None
        },
        'QT_MAT_ESP': {
            'label': 'Número de matrículas na educação especial',
            'valores': None
        },
    },

    'docentes': {
        'QT_DOC_BAS': {
            'label': 'Número de docentes na educação básica',
            'valores': None
        },
        'QT_DOC_INF': {
            'label': 'Número de docentes na educação infantil',
            'valores': None
        },
        'QT_DOC_FUND': {
            'label': 'Número de docentes no ensino fundamental',
            'valores': None
        },
        'QT_DOC_MED': {
            'label': 'Número de docentes no ensino médio',
            'valores': None
        },
        'QT_DOC_PROF': {
            'label': 'Número de docentes na educação profissional',
            'valores': None
        },
        'QT_DOC_EJA': {
            'label': 'Número de docentes na EJA',
            'valores': None
        },
        'QT_DOC_ESP': {
            'label': 'Número de docentes na educação especial',
            'valores': None
        },
    },

    'atividades_complementares': {
        'IN_ALIMENTACAO': {
            'label': 'Oferece alimentação escolar',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_AEE': {
            'label': 'Oferece Atendimento Educacional Especializado (AEE)',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
        'IN_ATIVIDADE_COMPLEMENTAR': {
            'label': 'Oferece atividade complementar',
            'valores': {
                '0': 'Não',
                '1': 'Sim'
            }
        },
    },
}


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def get_label(variavel: str, categoria: str = None) -> str:
    """
    Retorna o label de uma variável

    Args:
        variavel: Nome da variável
        categoria: Categoria da variável (opcional, para busca mais rápida)

    Returns:
        String com o label ou o próprio nome da variável se não encontrado
    """
    if categoria and categoria in METADADOS_INEP:
        if variavel in METADADOS_INEP[categoria]:
            return METADADOS_INEP[categoria][variavel]['label']

    # Busca em todas as categorias
    for cat in METADADOS_INEP.values():
        if variavel in cat:
            return cat[variavel]['label']

    return variavel


def get_valores(variavel: str, categoria: str = None) -> dict:
    """
    Retorna os valores possíveis de uma variável categórica

    Args:
        variavel: Nome da variável
        categoria: Categoria da variável (opcional)

    Returns:
        Dicionário com os valores ou None se não for categórica
    """
    if categoria and categoria in METADADOS_INEP:
        if variavel in METADADOS_INEP[categoria]:
            return METADADOS_INEP[categoria][variavel]['valores']

    # Busca em todas as categorias
    for cat in METADADOS_INEP.values():
        if variavel in cat:
            return cat[variavel]['valores']

    return None


def formatar_valor(variavel: str, valor, categoria: str = None) -> str:
    """
    Formata um valor de acordo com seus metadados

    Args:
        variavel: Nome da variável
        valor: Valor a ser formatado
        categoria: Categoria da variável (opcional)

    Returns:
        String formatada
    """
    valores = get_valores(variavel, categoria)

    if valores is None:
        return str(valor)

    valor_str = str(int(valor) if isinstance(valor, float) and valor.is_integer() else valor)

    if valor_str in valores:
        return f"{valor_str} - {valores[valor_str]}"

    return str(valor)


def listar_categorias() -> list:
    """
    Lista todas as categorias disponíveis

    Returns:
        Lista de nomes de categorias
    """
    return list(METADADOS_INEP.keys())


def listar_variaveis(categoria: str = None) -> list:
    """
    Lista variáveis de uma categoria ou todas as variáveis

    Args:
        categoria: Nome da categoria (opcional)

    Returns:
        Lista de nomes de variáveis
    """
    if categoria:
        if categoria in METADADOS_INEP:
            return list(METADADOS_INEP[categoria].keys())
        return []

    # Retorna todas as variáveis
    todas = []
    for cat in METADADOS_INEP.values():
        todas.extend(cat.keys())
    return todas


def get_categoria_variavel(variavel: str) -> str:
    """
    Retorna a categoria de uma variável

    Args:
        variavel: Nome da variável

    Returns:
        Nome da categoria ou None se não encontrada
    """
    for cat_nome, cat_vars in METADADOS_INEP.items():
        if variavel in cat_vars:
            return cat_nome
    return None

