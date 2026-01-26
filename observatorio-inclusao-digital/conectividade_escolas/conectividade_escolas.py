import pandas as pd
import os
from pathlib import Path


class AnalisadorConectividadeEscolas:
    """
    Classe para analisar dados de conectividade nas escolas.
    Otimizada para usar Parquet quando disponível.
    """
    
    def __init__(self, data_path=None, caminho_dados=None):
        """
        Inicializa o analisador com dados de conectividade nas escolas.
        
        Args:
            data_path: Caminho para o arquivo CSV/Parquet ou pasta com dados
            caminho_dados: Alias para data_path (para compatibilidade)
        """
        self.df = pd.DataFrame()
        
        # Permitir ambos os nomes de parâmetro
        caminho = data_path or caminho_dados
        
        if caminho is None:
            caminho = Path(__file__).parent
        
        self.caminho_dados = Path(caminho)
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega arquivos de conectividade (prefere Parquet, fallback para CSV)."""
        if not self.caminho_dados.exists():
            print(f"Caminho {self.caminho_dados} não encontrado")
            return
        
        # Se for um arquivo individual
        if self.caminho_dados.is_file():
            if self.caminho_dados.suffix == '.parquet':
                self._carregar_parquet_arquivo(self.caminho_dados)
            elif self.caminho_dados.suffix == '.csv':
                self._carregar_csv_arquivo(self.caminho_dados)
            return
        
        # Se for uma pasta, tentar carregar Parquets primeiro
        if self.caminho_dados.is_dir():
            pasta_parquet = self.caminho_dados / "parquet"
            
            # Preferir Parquet se existir
            if pasta_parquet.exists():
                self._carregar_multiplos_parquets(pasta_parquet)
            else:
                # Fallback para CSV
                self._carregar_multiplos_csvs(self.caminho_dados)
    
    def _carregar_parquet_arquivo(self, caminho):
        """Carrega um arquivo Parquet individual."""
        try:
            self.df = pd.read_parquet(caminho)
            print("[OK] Carregado (Parquet): {} ({} linhas)".format(caminho.name, len(self.df)))
        except Exception as e:
            print("[ERRO] Erro ao carregar {}: {}".format(caminho.name, e))
    
    def _carregar_csv_arquivo(self, caminho):
        """Carrega um arquivo CSV individual."""
        try:
            self.df = pd.read_csv(caminho, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
            print("[OK] Carregado (CSV): {} ({} linhas)".format(caminho.name, len(self.df)))
        except Exception as e:
            print("[ERRO] Erro ao carregar {}: {}".format(caminho.name, e))
    
    def _carregar_multiplos_parquets(self, pasta_parquet):
        """Carrega todos os Parquets de uma pasta (ultimos 10 periodos: 2023-2025)."""
        arquivos_parquet = sorted(pasta_parquet.glob("Conectividade_Escolas_*.parquet"))
        
        if not arquivos_parquet:
            print("[ERRO] Nenhum arquivo Parquet encontrado em {}".format(pasta_parquet))
            # Tentar fallback para CSV
            pasta_pai = pasta_parquet.parent
            if pasta_pai.exists():
                self._carregar_multiplos_csvs(pasta_pai)
            return
        
        # Carregar apenas os ultimos 5 periodos que têm todas as colunas necessárias (2024-2025)
        dfs = []
        tamanho_total = 0
        
        print("[INFO] Carregando periodos com dados completos (2024-2025)...")
        for arquivo in arquivos_parquet[-5:]:  # Últimos 5 têm os dados corretos
            try:
                df = pd.read_parquet(arquivo)
                
                # Extrair data do nome do arquivo (formato: Conectividade_Escolas_YYYY-MM.parquet)
                try:
                    data_str = arquivo.stem.split('_')[-1]  # Pega "2025-09" de "Conectividade_Escolas_2025-09"
                    if 'Data' not in df.columns:
                        df['Data'] = data_str
                except:
                    pass
                
                dfs.append(df)
                tamanho_total += len(df)
                print("[OK] Carregado (Parquet): {} ({:,} linhas)".format(arquivo.name, len(df)))
            except Exception as e:
                print("[ERRO] Erro ao carregar {}: {}".format(arquivo.name, e))
        
        if dfs:
            print("[INFO] Concatenando dados...")
            self.df = pd.concat(dfs, ignore_index=True)
            print("[OK] Total consolidado: {:,} linhas".format(len(self.df)))
    
    def _carregar_multiplos_csvs(self, pasta_csv):
        """Carrega todos os CSVs de uma pasta (ultimos 5 periodos)."""
        arquivos_csv = sorted(pasta_csv.glob("Conectividade_Escolas_*.csv"))
        
        if not arquivos_csv:
            print("[ERRO] Nenhum arquivo CSV encontrado em {}".format(pasta_csv))
            return
        
        dfs = []
        tamanho_total = 0
        
        print("[INFO] Carregando ultimos 10 periodos (2023-2025)...")
        for arquivo in arquivos_csv[-10:]:
            try:
                df = pd.read_csv(arquivo, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
                
                # Extrair data do nome do arquivo
                try:
                    data_str = arquivo.stem.split('_')[-1]
                    if 'Data' not in df.columns:
                        df['Data'] = data_str
                except:
                    pass
                
                # Preencher colunas que faltam
                colunas_esperadas = ['Data', 'SG_UF', 'NO_REGIAO', 'CONECT_POSSUI_INTERNET']
                for col in colunas_esperadas:
                    if col not in df.columns:
                        df[col] = None
                
                dfs.append(df)
                tamanho_total += len(df)
                print("[OK] Carregado (CSV): {} ({:,} linhas)".format(arquivo.name, len(df)))
            except Exception as e:
                print("[ERRO] Erro ao carregar {}: {}".format(arquivo.name, e))
        
        if dfs:
            print("[INFO] Concatenando dados...")
            self.df = pd.concat(dfs, ignore_index=True)
            print("[OK] Total consolidado: {:,} linhas".format(len(self.df)))
    
    def filtrar_dados(self, **kwargs):
        """
        Filtra dados com base em critérios fornecidos.
        
        Args:
            **kwargs: Dicionário com nomes de colunas e valores para filtrar
            
        Returns:
            DataFrame filtrado (cópia rasa, não copy() completo)
        """
        if self.df.empty:
            return pd.DataFrame()
        
        resultado = self.df
        
        for coluna, valor in kwargs.items():
            if coluna in resultado.columns:
                if isinstance(valor, list):
                    resultado = resultado[resultado[coluna].isin(valor)]
                else:
                    resultado = resultado[resultado[coluna] == valor]
        
        return resultado
