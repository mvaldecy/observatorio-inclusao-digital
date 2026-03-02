"""
Metadados e definições de campos para dados PCD.

Arquivo agregador para manter API estável com implementação modular.
"""

from pcd.metadados_partes import (
    CampoMeta,
    CAMPOS_BASE,
    CAMPOS_DEFICIENCIA,
    CAMPOS_ACESSO_TECNOLOGIA,
    CAMPOS_USO_INTERNET,
    CAMPOS_DEMOGRAFICOS,
    CAMPOS_ACESSIBILIDADE,
)


def get_todos_campos() -> dict:
    todos = {}
    todos.update(CAMPOS_BASE)
    todos.update(CAMPOS_DEFICIENCIA)
    todos.update(CAMPOS_ACESSO_TECNOLOGIA)
    todos.update(CAMPOS_USO_INTERNET)
    todos.update(CAMPOS_DEMOGRAFICOS)
    todos.update(CAMPOS_ACESSIBILIDADE)
    return todos


def get_campo(nome: str) -> CampoMeta:
    return get_todos_campos().get(nome)


def listar_campos_por_categoria() -> dict:
    return {
        'Base': CAMPOS_BASE,
        'Deficiência': CAMPOS_DEFICIENCIA,
        'Acesso à Tecnologia': CAMPOS_ACESSO_TECNOLOGIA,
        'Uso da Internet': CAMPOS_USO_INTERNET,
        'Demográficos': CAMPOS_DEMOGRAFICOS,
        'Acessibilidade': CAMPOS_ACESSIBILIDADE,
    }
