"""
Script auxiliar para conversão rápida de arquivos XLSX

Uso:
    python pcd/converter_dados.py caminho/para/arquivo.xlsx 2024
    python pcd/converter_dados.py caminho/para/arquivo.xlsx 2024 --multiplas
"""

import sys
import argparse
from pathlib import Path
from conversor_xlsx import ConversorXLSX


def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(
        description='Converte arquivos XLSX de dados PCD para formato cache (Parquet)'
    )
    
    parser.add_argument(
        'arquivo',
        type=str,
        help='Caminho para o arquivo XLSX'
    )
    
    parser.add_argument(
        'ano',
        type=int,
        help='Ano de referência dos dados'
    )
    
    parser.add_argument(
        '--multiplas',
        action='store_true',
        help='Processar múltiplas planilhas do arquivo'
    )
    
    parser.add_argument(
        '--sheet',
        type=str,
        default=None,
        help='Nome ou índice da planilha específica (padrão: primeira)'
    )
    
    args = parser.parse_args()
    
    # Validar arquivo
    arquivo_path = Path(args.arquivo)
    if not arquivo_path.exists():
        print(f"❌ Erro: Arquivo não encontrado: {args.arquivo}")
        sys.exit(1)
    
    if not arquivo_path.suffix.lower() in ['.xlsx', '.xls']:
        print(f"❌ Erro: Arquivo deve ser .xlsx ou .xls")
        sys.exit(1)
    
    # Criar conversor
    conversor = ConversorXLSX()
    
    print("\n" + "=" * 70)
    print(f"📄 Arquivo: {arquivo_path.name}")
    print(f"📅 Ano: {args.ano}")
    print("=" * 70 + "\n")
    
    try:
        if args.multiplas:
            # Processar múltiplas planilhas
            print("📚 Modo: Múltiplas planilhas\n")
            resultados = conversor.processar_multiplas_planilhas(
                str(arquivo_path),
                ano=args.ano
            )
            
            # Resumo
            sucesso = sum(1 for v in resultados.values() if v is not None)
            print(f"\n✅ {sucesso}/{len(resultados)} planilhas convertidas com sucesso")
            
        else:
            # Processar planilha única
            sheet = args.sheet if args.sheet else 0
            if args.sheet:
                print(f"📄 Planilha: {args.sheet}\n")
            else:
                print(f"📄 Planilha: primeira (índice 0)\n")
            
            arquivo_saida = conversor.processar_arquivo(
                str(arquivo_path),
                ano=args.ano,
                sheet_name=sheet
            )
            
            print(f"\n✅ Conversão concluída!")
            print(f"📁 Arquivo gerado: {Path(arquivo_saida).name}")
        
        # Listar arquivos em cache
        print("\n" + "=" * 70)
        print("📦 Arquivos em cache:")
        print("=" * 70)
        conversor.listar_arquivos_cache()
        
        print("\n🎯 Próximo passo:")
        print("   Execute o Streamlit: streamlit run streamlit/Home.py")
        print("   Acesse a página: PCD - Inclusão Digital")
        
    except Exception as e:
        print(f"\n❌ Erro durante conversão: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
