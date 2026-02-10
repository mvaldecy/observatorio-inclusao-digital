"""
Exemplo de uso do Analisador de Cobertura Móvel
Demonstra como fazer análises estatísticas e interpretar os resultados
"""

from analisador_cobertura_movel import AnalisadorCoberturaMovel
import pandas as pd

def exemplo_analise_completa():
    """
    Exemplo completo de análise estatística de cobertura móvel
    """
    print("=" * 60)
    print("📊 EXEMPLO DE ANÁLISE ESTATÍSTICA DE COBERTURA MÓVEL")
    print("=" * 60)
    
    # Supondo que você já tenha um DataFrame com dados de cobertura
    # df = pd.read_csv('dados_cobertura.csv')
    # analisador = AnalisadorCoberturaMovel(df)
    
    print("\n" + "=" * 60)
    print("1️⃣ ANÁLISE NACIONAL")
    print("=" * 60)
    
    # Gera ranking com análise estatística completa
    # resultado = analisador.ranking_cobertura(top_n=10, bottom_n=10)
    
    # Estatísticas gerais
    print("\n📊 ESTATÍSTICAS GERAIS")
    print("-" * 60)
    # stats = resultado['estatisticas']
    # print(f"Total de municípios: {stats['total_municipios']:,}")
    # print(f"Cobertura Média: {stats['cobertura_media']:.2f}%")
    # print(f"Mediana: {stats['cobertura_mediana']:.2f}%")
    # print(f"Máxima: {stats['cobertura_max']:.2f}%")
    # print(f"Mínima: {stats['cobertura_min']:.2f}%")
    # print(f"Desvio Padrão: {stats['desvio_padrao']:.2f}%")
    
    print("""
    📖 O QUE CADA MÉTRICA SIGNIFICA:
    
    → Média: Soma de todas as coberturas dividida pelo número de municípios
      Útil para ter uma noção geral, mas pode ser influenciada por valores extremos
    
    → Mediana: O valor que está no meio quando ordenamos todos os municípios
      Mais resistente a valores extremos que a média
    
    → Desvio Padrão: Mede o quanto os valores se afastam da média
      • Baixo (<10%): Coberturas similares entre municípios
      • Moderado (10-20%): Alguma variação
      • Alto (>20%): Grande diferença entre municípios
    """)
    
    print("\n" + "=" * 60)
    print("2️⃣ DISTRIBUIÇÃO POR FAIXAS DE COBERTURA")
    print("=" * 60)
    
    # print("\n📊 DISTRIBUIÇÃO")
    # print("-" * 60)
    # dist = stats['distribuicao']
    # dist_perc = stats['distribuicao_percentual']
    # 
    # for faixa, qtd in dist.items():
    #     perc = dist_perc[faixa]
    #     barra = "█" * int(perc / 2)  # Barra visual
    #     print(f"{faixa:.<30} {qtd:>6} ({perc:>5.1f}%) {barra}")
    
    print("""
    📖 ENTENDENDO A DISTRIBUIÇÃO:
    
    A distribuição mostra quantos municípios estão em cada faixa de cobertura.
    Isso é importante para:
    
    • Identificar desigualdades regionais
    • Priorizar investimentos
    • Estabelecer metas de melhoria
    
    Exemplo de interpretação:
    - Se muitos municípios estão em "Sem cobertura" ou "Muito Baixa":
      → Há um problema de inclusão digital urgente
    
    - Se a maioria está em "Boa" ou "Excelente":
      → O foco pode ser melhorar os que ficaram para trás
    """)
    
    print("\n" + "=" * 60)
    print("3️⃣ ANÁLISE POR ESTADO (UF)")
    print("=" * 60)
    
    # Análise específica do Piauí
    print("\n📍 Exemplo: Análise do Piauí")
    print("-" * 60)
    
    # resultado_pi = analisador.ranking_cobertura(por_uf='PI', top_n=5, bottom_n=5)
    # stats_pi = resultado_pi['estatisticas']
    
    # print(f"Municípios no Piauí: {stats_pi['total_municipios']}")
    # print(f"Cobertura Média: {stats_pi['cobertura_media']:.2f}%")
    
    # Interpretação automática
    # print("\n🤖 INTERPRETAÇÃO AUTOMÁTICA:")
    # print("-" * 60)
    # interpretacao = analisador.interpretar_estatisticas(stats_pi)
    # print(interpretacao)
    
    print("\n" + "=" * 60)
    print("4️⃣ COMPARAÇÃO ENTRE REGIÕES")
    print("=" * 60)
    
    print("""
    Para comparar regiões, analise:
    
    1. MÉDIA vs MEDIANA
       • Se média > mediana: Poucos municípios com alta cobertura
       • Se média < mediana: Poucos municípios com baixa cobertura
       • Se média ≈ mediana: Distribuição equilibrada
    
    2. DESVIO PADRÃO
       • Compara a homogeneidade da cobertura
       • Menor desvio = cobertura mais uniforme
    
    3. DISTRIBUIÇÃO POR FAIXAS
       • Quantos % estão com cobertura insuficiente (<50%)?
       • Quantos % alcançaram boa cobertura (>75%)?
    
    Exemplo de análise comparativa:
    
    Estado A: Média 70%, Desvio 15%
    → Cobertura moderada e razoavelmente uniforme
    
    Estado B: Média 75%, Desvio 30%
    → Cobertura média boa, mas muito desigual
    → Alguns municípios excelentes, outros precários
    """)
    
    print("\n" + "=" * 60)
    print("5️⃣ MÉTODO PARA ANÁLISE DE DISTRIBUIÇÃO")
    print("=" * 60)
    
    print("""
    Use o método obter_distribuicao_cobertura() para análise detalhada:
    
    # Nacional
    dist_nacional = analisador.obter_distribuicao_cobertura()
    
    # Por estado
    dist_piaui = analisador.obter_distribuicao_cobertura(por_uf='PI')
    
    Retorna um DataFrame com:
    - Faixa de Cobertura
    - Quantidade de Municípios
    - Percentual (%)
    """)
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISE COMPLETA!")
    print("=" * 60)
    print("""
    📝 RESUMO DAS MELHORES PRÁTICAS:
    
    1. Sempre analise MÉDIA + MEDIANA + DESVIO PADRÃO juntos
    2. Olhe a DISTRIBUIÇÃO para entender onde estão os problemas
    3. Compare regiões usando as mesmas métricas
    4. Use INTERPRETAÇÃO AUTOMÁTICA para insights rápidos
    5. Visualize dados com gráficos (histogramas, pizza, barras)
    
    🎯 O objetivo é identificar:
    - Onde investir prioritariamente
    - Quais municípios precisam de atenção
    - Como as regiões se comparam
    - Tendências de melhoria ou piora
    """)


if __name__ == "__main__":
    exemplo_analise_completa()
