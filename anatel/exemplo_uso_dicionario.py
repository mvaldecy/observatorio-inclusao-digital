"""
Exemplo de uso do dicionário de dados da ANATEL

Demonstra como usar as funções auxiliares para obter labels e trabalhar com metadados
"""

import sys
import os

# Adiciona o caminho do projeto ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

from anatel.dicionario_dados import (
    obter_label,
    obter_valor_label,
    eh_coluna_binaria,
    eh_coluna_numerica,
    listar_colunas_por_tipo,
    COLUNAS
)

def exemplo_basico():
    """Exemplo básico de uso das funções"""
    print("=" * 80)
    print("EXEMPLO BÁSICO - Obtendo labels de colunas")
    print("=" * 80)
    
    # Obter label de uma coluna
    print(f"\nColuna: COD_INEP")
    print(f"Label: {obter_label('COD_INEP')}")
    
    print(f"\nColuna: CONECT_POSSUI_INTERNET")
    print(f"Label: {obter_label('CONECT_POSSUI_INTERNET')}")
    
    print(f"\nColuna: VEL_MAX")
    print(f"Label: {obter_label('VEL_MAX')}")


def exemplo_valores():
    """Exemplo de conversão de valores para labels"""
    print("\n" + "=" * 80)
    print("EXEMPLO - Convertendo valores para labels")
    print("=" * 80)
    
    # Estados
    print(f"\nUF: PI -> {obter_valor_label('SG_UF', 'PI')}")
    print(f"UF: SP -> {obter_valor_label('SG_UF', 'SP')}")
    
    # Valores binários
    print(f"\nPOSSUI_GEOLOCALIZACAO: Sim -> {obter_valor_label('POSSUI_GEOLOCALIZACAO', 'Sim')}")
    print(f"CONECT_ADEQUADA: Não -> {obter_valor_label('CONECT_ADEQUADA', 'Não')}")
    
    # Região
    print(f"\nCO_REGIAO: 2 -> {obter_valor_label('CO_REGIAO', 2)}")


def exemplo_tipos():
    """Exemplo de verificação de tipos de colunas"""
    print("\n" + "=" * 80)
    print("EXEMPLO - Verificando tipos de colunas")
    print("=" * 80)
    
    colunas_teste = [
        'CONECT_POSSUI_INTERNET',
        'VEL_MAX',
        'LATITUDE',
        'NO_MUNICIPIO'
    ]
    
    for col in colunas_teste:
        print(f"\nColuna: {col}")
        print(f"  Binária: {eh_coluna_binaria(col)}")
        print(f"  Numérica: {eh_coluna_numerica(col)}")
        print(f"  Label: {obter_label(col)}")


def exemplo_listagem():
    """Exemplo de listagem de colunas por tipo"""
    print("\n" + "=" * 80)
    print("EXEMPLO - Listando colunas por tipo")
    print("=" * 80)
    
    print(f"\nTotal de colunas documentadas: {len(COLUNAS)}")
    
    binarias = listar_colunas_por_tipo('binarias')
    print(f"\nColunas binárias ({len(binarias)}):")
    for col in binarias[:5]:  # Mostra apenas as 5 primeiras
        print(f"  - {col}: {obter_label(col)}")
    print(f"  ... e mais {len(binarias) - 5} colunas")
    
    numericas = listar_colunas_por_tipo('numericas')
    print(f"\nColunas numéricas ({len(numericas)}):")
    for col in numericas[:5]:
        print(f"  - {col}: {obter_label(col)}")
    print(f"  ... e mais {len(numericas) - 5} colunas")
    
    coordenadas = listar_colunas_por_tipo('coordenadas')
    print(f"\nColunas de coordenadas ({len(coordenadas)}):")
    for col in coordenadas:
        print(f"  - {col}: {obter_label(col)}")


def exemplo_dataframe():
    """Exemplo de uso com pandas DataFrame"""
    print("\n" + "=" * 80)
    print("EXEMPLO - Uso com DataFrame")
    print("=" * 80)
    
    try:
        import pandas as pd
        
        # Exemplo de como renomear colunas usando o dicionário
        colunas_originais = ['COD_INEP', 'NO_MUNICIPIO', 'SG_UF', 'CONECT_POSSUI_INTERNET', 'VEL_MAX']
        
        print("\nRenomeando colunas para labels descritivas:")
        rename_dict = {col: obter_label(col) for col in colunas_originais}
        
        for original, label in rename_dict.items():
            print(f"  {original:30s} -> {label}")
        
        # Exemplo de como filtrar colunas por tipo
        print("\n\nFiltrando apenas colunas binárias de um DataFrame:")
        colunas_disponiveis = ['COD_INEP', 'CONECT_POSSUI_INTERNET', 'VEL_MAX', 'ESCOLAS_CONECTADAS']
        colunas_binarias_filtradas = [col for col in colunas_disponiveis if eh_coluna_binaria(col)]
        
        print(f"Colunas disponíveis: {colunas_disponiveis}")
        print(f"Colunas binárias filtradas: {colunas_binarias_filtradas}")
        
    except ImportError:
        print("Pandas não está instalado. Pulando exemplos com DataFrame.")


if __name__ == "__main__":
    exemplo_basico()
    exemplo_valores()
    exemplo_tipos()
    exemplo_listagem()
    exemplo_dataframe()
    
    print("\n" + "=" * 80)
    print("✓ Exemplos concluídos!")
    print("=" * 80)
