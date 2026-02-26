# -*- coding: utf-8 -*-
"""
DICIONÁRIO DE DADOS - PCD - PESSOAS COM DEFICIÊNCIA
Mapeamento completo das variáveis dos dados de inclusão digital para PCD
"""

DICIONARIO = {
    # Identificação
    'id': 'Identificador único do registro',
    'ano': 'Ano de referência dos dados',
    
    # Localização
    'uf': 'Sigla da Unidade Federativa',
    'regiao': 'Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)',
    'municipio': 'Nome do município',
    'cod_municipio': 'Código IBGE do município',
    'area': 'Área de localização (Urbana ou Rural)',
    
    # Deficiência
    'tem_deficiencia': 'Indica se a pessoa possui alguma deficiência',
    'tipo_deficiencia': 'Tipo principal de deficiência (Visual, Auditiva, Motora, Intelectual, Múltipla)',
    'grau_deficiencia': 'Grau de severidade (Leve, Moderado, Severo, Profundo)',
    'deficiencia_visual': 'Possui deficiência visual',
    'deficiencia_auditiva': 'Possui deficiência auditiva',
    'deficiencia_motora': 'Possui deficiência motora',
    'deficiencia_intelectual': 'Possui deficiência intelectual',
    
    # Acesso à Tecnologia
    'tem_internet': 'Possui acesso à internet',
    'tem_computador': 'Possui computador (mesa ou notebook)',
    'tem_notebook': 'Possui notebook',
    'tem_desktop': 'Possui computador de mesa',
    'tem_smartphone': 'Possui smartphone',
    'tem_tablet': 'Possui tablet',
    'tipo_conexao': 'Tipo de conexão de internet (Fibra, Cabo, Móvel, Satélite)',
    'velocidade_internet': 'Faixa de velocidade da internet em Mbps',
    
    # Uso da Internet
    'frequencia_uso': 'Frequência de uso da internet (Diária, Semanal, Mensal, Raramente)',
    'usa_redes_sociais': 'Utiliza redes sociais',
    'usa_servicos_gov': 'Utiliza serviços governamentais online',
    'usa_ecommerce': 'Realiza compras online (e-commerce)',
    'usa_educacao': 'Utiliza internet para educação/cursos online',
    'usa_trabalho': 'Utiliza internet para trabalho',
    'usa_servicos_financeiros': 'Utiliza serviços financeiros online (banco)',
    'usa_comunicacao': 'Utiliza internet para comunicação (email, videochamadas)',
    'usa_entretenimento': 'Utiliza internet para entretenimento (vídeos, jogos, música)',
    
    # Demografia
    'idade': 'Idade em anos',
    'faixa_etaria': 'Faixa etária',
    'sexo': 'Sexo (Masculino, Feminino)',
    'escolaridade': 'Nível de escolaridade',
    'renda_familiar': 'Faixa de renda familiar em salários mínimos',
    'situacao_trabalho': 'Situação no mercado de trabalho',
    'cor_raca': 'Cor/raça',
    
    # Acessibilidade Digital
    'usa_tecnologia_assistiva': 'Utiliza tecnologia assistiva para acesso digital',
    'tipo_tecnologia_assistiva': 'Tipo de tecnologia assistiva (Leitor de tela, Ampliador, etc)',
    'leitor_tela': 'Utiliza leitor de tela',
    'ampliador_tela': 'Utiliza ampliador de tela',
    'teclado_adaptado': 'Utiliza teclado adaptado',
    'mouse_adaptado': 'Utiliza mouse adaptado',
    'usa_legendas': 'Utiliza legendas/closed caption',
    
    # Barreiras
    'encontra_barreiras': 'Encontra barreiras no acesso digital',
    'tipo_barreira': 'Principal tipo de barreira (Custo, Interface, Conteúdo, etc)',
    'barreira_custo': 'Barreira relacionada a custo/preço',
    'barreira_interface': 'Barreira de interface não acessível',
    'barreira_conteudo': 'Barreira de conteúdo não adaptado',
    'barreira_conhecimento': 'Barreira por falta de conhecimento',
    'barreira_equipamento': 'Barreira por falta de equipamento adaptado',
    
    # Motivos para não ter internet
    'motivo_nao_internet_custo': 'Não tem internet porque é caro',
    'motivo_nao_internet_falta_interesse': 'Não tem internet por falta de interesse',
    'motivo_nao_internet_falta_habilidade': 'Não tem internet por falta de habilidade',
    'motivo_nao_internet_nao_disponivel': 'Não tem internet porque não está disponível',
    'motivo_nao_internet_usa_outro_local': 'Usa internet em outro local',
    'motivo_nao_internet_privacidade': 'Não tem internet por preocupações com privacidade',
    
    # Capacitação e Suporte
    'recebeu_treinamento': 'Recebeu treinamento para uso de tecnologia',
    'tipo_treinamento': 'Tipo de treinamento recebido',
    'precisa_ajuda': 'Precisa de ajuda para usar internet',
    'tem_suporte': 'Tem suporte disponível quando precisa',
    
    # Impacto
    'internet_melhora_vida': 'Considera que internet melhora qualidade de vida',
    'internet_importante_trabalho': 'Considera internet importante para trabalho',
    'internet_importante_educacao': 'Considera internet importante para educação',
    'internet_importante_inclusao': 'Considera internet importante para inclusão social',
}


def get_descricao(campo: str) -> str:
    """Retorna a descrição de um campo"""
    return DICIONARIO.get(campo, f"Campo '{campo}' não encontrado no dicionário")


def listar_campos() -> list:
    """Lista todos os campos disponíveis"""
    return list(DICIONARIO.keys())


def buscar_campos(termo: str) -> dict:
    """
    Busca campos que contenham um termo específico
    
    Args:
        termo: Termo de busca
        
    Returns:
        Dicionário com campos encontrados
    """
    termo_lower = termo.lower()
    return {
        campo: descricao
        for campo, descricao in DICIONARIO.items()
        if termo_lower in campo.lower() or termo_lower in descricao.lower()
    }
