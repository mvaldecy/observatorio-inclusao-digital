# Componentes de Cobertura Móvel

Esta pasta contém os componentes modulares para a página de Cobertura Móvel da ANATEL.

## 📁 Estrutura

```
cobertura-movel/
├── __init__.py                      # Exporta os componentes principais
├── config.py                        # Configurações, CSS e constantes
├── utils.py                         # Funções auxiliares reutilizáveis
├── filtros.py                       # Componente de filtros de UF e município
├── comparativo_brasil.py            # Comparativo Brasil/Nordeste/Piauí
├── comparativo_urbano_rural.py      # Análise urbano × rural
├── analise_municipios.py            # Análise detalhada de municípios
└── tabs_analise.py                  # Tabs de ranking, gráficos e personalização
```

## 🎯 Componentes

### `config.py`
- **Responsabilidade:** Configurações iniciais da página
- **Funções:**
  - `aplicar_configuracoes()`: Aplica título, CSS customizado e layout
- **Constantes:**
  - `NE_UF`: Lista de estados do Nordeste
  - `CSS_CUSTOM`: Estilos CSS para a página

### `utils.py`
- **Responsabilidade:** Funções auxiliares reutilizáveis
- **Funções:**
  - `safe_unique(series)`: Retorna valores únicos limpos de uma Series

### `filtros.py`
- **Responsabilidade:** Gerenciamento de filtros da página
- **Funções:**
  - `renderizar_filtros()`: Renderiza os selectboxes de UF e município
  - `aplicar_filtros()`: Aplica os filtros selecionados ao DataFrame
  - `renderizar_resumo_filtros()`: Mostra resumo dos dados filtrados

### `comparativo_brasil.py`
- **Responsabilidade:** Comparativo Brasil, Nordeste e Piauí
- **Funções:**
  - `renderizar_comparativo_brasil()`: Renderiza toda a seção de comparativo
  - `_calcular_stats()`: Calcula estatísticas de uma região
  - `_renderizar_visao_geral()`: Renderiza cards de métricas
  - `_renderizar_grafico_comparativo()`: Renderiza gráfico de barras

### `comparativo_urbano_rural.py`
- **Responsabilidade:** Análise comparativa urbano × rural
- **Funções:**
  - `renderizar_comparativo_urbano_rural()`: Função principal
  - `_detectar_coluna_localizacao()`: Detecta coluna urbano/rural
  - `_padronizar_tipos_area()`: Padroniza valores para Urbano/Rural
  - `_renderizar_metricas_urbano_rural()`: Renderiza cards de métricas
  - `_renderizar_graficos_urbano_rural()`: Renderiza gráficos comparativos

### `analise_municipios.py`
- **Responsabilidade:** Análise detalhada de municípios de um UF
- **Funções principais:**
  - `renderizar_analise_municipios()`: Função principal que orquestra tudo
  - `_preparar_dados_uf()`: Filtra e prepara dados do UF
  - `_calcular_ranking_municipios()`: Calcula ranking por cobertura
  - `_renderizar_estatisticas_gerais()`: Métricas gerais (total, média, etc)
  - `_renderizar_analise_estatistica()`: Estatísticas descritivas e distribuição
  - `_renderizar_destaques()`: Top 10 e Bottom 10
  - `_renderizar_tabs_analise()`: Tabs com análises detalhadas

### `tabs_analise.py`
- **Responsabilidade:** Conteúdo das tabs de análise detalhada
- **Funções:**
  - `renderizar_tab_ranking()`: Tab com ranking completo e busca
  - `renderizar_tab_graficos()`: Tab com gráficos (top/bottom, histograma, boxplot)
  - `renderizar_tab_personalizado()`: Tab com destaques personalizáveis
  - `_renderizar_histograma()`: Histograma com cores e referências
  - `_renderizar_boxplot()`: Box plot estatístico com anotações

## 🔄 Fluxo de Execução

O arquivo principal `4_Cobertura_Movel.py` orquestra os componentes nesta ordem:

1. **Configuração inicial** → `aplicar_configuracoes()`
2. **Carregamento de dados** → `get_analisador_cobertura_movel()`
3. **Comparativo Brasil** → `renderizar_comparativo_brasil()` (não afetado por filtros)
4. **Filtros** → `renderizar_filtros()` e `aplicar_filtros()`
5. **Comparativo Urbano × Rural** → `renderizar_comparativo_urbano_rural()`
6. **Análise de Municípios** → `renderizar_analise_municipios()`
7. **Resumo de Filtros** → `renderizar_resumo_filtros()`

## 💡 Benefícios da Modularização

- **Manutenibilidade:** Cada componente tem uma responsabilidade clara
- **Reusabilidade:** Funções podem ser reutilizadas em outras páginas
- **Testabilidade:** Componentes podem ser testados individualmente
- **Legibilidade:** Arquivo principal passou de ~1466 para ~170 linhas
- **Organização:** Fácil encontrar e modificar funcionalidades específicas

## 🎨 Padrões de Design

### Nomenclatura
- Funções públicas: `renderizar_*` ou `aplicar_*`
- Funções privadas: `_renderizar_*` ou `_calcular_*` (prefixo `_`)

### Parâmetros comuns
- `df`: DataFrame com dados completos
- `info`: Dicionário com informações do analisador
- `col_cobertura_selecionada`: Coluna de cobertura em uso
- `selected_uf`: UF selecionada pelo usuário
- `selected_municipio`: Município selecionado pelo usuário

### Estrutura de funções de renderização
```python
def renderizar_componente(df, info, ...):
    """
    Renderiza um componente completo.
    
    Args:
        df: DataFrame com os dados
        info: Informações do analisador
        ...
    
    Returns:
        Opcional: dados processados ou None
    """
    # 1. Validações iniciais
    # 2. Processamento de dados
    # 3. Renderização usando st.* ou funções auxiliares
```

## 🔧 Como Adicionar Novos Componentes

1. Crie um novo arquivo `.py` nesta pasta
2. Defina uma função principal `renderizar_*`
3. Adicione funções auxiliares privadas com prefixo `_`
4. Importe e exporte no `__init__.py`
5. Use no arquivo principal `4_Cobertura_Movel.py`

## 📝 Exemplo de Uso

```python
from components.cobertura_movel import renderizar_comparativo_brasil

# No arquivo principal
renderizar_comparativo_brasil(df, info, col_cobertura_selecionada)
```

## 🐛 Debug

Cada componente inclui expanders de debug quando apropriado:
- `comparativo_urbano_rural.py`: Debug de colunas disponíveis
- `analise_municipios.py`: Debug de dados brutos e ranking calculado

## 📚 Documentação

Todas as funções incluem docstrings com:
- Descrição clara do propósito
- Lista de parâmetros (Args)
- Retorno esperado (Returns) quando aplicável

---

**Última atualização:** 2026-02-11
**Autor:** Vicente
**Versão:** 1.0.0
