import pandas as pd
import os
from pathlib import Path


class AnalisadorAnatel:
    """
    Classe para analisar dados de cobertura móvel da ANATEL.
    Otimizada para usar Parquet quando disponível.
    """
    
    def __init__(self, data_path=None, caminho_dados=None):
        """
        Inicializa o analisador com dados de cobertura.
        
        Args:
            data_path: Caminho para o arquivo CSV/Parquet ou pasta com dados
            caminho_dados: Alias para data_path (para compatibilidade)
        """
        self.df = pd.DataFrame()
        
        # Permitir ambos os nomes de parâmetro
        caminho = data_path or caminho_dados
        
        if caminho is None:
            caminho = Path(__file__).parent / "cobertura_movel"
        
        self.caminho_dados = Path(caminho)
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega arquivos de cobertura (prefere Parquet, fallback para CSV)."""
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
            print("[ERRO] Erro ao carregar Parquet {}: {}".format(caminho.name, e))
    
    def _carregar_csv_arquivo(self, caminho):
        """Carrega um arquivo CSV individual."""
        try:
            self.df = pd.read_csv(
                caminho, 
                encoding='utf-8',
                sep=';',
                on_bad_lines='skip',
                engine='python'
            )
            print("[OK] Carregado (CSV): {} ({} linhas)".format(caminho.name, len(self.df)))
        except Exception as e:
            print("[ERRO] Erro ao carregar {}: {}".format(caminho.name, e))
    
    def _carregar_multiplos_parquets(self, pasta_parquet):
        """Carrega todos os Parquets de uma pasta."""
        # Preferir arquivos de Setores (têm dados de cobertura)
        arquivos_setores = sorted(pasta_parquet.glob("*Setores*.parquet"))
        arquivos_atributos = sorted(pasta_parquet.glob("*Atributos*.parquet"))
        
        # Se não encontrar Setores, carrega tudo
        if not arquivos_setores:
            arquivos_setores = sorted(pasta_parquet.glob("*.parquet"))
        
        if not arquivos_setores:
            print("[ERRO] Nenhum arquivo Parquet encontrado em {}".format(pasta_parquet))
            return
        
        dfs = []
        tamanho_total = 0
        
        # Carregar dados de Setores (ultimos 10 periodos: 2023, 2024, 2025)
        print("[INFO] Carregando ultimos 10 periodos (2023-2025)...")
        for arquivo in arquivos_setores[-10:]:
            try:
                df = pd.read_parquet(arquivo)
                dfs.append(df)
                tamanho_total += len(df)
                print("[OK] Carregado (Parquet): {} ({:,} linhas)".format(arquivo.name, len(df)))
            except Exception as e:
                print("[ERRO] Erro ao carregar {}: {}".format(arquivo.name, e))
        
        # Carregar dados de Atributos para juntar com Setores
        df_atributos = None
        if arquivos_atributos:
            try:
                df_atributos = pd.read_parquet(arquivos_atributos[0])
                print("[OK] Carregado (Atributos): {} ({:,} linhas)".format(arquivos_atributos[0].name, len(df_atributos)))
            except Exception as e:
                print("[ERRO] Erro ao carregar atributos: {}".format(e))
        
        if dfs:
            print("[INFO] Concatenando dados...")
            self.df = pd.concat(dfs, ignore_index=True)
            
            # Juntar com dados de atributos se disponível
            if df_atributos is not None and 'Código Setor Censitário' in self.df.columns and 'Código Setor Censitário' in df_atributos.columns:
                print("[INFO] Juntando dados com Atributos...")
                # Garantir que ambas as colunas têm o mesmo tipo de dados
                self.df['Código Setor Censitário'] = self.df['Código Setor Censitário'].astype(str)
                df_atributos['Código Setor Censitário'] = df_atributos['Código Setor Censitário'].astype(str)
                
                self.df = self.df.merge(
                    df_atributos[['Código Setor Censitário', 'Região', 'UF', 'Município']],
                    on='Código Setor Censitário',
                    how='left'
                )
                print("[OK] Juncao completa!")
            
            print("[OK] Total consolidado: {:,} linhas".format(len(self.df)))
    
    def _carregar_multiplos_csvs(self, pasta_csv):
        """Carrega todos os CSVs de uma pasta (fallback)."""
        # Preferir Setores
        arquivos_setores = sorted(pasta_csv.glob("*Setores.csv"))
        arquivos_atributos = sorted(pasta_csv.glob("Atributos_*.csv"))
        
        if not arquivos_setores:
            arquivos_setores = sorted(pasta_csv.glob("Cobertura_*.csv"))
        
        if not arquivos_setores:
            print("[ERRO] Nenhum arquivo CSV encontrado em {}".format(pasta_csv))
            return
        
        dfs = []
        
        # Carregar Setores (ultimos 10 periodos: 2023, 2024, 2025)
        print("[INFO] Carregando ultimos 10 periodos (2023-2025)...")
        for arquivo in arquivos_setores[-10:]:
            try:
                df = pd.read_csv(
                    arquivo, 
                    encoding='utf-8',
                    sep=';',
                    on_bad_lines='skip',
                    engine='python'
                )
                dfs.append(df)
                print("[OK] Carregado (CSV): {} ({:,} linhas)".format(arquivo.name, len(df)))
            except Exception as e:
                print("[ERRO] Erro ao carregar {}: {}".format(arquivo.name, e))
        
        # Carregar Atributos
        df_atributos = None
        if arquivos_atributos:
            try:
                df_atributos = pd.read_csv(
                    arquivos_atributos[0], 
                    encoding='utf-8',
                    sep=';',
                    on_bad_lines='skip',
                    engine='python'
                )
                print("[OK] Carregado (Atributos): {} ({:,} linhas)".format(arquivos_atributos[0].name, len(df_atributos)))
            except Exception as e:
                print("[ERRO] Erro ao carregar atributos: {}".format(e))
        
        if dfs:
            self.df = pd.concat(dfs, ignore_index=True)
            
            # Juntar com atributos
            if df_atributos is not None and 'Código Setor Censitário' in self.df.columns:
                print("[OK] Juntando com Atributos...")
                # Garantir que ambas as colunas têm o mesmo tipo de dados
                self.df['Código Setor Censitário'] = self.df['Código Setor Censitário'].astype(str)
                df_atributos['Código Setor Censitário'] = df_atributos['Código Setor Censitário'].astype(str)
                
                self.df = self.df.merge(
                    df_atributos[['Código Setor Censitário', 'Região', 'UF', 'Município']],
                    on='Código Setor Censitário',
                    how='left'
                )
                print("[OK] Juncao completa!")
            
            print("[OK] Total consolidado: {:,} linhas".format(len(self.df)))
    
    def filtrar_dados(self, **kwargs):
        """
        Filtra o DataFrame dinamicamente com base nos critérios fornecidos.
        Ignora colunas inexistentes e valores de placeholder ('Todos', 'Brasil', etc).
        """
        if self.df.empty:
            return self.df

        # Criamos uma cópia inicial para não mutar o DataFrame original da classe
        df_filtrado = self.df.copy()
        
        # Valores que indicam que nenhum filtro deve ser aplicado naquela coluna
        ignore_values = {"Todos", "Todas as UFs", "Todas", "Brasil", "Todos os Municípios"}

        for coluna, valor in kwargs.items():
            # 1. Pular se a coluna não existir
            if coluna not in df_filtrado.columns:
                continue
            
            # 2. Pular se o valor for nulo ou um placeholder de "ignorar"
            if valor is None or valor in ignore_values:
                continue

            # 3. Aplicar o filtro (suporta valor único ou lista de valores)
            if isinstance(valor, list):
                df_filtrado = df_filtrado[df_filtrado[coluna].isin(valor)]
            else:
                df_filtrado = df_filtrado[df_filtrado[coluna] == valor]

        return df_filtrado


class AnalisadorRodovias:
    """
    Classe para analisar dados de cobertura móvel em rodovias.
    Suporta rodovias federais e estaduais.
    """
    
    def __init__(self, tipo_rodovia="federais", data_path=None):
        """
        Inicializa o analisador de rodovias.
        
        Args:
            tipo_rodovia: "federais" ou "estaduais"
            data_path: Caminho customizado para os dados
        """
        self.df = pd.DataFrame()
        self.tipo_rodovia = tipo_rodovia.lower()
        
        if data_path is None:
            if self.tipo_rodovia == "federais":
                data_path = Path(__file__).parent / "cobertura_rodovias"
            else:
                data_path = Path(__file__).parent / "cobertura_rodovias_estaduais"
        
        self.caminho_dados = Path(data_path)
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega arquivos de cobertura de rodovias."""
        if not self.caminho_dados.exists():
            print(f"[ERRO] Caminho {self.caminho_dados} não encontrado")
            return
        
        # Se for um arquivo individual
        if self.caminho_dados.is_file():
            if self.caminho_dados.suffix == '.parquet':
                self._carregar_parquet_arquivo(self.caminho_dados)
            elif self.caminho_dados.suffix == '.csv':
                self._carregar_csv_arquivo(self.caminho_dados)
            return
        
        # Se for uma pasta, carregar CSVs
        if self.caminho_dados.is_dir():
            self._carregar_multiplos_csvs(self.caminho_dados)
    
    def _carregar_csv_arquivo(self, caminho):
        """Carrega um arquivo CSV de rodovias."""
        try:
            self.df = pd.read_csv(
                caminho, 
                encoding='utf-8',
                sep=';',
                on_bad_lines='skip',
                engine='python'
            )
            print("[OK] Carregado (CSV Rodovias): {} ({} linhas)".format(caminho.name, len(self.df)))
        except Exception as e:
            print("[ERRO] Erro ao carregar {}: {}".format(caminho.name, e))
    
    def _carregar_parquet_arquivo(self, caminho):
        """Carrega um arquivo Parquet de rodovias."""
        try:
            self.df = pd.read_parquet(caminho)
            print("[OK] Carregado (Parquet Rodovias): {} ({} linhas)".format(caminho.name, len(self.df)))
        except Exception as e:
            print("[ERRO] Erro ao carregar Parquet {}: {}".format(caminho.name, e))
    
    def _carregar_multiplos_csvs(self, pasta):
        """Carrega todos os CSVs de cobertura de rodovias."""
        arquivos_csv = sorted(pasta.glob("Cobertura_Rodovias*.csv"))
        
        if not arquivos_csv:
            print("[ERRO] Nenhum arquivo CSV de rodovias encontrado em {}".format(pasta))
            return
        
        dfs = []
        
        print("[INFO] Carregando arquivos de rodovias...")
        for arquivo in arquivos_csv:
            try:
                df = pd.read_csv(
                    arquivo, 
                    encoding='utf-8',
                    sep=';',
                    on_bad_lines='skip',
                    engine='python'
                )
                dfs.append(df)
                print("[OK] Carregado (CSV): {} ({:,} linhas)".format(arquivo.name, len(df)))
            except Exception as e:
                print("[ERRO] Erro ao carregar {}: {}".format(arquivo.name, e))
        
        if dfs:
            self.df = pd.concat(dfs, ignore_index=True)
            print("[OK] Total consolidado: {:,} linhas".format(len(self.df)))
    
    def filtrar_dados(self, **kwargs):
        """
        Filtra o DataFrame dinamicamente com base nos critérios fornecidos.
        """
        if self.df.empty:
            return self.df
        
        df_filtrado = self.df.copy()
        ignore_values = {"Todos", "Todas", "Todas as UFs", "Todas as Rodovias"}
        
        for coluna, valor in kwargs.items():
            if coluna not in df_filtrado.columns:
                continue
            
            if valor is None or valor in ignore_values:
                continue
            
            if isinstance(valor, list):
                df_filtrado = df_filtrado[df_filtrado[coluna].isin(valor)]
            else:
                df_filtrado = df_filtrado[df_filtrado[coluna] == valor]
        
        return df_filtrado
    
    def calcular_cobertura_por_tecnologia(self, df_filtrado=None):
        """
        Calcula a cobertura agregada por tecnologia.
        Retorna um dicionário com {tecnologia: percentual_coberto}
        """
        if df_filtrado is None:
            df_filtrado = self.df
        
        if df_filtrado.empty:
            return {}
        
        resultado = {}
        
        if 'Tecnologia' in df_filtrado.columns and 'Extensão coberta (km)' in df_filtrado.columns and 'Extensão (km)' in df_filtrado.columns:
            for tecnologia in df_filtrado['Tecnologia'].unique():
                df_tec = df_filtrado[df_filtrado['Tecnologia'] == tecnologia]
                extensao_coberta = pd.to_numeric(df_tec['Extensão coberta (km)'], errors='coerce').sum()
                extensao_total = pd.to_numeric(df_tec['Extensão (km)'], errors='coerce').sum()
                
                if extensao_total > 0:
                    resultado[str(tecnologia)] = (extensao_coberta / extensao_total) * 100
                else:
                    resultado[str(tecnologia)] = 0.0
        
        return resultado
    
    def calcular_cobertura_por_operadora(self, df_filtrado=None):
        """
        Calcula a cobertura por operadora.
        Retorna um dicionário com {operadora: percentual_coberto}
        """
        if df_filtrado is None:
            df_filtrado = self.df
        
        if df_filtrado.empty:
            return {}
        
        resultado = {}
        
        if 'Operadora' in df_filtrado.columns and 'Extensão coberta (km)' in df_filtrado.columns and 'Extensão (km)' in df_filtrado.columns:
            for operadora in df_filtrado['Operadora'].unique():
                df_op = df_filtrado[df_filtrado['Operadora'] == operadora]
                extensao_coberta = pd.to_numeric(df_op['Extensão coberta (km)'], errors='coerce').sum()
                extensao_total = pd.to_numeric(df_op['Extensão (km)'], errors='coerce').sum()
                
                if extensao_total > 0:
                    resultado[str(operadora)] = (extensao_coberta / extensao_total) * 100
                else:
                    resultado[str(operadora)] = 0.0
        
        return resultado