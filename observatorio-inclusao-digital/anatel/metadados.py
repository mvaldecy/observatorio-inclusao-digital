class MetadadosAnatel:
    """
    Mapeamento de colunas e valores para a base da ANATEL.
    Baseado na estrutura de setores censitários e cobertura.
    """
    class UF:
        column = 'UF'
        PIAUI = 'PI'
        MARANHAO = 'MA'
        CEARA = 'CE'
        SAO_PAULO = 'SP'
        # Adicione outros conforme necessário

    class REGIAO:
        column = 'Região'
        NORDESTE = 'Nordeste'
        SUDESTE = 'Sudeste'
        SUL = 'Sul'
        NORTE = 'Norte'
        CENTRO_OESTE = 'Centro-oeste'

    class TIPO_SETOR:
        column = 'Tipo Setor'
        URBANO = 'Urbano'
        RURAL = 'Rural'