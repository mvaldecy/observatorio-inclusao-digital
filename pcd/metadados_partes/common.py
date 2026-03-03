class CampoMeta:
    """Classe base para metadados de um campo"""

    def __init__(self, nome: str, label: str, descricao: str = "", tipo: str = "str"):
        self.nome = nome
        self.label = label
        self.descricao = descricao
        self.tipo = tipo
        self._opcoes = {}

    def com_opcoes(self, opcoes: dict):
        self._opcoes = opcoes
        return self

    @property
    def opcoes(self):
        return self._opcoes

    def __repr__(self):
        return f"<CampoMeta: {self.nome} ({self.label})>"
