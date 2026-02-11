# Sistema INEP - Implementação Completa

## 📁 Arquivos Essenciais

### Diretório `/inep/`
- **`__init__.py`**: Módulo Python que exporta todas as funções
- **`metadados_inep.py`**: Dicionário de metadados estilo CETIC ⭐ **PRINCIPAL**
- **`analisador_inep.py`**: Analisador de dados com filtros e agregadores ⭐ **PRINCIPAL**
- **`dicionario_educacao_basica.py`**: Carregador de metadados do Excel (compatibilidade)
- **`dicionário_dados_educação_básica.xlsx`**: Arquivo Excel fonte do INEP
- **`exemplo_analisador.py`**: Exemplos completos de uso
- **`exemplo_uso_inep.py`**: Exemplo básico de metadados

### Diretório `/streamlit/utils/`
- **`http_loader.py`**: Classe HTTPDataLoader com métodos `_carregar_inep()` e `_download_and_convert_csv_to_parquet()`
- **`data_loader.py`**: Funções de alto nível para Streamlit incluindo `get_analisador_inep()`
- **`data_sources.py`**: URLs dos arquivos CSV do INEP (2022, 2023, 2024)

## 🎯 Componentes Principais

### 1. Sistema de Metadados (estilo CETIC)

```python
from inep import METADADOS_INEP, get_label, get_valores, formatar_valor

# Estrutura: categoria -> variável -> {label, valores}
categorias = METADADOS_INEP.keys()  # 14 categorias

# Obter informações
get_label('TP_DEPENDENCIA')  # "Dependência Administrativa"
get_valores('TP_LOCALIZACAO')  # {'1': 'Urbana', '2': 'Rural'}
formatar_valor('TP_DEPENDENCIA', 3)  # "3 - Municipal"
```

**Categorias disponíveis:**
- `identificacao`: Localização geográfica
- `caracterizacao`: Características da escola
- `infraestrutura_agua`: Abastecimento de água
- `infraestrutura_energia`: Energia elétrica
- `infraestrutura_esgoto`: Esgotamento sanitário
- `infraestrutura_lixo`: Destinação de lixo
- `espacos_ambientes`: Dependências e espaços
- `equipamentos`: Equipamentos disponíveis
- `internet_computadores`: Internet e computadores ⭐
- `educacao_indigena`: Educação indígena
- `modalidades_ensino`: Modalidades de ensino
- `matriculas`: Quantidade de alunos
- `docentes`: Quantidade de professores
- `atividades_complementares`: Atividades extras

### 2. AnalisadorINEP

```python
from streamlit.utils.data_loader import get_analisador_inep

# Criar analisador
analisador = get_analisador_inep(ano=2024)

# Filtrar dados
analisador.filtrar_dados(CO_UF=22, TP_DEPENDENCIA=3, TP_LOCALIZACAO=2)

# Analisar indicador único
resultado = analisador.analisar_indicador('IN_INTERNET')

# Analisar múltiplos indicadores
resultado = analisador.analisar_indicador([
    'IN_INTERNET',
    'IN_BANDA_LARGA',
    'IN_LABORATORIO_INFORMATICA'
])

# Análise por agregador
resultado = analisador.analisar_por_agregador(
    indicador='IN_INTERNET',
    campo_agregador='TP_DEPENDENCIA'
)

# Resumo de infraestrutura
resumo = analisador.resumo_infraestrutura(CO_UF=22)
```

### 3. Data Loader

### 1. HTTP Loader (`streamlit/utils/http_loader.py`)
Adicionados métodos específicos para o INEP:

- **`_download_and_convert_csv_to_parquet()`**: Baixa arquivo CSV e converte para Parquet
  - Suporta encoding UTF-8 e Latin-1
  - Aplica limpeza e otimização de dados
  - Salva na estrutura: `cache/inep/{ano}/{tipo}.parquet`

- **`_carregar_inep()`**: Método principal para carregar dados do INEP
  - Verifica cache antes de baixar
  - Baixa CSV e converte para Parquet
  - Retorna DataFrame pronto para uso

### 2. Data Loader (`streamlit/utils/data_loader.py`)
Adicionadas funções de alto nível para uso no Streamlit:

- **`carregar_dados_inep(ano, tipo, force_download)`**: Carrega dados do INEP
- **`carregar_educacao_basica_inep(ano, force_download)`**: Atalho para educação básica
- **`get_anos_disponiveis_inep(tipo)`**: Lista anos disponíveis

