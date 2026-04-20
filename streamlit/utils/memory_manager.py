"""
Gerenciador de memória para páginas Streamlit.

Objetivo: manter em memória apenas o dataset da página atualmente ativa.
Ao trocar de página, os caches (@st.cache_data / @st.cache_resource) dos
datasets das páginas anteriores são descartados e um gc.collect() é
executado para liberar memória imediatamente.

Uso em cada página (logo após st.set_page_config):

    from utils.memory_manager import set_active_dataset
    set_active_dataset("inep")  # ou "cetic_domicilios", etc.

Chaves disponíveis (ver DATASET_LOADERS abaixo):
    - "cetic_domicilios"
    - "cetic_individuos"
    - "anatel_conectividade"
    - "anatel_cobertura_movel"   (cobertura geral + 4G/5G por UF)
    - "inep"
"""
from __future__ import annotations

import gc
from typing import Callable, Dict, List, Optional

import streamlit as st

from . import data_loader as _dl

# -----------------------------------------------------------------------------
# Registro: chave de dataset -> lista de funções cacheadas a serem limpas
# -----------------------------------------------------------------------------
# Cada entrada lista TODAS as funções (@st.cache_data e @st.cache_resource)
# que carregam dados grandes para aquele dataset. Ao trocar de dataset ativo,
# todas as funções das outras chaves têm .clear() chamado.
DATASET_LOADERS: Dict[str, List[Callable]] = {
    "cetic_domicilios": [
        _dl.carregar_dados_domicilios_cetic,
        _dl.get_analisador_domicilios,
    ],
    "cetic_individuos": [
        _dl.carregar_dados_individuos_cetic,
        _dl.get_analisador_individuos,
    ],
    "anatel_conectividade": [
        _dl.carregar_dados_anatel,
        _dl.carregar_conectividade_escola_anatel,
        _dl.get_analisador_anatel,
    ],
    "anatel_cobertura_movel": [
        _dl.carregar_cobertura_movel_anatel,
        _dl.carregar_cobertura_movel_4g_uf_anatel,
        _dl.carregar_cobertura_movel_5g_uf_anatel,
        _dl.get_analisador_cobertura_movel,
    ],
    "inep": [
        _dl.carregar_dados_inep,
        _dl.carregar_educacao_basica_inep,
        _dl.get_analisador_inep,
    ],
}

_ACTIVE_KEY = "_mm_active_dataset"


def _safe_clear(func: Callable) -> bool:
    """Invoca func.clear() se disponível. Retorna True se limpou algo."""
    clear = getattr(func, "clear", None)
    if callable(clear):
        try:
            clear()
            return True
        except Exception as exc:  # pragma: no cover - defensivo
            print(f"[memory_manager] Falha ao limpar {func.__name__}: {exc}")
    return False


def clear_dataset(key: str) -> int:
    """Limpa os caches de um dataset específico. Retorna nº de funções limpas."""
    loaders = DATASET_LOADERS.get(key, [])
    n = sum(1 for f in loaders if _safe_clear(f))
    return n


def clear_all_datasets() -> int:
    """Limpa caches de TODOS os datasets registrados."""
    total = 0
    for key in DATASET_LOADERS:
        total += clear_dataset(key)
    gc.collect()
    return total


def get_active_dataset() -> Optional[str]:
    return st.session_state.get(_ACTIVE_KEY)


def set_active_dataset(key: str, *, verbose: bool = False) -> None:
    """
    Marca `key` como dataset ativo e libera a memória de todos os outros
    datasets registrados. Se o dataset ativo já é `key`, não faz nada.

    Args:
        key: identificador do dataset (deve estar em DATASET_LOADERS)
        verbose: se True, exibe mensagem no sidebar ao liberar memória
    """
    if key not in DATASET_LOADERS:
        # Chave desconhecida: apenas registra e segue
        st.session_state[_ACTIVE_KEY] = key
        return

    current = st.session_state.get(_ACTIVE_KEY)
    if current == key:
        return

    # Limpa caches de todos os datasets exceto o novo ativo
    cleared_datasets: List[str] = []
    for other_key in DATASET_LOADERS:
        if other_key == key:
            continue
        n = clear_dataset(other_key)
        if n:
            cleared_datasets.append(other_key)

    if cleared_datasets:
        gc.collect()
        if verbose:
            st.sidebar.caption(
                "🧹 Memória liberada: " + ", ".join(cleared_datasets)
            )

    st.session_state[_ACTIVE_KEY] = key


def render_memory_sidebar(show_button: bool = True) -> None:
    """
    Componente opcional de sidebar: mostra o dataset ativo e um botão
    para liberar manualmente a memória de todos os datasets.
    """
    active = get_active_dataset()
    if active:
        st.sidebar.caption(f"📦 Dataset ativo: `{active}`")
    if show_button and st.sidebar.button(
        "🧹 Liberar memória de outros datasets",
        help="Descarta caches de datasets não utilizados pela página atual",
        use_container_width=True,
    ):
        total = 0
        for other in DATASET_LOADERS:
            if other != active:
                total += clear_dataset(other)
        gc.collect()
        st.sidebar.success(f"✓ {total} cache(s) liberado(s)")

