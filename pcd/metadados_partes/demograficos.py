from pcd.metadados_partes.common import CampoMeta


CAMPOS_DEMOGRAFICOS = {
    'idade': CampoMeta('idade', 'Idade', 'Idade em anos', 'int'),
    'faixa_etaria': CampoMeta('faixa_etaria', 'Faixa Etária', 'Faixa etária', 'str').com_opcoes({
        '10_17': '10 a 17 anos',
        '18_24': '18 a 24 anos',
        '25_34': '25 a 34 anos',
        '35_44': '35 a 44 anos',
        '45_59': '45 a 59 anos',
        '60_mais': '60 anos ou mais'
    }),
    'sexo': CampoMeta('sexo', 'Sexo', 'Sexo', 'str').com_opcoes({'masculino': 'Masculino', 'feminino': 'Feminino'}),
    'escolaridade': CampoMeta('escolaridade', 'Escolaridade', 'Nível de escolaridade', 'str').com_opcoes({
        'sem_instrucao': 'Sem instrução',
        'fundamental_incompleto': 'Fundamental incompleto',
        'fundamental_completo': 'Fundamental completo',
        'medio_incompleto': 'Médio incompleto',
        'medio_completo': 'Médio completo',
        'superior_incompleto': 'Superior incompleto',
        'superior_completo': 'Superior completo'
    }),
    'renda_familiar': CampoMeta('renda_familiar', 'Renda Familiar', 'Faixa de renda familiar em salários mínimos', 'str').com_opcoes({
        'ate_1': 'Até 1 SM',
        '1_a_2': '1 a 2 SM',
        '2_a_3': '2 a 3 SM',
        '3_a_5': '3 a 5 SM',
        '5_a_10': '5 a 10 SM',
        'mais_10': 'Mais de 10 SM'
    })
}