### 3. Dicionário de Dados (`inep/dicionario_educacao_basica.py`)
Sistema completo de metadados baseado no Excel do INEP:

#### Estruturas de Dados:
- **`METADADOS_INEP`**: Dict com informações de cada variável
  - `label`: Descrição da variável
  - `tipo`: Tipo de dado (Num, Char)
  - `tamanho`: Tamanho do campo
  - `categorias`: Valores possíveis (para variáveis categóricas)

- **`CATEGORIAS_INEP`**: Organização temática das variáveis
  - `identificacao`: Localização geográfica
  - `caracterizacao`: Características da escola
  - `infraestrutura_basica`: Água, energia, esgoto, lixo
  - `infraestrutura_espacos`: Salas, laboratórios, quadras
  - `equipamentos`: TVs, computadores, impressoras
  - `internet_computadores`: Internet e dispositivos
  - `acessibilidade`: Inclusão e materiais específicos
  - `organizacao_ensino`: Modalidades de ensino
  - `alunos_matriculas`: Quantidade de alunos
  - `profissionais`: Quantidade de profissionais
  - `alimentacao_transporte`: Serviços complementares

#### Funções Auxiliares:
- `get_metadados(variavel)`: Retorna metadados de uma variável
- `get_label(variavel)`: Retorna a descrição
- `get_categorias(variavel)`: Retorna valores possíveis
- `listar_categorias()`: Lista todas as categorias temáticas
- `listar_variaveis_por_categoria(categoria)`: Lista variáveis de uma categoria
- `formatar_valor_categorico(variavel, valor)`: Formata valor com descrição

### 4. Configuração de URLs (`streamlit/utils/data_sources.py`)
URLs já estavam configuradas para anos 2022, 2023 e 2024:
```python
'inep': {
    'urls': {
        2024: {'educacao-basica': 'https://...'},
        2023: {'educacao-basica': 'https://...'},
        2022: {'educacao-basica': 'https://...'}
    }
}
```

## 📖 Como usar

### Carregar dados no Streamlit:
```python
from streamlit.utils.data_loader import carregar_educacao_basica_inep

# Carrega dados de 2024
df = carregar_educacao_basica_inep(ano=2024)

# Forçar novo download
df = carregar_educacao_basica_inep(ano=2024, force_download=True)
```

### Usar o dicionário de dados:
```python
from inep import get_label, get_categorias, formatar_valor_categorico

# Obter descrição de uma variável
print(get_label('TP_DEPENDENCIA'))
# → "Dependência Administrativa"

# Obter valores possíveis
cats = get_categorias('TP_DEPENDENCIA')
# → {'1': 'Federal', '2': 'Estadual', '3': 'Municipal', '4': 'Privada'}

# Formatar valor
print(formatar_valor_categorico('TP_DEPENDENCIA', 1))
# → "1 - Federal"
```

### Listar variáveis por categoria:
```python
from inep import listar_variaveis_por_categoria, listar_categorias

# Ver todas as categorias
for cat_id, cat_label in listar_categorias():
    print(f"{cat_label}: {cat_id}")

# Ver variáveis de uma categoria
vars_internet = listar_variaveis_por_categoria('internet_computadores')
for var in vars_internet:
    print(f"  {var}: {get_label(var)}")
```

## 🗂️ Estrutura de Cache
```
data/
  cache/
    inep/
      2022/
        educacao-basica.parquet
      2023/
        educacao-basica.parquet
      2024/
        educacao-basica.parquet
```

## ✨ Recursos Implementados

1. **Download Inteligente**: Verifica cache antes de baixar
2. **Otimização de Dados**: Converte tipos e categoriza automaticamente
3. **Formato Eficiente**: Usa Parquet com compressão Snappy
4. **Metadados Completos**: 476 variáveis catalogadas
5. **Categorização Temática**: 11 categorias organizadas
6. **Valores Categóricos**: Parse automático de códigos e descrições
7. **Funções Helper**: Facilita uso dos metadados

## 🎯 Próximos Passos Sugeridos

1. Criar página Streamlit para visualizar dados do INEP
2. Adicionar filtros por categoria de variável
3. Criar visualizações de infraestrutura escolar
4. Análise de conectividade nas escolas
5. Comparativos entre regiões/estados/municípios

