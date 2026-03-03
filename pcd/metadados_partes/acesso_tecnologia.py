from pcd.metadados_partes.common import CampoMeta


CAMPOS_ACESSO_TECNOLOGIA = {
    'tem_internet': CampoMeta('tem_internet', 'Tem Acesso à Internet', 'Indica se tem acesso à internet', 'bool'),
    'tem_computador': CampoMeta('tem_computador', 'Tem Computador', 'Possui computador de mesa ou notebook', 'bool'),
    'tem_smartphone': CampoMeta('tem_smartphone', 'Tem Smartphone', 'Possui smartphone', 'bool'),
    'tem_tablet': CampoMeta('tem_tablet', 'Tem Tablet', 'Possui tablet', 'bool'),
    'tipo_conexao': CampoMeta('tipo_conexao', 'Tipo de Conexão', 'Tipo principal de conexão à internet', 'str').com_opcoes({
        'fibra': 'Fibra Óptica',
        'cabo': 'Cabo',
        'movel': 'Móvel (3G/4G/5G)',
        'satelite': 'Satélite',
        'outro': 'Outro'
    }),
    'velocidade_internet': CampoMeta('velocidade_internet', 'Velocidade da Internet', 'Faixa de velocidade da internet (Mbps)', 'str').com_opcoes({
        'ate_1': 'Até 1 Mbps',
        '1_a_5': '1 a 5 Mbps',
        '5_a_10': '5 a 10 Mbps',
        '10_a_50': '10 a 50 Mbps',
        'mais_50': 'Mais de 50 Mbps'
    })
}
