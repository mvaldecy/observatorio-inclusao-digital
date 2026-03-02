from pcd.metadados_partes.common import CampoMeta


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
    'encontra_barreiras': CampoMeta('encontra_barreiras', 'Encontra Barreiras', 'Encontra barreiras no acesso digital', 'bool'),
    'tipo_barreira': CampoMeta('tipo_barreira', 'Tipo de Barreira', 'Principal tipo de barreira encontrada', 'str').com_opcoes({
        'custo': 'Custo/Preço',
        'interface': 'Interface não acessível',
        'conteudo': 'Conteúdo não adaptado',
        'conhecimento': 'Falta de conhecimento',
        'equipamento': 'Falta de equipamento adaptado',
        'outro': 'Outro'
    })
}
