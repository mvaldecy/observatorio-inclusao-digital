# Componente Explorador de Dados

## Descrição

O componente `explorador_dados` é um componente reutilizável criado para facilitar a exploração de datasets no Streamlit. Ele fornece uma interface completa e consistente para carregar, visualizar e analisar diferentes tipos de dados.

## Arquivos Criados

### 1. `/streamlit/components/explorador_dados.py`
Componente reutilizável com as seguintes funcionalidades:

- **Interface de Seleção**: Permite escolher entre diferentes tipos de dados
- **Carregamento Dinâmico**: Suporta qualquer função de carregamento de dados
- **4 Abas de Exploração**:
  - **Visão Geral**: Métricas gerais e informações das colunas
  - **Primeiras Linhas**: Visualização das primeiras N linhas (configurável)
  - **Estatísticas**: Estatísticas descritivas para colunas numéricas e categóricas
  - **Dados Completos**: Visualização completa com filtro de colunas e download

### 2. `/streamlit/pages/5_Explorar_Cobertura_Movel.py`
Página de exemplo que usa o componente para explorar dados de cobertura móvel da ANATEL:

- Cobertura Móvel (Geral)
- Cobertura 4G por UF
- Cobertura 5G por UF

## Como Usar o Componente

### Exemplo Básico

```python
from components.explorador_dados import explorador_dados
from utils.data_loader import carregar_seus_dados

# Configurar os tipos de dados
TIPOS_DADOS = {
    "Nome do Tipo 1": {
        "loader": funcao_carregamento_1,
        "descricao": "Descrição do tipo de dado 1"
    },
    "Nome do Tipo 2": {
        "loader": funcao_carregamento_2,
        "descricao": "Descrição do tipo de dado 2"
    }
}

# Usar o componente
explorador_dados(
    tipos_dados=TIPOS_DADOS,
    titulo="Título da Página",
    descricao="Descrição personalizada (opcional)",
    fonte="Nome da Fonte de Dados"
)
```

### Parâmetros

- **tipos_dados** (obrigatório): Dicionário com configurações dos tipos de dados
  - Chave: Nome do tipo de dado (str)
  - Valor: Dicionário com:
    - `loader`: Função que carrega os dados (deve retornar um DataFrame)
    - `descricao`: Descrição do tipo de dado (str)

- **titulo** (opcional): Título da página (padrão: "🔍 Exploração de Dados")

- **descricao** (opcional): Descrição personalizada em Markdown (padrão: descrição automática)

- **fonte** (opcional): Nome da fonte dos dados para o rodapé

## Funcionalidades do Componente

### Visão Geral
- Número total de linhas e colunas
- Uso de memória
- Tabela com informações de cada coluna (tipo, valores nulos, etc.)

### Primeiras Linhas
- Slider para escolher quantas linhas visualizar (5-100)
- Visualização em formato tabular

### Estatísticas
- Estatísticas descritivas para colunas numéricas
- Contagem de valores únicos para colunas categóricas
- Amostras dos valores categóricos

### Dados Completos
- Visualização de todo o dataset
- Filtro de colunas (multiselect)
- Download em CSV
- Download em Excel (se openpyxl estiver instalado)

## Vantagens

1. **Reutilizável**: Use o mesmo componente para diferentes tipos de dados
2. **Consistente**: Interface padronizada em todas as páginas
3. **Completo**: Fornece todas as visualizações necessárias para exploração inicial
4. **Flexível**: Aceita qualquer função de carregamento que retorne um DataFrame
5. **Manutenível**: Alterações no componente refletem em todas as páginas que o usam

## Próximos Passos

Você pode criar novas páginas de exploração simplesmente:

1. Criando um novo arquivo em `/streamlit/pages/`
2. Definindo os tipos de dados e funções de carregamento
3. Chamando o componente `explorador_dados`

Exemplo para criar uma página de exploração de dados do CETIC:

```python
from components.explorador_dados import explorador_dados
from utils.data_loader import carregar_domicilios_cetic, carregar_individuos_cetic

TIPOS_DADOS = {
    "Domicílios": {
        "loader": carregar_domicilios_cetic,
        "descricao": "Dados da pesquisa TIC Domicílios"
    },
    "Indivíduos": {
        "loader": carregar_individuos_cetic,
        "descricao": "Dados da pesquisa TIC Indivíduos"
    }
}

explorador_dados(
    tipos_dados=TIPOS_DADOS,
    titulo="Exploração de Dados CETIC",
    fonte="CETIC.br"
)
```

## Como Executar

Para rodar a aplicação Streamlit:

```bash
cd /home/marcos/PycharmProjects/observatorio-inclusao-digital
streamlit run streamlit/Home.py
```

Depois navegue até a página "Explorar Cobertura Móvel" no menu lateral.

