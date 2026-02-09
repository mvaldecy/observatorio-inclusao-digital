# 📊 Guia de Análise Estatística de Cobertura Móvel

Este guia explica de forma clara e didática como interpretar as análises estatísticas de cobertura móvel.

---

## 🎯 Métricas Principais

### 1️⃣ **Cobertura Média**
**O que é:** A soma de todas as coberturas dividida pelo número de municípios.

**Como interpretar:**
- ✅ **80-100%**: Excelente - maioria bem conectada
- 🟢 **60-80%**: Boa - nível satisfatório
- 🟡 **40-60%**: Moderada - precisa melhorar
- 🔴 **0-40%**: Baixa - requer investimentos urgentes

**⚠️ Atenção:** A média pode esconder desigualdades! Um município com 100% e outro com 0% dão média de 50%.

---

### 2️⃣ **Mediana**
**O que é:** O valor do meio quando você ordena todos os municípios por cobertura.

**Por que é importante:**
- Não é afetada por valores extremos
- Mostra o que a "metade dos municípios" experimenta
- Metade tem cobertura acima, metade tem abaixo

**Como usar:**
Compare com a média para detectar desigualdades:

```
Média = 70%, Mediana = 75%
→ Alguns municípios com cobertura muito baixa puxam a média para baixo
→ A "maioria" está melhor que a média sugere

Média = 70%, Mediana = 65%
→ Alguns municípios excepcionais puxam a média para cima
→ A "maioria" está pior que a média sugere

Média ≈ Mediana
→ Distribuição equilibrada, média representa bem a realidade
```

---

### 3️⃣ **Desvio Padrão**
**O que é:** Mede o quanto os valores se afastam da média.

**Interpretação simples:**
- 📊 **Baixo (<10%)**: Municípios com coberturas similares
- 📈 **Moderado (10-20%)**: Alguma variação entre municípios
- 📉 **Alto (>20%)**: Grande desigualdade entre municípios

**Exemplo prático:**

```
Estado A: Média 70%, Desvio 5%
→ A maioria dos municípios tem entre 65% e 75%
→ Cobertura homogênea

Estado B: Média 70%, Desvio 25%
→ Municípios variam muito (de 20% a 100%)
→ Alta desigualdade - alguns excelentes, outros precários
```

---

### 4️⃣ **Valores Máximo e Mínimo**
**O que são:** Melhor e pior cobertura encontrada.

**Como usar:**
```
Max = 100%, Min = 0%
→ Há municípios sem cobertura e municípios com cobertura total
→ Amplitude de 100% indica extrema desigualdade

Max = 95%, Min = 75%
→ Todos os municípios têm boa cobertura
→ Amplitude de 20% indica homogeneidade
```

---

## 📊 Distribuição por Faixas

A distribuição mostra **quantos municípios** estão em cada nível de cobertura.

### Faixas de Classificação

| Faixa | Classificação | Cor | Significado |
|-------|---------------|-----|-------------|
| 0% | Sem cobertura | 🔴 | Sem acesso à internet móvel |
| 0-25% | Muito Baixa | 🟠 | Cobertura precária |
| 25-50% | Baixa | 🟡 | Insuficiente para uso regular |
| 50-75% | Média | 🔵 | Cobertura razoável |
| 75-90% | Boa | 🟢 | Cobertura satisfatória |
| 90-100% | Excelente | 🟢 | Cobertura quase universal |

### Como Interpretar a Distribuição

**Exemplo 1: Distribuição Desigual**
```
Sem cobertura: 20 municípios (20%)
Muito Baixa: 10 municípios (10%)
Baixa: 10 municípios (10%)
Média: 20 municípios (20%)
Boa: 20 municípios (20%)
Excelente: 20 municípios (20%)

⚠️ Problema: 30% sem cobertura adequada
→ Prioridade: Investir nos 30 municípios mais carentes
```

**Exemplo 2: Distribuição Concentrada no Topo**
```
Sem cobertura: 2 municípios (2%)
Muito Baixa: 3 municípios (3%)
Baixa: 5 municípios (5%)
Média: 10 municípios (10%)
Boa: 30 municípios (30%)
Excelente: 50 municípios (50%)

✅ Situação boa: 80% com cobertura boa/excelente
→ Foco: Melhorar os 10% com pior cobertura
```

---

## 🔍 Análise Comparativa Entre Regiões

