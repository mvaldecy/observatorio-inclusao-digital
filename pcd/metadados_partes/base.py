from pcd.metadados_partes.common import CampoMeta


CAMPOS_BASE = {
    'id': CampoMeta('id', 'ID', 'Identificador único do registro', 'int'),
    'ano': CampoMeta('ano', 'Ano', 'Ano de referência dos dados', 'int'),
    'uf': CampoMeta('uf', 'UF', 'Unidade Federativa', 'str'),
    'regiao': CampoMeta('regiao', 'Região', 'Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)', 'str'),
    'municipio': CampoMeta('municipio', 'Município', 'Nome do município', 'str'),
    'area': CampoMeta('area', 'Área', 'Área de localização', 'str').com_opcoes({'urbana': 'Urbana', 'rural': 'Rural'})
}
