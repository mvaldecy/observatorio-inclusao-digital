"""
Exemplo de uso do AnalisadorINEP
Demonstra filtros, agregadores e análise de indicadores
"""

print("=" * 80)
print("EXEMPLO DE USO DO ANALISADOR INEP")
print("=" * 80)

print("""
IMPORTANTE: Este exemplo mostra como usar o AnalisadorINEP.
Para rodar, você precisa ter os dados carregados via data_loader.

# =============================================================================
# 1. IMPORTAR E CARREGAR DADOS
# =============================================================================

from streamlit.utils.data_loader import get_analisador_inep
from inep import get_label, get_valores, formatar_valor

# Criar analisador para 2024
analisador = get_analisador_inep(ano=2024)

# =============================================================================
# 2. FILTRAR DADOS
# =============================================================================

# Filtrar escolas públicas do Piauí (UF=22)
analisador.filtrar_dados(CO_UF=22, TP_DEPENDENCIA=[1, 2, 3])
# Resultado: Escolas federais, estaduais e municipais do Piauí

# Filtrar escolas rurais com internet
analisador.filtrar_dados(TP_LOCALIZACAO=2, IN_INTERNET=1)
# Resultado: Escolas rurais que têm internet

# Filtrar por múltiplos critérios
analisador.filtrar_dados(
    CO_UF=22,                    # Piauí
    TP_DEPENDENCIA=3,            # Municipal
    TP_LOCALIZACAO=2,            # Rural
    IN_LABORATORIO_INFORMATICA=1 # Com laboratório
)

# =============================================================================
# 3. ANALISAR INDICADORES ÚNICOS
# =============================================================================

# Análise de acesso à internet
resultado = analisador.analisar_indicador('IN_INTERNET')
print(resultado)
# Output:
#   Descrição       Total  Percentual
#   Não             1234   45.60%
#   Sim             1472   54.40%

# Análise de dependência administrativa
resultado = analisador.analisar_indicador('TP_DEPENDENCIA')
print(resultado)
# Output:
#   Descrição       Total  Percentual
#   Federal         10     0.37%
#   Estadual        250    9.25%
#   Municipal       2200   81.48%
#   Privada         240    8.89%

# =============================================================================
# 4. ANALISAR MÚLTIPLOS INDICADORES
# =============================================================================

indicadores_internet = [
    'IN_INTERNET',
    'IN_BANDA_LARGA',
    'IN_LABORATORIO_INFORMATICA',
    'IN_INTERNET_ALUNOS',
    'IN_INTERNET_APRENDIZAGEM'
]

resultado = analisador.analisar_indicador(indicadores_internet)
print(resultado)
# Output:
#   Indicador                    Descrição                              Total  Percentual
#   IN_INTERNET                  Acesso à Internet                      1472   54.40%
#   IN_BANDA_LARGA              Banda larga                            1200   44.40%
#   IN_LABORATORIO_INFORMATICA  Laboratório de informática             890    32.90%
#   IN_INTERNET_ALUNOS          Internet para uso dos alunos           1350   49.90%
#   IN_INTERNET_APRENDIZAGEM    Internet para ensino e aprendizagem    1280   47.30%

# =============================================================================
# 5. ANÁLISE POR AGREGADOR
# =============================================================================

# Analisar acesso à internet por dependência administrativa
resultado = analisador.analisar_por_agregador(
    indicador='IN_INTERNET',
    campo_agregador='TP_DEPENDENCIA'
)
print(resultado)
# Output:
#   Dependência Administrativa  Agregador_Valor  Total_Grupo  Categoria  Total  Percentual
#   Federal                     1                10           Sim        9      90.0%
#   Federal                     1                10           Não        1      10.0%
#   Estadual                    2                250          Sim        200    80.0%
#   Estadual                    2                250          Não        50     20.0%
#   Municipal                   3                2200         Sim        1100   50.0%
#   Municipal                   3                2200         Não        1100   50.0%

# Analisar múltiplos indicadores por localização
resultado = analisador.analisar_por_agregador(
    indicador=['IN_INTERNET', 'IN_BANDA_LARGA', 'IN_LABORATORIO_INFORMATICA'],
    campo_agregador='TP_LOCALIZACAO'
)
print(resultado)

# Analisar por UF (estados)
resultado = analisador.analisar_por_agregador(
    indicador='IN_INTERNET',
    campo_agregador='CO_UF'
)
# Útil para comparar estados

# =============================================================================
# 6. ANÁLISES ESPECÍFICAS
# =============================================================================

# Análise rápida de acesso à internet (com filtros)
resultado = analisador.analisar_acesso_internet(
    CO_UF=22,
    TP_LOCALIZACAO=2
)
print(resultado)

# Resumo de infraestrutura tecnológica
resumo = analisador.resumo_infraestrutura(CO_UF=22)
print(resumo)
# Output:
#   Indicador                    Descrição                         Total  Percentual
#   IN_INTERNET                  Acesso à Internet                 1472   54.40%
#   IN_LABORATORIO_INFORMATICA  Laboratório de informática        890    32.90%
#   IN_BANDA_LARGA              Banda larga                       1200   44.40%
#   IN_INTERNET_ALUNOS          Internet para uso dos alunos      1350   49.90%
#   IN_INTERNET_APRENDIZAGEM    Internet para aprendizagem        1280   47.30%

# =============================================================================
# 7. USANDO METADADOS
# =============================================================================

from inep import get_label, get_valores, formatar_valor

# Obter descrição de uma variável
print(get_label('TP_DEPENDENCIA'))
# Output: "Dependência Administrativa"

# Obter valores possíveis
valores = get_valores('TP_LOCALIZACAO')
print(valores)
# Output: {'1': 'Urbana', '2': 'Rural'}

# Formatar valor para exibição
print(formatar_valor('TP_DEPENDENCIA', 3))
# Output: "3 - Municipal"

# =============================================================================
# 8. ENCADEAMENTO DE OPERAÇÕES
# =============================================================================

# Criar novo analisador
from streamlit.utils.data_loader import carregar_educacao_basica_inep
from inep import AnalisadorINEP

df = carregar_educacao_basica_inep(ano=2024)
analisador = AnalisadorINEP(df=df, ano=2024)

# Encadear filtros e análises
resultado = (
    analisador
    .filtrar_dados(CO_UF=22, TP_LOCALIZACAO=2)
    .analisar_por_agregador('IN_INTERNET', 'TP_DEPENDENCIA')
)
print(resultado)

# =============================================================================
# 9. CASOS DE USO COMUNS
# =============================================================================

# Caso 1: Comparar zonas urbana e rural
analisador_novo = AnalisadorINEP(df=df, ano=2024)
resultado_urbano_rural = analisador_novo.analisar_por_agregador(
    indicador=['IN_INTERNET', 'IN_BANDA_LARGA'],
    campo_agregador='TP_LOCALIZACAO'
)

# Caso 2: Análise por região
resultado_regiao = analisador_novo.analisar_por_agregador(
    indicador='IN_LABORATORIO_INFORMATICA',
    campo_agregador='CO_REGIAO'
)

# Caso 3: Escolas privadas vs públicas
analisador_novo.filtrar_dados(CO_UF=22)
resultado_dep = analisador_novo.analisar_por_agregador(
    indicador=['IN_INTERNET', 'QT_DESKTOP_ALUNO'],
    campo_agregador='TP_DEPENDENCIA'
)

# Caso 4: Análise temporal (comparar anos)
analisador_2023 = get_analisador_inep(ano=2023)
analisador_2024 = get_analisador_inep(ano=2024)

resultado_2023 = analisador_2023.analisar_indicador('IN_INTERNET')
resultado_2024 = analisador_2024.analisar_indicador('IN_INTERNET')

print("Evolução 2023-2024:")
print(resultado_2023)
print(resultado_2024)

# =============================================================================
# 10. RENOMEAR COLUNAS PARA EXIBIÇÃO
# =============================================================================

# Renomear colunas com labels legíveis
analisador.renomear_colunas_com_labels()
# Agora as colunas têm nomes como "Dependência Administrativa" ao invés de "TP_DEPENDENCIA"

print(analisador.df.columns[:10])
# Output: ['Ano do Censo', 'Nome da Região', 'Código da UF', ...]

""")

print("\n" + "=" * 80)
print("✓ Este exemplo mostra todas as funcionalidades do AnalisadorINEP")
print("=" * 80)

