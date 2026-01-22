"""
Carregador de dados via HTTP com cache local
"""
import requests
from pathlib import Path
import streamlit as st
from typing import Optional, Tuple
import pandas as pd
import pyreadstat
from .data_sources import get_fonte_urls, get_fonte_info, list_fontes


class HTTPDataLoader:
    """Carrega dados via HTTP com cache local"""

    def __init__(self, cache_dir: str = None, fonte: str = 'cetic'):
        """
        Inicializa o loader de dados

        Args:
            cache_dir: Diretório de cache (opcional)
            fonte: Fonte de dados ('cetic', 'anatel', 'ibge', etc.)
        """
        if cache_dir is None:
            # Usa diretório do projeto
            project_root = Path(__file__).parent.parent.parent
            cache_dir = project_root / "data" / "cache"

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.fonte = fonte

        # Valida se a fonte existe
        self.fonte_info = get_fonte_info(fonte)
        if not self.fonte_info:
            raise ValueError(f"Fonte '{fonte}' não encontrada. Fontes disponíveis: {', '.join(list_fontes())}")

        # Carrega URLs da fonte
        self.urls = get_fonte_urls(fonte)

    def _get_cache_path(self, ano: int, tipo: str) -> Path:
        """Retorna caminho do arquivo em cache com estrutura fonte/ano/tipo.sav"""
        fonte_dir = self.cache_dir / self.fonte / str(ano)
        fonte_dir.mkdir(parents=True, exist_ok=True)
        return fonte_dir / f"{tipo}.sav"

    def _download_file(self, url: str, destino: Path) -> bool:
        """Baixa arquivo via HTTP com barra de progresso"""
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Tamanho total
            total_size = int(response.headers.get('content-length', 0))

            # Barra de progresso
            progress_bar = st.progress(0)
            downloaded = 0

            with open(destino, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = downloaded / total_size
                            progress_bar.progress(progress)

            progress_bar.empty()
            return True

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erro no download: {str(e)}")
            if destino.exists():
                destino.unlink()  # Remove arquivo parcial
            return False
        except Exception as e:
            st.error(f"❌ Erro inesperado: {str(e)}")
            if destino.exists():
                destino.unlink()
            return False

    def carregar_dados(self, ano: int, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados (via cache ou download)

        Args:
            ano: Ano da pesquisa (2023, 2024, 2025)
            tipo: 'domicilios' ou 'individuos'
            force_download: Forçar novo download mesmo se existir cache

        Returns:
            (dataframe, metadados) ou None se falhar
        """
        # Valida entrada
        if ano not in self.urls:
            st.error(f"❌ Dados de {ano} ainda não disponíveis para {self.fonte}")
            return None

        if tipo not in self.urls[ano]:
            st.error(f"❌ Tipo '{tipo}' não disponível para {self.fonte}/{ano}")
            return None

        # Caminho do cache
        cache_path = self._get_cache_path(ano, tipo)
        url = self.urls[ano][tipo]

        # Verifica cache
        if not cache_path.exists() or force_download:
            # Baixa arquivo
            if not self._download_file(url, cache_path):
                return None

        # Carrega arquivo .sav
        try:
            df, meta = pyreadstat.read_sav(str(cache_path))
            return df, meta
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo: {str(e)}")
            return None

    def limpar_cache(self, ano: Optional[int] = None):
        """Remove arquivos em cache"""
        fonte_dir = self.cache_dir / self.fonte

        if ano:
            ano_dir = fonte_dir / str(ano)
            if ano_dir.exists():
                arquivos_removidos = 0
                for arquivo in ano_dir.glob("*.sav"):
                    arquivo.unlink()
                    arquivos_removidos += 1
                if arquivos_removidos > 0:
                    st.success(f"🗑️ {arquivos_removidos} arquivo(s) removido(s)")
        else:
            # Limpa todo o cache da fonte
            if fonte_dir.exists():
                arquivos_removidos = 0
                for arquivo in fonte_dir.rglob("*.sav"):
                    arquivo.unlink()
                    arquivos_removidos += 1
                if arquivos_removidos > 0:
                    st.success(f"🗑️ Cache limpo: {arquivos_removidos} arquivo(s)")

    def info_cache(self) -> dict:
        """Retorna informações sobre arquivos em cache"""
        info = {}
        fonte_dir = self.cache_dir / self.fonte

        if not fonte_dir.exists():
            return info

        for ano_dir in fonte_dir.iterdir():
            if ano_dir.is_dir() and ano_dir.name.isdigit():
                ano = int(ano_dir.name)
                info[ano] = {}
                for arquivo in ano_dir.glob("*.sav"):
                    tipo = arquivo.stem
                    tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
                    info[ano][tipo] = {
                        'tamanho_mb': round(tamanho_mb, 2),
                        'caminho': str(arquivo),
                        'existe': arquivo.exists()
                    }
        return info

    def get_anos_disponiveis(self, tipo: str = None) -> list:
        """
        Retorna lista de anos disponíveis

        Args:
            tipo: Filtrar por tipo específico ('domicilios' ou 'individuos'). Se None, retorna todos.
        """
        if tipo:
            # Retorna apenas anos que têm o tipo especificado
            anos = [ano for ano, tipos in self.urls.items() if tipo in tipos]
            return sorted(anos, reverse=True)
        return sorted(self.urls.keys(), reverse=True)

