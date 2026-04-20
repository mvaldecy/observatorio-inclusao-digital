# 📄 Páginas Desabilitadas Temporariamente

## 🏫 INEP - Censo Escolar (DESABILITADO)

**Status:** ⏸️ Temporariamente removido da navegação  
**Arquivo:** `streamlit/pages/_3_INEP_Censo_Escolar.py.disabled`  
**Motivo:** Dataset muito grande causa timeout no Streamlit Cloud

### ❌ Problema Identificado

A página do INEP carrega dados do Censo Escolar da Educação Básica, que contém:
- **150k-200k registros** de escolas
- **Centenas de colunas** com dados detalhados
- **Tamanho em memória:** ~2GB quando carregado completo

Isso causava:
- ⏱️ **Timeout** no deploy do Streamlit Cloud (limite de 60s para inicialização)
- 💾 **Uso excessivo de memória** (limite de 1GB no free tier)
- 🐌 **Lentidão extrema** na interface

### 🔄 Como Reativar

Quando implementar a solução de amostragem (ver código comentado no arquivo), execute:

```bash
cd /home/marcos/PycharmProjects/observatorio-inclusao-digital
mv streamlit/pages/_3_INEP_Censo_Escolar.py.disabled streamlit/pages/3_INEP_Censo_Escolar.py
git add streamlit/pages/3_INEP_Censo_Escolar.py
git commit -m "feat: reativar página INEP com amostragem implementada"
git push
```

### 💡 Solução Recomendada (Para Implementação Futura)

O arquivo desabilitado já contém comentários com o código necessário para implementar:

1. **Modo de Carregamento com Seletor**
   - 🚀 Modo Rápido: Amostra de 10k escolas (padrão)
   - 💾 Modo Completo: Todos os dados (opcional)

2. **Amostragem Estratificada por UF**
   - Mantém proporção de escolas por estado
   - Garante representatividade nacional

3. **Carregamento Otimizado**
   - Lê diretamente do parquet em cache
   - Não carrega dataset completo antes de amostrar

### 📊 Outras Páginas Ativas

✅ **Páginas funcionando normalmente:**
- 1️⃣ Cetic Domicílios
- 2️⃣ Cetic Indivíduos  
- 3️⃣ IBGE Acesso Internet
- 4️⃣ Cobertura Móvel
- 4️⃣ Conectividade nas Escolas
- 5️⃣ Explorar Cobertura Móvel
- 6️⃣ Mapas Cobertura
- 7️⃣ PCD Inclusão Digital

---

## 📝 Histórico de Mudanças

### 2025-03-31
- ⏸️ Desabilitada página INEP temporariamente
- 📋 Renomeado para `_3_INEP_Censo_Escolar.py.disabled`
- 💡 Solução de amostragem documentada no código
- 🎯 Aguardando implementação da otimização

---

## 🚀 Deploy

Após esta mudança, o deploy no Streamlit Cloud deve funcionar sem timeouts.

**Próximos passos:**
1. ✅ Commit e push das mudanças
2. ✅ Deploy no Streamlit Cloud
3. ✅ Verificar que não há mais timeout
4. 📋 Implementar amostragem na página INEP
5. ✅ Reativar a página

