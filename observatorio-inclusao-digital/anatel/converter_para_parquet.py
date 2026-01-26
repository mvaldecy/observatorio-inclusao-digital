"""
Script para converter dados de cobertura ANATEL de CSV para Parquet comprimido
Reduz tamanho em ~80% e melhora velocidade de leitura em ~10x
"""

import pandas as pd
import os
from pathlib import Path
import time

def converter_csv_para_parquet():
    """Converte todos os CSVs de cobertura para Parquet com compressão."""
    
    pasta_dados = Path(__file__).parent / "cobertura_movel"
    pasta_parquet = pasta_dados / "parquet"
    
    # Criar pasta para parquets se não existir
    pasta_parquet.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("🔄 CONVERTENDO DADOS DE CSV PARA PARQUET")
    print("=" * 70)
    
    # Encontrar todos os CSVs
    arquivos_csv = sorted(pasta_dados.glob("Cobertura_*.csv"))
    
    if not arquivos_csv:
        print("❌ Nenhum arquivo CSV encontrado!")
        return
    
    tamanho_total_csv = 0
    tamanho_total_parquet = 0
    
    for i, arquivo_csv in enumerate(arquivos_csv, 1):
        print(f"\n[{i}/{len(arquivos_csv)}] Processando: {arquivo_csv.name}")
        
        try:
            # Ler CSV com tipos otimizados
            print("  📖 Lendo CSV...")
            start = time.time()
            df = pd.read_csv(
                arquivo_csv,
                sep=';',
                encoding='utf-8',
                on_bad_lines='skip',
                engine='python',
                dtype={
                    'Período': 'str',
                    'Operadora': 'category',
                    'Código Setor Censitário': 'str'
                }
            )
            tempo_leitura = time.time() - start
            
            # Converter colunas de cobertura para float32 (economia de memória)
            colunas_cobertura = [col for col in df.columns if col.startswith('Cobertura_')]
            for col in colunas_cobertura:
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(',', '.'),
                    errors='coerce',
                    downcast='float'
                )
            
            print(f"  ✓ Lido: {len(df):,} linhas em {tempo_leitura:.2f}s")
            
            # Salvar como Parquet com compressão
            print("  💾 Salvando em Parquet...")
            arquivo_parquet = pasta_parquet / f"{arquivo_csv.stem}.parquet"
            
            start = time.time()
            df.to_parquet(
                arquivo_parquet,
                engine='pyarrow',
                compression='snappy',  # Bom balanço entre compressão e velocidade
                index=False
            )
            tempo_save = time.time() - start
            
            # Calcular tamanho
            tamanho_csv = arquivo_csv.stat().st_size / (1024**2)
            tamanho_pq = arquivo_parquet.stat().st_size / (1024**2)
            reducao = ((tamanho_csv - tamanho_pq) / tamanho_csv) * 100
            
            tamanho_total_csv += tamanho_csv
            tamanho_total_parquet += tamanho_pq
            
            print(f"  ✓ Salvo: {arquivo_parquet.name}")
            print(f"  📊 CSV: {tamanho_csv:.1f}MB → Parquet: {tamanho_pq:.1f}MB (redução: {reducao:.1f}%)")
            
        except Exception as e:
            print(f"  ❌ Erro: {e}")
    
    # Resumo final
    print("\n" + "=" * 70)
    print("✅ CONVERSÃO CONCLUÍDA!")
    print("=" * 70)
    print(f"Total CSV: {tamanho_total_csv:.1f}MB")
    print(f"Total Parquet: {tamanho_total_parquet:.1f}MB")
    reducao_total = ((tamanho_total_csv - tamanho_total_parquet) / tamanho_total_csv) * 100
    print(f"Redução total: {reducao_total:.1f}%")
    print(f"\n✅ Arquivos Parquet salvos em: {pasta_parquet}")
    print("\nPróximo passo: Use o carregador otimizado no Streamlit!")

if __name__ == "__main__":
    converter_csv_para_parquet()
