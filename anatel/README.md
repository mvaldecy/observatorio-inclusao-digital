# Analisador ANATEL

Módulo de análise de dados da ANATEL (Agência Nacional de Telecomunicações) para conectividade escolar e cobertura móvel.

## 📚 Documentação

- **[GUIA_ESTATISTICAS.md](GUIA_ESTATISTICAS.md)** - Guia completo sobre análise estatística de cobertura móvel
- **[exemplo_analise_estatistica.py](exemplo_analise_estatistica.py)** - Exemplos práticos de análise
- **[exemplo_uso.py](exemplo_uso.py)** - Exemplos básicos de uso
- **[dicionario_dados.py](dicionario_dados.py)** - Dicionário de metadados das colunas
- **[exemplo_uso_dicionario.py](exemplo_uso_dicionario.py)** - Exemplos de uso do dicionário de dados

## 📋 Estrutura

```
anatel/
├── __init__.py                      # Inicialização do módulo
├── analisador_anatel.py             # Análise de dados escolares
├── analisador_cobertura_movel.py    # Análise de cobertura móvel
├── municipios_ibge.py               # Mapeamento de códigos IBGE
├── dicionario_dados.py              # Dicionário de metadados (labels das colunas)
├── exemplo_uso.py                   # Exemplos básicos
├── exemplo_uso_dicionario.py        # Exemplos de uso do dicionário
├── exemplo_analise_estatistica.py   # Exemplos de análise estatística
├── GUIA_ESTATISTICAS.md            # Guia didático de estatísticas
└── README.md                        # Esta documentação
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

## 📖 Dicionário de Dados

O módulo `dicionario_dados.py` fornece metadados para todas as 81 colunas dos dados da ANATEL, similar ao padrão usado nos dados CETIC.

### Funções Disponíveis

```python
from anatel.dicionario_dados import (
    obter_label,
    obter_valor_label,
    eh_coluna_binaria,
    eh_coluna_numerica,
    listar_colunas_por_tipo,
    COLUNAS,
    VALORES
)

# Obter descrição de uma coluna
label = obter_label('CONECT_POSSUI_INTERNET')
# Retorna: "Indica se possui acesso à internet"

# Obter label de um valor
uf_nome = obter_valor_label('SG_UF', 'PI')
# Retorna: "Piauí"

# Verificar tipo de coluna
if eh_coluna_binaria('ESCOLAS_CONECTADAS'):
    print("Esta é uma coluna de Sim/Não")

# Listar colunas por tipo
binarias = listar_colunas_por_tipo('binarias')  # 34 colunas
numericas = listar_colunas_por_tipo('numericas')  # 18 colunas
coordenadas = listar_colunas_por_tipo('coordenadas')  # 2 colunas
```

### Categorias de Colunas

- **Identificação**: COD_INEP, NO_ENTIDADE
- **Localização**: UF, município, região, latitude/longitude
- **Tipo de escola**: dependência administrativa, localização urbana/rural
- **Dados escolares**: matrículas, turmas, docentes
- **Energia**: tipos de energia, adequação
- **Conectividade**: acesso, cobertura, adequação
- **Programas**: ENEC, EACE, FUST, GESAC, PBLE, RNP, etc
- **Velocidades**: velocidades contratadas e medidas
- **Monitoramento**: NIC.br, quantidade de programas

### Uso com Streamlit

```python
import streamlit as st
from anatel.dicionario_dados import obter_label, listar_colunas_por_tipo

# Criar seletor de indicadores com labels descritivas
colunas_binarias = listar_colunas_por_tipo('binarias')
labels_dict = {col: obter_label(col) for col in colunas_binarias}

