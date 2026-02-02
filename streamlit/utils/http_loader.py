"""
Carregador de dados via HTTP com cache local
Organizado por fonte de dados com métodos específicos para cada uma
"""
import requests
from pathlib import Path
import streamlit as st
from typing import Optional, Tuple, List, Dict
import pandas as pd
import pyreadstat
import zipfile
from .data_sources import get_fonte_urls, get_fonte_info, list_fontes


class HTTPDataLoader:
    """
    Carrega dados via HTTP com cache local
    Suporta múltiplas fontes: CETIC, ANATEL, IBGE, etc.
    """

    def __init__(self, cache_dir: str = None, fonte: str = 'cetic'):
        """
        Inicializa o loader de dados

        Args:
            cache_dir: Diretório de cache (opcional)
            fonte: Fonte de dados ('cetic', 'anatel', 'ibge', etc.)
        """
        if cache_dir is None:
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

        # Cria pasta específica da fonte (importante para deploy)
        fonte_dir = self.cache_dir / self.fonte
        fonte_dir.mkdir(parents=True, exist_ok=True)

    # =============================================================================
    # MÉTODOS AUXILIARES GERAIS
    # =============================================================================

    def _get_cache_path(self, ano: any, tipo: str, extensao: str = None) -> Path:
        """
        Retorna caminho do arquivo em cache

        Args:
            ano: Ano dos dados
            tipo: Tipo dos dados (ex: 'domicilios', 'individuos')
            extensao: Extensão do arquivo (se None, detecta da URL)
        """
        fonte_dir = self.cache_dir / self.fonte / str(ano)
        fonte_dir.mkdir(parents=True, exist_ok=True)

        if extensao is None:
            if ano not in self.urls or tipo not in self.urls[ano]:
                extensao = "sav"  # Fallback padrão
            else:
                url = self.urls[ano][tipo]
                extensao = url.split('.')[-1].lower().split('?')[0]

                # Validação de extensão
                if len(extensao) > 5:
                    extensao = "sav"

                # ANATEL sempre usa CSV/Parquet após processamento
                if self.fonte == 'anatel' or extensao == 'zip':
                    extensao = 'csv'

        return fonte_dir / f"{tipo}.{extensao}"

    def _download_file(self, url: str, destino: Path) -> bool:
        """
        Baixa arquivo via HTTP silenciosamente

        Args:
            url: URL do arquivo
            destino: Path de destino

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            with open(destino, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return True

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erro no download: {str(e)}")
            if destino.exists():
                destino.unlink()
            return False
        except Exception as e:
            st.error(f"❌ Erro inesperado: {str(e)}")
            if destino.exists():
                destino.unlink()
            return False

    def _limpar_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa nomes de colunas: remove BOM, corrige encoding e normaliza para maiúsculo

        Args:
            df: DataFrame a ser limpo

        Returns:
            DataFrame com colunas limpas
        """
        if df is None or df.empty:
            return df
            
        novas_colunas = []
        for col in df.columns:
            # Corrige encoding se necessário
            try:
                if any(x in col for x in ['Ã', 'Â', 'Ê', 'Î', 'Ô', 'Û', 'õ', 'ç']):
                    limpo = col.encode('latin-1').decode('utf-8')
                else:
                    limpo = col
            except:
                limpo = col
            
            # Remove BOM e espaços extras
            limpo = limpo.replace('\ufeff', '').replace('ï»¿', '').replace('»¿', '').strip()
            
            # Normaliza para MAIÚSCULO
            limpo = limpo.upper()
            
            novas_colunas.append(limpo)
            
        df.columns = novas_colunas
        return df

    def _preparar_dataframe(self, df: pd.DataFrame, aplicar_categorizacao: bool = True) -> pd.DataFrame:
        """
        Otimiza o DataFrame tratando tipos e reduzindo uso de memória

        Args:
            df: DataFrame a ser otimizado
            aplicar_categorizacao: Se True, converte strings com poucos valores únicos em category

        Returns:
            DataFrame otimizado
        """
        if df is None or df.empty:
            return df

        for col in df.columns:
            # Trata colunas numéricas
            if pd.api.types.is_numeric_dtype(df[col]):
                if pd.api.types.is_integer_dtype(df[col]):
                    if df[col].isna().any():
                        df[col] = pd.to_numeric(df[col], downcast='float')
                    else:
                        df[col] = pd.to_numeric(df[col], downcast='integer')
                else:
                    df[col] = pd.to_numeric(df[col], downcast='float')
                continue

            # Trata colunas object (strings)
            if df[col].dtype == 'object':
                try:
                    # Limpeza básica
                    df[col] = df[col].replace(['', ' ', '  ', 'nan', 'None', 'NaT', '<NA>', '-'], pd.NA)
                    
                    # Tenta converter para numérico
                    s_num = pd.to_numeric(df[col], errors='coerce')
                    
                    # Trata vírgula como decimal
                    if s_num.notna().sum() < df[col].notna().sum() * 0.5:
                        if df[col].astype(str).str.contains(',').any():
                            s_temp = df[col].astype(str).str.replace(',', '.', regex=False)
                            s_num = pd.to_numeric(s_temp, errors='coerce')

                    # Se conversão for bem-sucedida (80% ou mais)
                    if s_num.notna().sum() > 0 and (s_num.notna().sum() >= df[col].notna().sum() * 0.8):
                        df[col] = s_num
                    
                    # Categoriza strings com poucos valores únicos
                    if aplicar_categorizacao and df[col].dtype == 'object':
                        n_unicos = df[col].nunique()
                        if n_unicos < 500:
                            df[col] = df[col].astype('category')
                except Exception:
                    pass

        return df

    # =============================================================================
    # MÉTODOS ESPECÍFICOS DA ANATEL
    # =============================================================================

    def _filtrar_csvs_setembro(self, csv_paths: list) -> dict:
        """
        Filtra apenas arquivos CSV que terminam com -09 (setembro) e mapeia por ano

        Args:
            csv_paths: Lista de caminhos para arquivos CSV

        Returns:
            Dicionário {ano: path_do_csv}
        """
        mapeamento = {}

        for csv_path in csv_paths:
            nome = csv_path.stem
            partes = nome.split('_')

            for parte in partes:
                # Formato YYYY-MM, verifica se termina com -09
                if '-09' in parte and len(parte) == 7:
                    ano = parte[:4]
                    mapeamento[ano] = csv_path
                    break

        return mapeamento

    def _processar_csvs_setembro(self, csv_paths: list, tipo: str) -> bool:
        """
        Processa apenas os CSVs de setembro (finais com -09) e salva como parquet
        Um arquivo por ano, sem consolidação de múltiplos CSVs

        Args:
            csv_paths: Lista de caminhos para arquivos CSV
            tipo: Tipo dos dados (ex: 'conectividade-escola')

        Returns:
            True se sucesso, False caso contrário
        """
        if not csv_paths:
            return False

        try:
            # Filtra apenas arquivos -09 (setembro)
            mapeamento = self._filtrar_csvs_setembro(csv_paths)

            if not mapeamento:
                st.error("❌ Nenhum arquivo com sufixo -09 (setembro) encontrado")
                return False

            sucesso_total = True

            for ano, csv_path in sorted(mapeamento.items()):
                try:
                    # Lê o CSV
                    try:
                        df = pd.read_csv(csv_path, sep=';', encoding='utf-8-sig',
                                       low_memory=False, na_values=['', ' ', '  '],
                                       keep_default_na=True, decimal=',')
                    except Exception:
                        df = pd.read_csv(csv_path, sep=';', encoding='latin-1',
                                       low_memory=False, na_values=['', ' ', '  '],
                                       keep_default_na=True, decimal=',')

                    # Limpa e otimiza
                    df = self._limpar_colunas(df)
                    df = self._preparar_dataframe(df, aplicar_categorizacao=True)

                    # Cria pasta do ano e salva parquet
                    ano_dir = self.cache_dir / self.fonte / ano
                    ano_dir.mkdir(parents=True, exist_ok=True)
                    destino_parquet = ano_dir / f"{tipo}.parquet"
                    df.to_parquet(destino_parquet, compression='snappy', engine='pyarrow')

                except Exception as e:
                    st.error(f"❌ Erro ao processar ano {ano}: {str(e)}")
                    sucesso_total = False

            return sucesso_total

        except Exception as e:
            st.error(f"❌ Erro no processamento: {str(e)}")
            return False

    def _download_and_extract_zip(self, url: str, tipo: str) -> bool:
        """
        Baixa um ZIP, extrai e processa apenas os CSVs de setembro (-09)
        Cada CSV é convertido para parquet e salvo na pasta do ano correspondente

        Args:
            url: URL do arquivo ZIP
            tipo: Tipo dos dados (ex: 'conectividade-escola')

        Returns:
            True se sucesso, False caso contrário
        """
        # Cria diretório temporário para extração
        temp_dir = self.cache_dir / self.fonte / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_zip = temp_dir / 'download.zip'

        sucesso_processamento = False

        try:
            if self._download_file(url, temp_zip):
                with zipfile.ZipFile(temp_zip, 'r') as z:
                    nomes_arquivos = z.namelist()
                    csv_files = [f for f in nomes_arquivos if f.endswith('.csv')]

                    if not csv_files:
                        st.error(f"❌ Nenhum CSV encontrado dentro do arquivo ZIP")
                        return False

                    z.extractall(temp_dir)
                    csv_paths = [temp_dir / f for f in csv_files]

                # Processa apenas CSVs de setembro (-09)
                sucesso_processamento = self._processar_csvs_setembro(csv_paths, tipo)
                return sucesso_processamento

        except Exception as e:
            st.error(f"❌ Erro ao extrair ZIP: {str(e)}")
            return False
        finally:
            # Limpa todo o diretório temporário
            if temp_dir.exists():
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass

    def _carregar_anatel(self, ano: any, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados da ANATEL de um ano específico
        Se não existir em cache, baixa o ZIP (que contém todos os anos) e processa

        Args:
            ano: Ano dos dados (2022, 2023, 2024, 2025)
            tipo: Tipo dos dados (ex: 'conectividade-escola')
            force_download: Forçar download mesmo se existir cache

        Returns:
            Tupla (DataFrame, None) ou None se erro
        """
        fonte_dir = self.cache_dir / self.fonte
        ano_dir = fonte_dir / str(ano)
        parquet_path = ano_dir / f"{tipo}.parquet"

        # Se existe cache e não forçou download, carrega direto
        if parquet_path.exists() and not force_download:
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                st.error(f"❌ Erro ao carregar parquet: {str(e)}")
                return None, None

        # Se não existe cache ou forçou download, precisa baixar o ZIP
        # O ZIP contém todos os anos, então busca da URL 'consolidado'
        url = None

        # Tenta pegar URL do ano específico primeiro
        if ano in self.urls and tipo in self.urls[ano]:
            url = self.urls[ano][tipo]
        # Se não encontrar, tenta pegar de 'consolidado' (caso comum da ANATEL)
        elif 'consolidado' in self.urls and tipo in self.urls['consolidado']:
            url = self.urls['consolidado'][tipo]

        if not url:
            st.error(f"❌ URL não encontrada para {self.fonte}/{tipo}")
            return None, None

        # Baixa e processa o ZIP (cria parquets para TODOS os anos)
        if not self._download_and_extract_zip(url, tipo):
            return None, None

        # Após processar, carrega o ano solicitado
        if parquet_path.exists():
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                st.error(f"❌ Erro ao carregar parquet após download: {str(e)}")
                return None, None
        else:
            st.error(f"❌ Dados de {ano} não foram encontrados no ZIP")
            return None, None

    # =============================================================================
    # MÉTODOS ESPECÍFICOS DO CETIC
    # =============================================================================

    def _carregar_cetic(self, ano: any, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados do CETIC (arquivos SPSS .sav)

        Args:
            ano: Ano dos dados
            tipo: Tipo dos dados (ex: 'domicilios', 'individuos')
            force_download: Forçar download mesmo se existir cache

        Returns:
            Tupla (DataFrame, metadados) ou None se erro
        """
        cache_path = self._get_cache_path(ano, tipo)
        url = self.urls[ano][tipo]

        if not cache_path.exists() or force_download:
            if not self._download_file(url, cache_path):
                return None, None

        try:
            df, meta = pyreadstat.read_sav(str(cache_path))
            return df, meta
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo SAV {cache_path.name}: {str(e)}")
            return None, None

    # =============================================================================
    # MÉTODOS PÚBLICOS
    # =============================================================================

    def carregar_dados(self, ano: any, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados (via cache ou download)

        Args:
            ano: Ano dos dados
            tipo: Tipo dos dados (ex: 'domicilios', 'individuos')
            force_download: Forçar download mesmo se existir cache

        Returns:
            Tupla (DataFrame, metadados) ou None se erro
        """
        # Para ANATEL, não valida ano aqui pois usa 'consolidado' nas URLs
        if self.fonte != 'anatel':
            if ano not in self.urls:
                st.error(f"❌ Dados de {ano} ainda não disponíveis para {self.fonte}")
                return None, None

            if tipo not in self.urls[ano]:
                st.error(f"❌ Tipo '{tipo}' não disponível para {self.fonte}/{ano}")
                return None, None

        # Chama o método específico da fonte
        metodo_nome = f"_carregar_{self.fonte}"
        metodo_loader = getattr(self, metodo_nome, None)

        if metodo_loader:
            return metodo_loader(ano, tipo, force_download)

        st.error(f"❌ Carregador não implementado para a fonte: {self.fonte}")
        return None, None

    # =============================================================================
    # MÉTODOS DE GERENCIAMENTO DE CACHE
    # =============================================================================

    def limpar_cache(self, ano: Optional[any] = None):
        """
        Remove arquivos em cache

        Args:
            ano: Ano específico para limpar. Se None, limpa todo o cache da fonte
        """
        fonte_dir = self.cache_dir / self.fonte

        if ano:
            ano_dir = fonte_dir / str(ano)
            if ano_dir.exists():
                arquivos_removidos = 0
                for arquivo in ano_dir.iterdir():
                    if arquivo.is_file():
                        arquivo.unlink()
                        arquivos_removidos += 1
                if arquivos_removidos > 0:
                    st.success(f"🗑️ {arquivos_removidos} arquivo(s) removido(s)")
        else:
            # Limpa todo o cache da fonte
            if fonte_dir.exists():
                arquivos_removidos = 0
                for arquivo in fonte_dir.rglob("*"):
                    if arquivo.is_file():
                        arquivo.unlink()
                        arquivos_removidos += 1
                if arquivos_removidos > 0:
                    st.success(f"🗑️ Cache limpo: {arquivos_removidos} arquivo(s)")

    def info_cache(self) -> dict:
        """
        Retorna informações sobre arquivos em cache

        Returns:
            Dicionário com informações de cache por ano e tipo
        """
        info = {}
        fonte_dir = self.cache_dir / self.fonte

        if not fonte_dir.exists():
            return info

        for ano_dir in fonte_dir.iterdir():
            if ano_dir.is_dir() and ano_dir.name.isdigit():
                chave_ano = ano_dir.name
                info[chave_ano] = {}
                for arquivo in ano_dir.iterdir():
                    if arquivo.is_file():
                        tipo = arquivo.stem
                        tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
                        info[chave_ano][tipo] = {
                            'tamanho_mb': round(tamanho_mb, 2),
                            'caminho': str(arquivo),
                            'existe': arquivo.exists(),
                            'extensao': arquivo.suffix
                        }
        return info

    def get_anos_disponiveis(self, tipo: str = None) -> list:
        """
        Retorna lista de anos disponíveis

        Args:
            tipo: Filtrar por tipo específico (ex: 'domicilios', 'cobertura-movel'). Se None, retorna todos.

        Returns:
            Lista de anos disponíveis ordenados do mais recente ao mais antigo
        """
        if tipo:
            # Retorna apenas anos que têm o tipo especificado
            anos = [ano for ano, tipos in self.urls.items() if tipo in tipos]
            return sorted(anos, reverse=True, key=lambda x: str(x))
        return sorted(self.urls.keys(), reverse=True, key=lambda x: str(x))

