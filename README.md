# 📊 Observatório de Inclusão Digital

Aplicação de análise e visualização dos dados da pesquisa TIC (Tecnologias de Informação e Comunicação) realizada pelo CETIC.br.

## 🚀 Deploy

### Streamlit Cloud

Esta aplicação está configurada para deploy no Streamlit Cloud. Os arquivos necessários são:

- `requirements.txt` - Dependências Python
- `packages.txt` - Dependências do sistema (necessário para pyreadstat)
- `.streamlit/config.toml` - Configurações da aplicação

### Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## 📦 Instalação Local

```bash
# Clone o repositório
git clone <repo-url>
cd observatorio-inclusao-digital

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run streamlit/app.py
```

## 🗂️ Estrutura do Projeto

```
observatorio-inclusao-digital/
├── streamlit/              # Aplicação Streamlit
│   ├── app.py             # Página principal
│   ├── pages/             # Páginas da aplicação
│   ├── components/        # Componentes reutilizáveis
│   └── utils/             # Utilitários (data_loader, http_loader)
├── cetic/                 # Analisadores de dados CETIC
│   ├── domicilios/        # Análise de domicílios
│   └── individuos/        # Análise de indivíduos
├── data/                  # Dados e cache
│   └── cache/             # Cache HTTP dos dados
├── requirements.txt       # Dependências Python
├── packages.txt          # Dependências do sistema
└── .streamlit/           # Configurações Streamlit
    └── config.toml
```

## 🌐 Cache de Dados

A aplicação utiliza um sistema de cache HTTP para baixar e armazenar localmente os dados do CETIC.br:

- **Primeira execução**: Download automático dos dados
- **Execuções seguintes**: Uso do cache local em `data/cache/`
- **Atualização**: Botão "🔄 Atualizar" força novo download
- **Limpeza**: Botão "🗑️ Limpar Cache" remove dados locais

## 📊 Funcionalidades

### Comparativo Geográfico
- Visualização fixa de **Brasil | Nordeste | Piauí**
- Filtros adicionais aplicáveis
- Gráficos individuais por região
- Tabela comparativa consolidada
- Export CSV

### Análise Customizada
- Filtros totalmente personalizados
- Múltiplos indicadores disponíveis
- Visualizações interativas
- Export de dados

## 🔧 Desenvolvimento

### Adicionar Novos Anos

Quando o CETIC lançar novos dados:

1. Edite `streamlit/utils/data_sources.py`
2. Adicione as URLs dos novos dados
3. A aplicação detectará automaticamente o novo ano

### Adicionar Novos Indicadores

1. Edite `streamlit/components/categorias_cetic.py`
2. Adicione o novo indicador na categoria apropriada
3. Os gráficos serão gerados automaticamente

## 📝 Licença

[Adicione informações de licença aqui]

## 👥 Autores

[Adicione informações dos autores aqui]

## 🙏 Agradecimentos

Dados fornecidos pelo [CETIC.br - Centro Regional de Estudos para o Desenvolvimento da Sociedade da Informação](https://cetic.br/)

