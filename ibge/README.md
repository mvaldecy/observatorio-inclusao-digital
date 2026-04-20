# IBGE - Instituto Brasileiro de Geografia e Estatística

Módulo para análise de dados demográficos e socioeconômicos do Brasil.

## Dados Disponíveis

### Tabela 7336: Acesso à Internet
- **Período**: 2021-2024
- **Descrição**: Pessoas de 10 anos ou mais de idade, por acesso à Internet
- **Fonte**: PNAD Contínua (Pesquisa Nacional por Amostra de Domicílios Contínua)
- **Dimensões**: UF, Região, Localização (Urbana/Rural), Período

## Estrutura do Módulo

```
ibge/
├── __init__.py                  # Importações principais
├── analisador_tabela7336.py     # Analisador dos dados de acesso à Internet
├── metadados.py                 # Informações sobre os dados
├── utils.py                     # Funções utilitárias
└── README.md                    # Esta documentação
```

## Uso

### Carregamento via Streamlit (Recomendado)

```python
from streamlit.utils.data_loader import get_analisador_ibge

# Carrega o analisador
analisador = get_analisador_ibge()

# Filtra e analisa
analisador.filtrar_por_ano(2024)
analisador.filtrar_por_regiao('Sudeste')

# Obtém distribuição por UF
df_ufs = analisador.distribucao_por_uf()
```

### Uso Direto

```python
import pandas as pd
from ibge.analisador_tabela7336 import AnalisadorTabela7336

# Carrega o CSV
df = pd.read_csv('tabela7336.csv')

# Cria analisador
analisador = AnalisadorTabela7336(df)

# Usa métodos
analisador.filtrar_por_uf('SP')
df_filtrado = analisador.obtener_df()
```

## Métodos Disponíveis

### Filtros
- `filtrar_por_ano(ano)` - Filtra por ano
- `filtrar_por_uf(uf)` - Filtra por unidade federativa
- `filtrar_por_regiao(regiao)` - Filtra por região
- `filtrar_por_localizacao(localizacao)` - Filtra por urbana/rural
- `reset_filtros()` - Remove todos os filtros

### Análises
- `distribucao_por_uf()` - Agrupa dados por UF
- `distribucao_por_regiao()` - Agrupa dados por região
- `distribucao_urbano_rural()` - Compara urbano vs rural
- `evolucao_temporal(dimensao)` - Mostra evolução ao longo dos anos
- `resumo_estatistico()` - Estatísticas descritivas

### Utilitários
- `obtener_df()` - Retorna DataFrame atual
- `normalizar_nomes_colunas()` - Normaliza nomes das colunas
- `salvar_cache()` - Salva em cache
- `carregar_cache()` - Carrega do cache

## Integração com Streamlit

Os dados são automaticamente:
1. ✓ Baixados via HTTP
2. ✓ Armazenados em cache
3. ✓ Carregados via `data_loader.py`
4. ✓ Disponíveis em páginas Streamlit

## Padrão de Código

Este módulo segue os padrões estabelecidos por ANATEL e CETIC:
- Módulos pequenos e especializados (< 200 linhas)
- Métodos com responsabilidade única
- Cache local para melhor desempenho
- Integração com `data_loader.py` do Streamlit
