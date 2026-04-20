# Módulo PCD - Pessoas com Deficiência

Este módulo contém ferramentas para análise de dados de inclusão digital para pessoas com deficiência.

## Estrutura

```
pcd/
├── __init__.py              # Exporta classes principais
├── README.md                # Este arquivo
├── metadados.py             # Definições de campos e metadados
├── dicionario_dados.py      # Dicionário completo dos dados
├── conversor_xlsx.py        # Conversor de XLSX para formato cache
├── analisador_pcd.py        # Analisador principal dos dados
├── estatisticas.py          # Cálculos estatísticos e agregações
└── visualizacoes.py         # Helpers para gráficos e visualizações
```

## Uso Básico

### 1. Converter arquivo XLSX para cache

```python
from pcd.conversor_xlsx import ConversorXLSX

conversor = ConversorXLSX()
conversor.processar_arquivo('caminho/para/arquivo.xlsx')
```

### 2. Analisar dados

```python
from streamlit.utils.data_loader import get_analisador_pcd

# Em aplicações Streamlit (recomendado)
analisador = get_analisador_pcd(ano=2024)

# Filtros
analisador.filtrar_por_uf('SP')
analisador.filtrar_por_tipo_deficiencia('visual')

# Análises
stats = analisador.estatisticas_acesso_internet()
comparacao = analisador.comparar_com_populacao_geral()
```

### 3. Visualizar dados no Streamlit

Os dados são exibidos na página **"PCD - Inclusão Digital"** do painel Streamlit.

## Dados

Os dados são armazenados em cache no formato Parquet em:
```
data/cache/pcd/pcd_{ano}.parquet
```

## Funcionalidades

- ✅ Conversão de XLSX para formato otimizado
- ✅ Cache automático de dados
- ✅ Filtros por UF, região, tipo de deficiência
- ✅ Estatísticas de acesso à internet
- ✅ Comparações com população geral
- ✅ Análises temporais
- ✅ Visualizações interativas no Streamlit

## Dependências

- pandas
- openpyxl (para leitura de XLSX)
- streamlit
- plotly

## Contribuindo

Mantenha os arquivos pequenos e modulares:
- Cada arquivo deve ter uma responsabilidade única
- Máximo de ~200-300 linhas por arquivo
- Use imports relativos dentro do módulo
