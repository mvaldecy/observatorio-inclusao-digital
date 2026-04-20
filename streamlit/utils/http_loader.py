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

    def _download_and_convert_xlsx_to_parquet(self, url: str, tipo: str = 'cobertura-movel') -> bool:
        """
        Baixa um arquivo Excel (.xlsx) e converte para Parquet
        Guarda o arquivo na pasta cache/anatel/cobertura-movel/

        Args:
            url: URL do arquivo Excel
            tipo: Tipo dos dados (default: 'cobertura-movel')

        Returns:
            True se sucesso, False caso contrário
        """
        # Cria diretório de destino para cobertura móvel
        destino_dir = self.cache_dir / self.fonte / tipo
        destino_dir.mkdir(parents=True, exist_ok=True)

        # Cria diretório temporário para download
        temp_dir = self.cache_dir / self.fonte / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_xlsx = temp_dir / f'{tipo}.xlsx'

        try:
            if not self._download_file(url, temp_xlsx):
                return False

            # Lê o arquivo Excel
            df = pd.read_excel(temp_xlsx, engine='openpyxl')

            if df is None or df.empty:
                st.error(f"❌ Arquivo Excel está vazio")
                return False

            # Limpa e otimiza o DataFrame
            df = self._limpar_colunas(df)
            df = self._preparar_dataframe(df, aplicar_categorizacao=True)

            # Salva como parquet
            destino_parquet = destino_dir / f'{tipo}.parquet'
            df.to_parquet(destino_parquet, compression='snappy', engine='pyarrow')

            return True

        except Exception as e:
            st.error(f"❌ Erro ao baixar/converter cobertura móvel: {str(e)}")
            import traceback
            st.error(f"Detalhes: {traceback.format_exc()}")
            return False
        finally:
            # Limpa o diretório temporário
            if temp_dir.exists():
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass

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
        Carrega dados da ANATEL de um ano específico ou consolidado
        Se não existir em cache, baixa e processa

        Args:
            ano: Ano dos dados (2022, 2023, 2024, 2025) ou 'consolidado'
            tipo: Tipo dos dados (ex: 'conectividade-escola', 'cobertura-movel', 'cobertura-movel-5g-uf', 'cobertura-movel-4g-uf')
            force_download: Forçar download mesmo se existir cache

        Returns:
            Tupla (DataFrame, None) ou None se erro
        """
        fonte_dir = self.cache_dir / self.fonte

        # Datasets consolidados (não baseados em ano): cobertura móvel (geral, 4G, 5G)
        tipos_consolidados = ['cobertura-movel', 'cobertura-movel-5g-uf', 'cobertura-movel-4g-uf']

        if tipo in tipos_consolidados:
            # Estrutura: cache/anatel/{tipo}/{tipo}.parquet
            tipo_dir = fonte_dir / tipo
            tipo_dir.mkdir(parents=True, exist_ok=True)
            parquet_path = tipo_dir / f"{tipo}.parquet"

            # Se existe cache e não forçou download, carrega direto
            if parquet_path.exists() and not force_download:
                try:
                    df = pd.read_parquet(str(parquet_path))
                    return df, None
                except Exception as e:
                    st.error(f"❌ Erro ao carregar parquet: {str(e)}")
                    return None, None

            # Busca URL no consolidado
            url = None
            if 'consolidado' in self.urls and tipo in self.urls['consolidado']:
                url = self.urls['consolidado'][tipo]

            if not url:
                st.error(f"❌ URL não encontrada para {tipo}")
                return None, None

            # Baixa e converte (todos são Excel)
            if url.lower().endswith('.xlsx') or url.lower().endswith('.xls'):
                if not self._download_and_convert_xlsx_to_parquet(url, tipo):
                    return None, None
            else:
                st.error(f"❌ Formato não suportado: {url}")
                return None, None

            # Carrega o parquet gerado
            if parquet_path.exists():
                try:
                    df = pd.read_parquet(str(parquet_path))
                    return df, None
                except Exception as e:
                    st.error(f"❌ Erro ao carregar parquet: {str(e)}")
                    return None, None
            else:
                st.error(f"❌ Falha ao criar parquet para {tipo}")
                return None, None

        # Datasets baseados em ano: conectividade-escola, etc
        # Estrutura: cache/anatel/{ano}/{tipo}.parquet
        ano_dir = fonte_dir / str(ano)
        ano_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = ano_dir / f"{tipo}.parquet"

        # Se existe cache e não forçou download, carrega direto
        if parquet_path.exists() and not force_download:
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                st.error(f"❌ Erro ao carregar parquet: {str(e)}")
                return None, None

        # Busca URL (ano específico ou consolidado)
        url = None
        if ano in self.urls and tipo in self.urls[ano]:
            url = self.urls[ano][tipo]
        elif 'consolidado' in self.urls and tipo in self.urls['consolidado']:
            url = self.urls['consolidado'][tipo]

        if not url:
            st.error(f"❌ URL não encontrada para {tipo} (ano {ano})")
            return None, None

        # Baixa e processa o ZIP (cria parquets para todos os anos)
        if not self._download_and_extract_zip(url, tipo):
            return None, None

        # Carrega o ano solicitado
        if parquet_path.exists():
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                st.error(f"❌ Erro ao carregar parquet: {str(e)}")
                return None, None
        else:
            st.error(f"❌ Dados de {ano} não encontrados no ZIP")
            return None, None

    # =============================================================================
    # MÉTODOS ESPECÍFICOS DO CETIC
    # =============================================================================

    def _sav_to_parquet(self, sav_path: Path, parquet_path: Path) -> bool:
        """
        Converte um arquivo SPSS (.sav) para Parquet aplicando limpeza e
        otimização de colunas. Não remove o .sav de origem.

        Args:
            sav_path: arquivo .sav de origem
            parquet_path: destino .parquet

        Returns:
            True em caso de sucesso.
        """
        try:
            df, _meta = pyreadstat.read_sav(str(sav_path))
            if df is None or df.empty:
                st.error(f"❌ Arquivo SAV está vazio: {sav_path.name}")
                return False

            df = self._limpar_colunas(df)
            df = self._preparar_dataframe(df, aplicar_categorizacao=True)

            parquet_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(parquet_path, compression='snappy', engine='pyarrow')
            return True
        except Exception as e:
            st.error(f"❌ Erro ao converter SAV para Parquet ({sav_path.name}): {str(e)}")
            return False

    def _download_and_convert_sav_to_parquet(self, url: str, ano: any, tipo: str) -> bool:
        """
        Baixa um arquivo SPSS (.sav) do CETIC e converte para Parquet.
        Guarda o arquivo em cache/cetic/{ano}/{tipo}.parquet e remove o .sav temporário.

        Returns:
            True se sucesso, False caso contrário
        """
        destino_dir = self.cache_dir / self.fonte / str(ano)
        destino_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = destino_dir / f"{tipo}.parquet"

        temp_dir = self.cache_dir / self.fonte / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_sav = temp_dir / f'{tipo}.sav'

        try:
            if not self._download_file(url, temp_sav):
                return False
            return self._sav_to_parquet(temp_sav, parquet_path)
        finally:
            if temp_dir.exists():
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except Exception:
                    pass

    def _carregar_cetic(self, ano: any, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados do CETIC usando cache Parquet.

        Estratégia:
          1. Se existir cache/cetic/{ano}/{tipo}.parquet → lê direto.
          2. Se existir legado cache/cetic/{ano}/{tipo}.sav → converte para
             Parquet uma vez e remove o .sav.
          3. Caso contrário, baixa o .sav da URL e converte para Parquet.

        Retorna (DataFrame, None) — os metadados SPSS não são preservados
        pois os módulos `metadados*.py` estáticos já fornecem os labels.
        """
        ano_dir = self.cache_dir / self.fonte / str(ano)
        ano_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = ano_dir / f"{tipo}.parquet"
        legacy_sav = ano_dir / f"{tipo}.sav"

        # 1) Cache parquet disponível
        if parquet_path.exists() and not force_download:
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                st.error(f"❌ Erro ao ler parquet CETIC ({parquet_path.name}): {str(e)}")
                return None, None

        # 2) Migração automática de .sav legado → parquet
        if legacy_sav.exists() and not force_download:
            if self._sav_to_parquet(legacy_sav, parquet_path):
                try:
                    legacy_sav.unlink()
                except Exception:
                    pass
                try:
                    df = pd.read_parquet(str(parquet_path))
                    return df, None
                except Exception as e:
                    st.error(f"❌ Erro ao ler parquet recém-convertido: {str(e)}")
                    return None, None

        # 3) Download + conversão
        try:
            url = self.urls[ano][tipo]
        except KeyError:
            st.error(f"❌ URL não encontrada para CETIC/{tipo} ({ano})")
            return None, None

        if not self._download_and_convert_sav_to_parquet(url, ano, tipo):
            return None, None

        try:
            df = pd.read_parquet(str(parquet_path))
            return df, None
        except Exception as e:
            st.error(f"❌ Erro ao ler parquet CETIC após download: {str(e)}")
            return None, None

    # =============================================================================
    # MÉTODOS ESPECÍFICOS DO INEP
    # =============================================================================

    def _download_and_convert_csv_to_parquet(self, url: str, ano: any, tipo: str = 'educacao-basica') -> bool:
        """
        Baixa um arquivo CSV do INEP e converte para Parquet
        Guarda o arquivo na pasta cache/inep/{ano}/

        Args:
            url: URL do arquivo CSV
            ano: Ano dos dados
            tipo: Tipo dos dados (default: 'educacao-basica')

        Returns:
            True se sucesso, False caso contrário
        """
        # Cria diretório de destino para o ano
        destino_dir = self.cache_dir / self.fonte / str(ano)
        destino_dir.mkdir(parents=True, exist_ok=True)

        # Cria diretório temporário para download
        temp_dir = self.cache_dir / self.fonte / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_csv = temp_dir / f'{tipo}.csv'

        try:
            if not self._download_file(url, temp_csv):
                return False

            # Lê o arquivo CSV com tratamento de encoding
            try:
                df = pd.read_csv(temp_csv, sep=';', encoding='utf-8-sig',
                               low_memory=False, na_values=['', ' ', '  '],
                               keep_default_na=True, decimal=',')
            except Exception:
                # Tenta com encoding latin-1 se UTF-8 falhar
                df = pd.read_csv(temp_csv, sep=';', encoding='latin-1',
                               low_memory=False, na_values=['', ' ', '  '],
                               keep_default_na=True, decimal=',')

            if df is None or df.empty:
                st.error(f"❌ Arquivo CSV está vazio")
                return False

            # Limpa e otimiza o DataFrame
            df = self._limpar_colunas(df)
            df = self._preparar_dataframe(df, aplicar_categorizacao=True)

            # Salva como parquet
            destino_parquet = destino_dir / f'{tipo}.parquet'
            df.to_parquet(destino_parquet, compression='snappy', engine='pyarrow')

            return True

        except Exception as e:
            st.error(f"❌ Erro ao baixar/converter CSV do INEP: {str(e)}")
            import traceback
            st.error(f"Detalhes: {traceback.format_exc()}")
            return False
        finally:
            # Limpa o diretório temporário
            if temp_dir.exists():
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass

    def _carregar_inep(self, ano: any, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados do INEP (Censo Escolar)
        Baixa arquivos CSV e converte para Parquet

        Args:
            ano: Ano dos dados (2022, 2023, 2024)
            tipo: Tipo dos dados (ex: 'educacao-basica')
            force_download: Forçar download mesmo se existir cache

        Returns:
            Tupla (DataFrame, None) ou None se erro
        """
        # Estrutura: cache/inep/{ano}/{tipo}.parquet
        ano_dir = self.cache_dir / self.fonte / str(ano)
        ano_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = ano_dir / f"{tipo}.parquet"

        # Se existe cache e não forçou download, carrega direto
        if parquet_path.exists() and not force_download:
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                st.error(f"❌ Erro ao carregar parquet: {str(e)}")
                return None, None

        # Busca URL
        url = None
        if ano in self.urls and tipo in self.urls[ano]:
            url = self.urls[ano][tipo]

        if not url:
            st.error(f"❌ URL não encontrada para {tipo} (ano {ano})")
            return None, None

        # Baixa e converte CSV para Parquet
        if not self._download_and_convert_csv_to_parquet(url, ano, tipo):
            return None, None

        # Carrega o parquet gerado
        if parquet_path.exists():
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                st.error(f"❌ Erro ao carregar parquet: {str(e)}")
                return None, None
        else:
            st.error(f"❌ Falha ao criar parquet para {tipo}")
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
                for arquivo in ano_dir.iterdir():
                    if arquivo.is_file():
                        arquivo.unlink()
        else:
            # Limpa todo o cache da fonte
            if fonte_dir.exists():
                for arquivo in fonte_dir.rglob("*"):
                    if arquivo.is_file():
                        arquivo.unlink()

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

