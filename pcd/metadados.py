"""
Metadados e definições de campos para dados PCD

Este arquivo define as estruturas de metadados dos dados de 
inclusão digital para pessoas com deficiência.
"""


class CampoMeta:
    """Classe base para metadados de um campo"""
    
    def __init__(self, nome: str, label: str, descricao: str = "", tipo: str = "str"):
        self.nome = nome
        self.label = label
        self.descricao = descricao
        self.tipo = tipo
        self._opcoes = {}
    
    def com_opcoes(self, opcoes: dict):
        """Define opções/categorias para o campo"""
        self._opcoes = opcoes
        return self
    
    @property
    def opcoes(self):
        return self._opcoes
    
    def __repr__(self):
        return f"<CampoMeta: {self.nome} ({self.label})>"


# Metadados principais
CAMPOS_BASE = {
    'id': CampoMeta(
        'id',
        'ID',
        'Identificador único do registro',
        'int'
    ),
    'ano': CampoMeta(
        'ano',
        'Ano',
        'Ano de referência dos dados',
        'int'
    ),
    'uf': CampoMeta(
        'uf',
        'UF',
        'Unidade Federativa',
        'str'
    ),
    'regiao': CampoMeta(
        'regiao',
        'Região',
        'Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)',
        'str'
    ),
    'municipio': CampoMeta(
        'municipio',
        'Município',
        'Nome do município',
        'str'
    ),
    'area': CampoMeta(
        'area',
        'Área',
        'Área de localização',
        'str'
    ).com_opcoes({
        'urbana': 'Urbana',
        'rural': 'Rural'
    })
}


# Campos relacionados a deficiência
CAMPOS_DEFICIENCIA = {
    'tem_deficiencia': CampoMeta(
        'tem_deficiencia',
        'Tem Deficiência',
        'Indica se a pessoa tem alguma deficiência',
        'bool'
    ),
    'tipo_deficiencia': CampoMeta(
        'tipo_deficiencia',
        'Tipo de Deficiência',
        'Tipo principal de deficiência',
        'str'
    ).com_opcoes({
        'visual': 'Visual',
        'auditiva': 'Auditiva',
        'motora': 'Motora',
        'intelectual': 'Intelectual',
        'multipla': 'Múltipla'
    }),
    'grau_deficiencia': CampoMeta(
        'grau_deficiencia',
        'Grau da Deficiência',
        'Grau de severidade da deficiência',
        'str'
    ).com_opcoes({
        'leve': 'Leve',
        'moderado': 'Moderado',
        'severo': 'Severo',
        'profundo': 'Profundo'
    })
}


# Campos de acesso à tecnologia
CAMPOS_ACESSO_TECNOLOGIA = {
    'tem_internet': CampoMeta(
        'tem_internet',
        'Tem Acesso à Internet',
        'Indica se tem acesso à internet',
        'bool'
    ),
    'tem_computador': CampoMeta(
        'tem_computador',
        'Tem Computador',
        'Possui computador de mesa ou notebook',
        'bool'
    ),
    'tem_smartphone': CampoMeta(
        'tem_smartphone',
        'Tem Smartphone',
        'Possui smartphone',
        'bool'
    ),
    'tem_tablet': CampoMeta(
        'tem_tablet',
        'Tem Tablet',
        'Possui tablet',
        'bool'
    ),
    'tipo_conexao': CampoMeta(
        'tipo_conexao',
        'Tipo de Conexão',
        'Tipo principal de conexão à internet',
        'str'
    ).com_opcoes({
        'fibra': 'Fibra Óptica',
        'cabo': 'Cabo',
        'movel': 'Móvel (3G/4G/5G)',
        'satelite': 'Satélite',
        'outro': 'Outro'
    }),
    'velocidade_internet': CampoMeta(
        'velocidade_internet',
        'Velocidade da Internet',
        'Faixa de velocidade da internet (Mbps)',
        'str'
    ).com_opcoes({
        'ate_1': 'Até 1 Mbps',
        '1_a_5': '1 a 5 Mbps',
        '5_a_10': '5 a 10 Mbps',
        '10_a_50': '10 a 50 Mbps',
        'mais_50': 'Mais de 50 Mbps'
    })
}


# Campos de uso da internet
CAMPOS_USO_INTERNET = {
    'frequencia_uso': CampoMeta(
        'frequencia_uso',
        'Frequência de Uso',
        'Frequência de uso da internet',
        'str'
    ).com_opcoes({
        'diaria': 'Diária',
        'semanal': 'Semanal',
        'mensal': 'Mensal',
        'raramente': 'Raramente',
        'nunca': 'Nunca'
    }),
    'usa_redes_sociais': CampoMeta(
        'usa_redes_sociais',
        'Usa Redes Sociais',
        'Utiliza redes sociais',
        'bool'
    ),
    'usa_servicos_gov': CampoMeta(
        'usa_servicos_gov',
        'Usa Serviços Governamentais',
        'Utiliza serviços governamentais online',
        'bool'
    ),
    'usa_ecommerce': CampoMeta(
        'usa_ecommerce',
        'Usa E-commerce',
        'Realiza compras online',
        'bool'
    ),
    'usa_educacao': CampoMeta(
        'usa_educacao',
        'Usa para Educação',
        'Utiliza internet para educação/cursos',
        'bool'
    ),
    'usa_trabalho': CampoMeta(
        'usa_trabalho',
        'Usa para Trabalho',
        'Utiliza internet para trabalho',
        'bool'
    )
}


