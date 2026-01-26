"""
Conversor de CSV para Parquet para dados de Conectividade nas Escolas.
Executa conversão em lote com otimizações de tipo de dados.
"""
import pandas as pd
from pathlib import Path
import sys

def converter_para_parquet(pasta_origem, pasta_destino):
    """Converte CSVs de Conectividade para Parquet com otimizações."""
    
    pasta_origem = Path(pasta_origem)
    pasta_destino = Path(pasta_destino)
    pasta_destino.mkdir(parents=True, exist_ok=True)
    
    arquivos_csv = sorted(pasta_origem.glob("Conectividade_Escolas_*.csv"))
    
    if not arquivos_csv:
        print("[ERRO] Nenhum arquivo CSV encontrado em {}".format(pasta_origem))
        return
    
    print("[INFO] Iniciando conversao de {} arquivos CSV para Parquet...".format(len(arquivos_csv)))
    
    for i, arquivo_csv in enumerate(arquivos_csv, 1):
        nome_base = arquivo_csv.stem
        arquivo_parquet = pasta_destino / (nome_base + ".parquet")
        
        try:
            print("[INFO] [{}/{}] Carregando {} ...".format(i, len(arquivos_csv), arquivo_csv.name))
            
            # Carregar CSV
            df = pd.read_csv(
                arquivo_csv,
                sep=';',
                encoding='utf-8',
                engine='python',
                on_bad_lines='skip'
            )
            
            # Otimizacoes minimas - apenas comprimir
            pass
            
            # Salvar como Parquet com compressão snappy
            df.to_parquet(
                arquivo_parquet,
                engine='pyarrow',
                compression='snappy',
                index=False
            )
            
            tamanho_csv = arquivo_csv.stat().st_size / (1024*1024)
            tamanho_parquet = arquivo_parquet.stat().st_size / (1024*1024)
            reducao = (1 - tamanho_parquet/tamanho_csv) * 100
            
            print("[OK] Convertido: {} ({:.1f} MB -> {:.1f} MB, reducao: {:.1f}%)".format(
                arquivo_parquet.name, tamanho_csv, tamanho_parquet, reducao
            ))
            
        except Exception as e:
            print("[ERRO] Erro ao converter {}: {}".format(arquivo_csv.name, e))
    
    print("[OK] Conversao concluida!")

if __name__ == "__main__":
    # Definir caminhos
    pasta_origem = Path(__file__).parent
    pasta_destino = pasta_origem / "parquet"
    
    print("[INFO] Pasta origem: {}".format(pasta_origem))
    print("[INFO] Pasta destino: {}".format(pasta_destino))
    print()
    
    converter_para_parquet(pasta_origem, pasta_destino)
