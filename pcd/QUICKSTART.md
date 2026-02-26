# 🚀 Guia Rápido - Módulo PCD

Este guia mostra como usar o módulo PCD (Pessoas com Deficiência) para análise de dados de inclusão digital.

## 📋 Índice

1. [Instalação de Dependências](#instalação-de-dependências)
2. [Converter Arquivo XLSX](#converter-arquivo-xlsx)
3. [Executar Streamlit](#executar-streamlit)
4. [Uso em Scripts Python](#uso-em-scripts-python)
5. [Estrutura dos Dados](#estrutura-dos-dados)
6. [Solução de Problemas](#solução-de-problemas)

---

## 📦 Instalação de Dependências

Certifique-se de ter as dependências instaladas:

```bash
pip install pandas openpyxl pyarrow streamlit plotly
```

Ou use o arquivo de requirements do projeto:

```bash
pip install -r requirements.txt
```

---

## 🔄 Converter Arquivo XLSX

### Opção 1: Usando script de linha de comando

```bash
# Converter arquivo único
python pcd/converter_dados.py caminho/para/arquivo.xlsx 2024

# Converter múltiplas planilhas
python pcd/converter_dados.py caminho/para/arquivo.xlsx 2024 --multiplas

# Converter planilha específica
python pcd/converter_dados.py caminho/para/arquivo.xlsx 2024 --sheet "Nome da Planilha"
```

### Opção 2: Usando Python diretamente

```python
from pcd.conversor_xlsx import converter_xlsx

# Converter arquivo
converter_xlsx('caminho/para/arquivo.xlsx', ano=2024)
```

### Opção 3: Converter múltiplas planilhas

```python
from pcd.conversor_xlsx import ConversorXLSX

conversor = ConversorXLSX()
resultados = conversor.processar_multiplas_planilhas(
    'caminho/para/arquivo.xlsx',
    ano=2024
)
```

**Importante:** Os arquivos convertidos serão salvos em:
```
data/cache/pcd/pcd_2024.parquet
```

---

## 🚀 Executar Streamlit

Após converter os dados, execute o Streamlit:

```bash
streamlit run streamlit/Home.py
```

No navegador, acesse a página **"PCD - Inclusão Digital"** no menu lateral.

---

## 🐍 Uso em Scripts Python

### Análise básica

```python
from pcd.analisador_pcd import AnalisadorPCD
import pandas as pd

# Carregar dados do cache
df = pd.read_parquet('data/cache/pcd/pcd_2024.parquet')

# Criar analisador
analisador = AnalisadorPCD(df=df, ano=2024)

# Aplicar filtros
analisador.filtrar_por_uf('SP')
analisador.filtrar_por_tipo_deficiencia('visual')

# Obter dados filtrados
dados = analisador.get_dados_atuais()
print(f"Total de registros: {len(dados)}")
```

### Gerar estatísticas

```python
from pcd.estatisticas import EstatisticasPCD

# Criar objeto de estatísticas
stats = EstatisticasPCD(df)

# Percentual de acesso à internet
print(f"Acesso: {stats.percentual_acesso_internet():.1f}%")

# Acesso por tipo de deficiência
acesso_tipo = stats.acesso_por_tipo_deficiencia()
print(acesso_tipo)

# Principais barreiras
barreiras = stats.principais_barreiras(top_n=5)
print(barreiras)

# Resumo completo
resumo = stats.resumo_geral()
print(resumo)
```

### Criar visualizações

```python
from pcd.visualizacoes import VisualizadorPCD

viz = VisualizadorPCD()

# Criar gráfico de barras
fig = viz.grafico_barras_horizontais(
    dispositivos,
    titulo="Distribuição de Dispositivos"
)
fig.show()  # Abre no navegador

# Gauge de percentual
fig = viz.grafico_percentual_acesso(75.5, titulo="Acesso à Internet")
fig.show()
```

### Uso em Streamlit

```python
import streamlit as st
from streamlit.utils.data_loader import get_analisador_pcd
from pcd.estatisticas import EstatisticasPCD
from pcd.visualizacoes import VisualizadorPCD

# Carregar com cache automático
analisador = get_analisador_pcd(ano=2024)
df = analisador.get_dados_atuais()

# Estatísticas
stats = EstatisticasPCD(df)
viz = VisualizadorPCD()

# Exibir métrica
st.metric("Acesso à Internet", f"{stats.percentual_acesso_internet():.1f}%")

# Exibir gráfico
fig = viz.grafico_barras_simples(stats.distribuicao_dispositivos())
st.plotly_chart(fig, use_container_width=True)
```

---

## 📊 Estrutura dos Dados

### Campos principais esperados

O módulo espera dados com as seguintes colunas (nem todas são obrigatórias):

**Identificação:**
- `id`, `ano`

**Localização:**
- `uf`, `regiao`, `municipio`, `area` (urbana/rural)

**Deficiência:**
- `tem_deficiencia`, `tipo_deficiencia`, `grau_deficiencia`

**Acesso:**
- `tem_internet`, `tem_computador`, `tem_smartphone`, `tem_tablet`
- `tipo_conexao`, `velocidade_internet`, `frequencia_uso`

**Uso:**
- `usa_redes_sociais`, `usa_servicos_gov`, `usa_ecommerce`, `usa_educacao`, `usa_trabalho`

**Acessibilidade:**
- `usa_tecnologia_assistiva`, `tipo_tecnologia_assistiva`
- `encontra_barreiras`, `tipo_barreira`

**Demografia:**
- `idade`, `faixa_etaria`, `sexo`, `escolaridade`, `renda_familiar`

### Formato esperado

- Colunas com nomes em minúsculas, separadas por underscore
- Valores booleanos para campos sim/não (`True`/`False`)
- Categorias como strings (ex: 'visual', 'auditiva', etc)

O conversor XLSX normaliza automaticamente os nomes das colunas.

---

## 🔧 Solução de Problemas

### Erro: "Nenhum dado PCD encontrado"

**Causa:** Não há arquivos `.parquet` na pasta `data/cache/pcd/`

**Solução:** 
1. Converta seu arquivo XLSX usando o conversor
2. Verifique se o arquivo foi criado em `data/cache/pcd/`

### Erro: "Coluna não encontrada"

**Causa:** Seu arquivo XLSX não contém todas as colunas esperadas

**Solução:** 
- O módulo é flexível e funciona com subconjuntos de colunas
- Análises que dependem de colunas ausentes serão ignoradas automaticamente
- Verifique os nomes das colunas no seu arquivo XLSX

### Arquivo XLSX muito grande

**Solução:**
- Use o formato Parquet (mais eficiente)
- Filtre dados desnecessários antes de converter
- Divida em múltiplos arquivos por ano

### Gráficos não aparecem no Streamlit

**Solução:**
- Use `st.plotly_chart(fig, use_container_width=True)`
- Certifique-se de que plotly está instalado
- Verifique se há dados suficientes para o gráfico

---

## 📚 Arquivos Importantes

```
pcd/
├── README.md              # Documentação completa
├── QUICKSTART.md          # Este arquivo (guia rápido)
├── exemplo_uso.py         # Exemplos de código
├── converter_dados.py     # Script de conversão
├── conversor_xlsx.py      # Módulo de conversão
├── analisador_pcd.py      # Analisador principal
├── estatisticas.py        # Cálculos estatísticos
├── visualizacoes.py       # Gráficos e visualizações
├── metadados.py           # Definições de campos
└── dicionario_dados.py    # Dicionário completo
```

---

## 🆘 Precisa de Ajuda?

1. Consulte o [README.md](README.md) completo
2. Execute `python pcd/exemplo_uso.py` para ver exemplos
3. Verifique a documentação nos próprios arquivos Python (docstrings)

---

## ✨ Exemplo Completo

```python
# 1. Converter arquivo XLSX
from pcd.conversor_xlsx import converter_xlsx
converter_xlsx('dados_pcd_2024.xlsx', ano=2024)

# 2. Carregar e analisar
import pandas as pd
from pcd.analisador_pcd import AnalisadorPCD
from pcd.estatisticas import EstatisticasPCD

df = pd.read_parquet('data/cache/pcd/pcd_2024.parquet')
analisador = AnalisadorPCD(df=df, ano=2024)

# 3. Filtrar
analisador.filtrar_por_regiao('Sudeste')
analisador.filtrar_com_internet(True)

# 4. Estatísticas
stats = EstatisticasPCD(analisador.get_dados_atuais())
print(f"Acesso: {stats.percentual_acesso_internet():.1f}%")

# 5. Visualizar no Streamlit
# streamlit run streamlit/Home.py
```

---

**Pronto! Você está pronto para usar o módulo PCD! 🎉**