indicador = st.selectbox(
    "Selecione o indicador",
    options=colunas_binarias,
    format_func=lambda x: labels_dict[x]
)
```

## 🎯 Diferenças do CETIC

O AnalisadorAnatel é **mais simples** que os analisadores CETIC porque:

1. **Sem metadados SPSS**: ANATEL usa CSV/Parquet, não tem metadados complexos
2. **Busca flexível**: Encontra colunas por nome aproximado (ex: busca por "UF" encontra "SIGLA_UF")
3. **Filtros por nome**: Usa nomes de colunas diretamente, não precisa de classe de metadados
4. **Foco em análise geográfica**: Métodos específicos para UF, região, urbano/rural
5. **Dicionário de dados**: Agora possui dicionário similar ao CETIC para padronizar labels

## 🔄 Anos Disponíveis

```python
from utils.data_loader import get_anos_disponiveis_anatel

anos = get_anos_disponiveis_anatel('conectividade-escola')
# Retorna: [2025, 2024, 2023, 2022]
```

## 💾 Cache

O analisador usa `@st.cache_resource` para manter uma única instância por ano, economizando memória e melhorando performance.

## � Análise de Cobertura Móvel

### Uso Básico

```python
from utils.data_loader import get_analisador_cobertura_movel

# Carrega analisador de cobertura móvel
analisador = get_analisador_cobertura_movel()

# Ranking de cobertura
resultado = analisador.ranking_cobertura(top_n=10, bottom_n=10)

# Acessa os resultados
print("Top 10 municípios:")
print(resultado['top'])

print("\nEstatísticas:")
stats = resultado['estatisticas']
print(f"Média: {stats['cobertura_media']:.2f}%")
print(f"Mediana: {stats['cobertura_mediana']:.2f}%")
print(f"Desvio Padrão: {stats['desvio_padrao']:.2f}%")

# Distribuição por faixas
print("\nDistribuição:")
for faixa, qtd in stats['distribuicao'].items():
    perc = stats['distribuicao_percentual'][faixa]
    print(f"{faixa}: {qtd} municípios ({perc}%)")
```

### Análise por Estado

```python
# Ranking apenas do Piauí
resultado_pi = analisador.ranking_cobertura(por_uf='PI', top_n=5, bottom_n=5)

# Resumo estatístico por UF
resumo_ufs = analisador.obter_resumo_por_uf()
print(resumo_ufs)
```

### Distribuição de Cobertura

```python
# Distribuição nacional
dist = analisador.obter_distribuicao_cobertura()

# Distribuição por estado
dist_pi = analisador.obter_distribuicao_cobertura(por_uf='PI')

print(dist)
# Faixa de Cobertura | Quantidade de Municípios | Percentual (%)
# Sem cobertura      | 150                      | 15.0%
# Muito Baixa        | 200                      | 20.0%
# ...
```

### Interpretação Automática

```python
# Gera interpretação em linguagem clara
interpretacao = analisador.interpretar_estatisticas(stats)
print(interpretacao)

# Exemplo de saída:
# ✅ Boa cobertura média (65.5%) - Nível satisfatório de conectividade
# 
# ⚠️ Desigualdade positiva - Poucos municípios com alta cobertura elevam a média
# 
# 🟡 Variação moderada (18.2%) - Alguma desigualdade na distribuição
```

### 📖 Entendendo as Estatísticas

Para uma explicação completa e didática sobre as métricas estatísticas, consulte:
- **[GUIA_ESTATISTICAS.md](GUIA_ESTATISTICAS.md)** - Guia completo com exemplos práticos
- **[exemplo_analise_estatistica.py](exemplo_analise_estatistica.py)** - Código de exemplo

**Resumo rápido:**
- **Média**: Cobertura média de todos os municípios (pode ser influenciada por extremos)
- **Mediana**: Valor do meio - metade tem mais, metade tem menos (mais resistente a extremos)
- **Desvio Padrão**: Mede a desigualdade - quanto maior, mais heterogênea é a cobertura
- **Distribuição**: Mostra quantos municípios estão em cada faixa de conectividade

**Dica importante:** Sempre analise MÉDIA + MEDIANA + DESVIO juntos para ter uma visão completa!

## �🐛 Tratamento de Erros

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
