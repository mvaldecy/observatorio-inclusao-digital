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
import unicodedata
from .data_sources import get_fonte_urls, get_fonte_info, list_fontes


def _log_error(mensagem: str):
    """
    Exibe erro usando streamlit se disponível, caso contrário usa print
    """
    try:
        if hasattr(st, 'error'):
            _log_error(mensagem)
        else:
            print(mensagem)
    except:
        print(mensagem)


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
            _log_error(f"❌ Erro no download: {str(e)}")
            if destino.exists():
                destino.unlink()
            return False
        except Exception as e:
            _log_error(f"❌ Erro inesperado: {str(e)}")
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
                _log_error(f"❌ Arquivo Excel está vazio")
                return False

            # Limpa e otimiza o DataFrame
            df = self._limpar_colunas(df)
            df = self._preparar_dataframe(df, aplicar_categorizacao=True)

            # Salva como parquet
            destino_parquet = destino_dir / f'{tipo}.parquet'
            df.to_parquet(destino_parquet, compression='snappy', engine='pyarrow')

            return True

        except Exception as e:
            _log_error(f"❌ Erro ao baixar/converter cobertura móvel: {str(e)}")
            import traceback
            _log_error(f"Detalhes: {traceback.format_exc()}")
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
                _log_error("❌ Nenhum arquivo com sufixo -09 (setembro) encontrado")
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
                    _log_error(f"❌ Erro ao processar ano {ano}: {str(e)}")
                    sucesso_total = False

            return sucesso_total

        except Exception as e:
            _log_error(f"❌ Erro no processamento: {str(e)}")
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
                        _log_error(f"❌ Nenhum CSV encontrado dentro do arquivo ZIP")
                        return False

                    z.extractall(temp_dir)
                    csv_paths = [temp_dir / f for f in csv_files]

                # Processa apenas CSVs de setembro (-09)
                sucesso_processamento = self._processar_csvs_setembro(csv_paths, tipo)
                return sucesso_processamento

        except Exception as e:
            _log_error(f"❌ Erro ao extrair ZIP: {str(e)}")
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
                    _log_error(f"❌ Erro ao carregar parquet: {str(e)}")
                    return None, None

            # Busca URL no consolidado
            url = None
            if 'consolidado' in self.urls and tipo in self.urls['consolidado']:
                url = self.urls['consolidado'][tipo]

            if not url:
                _log_error(f"❌ URL não encontrada para {tipo}")
                return None, None

            # Baixa e converte (todos são Excel)
            if url.lower().endswith('.xlsx') or url.lower().endswith('.xls'):
                if not self._download_and_convert_xlsx_to_parquet(url, tipo):
                    return None, None
            else:
                _log_error(f"❌ Formato não suportado: {url}")
                return None, None

            # Carrega o parquet gerado
            if parquet_path.exists():
                try:
                    df = pd.read_parquet(str(parquet_path))
                    return df, None
                except Exception as e:
                    _log_error(f"❌ Erro ao carregar parquet: {str(e)}")
                    return None, None
            else:
                _log_error(f"❌ Falha ao criar parquet para {tipo}")
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
                _log_error(f"❌ Erro ao carregar parquet: {str(e)}")
                return None, None

        # Busca URL (ano específico ou consolidado)
        url = None
        if ano in self.urls and tipo in self.urls[ano]:
            url = self.urls[ano][tipo]
        elif 'consolidado' in self.urls and tipo in self.urls['consolidado']:
            url = self.urls['consolidado'][tipo]

        if not url:
            _log_error(f"❌ URL não encontrada para {tipo} (ano {ano})")
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
                _log_error(f"❌ Erro ao carregar parquet: {str(e)}")
                return None, None
        else:
            _log_error(f"❌ Dados de {ano} não encontrados no ZIP")
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
            _log_error(f"❌ Erro ao processar arquivo SAV {cache_path.name}: {str(e)}")
            return None, None

    # =============================================================================
    # MÉTODOS ESPECÍFICOS DO IBGE
    # =============================================================================

    def _carregar_ibge(self, ano: any, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados do IBGE (arquivos CSV)

        Args:
            ano: Ano dos dados ou 'consolidado'
            tipo: Tipo dos dados (ex: 'tabela-7336')
            force_download: Forçar download mesmo se existir cache

        Returns:
            Tupla (DataFrame, None) ou None se erro
        """
        fonte_dir = self.cache_dir / self.fonte

        # Para IBGE, dados consolidados são armazenados em cache/ibge/consolidado/
        if ano == 'consolidado':
            tipo_dir = fonte_dir / 'consolidado'
            tipo_dir.mkdir(parents=True, exist_ok=True)
            parquet_path = tipo_dir / f"{tipo}.parquet"
        else:
            ano_dir = fonte_dir / str(ano)
            ano_dir.mkdir(parents=True, exist_ok=True)
            parquet_path = ano_dir / f"{tipo}.parquet"

        # Se existe parquet processado, carrega dele (mais rápido e limpo)
        if parquet_path.exists() and not force_download:
            try:
                df = pd.read_parquet(str(parquet_path))
                return df, None
            except Exception as e:
                _log_error(f"❌ Erro ao carregar Parquet: {str(e)}")
                return None, None

        # Busca URL
        url = None
        if ano in self.urls and tipo in self.urls[ano]:
            url = self.urls[ano][tipo]
        elif 'consolidado' in self.urls and tipo in self.urls['consolidado']:
            url = self.urls['consolidado'][tipo]

        if not url:
            _log_error(f"❌ URL não encontrada para IBGE/{tipo}")
            return None, None

        # Baixa o arquivo CSV em memória (não salva em disco ainda)
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            csv_content = response.text
        except Exception as e:
            _log_error(f"❌ Erro ao baixar arquivo: {str(e)}")
            return None, None

        # Carrega o CSV em memória com parâmetros específicos do IBGE
        # Os CSVs do IBGE têm headers complexos, por isso precisam de tratamento especial
        try:
            from io import StringIO
            
            df = pd.read_csv(
                StringIO(csv_content),
                sep=';',
                encoding='utf-8',
                skiprows=5  # Pula linhas de header complexas
            )
            
            # Normaliza nomes de colunas
            df.columns = [str(col).strip() for col in df.columns]
            
            # Salva APENAS em Parquet (nunca salva CSV bruto que vai dar erro)
            df.to_parquet(str(parquet_path), index=False)
            
            return df, None
        except Exception as e:
            _log_error(f"❌ Erro ao processar dados IBGE: {str(e)}")
            return None, None

    # =============================================================================
    # MÉTODOS ESPECÍFICOS DO PCD
    # =============================================================================

    def _carregar_pcd(self, ano: any, tipo: str, force_download: bool = False) -> Optional[Tuple[pd.DataFrame, any]]:
        """
        Carrega dados PCD (arquivos XLSX do GitHub Releases)
        Arquivo tem 2 abas:
        - Planilha1: dados populacionais por município  
        - Planilha25: dados de alfabetização e raça/cor por município

        Args:
            ano: Ano dos dados
            tipo: Tipo dos dados (ex: 'dados-pcd')
            force_download: Forçar download mesmo se existir cache

        Returns:
            Tupla (DataFrame, None) ou None se erro
        """
        fonte_dir = self.cache_dir / self.fonte
        ano_dir = fonte_dir / str(ano)
        ano_dir.mkdir(parents=True, exist_ok=True)
        
        parquet_path = ano_dir / f"{tipo}.parquet"

        def _normalizar_municipio(valor):
            if pd.isna(valor):
                return None
            texto = str(valor).strip()
            if not texto or texto == '-':
                return None
            texto = texto.replace('(PI)', '').replace('(Pi)', '').replace('(pi)', '')
            return texto.strip().upper()

        def _to_numeric(serie):
            if serie is None:
                return None
            s = serie.astype(str).str.strip()
            s = s.replace({'-': None, 'nan': None, 'None': None, '': None})
            s = s.str.replace('.', '', regex=False)
            s = s.str.replace(',', '.', regex=False)
            return pd.to_numeric(s, errors='coerce')

        def _normalizar_texto(valor: str) -> str:
            txt = str(valor).strip().lower()
            txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode('ascii')
            txt = ' '.join(txt.split())
            return txt

        def _extrair_tabela_por_municipio(sheet_name: str, mapeamento: dict):
            try:
                df_sheet = pd.read_excel(temp_xlsx, sheet_name=sheet_name, engine='openpyxl')
            except Exception:
                return None

            candidatos_municipio = [
                'Unnamed: 1',
                'MUNICÍPIOS',
                'Município.1',
                'Município',
                'Unnamed: 6'
            ]
            col_municipio = None
            melhor_qtd = -1
            for candidato in candidatos_municipio:
                if candidato in df_sheet.columns:
                    qtd = df_sheet[candidato].notna().sum()
                    if qtd > melhor_qtd:
                        melhor_qtd = qtd
                        col_municipio = candidato

            if col_municipio is None:
                return None

            df_out = pd.DataFrame()
            df_out['municipio_join'] = df_sheet[col_municipio].apply(_normalizar_municipio)

            colunas_metricas = []
            colunas_sheet = list(df_sheet.columns)
            colunas_normalizadas = {_normalizar_texto(c): c for c in colunas_sheet}
            for origem, destino in mapeamento.items():
                col_origem = None

                if origem in df_sheet.columns:
                    col_origem = origem
                else:
                    origem_norm = _normalizar_texto(origem)
                    if origem_norm in colunas_normalizadas:
                        col_origem = colunas_normalizadas[origem_norm]
                    else:
                        for c in colunas_sheet:
                            if origem_norm in _normalizar_texto(c):
                                col_origem = c
                                break

                if col_origem is not None:
                    df_out[destino] = _to_numeric(df_sheet[col_origem])
                    colunas_metricas.append(destino)

            if not colunas_metricas:
                return None

            df_out = df_out.dropna(subset=['municipio_join'])
            df_out = df_out[df_out[colunas_metricas].notna().any(axis=1)]
            if df_out.empty:
                return None

            df_out = df_out.groupby('municipio_join', as_index=False).first()
            return df_out

        def _extrair_idade_planilha31():
            try:
                df_sheet = pd.read_excel(temp_xlsx, sheet_name='Planilha31', engine='openpyxl')
            except Exception:
                return None

            if 'Unnamed: 1' not in df_sheet.columns:
                return None

            colunas_valor = ['Grupo de idade'] + [
                c for c in df_sheet.columns
                if str(c).startswith('Unnamed:') and c not in ['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']
            ]

            if not colunas_valor:
                return None

            rotulos = df_sheet.iloc[0][colunas_valor].tolist()

            mapa_idades = {
                'total': 'pcd_idade_total',
                '2 a 4 anos': 'pcd_idade_2_4',
                '5 a 9 anos': 'pcd_idade_5_9',
                '10 a 14 anos': 'pcd_idade_10_14',
                '15 a 19 anos': 'pcd_idade_15_19',
                '20 a 24 anos': 'pcd_idade_20_24',
                '25 a 29 anos': 'pcd_idade_25_29',
                '30 a 34 anos': 'pcd_idade_30_34',
                '35 a 39 anos': 'pcd_idade_35_39',
                '40 a 44 anos': 'pcd_idade_40_44',
                '45 a 49 anos': 'pcd_idade_45_49',
                '50 a 54 anos': 'pcd_idade_50_54',
                '55 a 59 anos': 'pcd_idade_55_59',
                '60 a 64 anos': 'pcd_idade_60_64',
                '65 a 69 anos': 'pcd_idade_65_69',
                '70 a 74 anos': 'pcd_idade_70_74',
                '75 a 79 anos': 'pcd_idade_75_79',
                '80 a 84 anos': 'pcd_idade_80_84',
                '85 a 89 anos': 'pcd_idade_85_89',
                '90 a 94 anos': 'pcd_idade_90_94',
                '95 a 99 anos': 'pcd_idade_95_99',
                '100 anos ou mais': 'pcd_idade_100_mais'
            }
            mapa_idades_norm = {_normalizar_texto(k): v for k, v in mapa_idades.items()}

            registros = []
            for i in range(0, len(df_sheet) - 1):
                municipio = _normalizar_municipio(df_sheet.iloc[i].get('Unnamed: 1'))
                if not municipio:
                    continue

                linha_valores = df_sheet.iloc[i + 1]
                registro = {'municipio_join': municipio}
                tem_valor = False

                for coluna, rotulo in zip(colunas_valor, rotulos):
                    destino = mapa_idades_norm.get(_normalizar_texto(rotulo))
                    if not destino:
                        continue
                    valor = _to_numeric(pd.Series([linha_valores.get(coluna)])).iloc[0]
                    registro[destino] = valor
                    if pd.notna(valor):
                        tem_valor = True

                if tem_valor:
                    registros.append(registro)

            if not registros:
                return None

            df_out = pd.DataFrame(registros)
            return df_out.groupby('municipio_join', as_index=False).first()

        def _carregar_tabela10126_brasil_nordeste() -> Optional[pd.DataFrame]:
            """Fallback para arquivo agregado Brasil/Nordeste (tabela10126.xlsx)."""
            try:
                df_t1 = pd.read_excel(temp_xlsx, sheet_name='Tabela 1', engine='openpyxl', header=None)
                df_t2 = pd.read_excel(temp_xlsx, sheet_name='Tabela 2', engine='openpyxl', header=None)
            except Exception:
                return None

            if len(df_t1) < 7 or len(df_t2) < 7:
                return None

            try:
                registros = []
                for linha in [5, 6]:
                    regiao = df_t1.iloc[linha, 0]
                    total = pd.to_numeric(pd.Series([df_t1.iloc[linha, 1]]), errors='coerce').iloc[0]
                    com_def = pd.to_numeric(pd.Series([df_t2.iloc[linha, 1]]), errors='coerce').iloc[0]

                    if pd.isna(regiao) or pd.isna(total) or pd.isna(com_def):
                        continue

                    regiao_txt = str(regiao).strip()
                    registros.append({
                        'municipio': regiao_txt,
                        'municipio_join': regiao_txt.upper(),
                        'regiao': regiao_txt,
                        'uf': 'BR' if regiao_txt.lower() == 'brasil' else None,
                        'estado': None,
                        'total_pessoas_2_mais': float(total),
                        'pessoas_com_deficiencia_2_mais': float(com_def),
                        'pessoas_sem_deficiencia_2_mais': float(total - com_def),
                        'ano': ano,
                    })

                if not registros:
                    return None

                df_out = pd.DataFrame(registros)
                df_out['perc_pessoas_com_deficiencia_2_mais'] = (
                    df_out['pessoas_com_deficiencia_2_mais'] / df_out['total_pessoas_2_mais'] * 100
                )
                df_out['perc_pessoas_sem_deficiencia_2_mais'] = (
                    df_out['pessoas_sem_deficiencia_2_mais'] / df_out['total_pessoas_2_mais'] * 100
                )
                return df_out
            except Exception:
                return None

        # Se existe parquet processado, carrega dele (mais rápido)
        if parquet_path.exists() and not force_download:
            try:
                df = pd.read_parquet(str(parquet_path))
                colunas_df = set(df.columns)

                if tipo == 'dados-pcd':
                    colunas_municipais = {
                        'TOTAL_PESSOAS_2_MAIS',
                        'PESSOAS_COM_DEFICIENCIA_2_MAIS',
                        'POPULACAO_RESIDENTE_DIAGNOSTICADA_COM_AUTISMO',
                        'PCD_IDADE_2_4'
                    }
                    if colunas_municipais.issubset(colunas_df):
                        qtd_municipios = 0
                        if 'MUNICIPIO' in df.columns:
                            qtd_municipios = int(df['MUNICIPIO'].nunique())
                        elif 'municipio' in df.columns:
                            qtd_municipios = int(df['municipio'].nunique())

                        if qtd_municipios >= 50:
                            return df, None

                elif tipo == 'dados-pcd-br-ne':
                    colunas_agregadas = {
                        'TOTAL_PESSOAS_2_MAIS',
                        'PESSOAS_COM_DEFICIENCIA_2_MAIS'
                    }
                    if colunas_agregadas.issubset(colunas_df):
                        return df, None
            except Exception as e:
                _log_error(f"❌ Erro ao carregar Parquet: {str(e)}")
                return None, None

        # Busca URL
        url = None
        if ano in self.urls and tipo in self.urls[ano]:
            url = self.urls[ano][tipo]
        
        if not url:
            _log_error(f"❌ URL não encontrada para PCD/{ano}/{tipo}")
            return None, None

        # Baixa arquivo XLSX
        temp_dir = fonte_dir / 'temp'
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_xlsx = temp_dir / f'{tipo}.xlsx'

        try:
            # Download
            if not self._download_file(url, temp_xlsx):
                return None, None

            # Lê as abas relevantes do arquivo (layout legado)
            # População_2022: dados populacionais 2022
            df_pop2022 = pd.read_excel(temp_xlsx, sheet_name='População_2022', engine='openpyxl')
            
            # População_2010: dados populacionais 2010  
            df_pop2010 = pd.read_excel(temp_xlsx, sheet_name='População_2010', engine='openpyxl')
            
            # Planilha25: alfabetização por raça/cor
            df_alfa = pd.read_excel(temp_xlsx, sheet_name='Planilha25', engine='openpyxl')
            
            # Merge dos dados de população
            df = pd.merge(
                df_pop2022,
                df_pop2010,
                on='Município',
                how='inner',
                suffixes=('_2022', '_2010')
            )
            
            # Renomeia colunas de população
            df.columns = ['municipio', 'populacao_2022', 'populacao_2010']
            
            # Calcula variação populacional
            df['variacao_populacao'] = df['populacao_2022'] - df['populacao_2010']
            
            # Merge com dados de alfabetização (Planilha25)
            # Primeiro renomeia a coluna Município para fazer match
            df_alfa = df_alfa.rename(columns={'Município': 'municipio'})
            
            # Remove a segunda coluna (Unnamed: 1) se existir
            if 'Unnamed: 1' in df_alfa.columns:
                df_alfa = df_alfa.drop(columns=['Unnamed: 1'])
            
            # Merge
            df = pd.merge(
                df,
                df_alfa,
                on='municipio',
                how='left'
            )
            
            # Renomeia colunas de alfabetização
            rename_map = {
                'Branca': 'pop_branca',
                'Preta': 'pop_preta',
                'Amarela': 'pop_amarela',
                'Parda': 'pop_parda',
                'Indígena': 'pop_indigena',
                'alafabetização': 'taxa_alfabetizacao_geral',
                'Taxa de alfabetização das pessoas indígenas': 'taxa_alfa_indigena',
                'Branca.1': 'taxa_alfa_branca',
                'Preta.1': 'taxa_alfa_preta',
                'Amarela.1': 'taxa_alfa_amarela',
                'Parda.1': 'taxa_alfa_parda'
            }
            
            # Renomeia apenas colunas que existem
            for old_name, new_name in rename_map.items():
                if old_name in df.columns:
                    df = df.rename(columns={old_name: new_name})
            
            # Adiciona informações geográficas
            df['uf'] = 'PI'
            df['estado'] = 'Piauí'
            df['regiao'] = 'Nordeste'
            df['ano'] = ano
            
            # Calcula população total por raça/cor
            df['populacao_total'] = (
                pd.to_numeric(df.get('pop_branca', 0), errors='coerce').fillna(0) + 
                pd.to_numeric(df.get('pop_preta', 0), errors='coerce').fillna(0) + 
                pd.to_numeric(df.get('pop_amarela', 0), errors='coerce').fillna(0) + 
                pd.to_numeric(df.get('pop_parda', 0), errors='coerce').fillna(0) + 
                pd.to_numeric(df.get('pop_indigena', 0), errors='coerce').fillna(0)
            )
            
            # Calcula percentuais por raça/cor
            for raca in ['branca', 'preta', 'amarela', 'parda', 'indigena']:
                col_pop = f'pop_{raca}'
                col_perc = f'perc_{raca}'
                if col_pop in df.columns:
                    df[col_perc] = (pd.to_numeric(df[col_pop], errors='coerce') / df['populacao_total'] * 100).round(2)

            # Chave de merge por município (normalizada)
            df['municipio_join'] = df['municipio'].apply(_normalizar_municipio)

            # =============================================================
            # Planilhas complementares (Deficiência e Autismo - 2022)
            # =============================================================

            mapas_planilhas = [
                (
                    'Planilha53',
                    {
                        'Total': 'total_pessoas_2_mais',
                        'Pessoa com deficiência': 'pessoas_com_deficiencia_2_mais',
                        'Pessoa sem deficiência': 'pessoas_sem_deficiencia_2_mais'
                    }
                ),
                (
                    'deficiência por  grupos de idad',
                    {}
                ),
                (
                    'Planilha33',
                    {
                        'Total': 'pcd_cor_total',
                        'Branca': 'pcd_cor_branca',
                        'Preta': 'pcd_cor_preta',
                        'Amarela': 'pcd_cor_amarela',
                        'Parda': 'pcd_cor_parda',
                        'Indígena': 'pcd_cor_indigena'
                    }
                ),
                (
                    'Planilha35',
                    {
                        'Total': 'pcd_dificuldades_total',
                        'Dificuldade permanente para enxergar, mesmo usando óculos ou lentes de contato': 'pcd_dificuldade_enxergar',
                        'Dificuldade permanente para ouvir, mesmo usando aparelhos auditivos': 'pcd_dificuldade_ouvir',
                        'Dificuldade permanente para andar ou subir degraus, mesmo usando prótese ou outro aparelho de auxílio': 'pcd_dificuldade_andar',
                        'Dificuldade permanente para pegar pequenos objetos, como botão ou lápis, ou abrir e fechar tampas de garrafas, mesmo usando aparelho de auxílio': 'pcd_dificuldade_pegar_objetos',
                        'Dificuldade permanente para se comunicar, realizar cuidados pessoais, trabalhar ou estudar por causa de alguma limitação nas funções mentais': 'pcd_dificuldade_mental'
                    }
                ),
                (
                    'Planilha37',
                    {
                        'Total': 'pcd_qtd_dificuldades_total',
                        '1 dificuldade': 'pcd_qtd_1_dificuldade',
                        '2 ou mais dificuldades': 'pcd_qtd_2_mais_dificuldades'
                    }
                ),
                (
                    'Planilha39',
                    {
                        'Total': 'taxa_analfabetismo_pcd_total',
                        'Branca': 'taxa_analfabetismo_pcd_branca',
                        'Preta': 'taxa_analfabetismo_pcd_preta',
                        'Amarela': 'taxa_analfabetismo_pcd_amarela',
                        'Parda': 'taxa_analfabetismo_pcd_parda',
                        'Indígena': 'taxa_analfabetismo_pcd_indigena'
                    }
                ),
                (
                    'Planilha41',
                    {
                        'Total': 'pcd_instrucao_25_mais_total',
                        'Sem instrução e fundamental incompleto': 'pcd_instrucao_sem_instr_fund_incomp',
                        'Fundamental completo e médio incompleto': 'pcd_instrucao_fund_comp_medio_incomp',
                        'Médio completo e superior incompleto': 'pcd_instrucao_medio_comp_sup_incomp',
                        'Superior completo': 'pcd_instrucao_superior_comp'
                    }
                ),
                (
                    'Planilha43',
                    {
                        ' População residente': 'populacao_residente_total',
                        'População residente diagnosticada com autismo': 'populacao_residente_diagnosticada_com_autismo',
                        'Percentual da população residente diagnosticada com autismo no total da população residente (%)': 'percentual_autismo_pop_residente'
                    }
                ),
                (
                    'Planilha45',
                    {
                        'Total': 'autismo_cor_total',
                        'Branca': 'autismo_cor_branca',
                        'Preta': 'autismo_cor_preta',
                        'Amarela': 'autismo_cor_amarela',
                        'Parda': 'autismo_cor_parda',
                        'Indígena': 'autismo_cor_indigena'
                    }
                ),
                (
                    'Planilha47',
                    {
                        'Total': 'autismo_homens_mulheres_total',
                        'Homens': 'autismo_homens',
                        'Mulheres': 'autismo_mulheres'
                    }
                ),
                (
                    'Planilha49',
                    {
                        'Total': 'autismo_25_mais_instrucao_total',
                        'Sem instrução e fundamental incompleto': 'autismo_25_mais_sem_instr_fund_incomp',
                        'Fundamental completo e médio incompleto': 'autismo_25_mais_fund_comp_medio_incomp',
                        'Médio completo e superior incompleto': 'autismo_25_mais_medio_comp_sup_incomp',
                        'Superior completo': 'autismo_25_mais_superior_comp'
                    }
                ),
                (
                    'Planilha51',
                    {
                        'Domicílios particulares permanentes ocupados- Total': 'domicilios_total',
                        'Domicílios particulares permanentes ocupados com pelo menos um morador diagnosticado com autismo (Unidades)': 'domicilios_com_morador_autismo',
                        'Percentual de domicílios particulares permanentes ocupados com pelo menos um morador diagnosticado com autismo no total de domicílios particulares permanentes ocupados (%)': 'percentual_domicilios_com_autismo'
                    }
                )
            ]

            for sheet_name, mapa in mapas_planilhas:
                tabela = _extrair_tabela_por_municipio(sheet_name, mapa)
                if tabela is not None and not tabela.empty:
                    df = df.merge(tabela, on='municipio_join', how='left')

            tabela_idade = _extrair_idade_planilha31()
            if tabela_idade is not None and not tabela_idade.empty:
                df = df.merge(tabela_idade, on='municipio_join', how='left')

            # Percentuais derivados (2 anos ou mais)
            if {'total_pessoas_2_mais', 'pessoas_com_deficiencia_2_mais'}.issubset(df.columns):
                df['perc_pessoas_com_deficiencia_2_mais'] = (
                    df['pessoas_com_deficiencia_2_mais'] / df['total_pessoas_2_mais'] * 100
                )

            if {'total_pessoas_2_mais', 'pessoas_sem_deficiencia_2_mais'}.issubset(df.columns):
                df['perc_pessoas_sem_deficiencia_2_mais'] = (
                    df['pessoas_sem_deficiencia_2_mais'] / df['total_pessoas_2_mais'] * 100
                )

            # Remove coluna auxiliar
            if 'municipio_join' in df.columns:
                df = df.drop(columns=['municipio_join'])
            
            # Remove registros sem dados essenciais
            df = df.dropna(subset=['municipio'])
            
            if df.empty:
                _log_error("Nenhum dado válido encontrado após processamento")
                return None, None

            # Limpa e otimiza o DataFrame
            df = self._limpar_colunas(df)
            df = self._preparar_dataframe(df, aplicar_categorizacao=True)

            # Salva como parquet
            df.to_parquet(parquet_path, compression='snappy', engine='pyarrow')
            
            print(f"Dados PCD processados: {len(df)} municípios do Piauí")

            return df, None

        except Exception as e:
            # Fallback: novo layout agregado (Brasil e Grande Região)
            df_fallback = _carregar_tabela10126_brasil_nordeste()
            if df_fallback is not None and not df_fallback.empty:
                try:
                    df_fallback = self._limpar_colunas(df_fallback)
                    df_fallback = self._preparar_dataframe(df_fallback, aplicar_categorizacao=True)
                    df_fallback.to_parquet(parquet_path, compression='snappy', engine='pyarrow')
                    print(f"Dados PCD processados (agregado Brasil/Nordeste): {len(df_fallback)} registros")
                    return df_fallback, None
                except Exception as e2:
                    print(f"Erro no fallback do PCD agregado: {str(e2)}")

            _log_error(f"Erro ao baixar/processar dados PCD: {str(e)}")
            import traceback
            _log_error(f"Detalhes: {traceback.format_exc()}")
            return None, None
        finally:
            # Limpa o diretório temporário
            if temp_dir.exists():
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass

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
        # Para ANATEL, IBGE e PCD, não valida ano aqui pois usam 'consolidado' nas URLs
        if self.fonte not in ['anatel', 'ibge', 'pcd']:
            if ano not in self.urls:
                _log_error(f"❌ Dados de {ano} ainda não disponíveis para {self.fonte}")
                return None, None

            if tipo not in self.urls[ano]:
                _log_error(f"❌ Tipo '{tipo}' não disponível para {self.fonte}/{ano}")
                return None, None

        # Chama o método específico da fonte
        metodo_nome = f"_carregar_{self.fonte}"
        metodo_loader = getattr(self, metodo_nome, None)

        if metodo_loader:
            return metodo_loader(ano, tipo, force_download)

        _log_error(f"❌ Carregador não implementado para a fonte: {self.fonte}")
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

