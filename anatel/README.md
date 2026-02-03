# Analisador ANATEL

Módulo de análise de dados da ANATEL (Agência Nacional de Telecomunicações) para conectividade escolar.

## 📋 Estrutura

```
anatel/
├── __init__.py              # Inicialização do módulo
├── analisador_anatel.py     # Classe principal AnalisadorAnatel
├── exemplo_uso.py           # Exemplos de uso
└── README.md               # Esta documentação
```

## 🚀 Uso no Streamlit

### Importar e Criar Analisador

```python
from utils.data_loader import get_analisador_anatel

# Carrega analisador com dados de 2024
analisador = get_analisador_anatel(ano=2024)
```

### Métodos Disponíveis

#### Resumo e Informações

```python
# Resumo geral dos dados
resumo = analisador.resumo_geral()
# Retorna: {'total_registros': N, 'total_colunas': M, 'ano': 2024, 'colunas': [...]}

# Listar colunas disponíveis
colunas = analisador.get_colunas()

# Obter DataFrame atual
df = analisador.get_dataframe()
```

#### Filtragem de Dados

```python
# Filtrar por UF
analisador.filtrar_por_uf('PI')  # Uma UF
analisador.filtrar_por_uf('PI', 'CE', 'BA')  # Múltiplas UFs

# Filtrar por região
analisador.filtrar_por_regiao('NORDESTE')

# Filtrar por localização
analisador.filtrar_por_localizacao('URBANA')
analisador.filtrar_por_localizacao('RURAL')

# Filtro genérico (por qualquer coluna)
analisador.filtrar(UF='PI', LOCALIZACAO='URBANA')

# Resetar todos os filtros
analisador.reset_filtros()
```

#### Análises Estatísticas

```python
# Distribuição por região
regioes = analisador.escolas_por_regiao()

# Distribuição por UF (top 10)
ufs = analisador.escolas_por_uf(top=10)

# Contar valores únicos de uma coluna
contagem = analisador.contar_por('REGIAO')

# Distribuição percentual
dist = analisador.distribuicao_percentual('UF', top=10)
# Retorna DataFrame com: Valor, Contagem, Percentual, Percentual_Formatado

# Agrupar por múltiplas colunas
grupos = analisador.agrupar_por('REGIAO', 'LOCALIZACAO')

# Comparar urbano x rural
comparacao = analisador.comparar_localizacao('COLUNA_NUMERICA')
# Retorna: Localização, Total, Média, Mediana
```

## 📊 Exemplo Completo no Streamlit

```python
import streamlit as st
from utils.data_loader import get_analisador_anatel, get_anos_disponiveis_anatel

# Seletor de ano
anos = get_anos_disponiveis_anatel()
ano_selecionado = st.sidebar.selectbox("Ano", anos)

# Carrega analisador
analisador = get_analisador_anatel(ano=ano_selecionado)

# Exibe resumo
resumo = analisador.resumo_geral()
st.metric("Total de Escolas", f"{resumo['total_registros']:,}")

# Filtro por região no sidebar
regiao = st.sidebar.selectbox("Região", ["Todas", "Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"])

if regiao != "Todas":
    analisador.filtrar_por_regiao(regiao)
    st.info(f"Filtrando por: {regiao}")

# Análise por UF
st.subheader("Escolas por UF")
ufs = analisador.escolas_por_uf(top=10)
st.dataframe(ufs)
st.bar_chart(ufs.set_index('Valor')['Contagem'])

# Comparação urbano x rural
st.subheader("Urbano x Rural")
comparacao = analisador.comparar_localizacao('ALGUMA_COLUNA')
st.dataframe(comparacao)
```

## 🔧 Uso Standalone (Fora do Streamlit)

```python
import pandas as pd
from anatel.analisador_anatel import AnalisadorAnatel

# Carrega DataFrame manualmente
df = pd.read_parquet('data/cache/anatel/2024/conectividade-escola.parquet')

# Cria analisador
analisador = AnalisadorAnatel(df=df, ano=2024)

# Usa os métodos
print(analisador.resumo_geral())
print(analisador.escolas_por_regiao())

# Aplica filtros
analisador.filtrar_por_uf('PI')
analisador.filtrar_por_localizacao('RURAL')

print(f"Total de escolas rurais no PI: {len(analisador.df):,}")
```

## 📝 Métodos Principais

| Método | Descrição | Retorno |
|--------|-----------|---------|
| `filtrar_por_uf(*ufs)` | Filtra por UF(s) | DataFrame |
| `filtrar_por_regiao(regiao)` | Filtra por região | DataFrame |
| `filtrar_por_localizacao(loc)` | Filtra por urbano/rural | DataFrame |
| `filtrar(**kwargs)` | Filtro genérico por coluna | DataFrame |
| `reset_filtros()` | Remove todos os filtros | DataFrame |
| `resumo_geral()` | Resumo estatístico | Dict |
| `escolas_por_regiao()` | Distribuição por região | DataFrame |
| `escolas_por_uf(top)` | Distribuição por UF | DataFrame |
| `contar_por(coluna, top)` | Conta valores únicos | Series |
| `distribuicao_percentual(coluna, top)` | Distribuição com % | DataFrame |
| `agrupar_por(*colunas)` | Agrupa por colunas | DataFrame |
| `comparar_localizacao(coluna)` | Compara urbano x rural | DataFrame |
| `get_dataframe()` | Retorna DataFrame atual | DataFrame |
| `get_colunas()` | Lista colunas | List |

## 🎯 Diferenças do CETIC

O AnalisadorAnatel é **mais simples** que os analisadores CETIC porque:

1. **Sem metadados SPSS**: ANATEL usa CSV/Parquet, não tem metadados complexos
2. **Busca flexível**: Encontra colunas por nome aproximado (ex: busca por "UF" encontra "SIGLA_UF")
3. **Filtros por nome**: Usa nomes de colunas diretamente, não precisa de classe de metadados
4. **Foco em análise geográfica**: Métodos específicos para UF, região, urbano/rural

## 🔄 Anos Disponíveis

```python
from utils.data_loader import get_anos_disponiveis_anatel

anos = get_anos_disponiveis_anatel('conectividade-escola')
# Retorna: [2025, 2024, 2023, 2022]
```

## 💾 Cache

O analisador usa `@st.cache_resource` para manter uma única instância por ano, economizando memória e melhorando performance.

## 🐛 Tratamento de Erros

```python
try:
    analisador = get_analisador_anatel(ano=2024)
except ValueError as e:
    st.error(f"Erro ao carregar dados: {e}")
```

## 📚 Referências

- **data_loader.py**: Funções de carregamento HTTP
- **http_loader.py**: Download e cache de dados
- **data_sources.py**: URLs e configuração de fontes
