"""
Conversor de arquivos XLSX para formato cache (Parquet)

Responsabilidade: Ler arquivos XLSX e converter para formato otimizado
"""
import pandas as pd
from pathlib import Path
from datetime import datetime


class ConversorXLSX:
    """
    Converte arquivos XLSX para formato Parquet otimizado para cache
    
    Responsabilidades:
    - Ler arquivos XLSX
    - Validar estrutura de dados
    - Normalizar nomes de colunas
    - Salvar em formato Parquet
    """
    
    def __init__(self, cache_dir: str = None):
        """
        Inicializa o conversor
        
        Args:
            cache_dir: Diretório para salvar arquivos de cache
        """
        if cache_dir is None:
            # Usa diretório padrão
            base_dir = Path(__file__).parent.parent
            cache_dir = base_dir / 'data' / 'cache' / 'pcd'
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Conversor inicializado. Cache em: {self.cache_dir}")
    
    def normalizar_colunas(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza nomes de colunas (minúsculas, sem espaços)
        
        Args:
            df: DataFrame a normalizar
            
        Returns:
            DataFrame com colunas normalizadas
        """
        # Cria dicionário de mapeamento
        rename_dict = {}
        for col in df.columns:
            # Remove espaços, converte para minúsculas, substitui caracteres especiais
            novo_nome = str(col).strip().lower()
            novo_nome = novo_nome.replace(' ', '_')
            novo_nome = novo_nome.replace('-', '_')
            novo_nome = novo_nome.replace('/', '_')
            novo_nome = novo_nome.replace('(', '')
            novo_nome = novo_nome.replace(')', '')
            novo_nome = novo_nome.replace('?', '')
            novo_nome = novo_nome.replace(':', '')
            novo_nome = novo_nome.replace('.', '')
            
            # Remove underscores duplicados
            while '__' in novo_nome:
                novo_nome = novo_nome.replace('__', '_')
            
            rename_dict[col] = novo_nome
        
        df = df.rename(columns=rename_dict)
        print(f"✓ {len(rename_dict)} colunas normalizadas")
        
        return df
    
    def processar_arquivo(self, arquivo_xlsx: str, ano: int = None, sheet_name: str = 0) -> str:
        """
        Processa arquivo XLSX e salva como Parquet
        
        Args:
            arquivo_xlsx: Caminho para o arquivo XLSX
            ano: Ano de referência dos dados (opcional)
            sheet_name: Nome ou índice da planilha (default: primeira planilha)
            
        Returns:
            Caminho do arquivo Parquet criado
        """
        arquivo_path = Path(arquivo_xlsx)
        
        if not arquivo_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_xlsx}")
        
        print(f"📖 Lendo arquivo: {arquivo_path.name}")
        
        try:
            # Lê arquivo XLSX
            df = pd.read_excel(arquivo_xlsx, sheet_name=sheet_name)
            print(f"✓ Arquivo lido: {len(df):,} linhas, {len(df.columns)} colunas")
            
            # Normaliza colunas
            df = self.normalizar_colunas(df)
            
            # Adiciona coluna de ano se especificado
            if ano is not None:
                df['ano'] = ano
                print(f"✓ Coluna 'ano' adicionada: {ano}")
            elif 'ano' not in df.columns:
                # Tenta inferir do nome do arquivo
                ano_inferido = self._inferir_ano_do_nome(arquivo_path.name)
                if ano_inferido:
                    df['ano'] = ano_inferido
                    print(f"✓ Ano inferido do nome do arquivo: {ano_inferido}")
            
            # Define nome do arquivo de saída
            if ano is not None:
                nome_saida = f"pcd_{ano}.parquet"
            else:
                nome_saida = f"pcd_{arquivo_path.stem}.parquet"
            
            arquivo_saida = self.cache_dir / nome_saida
            
            # Salva como Parquet
            df.to_parquet(arquivo_saida, index=False, compression='snappy')
            
            print(f"✅ Arquivo convertido com sucesso!")
            print(f"   📁 Salvo em: {arquivo_saida}")
            print(f"   📊 Registros: {len(df):,}")
            print(f"   📋 Colunas: {len(df.columns)}")
            
            return str(arquivo_saida)
            
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
            raise
    
    def processar_multiplas_planilhas(self, arquivo_xlsx: str, ano: int = None) -> dict:
        """
        Processa múltiplas planilhas de um arquivo XLSX
        
        Args:
            arquivo_xlsx: Caminho para o arquivo XLSX
            ano: Ano de referência dos dados
            
        Returns:
            Dicionário com nome da planilha e caminho do arquivo gerado
        """
        arquivo_path = Path(arquivo_xlsx)
        
        if not arquivo_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_xlsx}")
        
        # Lê todos os nomes das planilhas
        xl_file = pd.ExcelFile(arquivo_xlsx)
        sheet_names = xl_file.sheet_names
        
        print(f"📚 Arquivo com {len(sheet_names)} planilhas: {sheet_names}")
        
        resultados = {}
        
        for sheet_name in sheet_names:
            print(f"\n➡️  Processando planilha: {sheet_name}")
            try:
                # Processa cada planilha
                df = pd.read_excel(arquivo_xlsx, sheet_name=sheet_name)
                df = self.normalizar_colunas(df)
                
                if ano is not None:
                    df['ano'] = ano
                
                # Nome do arquivo baseado na planilha
                nome_normalizado = sheet_name.lower().replace(' ', '_')
                if ano:
                    nome_saida = f"pcd_{ano}_{nome_normalizado}.parquet"
                else:
                    nome_saida = f"pcd_{nome_normalizado}.parquet"
                
                arquivo_saida = self.cache_dir / nome_saida
                df.to_parquet(arquivo_saida, index=False, compression='snappy')
                
                resultados[sheet_name] = str(arquivo_saida)
                print(f"   ✓ {len(df):,} registros salvos")
                
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                resultados[sheet_name] = None
        
        print(f"\n✅ Processamento concluído: {len([v for v in resultados.values() if v])} planilhas convertidas")
        return resultados
    
    def _inferir_ano_do_nome(self, nome_arquivo: str) -> int:
        """Tenta inferir o ano do nome do arquivo"""
        import re
        # Procura por 4 dígitos consecutivos que pareçam um ano (2000-2099)
        match = re.search(r'20[0-9]{2}', nome_arquivo)
        if match:
            return int(match.group())
        return None
    
    def listar_arquivos_cache(self) -> list:
        """Lista arquivos Parquet no cache"""
        arquivos = list(self.cache_dir.glob('*.parquet'))
        
        if not arquivos:
            print("📭 Nenhum arquivo em cache")
            return []
        
        print(f"\n📦 Arquivos em cache ({len(arquivos)}):")
        for arq in sorted(arquivos):
            tamanho = arq.stat().st_size / 1024  # KB
            print(f"   • {arq.name} ({tamanho:.1f} KB)")
        
        return [str(a) for a in arquivos]
    
    def validar_estrutura(self, df: pd.DataFrame) -> dict:
        """
        Valida estrutura básica do DataFrame
        
        Returns:
            Dicionário com informações da validação
        """
        info = {
            'total_linhas': len(df),
            'total_colunas': len(df.columns),
            'colunas': list(df.columns),
            'tipos': df.dtypes.to_dict(),
            'valores_nulos': df.isnull().sum().to_dict(),
            'memoria_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        return info


# Função helper para uso direto
def converter_xlsx(arquivo: str, ano: int = None) -> str:
    """
    Função helper para converter rapidamente um arquivo XLSX
    
    Args:
        arquivo: Caminho do arquivo XLSX
        ano: Ano de referência
        
    Returns:
        Caminho do arquivo Parquet gerado
    """
    conversor = ConversorXLSX()
    return conversor.processar_arquivo(arquivo, ano=ano)