### Como Comparar Regiões

#### 1. Compare as Médias
```
Brasil: 70%
Nordeste: 65% (-5%)
Piauí: 60% (-10%)

→ Piauí está 10 pontos abaixo da média nacional
```

#### 2. Compare os Desvios Padrões
```
Brasil: Desvio 18%
Nordeste: Desvio 22%
Piauí: Desvio 25%

→ Piauí tem maior desigualdade interna
→ Alguns municípios muito bons, outros muito ruins
```

#### 3. Compare as Distribuições
```
Brasil: 60% com cobertura boa/excelente
Nordeste: 45% com cobertura boa/excelente
Piauí: 35% com cobertura boa/excelente

→ Piauí tem menos municípios bem conectados
```

---

## 💡 Casos de Uso Práticos

### Caso 1: Priorização de Investimentos
**Pergunta:** Onde investir primeiro?

**Análise:**
1. Identifique municípios com cobertura < 25% (usando distribuição)
2. Calcule quantos habitantes são afetados
3. Priorize por:
   - População afetada
   - Importância econômica
   - Facilidade de implementação

### Caso 2: Avaliação de Políticas Públicas
**Pergunta:** A política melhorou a cobertura?

**Análise:**
```
Antes: Média 60%, Desvio 25%
Depois: Média 65%, Desvio 20%

✅ Melhorou em 2 aspectos:
- Média aumentou (+5%)
- Desigualdade diminuiu (-5% no desvio)
```

### Caso 3: Comparação Regional
**Pergunta:** Como meu estado se compara ao Brasil?

**Checklist:**
- [ ] Média está acima ou abaixo da nacional?
- [ ] Desvio padrão é maior ou menor?
- [ ] Distribuição tem mais ou menos municípios bem conectados?
- [ ] Há municípios sem cobertura?

---

## 🎓 Glossário Estatístico

| Termo | Definição Simples |
|-------|-------------------|
| **Média Aritmética** | Soma de todos os valores ÷ quantidade |
| **Mediana** | Valor do meio quando ordenado |
| **Desvio Padrão** | Quanto os valores se afastam da média |
| **Distribuição** | Como os valores se espalham |
| **Amplitude** | Diferença entre máximo e mínimo |
| **Percentual/Delta** | Diferença relativa entre valores |
| **Homogeneidade** | Valores similares entre si (baixo desvio) |
| **Heterogeneidade** | Valores muito diferentes (alto desvio) |

---

## ⚠️ Armadilhas Comuns

### 1. Confiar apenas na média
```
❌ "Média de 70% é boa!"
✅ "Média de 70%, mas 30% dos municípios têm menos de 25%"
```

### 2. Ignorar o desvio padrão
```
❌ Estado A (média 70%) é igual ao Estado B (média 70%)
✅ Estado A (desvio 10%) é mais homogêneo que Estado B (desvio 30%)
```

### 3. Não olhar a distribuição
```
❌ "Metade tem mais de 75% de cobertura"
✅ "Mas 20% não tem cobertura alguma - problema urgente"
```

---

## 🚀 Próximos Passos

Depois de entender as estatísticas:

1. **Identifique problemas:** Municípios com baixa cobertura
2. **Analise causas:** Geografia? Economia? População?
3. **Priorize ações:** Quais são urgentes?
4. **Monitore evolução:** Compare ao longo do tempo
5. **Comunique resultados:** Use gráficos e linguagem clara

---

## 📚 Recursos Adicionais

- [exemplo_analise_estatistica.py](exemplo_analise_estatistica.py) - Código com exemplos práticos
- [analisador_cobertura_movel.py](analisador_cobertura_movel.py) - Código fonte do analisador

---

## ❓ Perguntas Frequentes

**P: Por que média e mediana são diferentes?**  
R: Indicam desigualdade. Valores extremos afetam a média, mas não a mediana.

**P: O que é um "bom" desvio padrão?**  
R: Depende do contexto. Para cobertura, <10% indica homogeneidade.

**P: Como saber se minha análise está correta?**  
R: Verifique se média + desvio cobre a maioria dos valores (regra 68-95-99.7).

**P: Posso comparar estados de tamanhos diferentes?**  
R: Sim! Use percentuais e métricas relativas (média, mediana), não valores absolutos.

---

**📝 Última atualização:** 2026-02-05  
**👤 Autor:** Sistema de Análise ANATEL
