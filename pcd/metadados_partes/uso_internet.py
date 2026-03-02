from pcd.metadados_partes.common import CampoMeta


CAMPOS_USO_INTERNET = {
    'frequencia_uso': CampoMeta('frequencia_uso', 'Frequência de Uso', 'Frequência de uso da internet', 'str').com_opcoes({
        'diaria': 'Diária',
        'semanal': 'Semanal',
        'mensal': 'Mensal',
        'raramente': 'Raramente',
        'nunca': 'Nunca'
    }),
    'usa_redes_sociais': CampoMeta('usa_redes_sociais', 'Usa Redes Sociais', 'Utiliza redes sociais', 'bool'),
    'usa_servicos_gov': CampoMeta('usa_servicos_gov', 'Usa Serviços Governamentais', 'Utiliza serviços governamentais online', 'bool'),
    'usa_ecommerce': CampoMeta('usa_ecommerce', 'Usa E-commerce', 'Realiza compras online', 'bool'),
    'usa_educacao': CampoMeta('usa_educacao', 'Usa para Educação', 'Utiliza internet para educação/cursos', 'bool'),
    'usa_trabalho': CampoMeta('usa_trabalho', 'Usa para Trabalho', 'Utiliza internet para trabalho', 'bool')
}
