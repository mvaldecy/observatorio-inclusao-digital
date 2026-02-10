"""
Módulo para carregar e mapear códigos IBGE para nomes de municípios
"""
import pandas as pd
import requests
from pathlib import Path


def carregar_municipios_ibge():
    """
    Carrega tabela de municípios do IBGE com código e nome
    
    Returns:
        DataFrame com colunas: codigo_municipio, nome_municipio, uf
    """
    cache_dir = Path(__file__).parent.parent / 'data' / 'cache' / 'ibge'
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / 'municipios.csv'
    
    # Se já tem em cache, carrega
    if cache_file.exists():
        print(f"✓ Carregando municípios do cache...")
        return pd.read_csv(cache_file, dtype={'codigo_municipio': str})
    
    # Se não, tenta baixar da API do IBGE (nova URL mais simples)
    print("⏳ Baixando lista de municípios do IBGE...")
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        municipios = response.json()
        
        if not municipios:
            raise ValueError("Lista de municípios vazia")
        
        # Processa os dados - estrutura correta da API
        dados = []
        for m in municipios:
            try:
                codigo = str(m['id'])
                nome = m['nome']
                uf = m['microrregiao']['mesorregiao']['UF']['sigla']
                
                dados.append({
                    'codigo_municipio': codigo,
                    'nome_municipio': nome,
                    'uf': uf
                })
            except (KeyError, TypeError) as e:
                # Ignora municípios com dados incompletos (não deveria acontecer)
                continue
        
        if not dados:
            raise ValueError("Nenhum município processado com sucesso")
        
        df = pd.DataFrame(dados)
        
        # Salva em cache
        df.to_csv(cache_file, index=False)
        print(f"✓ {len(df)} municípios carregados e salvos em cache")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro ao carregar municípios da API: {e}")
        # Retorna DataFrame vazio - o mapeamento lidará com isso
        return pd.DataFrame(columns=['codigo_municipio', 'nome_municipio', 'uf'])


def obter_mapeamento_codigo_nome():
    """
    Retorna dicionário mapeando código IBGE -> nome do município
    
    Returns:
        dict: {codigo: nome_municipio}
    """
    df = carregar_municipios_ibge()
    return dict(zip(df['codigo_municipio'], df['nome_municipio']))


def adicionar_nome_municipio(df, coluna_codigo='CÓDIGO MUNICÍPIO', coluna_nova='MUNICÍPIO'):
    """
    Adiciona coluna com nome do município baseado no código IBGE
    
    Args:
        df: DataFrame com códigos de município
        coluna_codigo: Nome da coluna com código IBGE
        coluna_nova: Nome da nova coluna a criar
    
    Returns:
        DataFrame com nova coluna de nomes
    """
    # Carrega mapeamento
    mapeamento = obter_mapeamento_codigo_nome()
    
    if not mapeamento:
        print("⚠️ Mapeamento de municípios vazio, mantendo códigos")
        df = df.copy()
        df[coluna_nova] = df[coluna_codigo]
        return df
    
    # Converte código para string e limpa
    df = df.copy()
    df['_cod_temp'] = df[coluna_codigo].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    
    # Mapeia código para nome
    df[coluna_nova] = df['_cod_temp'].map(mapeamento)
    
    # Para códigos não encontrados, tenta sem o último dígito verificador
    mask_nao_encontrado = df[coluna_nova].isna()
    if mask_nao_encontrado.any():
        print(f"⚠️ {mask_nao_encontrado.sum()} códigos não encontrados, tentando sem dígito verificador...")
        df.loc[mask_nao_encontrado, coluna_nova] = df.loc[mask_nao_encontrado, '_cod_temp'].str[:-1].map(mapeamento)
    
    # Substitui None pelo código quando não encontrar (para debug)
    mask_ainda_nao_encontrado = df[coluna_nova].isna()
    if mask_ainda_nao_encontrado.any():
        print(f"⚠️ {mask_ainda_nao_encontrado.sum()} códigos ainda não encontrados")
        df.loc[mask_ainda_nao_encontrado, coluna_nova] = df.loc[mask_ainda_nao_encontrado, '_cod_temp']
    
    # Remove coluna temporária
    df = df.drop(columns=['_cod_temp'])
    
    return df
