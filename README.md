# 📊 Observatório de Inclusão Digital

Aplicação de análise e visualização dos dados da pesquisa TIC (Tecnologias de Informação e Comunicação) realizada pelo CETIC.br.

## 🚀 Deploy

### Opção 1 – Docker (recomendado para datasets grandes)

A forma mais confiável de rodar o app em produção é via Docker, pois os datasets são grandes e o Streamlit Cloud gratuito pode não ter memória suficiente.

```bash
# Build e start com docker-compose (inclui volume persistente para o cache)
docker-compose up -d

# Acesse em http://localhost:8501
```

### Opção 2 – Render.com (plataforma cloud com Docker)

1. Faça fork/push deste repositório para o GitHub
2. Crie uma conta em [render.com](https://render.com)
3. Clique em **New → Blueprint** e aponte para este repositório
4. O Render lerá o arquivo `render.yaml` e provisionará o serviço automaticamente
5. ⚠️ Escolha o plano **Standard (2 GB RAM)** para datasets grandes

### Opção 3 – Streamlit Cloud

Esta aplicação também pode ser implantada no Streamlit Cloud. Os arquivos necessários já estão configurados:

- `requirements.txt` – Dependências Python
- `packages.txt` – Dependências do sistema (necessário para pyreadstat)
- `.streamlit/config.toml` – Configurações do servidor

> **Atenção:** O plano gratuito do Streamlit Cloud tem limite de 1 GB de RAM. Com datasets grandes (arquivos CETIC .sav com centenas de MB), o app pode ser encerrado por falta de memória. Considere o Docker ou Render.com para maior estabilidade.

### Requisitos

- Python 3.11+
- Docker (para deploy em container)
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
streamlit run streamlit/Home.py
```

## 🗂️ Estrutura do Projeto

```
observatorio-inclusao-digital/
├── streamlit/              # Aplicação Streamlit
│   ├── Home.py            # Página principal (Home)
│   ├── pages/             # Páginas da aplicação
│   ├── components/        # Componentes reutilizáveis
│   └── utils/             # Utilitários (data_loader, http_loader)
├── cetic/                 # Analisadores de dados CETIC
│   ├── domicilios/        # Análise de domicílios
│   └── individuos/        # Análise de indivíduos
├── data/                  # Dados e cache
│   └── cache/             # Cache dos dados (parquet)
├── Dockerfile             # Imagem Docker para deploy
├── docker-compose.yml     # Orquestração local/produção
├── render.yaml            # Deploy no Render.com
├── requirements.txt       # Dependências Python
├── packages.txt           # Dependências do sistema
└── .streamlit/            # Configurações Streamlit
    └── config.toml
```

## 🌐 Cache de Dados

A aplicação utiliza um sistema de cache para baixar e armazenar localmente os dados:

- **Primeira execução**: Download automático dos dados (pode demorar alguns minutos)
- **Execuções seguintes**: Dados lidos do cache Parquet local em `data/cache/` (muito mais rápido)
- **Formato Parquet**: Após o primeiro download, os dados são convertidos de `.sav`/`.csv` para Parquet com compressão Snappy, reduzindo drasticamente o uso de memória e o tempo de leitura
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

