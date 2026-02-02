# Fluxo de Download e Processamento ANATEL

## Estrutura Implementada

### 1. Configuração (data_sources.py)
```python
'anatel': {
    'urls': {
        'consolidado': {
            'conectividade-escola': "https://www.anatel.gov.br/dadosabertos/paineis_de_dados/infraestrutura/conectividade_escolas.zip"
        }
    }
}
```

### 2. Fluxo de Processamento (SIMPLIFICADO)

#### Quando chamado: `carregar_dados_anatel(ano='consolidado', tipo='conectividade-escola')`

1. **Verifica cache existente**
   - Procura por pastas com anos: `data/cache/anatel/2022/`, `2023/`, etc.
   - Se encontrar parquets e não forçar download, carrega do cache

2. **Download e Processamento** (se não houver cache ou force_download=True)
   - Baixa o arquivo ZIP da URL configurada
   - Extrai todos os CSVs para pasta temporária
   - **FILTRA apenas arquivos que terminam com `-09` (setembro)**
     * Exemplo: `Conectividade_Escolas_2024-09.csv` ✅
     * Exemplo: `Conectividade_Escolas_2024-03.csv` ❌ (ignorado)
     * Exemplo: `Conectividade_Escolas_2024-06.csv` ❌ (ignorado)

3. **Conversão Direta** (sem consolidação)
   Para cada arquivo `-09`:
   - Identifica o ano pelo nome (ex: `2024-09` → ano 2024)
   - Lê o CSV
   - Limpa e padroniza colunas (maiúsculas, sem BOM)
   - Otimiza tipos de dados
   - **Salva como parquet** em: `data/cache/anatel/{ano}/conectividade-escola.parquet`

4. **Limpeza**
   - Remove pasta temporária com todos os CSVs
   - Mantém apenas os parquets organizados por ano

5. **Retorno**
   - Carrega todos os parquets de todos os anos
   - Concatena em um único DataFrame
   - Retorna DataFrame consolidado

### 3. Estrutura Final do Cache

```
data/cache/anatel/
├── 2022/
│   └── conectividade-escola.parquet  (dados de setembro/2022)
├── 2023/
│   └── conectividade-escola.parquet  (dados de setembro/2023)
├── 2024/
│   └── conectividade-escola.parquet  (dados de setembro/2024)
└── 2025/
    └── conectividade-escola.parquet  (dados de setembro/2025)
```

**Cada parquet contém apenas os dados do arquivo `-09` (setembro) do respectivo ano**

### 4. Uso no Código

#### Carregar todos os anos (consolidado)
```python
from streamlit.utils.data_loader import carregar_dados_anatel

# Carrega todos os anos em um único DataFrame
df, _ = carregar_dados_anatel(ano='consolidado', tipo='conectividade-escola')
```

#### Forçar redownload
```python
# Força download e reprocessamento
df, _ = carregar_dados_anatel(ano='consolidado', tipo='conectividade-escola', force_download=True)
```

#### Carregar apenas um ano específico
```python
# Carrega apenas 2024 (precisa já estar em cache)
df, _ = carregar_dados_anatel(ano=2024, tipo='conectividade-escola')
```

### 5. Métodos Implementados

#### `_filtrar_csvs_setembro(csv_paths)`
- Filtra apenas arquivos que terminam com `-09` (setembro)
- Mapeia cada arquivo ao seu ano
- Retorna: `{ano: path_do_csv}`

#### `_processar_csvs_setembro(csv_paths, tipo)`
- Processa cada arquivo `-09` individualmente
- Salva parquet na pasta do ano
- Exibe progresso no Streamlit
- **SEM consolidação de múltiplos arquivos**

#### `_download_and_extract_zip(url, tipo)`
- Baixa o ZIP
- Extrai para pasta temporária
- Chama `_processar_csvs_setembro`
- Limpa pasta temporária

#### `_carregar_anatel(ano, tipo, force_download)`
- Método principal de carregamento
- Gerencia cache e download
- Retorna DataFrame

### 6. Vantagens da Estrutura Simplificada

✅ **Apenas dados de setembro**: Usa os arquivos consolidados mais recentes
✅ **Sem duplicação**: Não processa março, junho, etc.
✅ **Organização por ano**: Cada ano em sua pasta
✅ **Economia de espaço**: Parquet comprimido, sem CSVs grandes
✅ **Performance**: Parquet é muito mais rápido para ler
✅ **Limpeza automática**: Remove temporários após processamento
✅ **Flexibilidade**: Pode carregar anos específicos ou todos juntos
✅ **Cache inteligente**: Só baixa se necessário

### 7. Por que apenas `-09` (setembro)?

Os arquivos de setembro contêm os dados consolidados e mais completos do ano até aquele ponto.
Não há necessidade de processar março, junho, etc., pois setembro já inclui tudo.

