from pcd.metadados_partes.common import CampoMeta


CAMPOS_DEFICIENCIA = {
    'tem_deficiencia': CampoMeta('tem_deficiencia', 'Tem Deficiência', 'Indica se a pessoa tem alguma deficiência', 'bool'),
    'tipo_deficiencia': CampoMeta('tipo_deficiencia', 'Tipo de Deficiência', 'Tipo principal de deficiência', 'str').com_opcoes({
        'visual': 'Visual',
        'auditiva': 'Auditiva',
        'motora': 'Motora',
        'intelectual': 'Intelectual',
        'multipla': 'Múltipla'
    }),
    'grau_deficiencia': CampoMeta('grau_deficiencia', 'Grau da Deficiência', 'Grau de severidade da deficiência', 'str').com_opcoes({
        'leve': 'Leve',
        'moderado': 'Moderado',
        'severo': 'Severo',
        'profundo': 'Profundo'
    })
}