# Campos demográficos
CAMPOS_DEMOGRAFICOS = {
    'idade': CampoMeta(
        'idade',
        'Idade',
        'Idade em anos',
        'int'
    ),
    'faixa_etaria': CampoMeta(
        'faixa_etaria',
        'Faixa Etária',
        'Faixa etária',
        'str'
    ).com_opcoes({
        '10_17': '10 a 17 anos',
        '18_24': '18 a 24 anos',
        '25_34': '25 a 34 anos',
        '35_44': '35 a 44 anos',
        '45_59': '45 a 59 anos',
        '60_mais': '60 anos ou mais'
    }),
    'sexo': CampoMeta(
        'sexo',
        'Sexo',
        'Sexo',
        'str'
    ).com_opcoes({
        'masculino': 'Masculino',
        'feminino': 'Feminino'
    }),
    'escolaridade': CampoMeta(
        'escolaridade',
        'Escolaridade',
        'Nível de escolaridade',
        'str'
    ).com_opcoes({
        'sem_instrucao': 'Sem instrução',
        'fundamental_incompleto': 'Fundamental incompleto',
        'fundamental_completo': 'Fundamental completo',
        'medio_incompleto': 'Médio incompleto',
        'medio_completo': 'Médio completo',
        'superior_incompleto': 'Superior incompleto',
        'superior_completo': 'Superior completo'
    }),
    'renda_familiar': CampoMeta(
        'renda_familiar',
        'Renda Familiar',
        'Faixa de renda familiar em salários mínimos',
        'str'
    ).com_opcoes({
        'ate_1': 'Até 1 SM',
        '1_a_2': '1 a 2 SM',
        '2_a_3': '2 a 3 SM',
        '3_a_5': '3 a 5 SM',
        '5_a_10': '5 a 10 SM',
        'mais_10': 'Mais de 10 SM'
    })
}


# Campos de barreiras e acessibilidade
CAMPOS_ACESSIBILIDADE = {
    'usa_tecnologia_assistiva': CampoMeta(
        'usa_tecnologia_assistiva',
        'Usa Tecnologia Assistiva',
        'Utiliza tecnologia assistiva para acesso digital',
        'bool'
    ),
    'tipo_tecnologia_assistiva': CampoMeta(
        'tipo_tecnologia_assistiva',
        'Tipo de Tecnologia Assistiva',
        'Tipo de tecnologia assistiva utilizada',
        'str'
    ).com_opcoes({
        'leitor_tela': 'Leitor de tela',
        'ampliador': 'Ampliador de tela',
        'teclado_adaptado': 'Teclado adaptado',
        'mouse_adaptado': 'Mouse adaptado',
        'legenda': 'Legendas/Closed caption',
        'outro': 'Outro'
    }),
    'encontra_barreiras': CampoMeta(
        'encontra_barreiras',
        'Encontra Barreiras',
        'Encontra barreiras no acesso digital',
        'bool'
    ),
    'tipo_barreira': CampoMeta(
        'tipo_barreira',
        'Tipo de Barreira',
        'Principal tipo de barreira encontrada',
        'str'
    ).com_opcoes({
        'custo': 'Custo/Preço',
        'interface': 'Interface não acessível',
        'conteudo': 'Conteúdo não adaptado',
        'conhecimento': 'Falta de conhecimento',
        'equipamento': 'Falta de equipamento adaptado',
        'outro': 'Outro'
    })
}


def get_todos_campos() -> dict:
    """Retorna todos os campos de metadados"""
    todos = {}
    todos.update(CAMPOS_BASE)
    todos.update(CAMPOS_DEFICIENCIA)
    todos.update(CAMPOS_ACESSO_TECNOLOGIA)
    todos.update(CAMPOS_USO_INTERNET)
    todos.update(CAMPOS_DEMOGRAFICOS)
    todos.update(CAMPOS_ACESSIBILIDADE)
    return todos


def get_campo(nome: str) -> CampoMeta:
    """Recupera metadados de um campo específico"""
    todos = get_todos_campos()
    return todos.get(nome)


def listar_campos_por_categoria() -> dict:
    """Lista campos organizados por categoria"""
    return {
        'Base': CAMPOS_BASE,
        'Deficiência': CAMPOS_DEFICIENCIA,
        'Acesso à Tecnologia': CAMPOS_ACESSO_TECNOLOGIA,
        'Uso da Internet': CAMPOS_USO_INTERNET,
        'Demográficos': CAMPOS_DEMOGRAFICOS,
        'Acessibilidade': CAMPOS_ACESSIBILIDADE
    }
