# 📁 CETIC Domicílios - Scripts de Processamento

## 📚 Estrutura de Arquivos

### 🔧 Arquivos Principais
- **`analisador_domicilios_cetic.py`** - Classe principal para análise dos dados
- **`metadados.py`** - Metadados gerados automaticamente com labels e códigos

### 🛠️ Scripts Auxiliares (Geração de Metadados)
Estes arquivos são utilizados apenas para gerar os metadados a partir dos arquivos .sav:

- **`dicionario_dados.py`** - Dicionário manual de variáveis (legado)
- **`explore_sav.py`** - Script para explorar estrutura de arquivos .sav
- **`export_labels.py`** - Exporta labels para CSV
- **`export_labels_json.py`** - Exporta labels para JSON
- **`export_sav_py.py`** - Gera arquivo metadados.py a partir do .sav
- **`parquet_converter.py`** - Converte .sav para .parquet (opcional)

---

## 📥 Fonte dos Dados

Os dados são carregados automaticamente via HTTP do cache local:

```
data/cache/cetic/{ano}/domicilios.sav
```

**Não é necessário fazer upload de arquivos!** O sistema:
1. Verifica se existe no cache local
2. Se não existe, baixa automaticamente da fonte oficial
3. Armazena em cache para uso futuro

---

## 🔄 Workflow de Uso

### Para Análise (Uso Normal)
```python
from cetic.domicilios.analisador_domicilios_cetic import AnalisadorDomiciliosCetic

# Carrega dados do ano desejado (usa cache HTTP)
analisador = AnalisadorDomiciliosCetic(ano=2025)

# Analisa indicadores
resultado = analisador.analisar_indicador('A4')
```

### Para Gerar Metadados (Apenas quando necessário)
```bash
# 1. Explorar estrutura do .sav
python explore_sav.py

# 2. Gerar arquivo metadados.py
python export_sav_py.py

# 3. (Opcional) Exportar labels para outros formatos
python export_labels.py
python export_labels_json.py
```

---

## 🗂️ Cache Local

Os arquivos .sav são armazenados em:
```
data/cache/cetic/
├── 2023/
│   ├── domicilios.sav
│   └── individuos.sav
├── 2024/
│   ├── domicilios.sav
│   └── individuos.sav
└── 2025/
    ├── domicilios.sav
    └── individuos.sav
```

**Gerenciamento do Cache:**
- ✅ Automático via `HTTPDataLoader`
- ✅ Interface no Streamlit para limpar/atualizar
- ✅ Gitignore configurado (não versiona .sav)

---

## 🧹 Limpeza da Pasta

### Arquivos que DEVEM permanecer:
- ✅ `analisador_domicilios_cetic.py`
- ✅ `metadados.py`
- ✅ `README.md` (este arquivo)

### Arquivos auxiliares (podem ser mantidos ou removidos):
- ⚠️ Scripts de geração (`export_*.py`, `explore_sav.py`, etc.)
- ⚠️ `dicionario_dados.py` (legado, não usado mais)

**Recomendação:** Mover scripts auxiliares para uma pasta `_tools/` ou `_generators/`

---

## 📝 Notas Importantes

1. **Não fazer upload manual de arquivos**
   - O sistema usa cache HTTP automático
   - Arquivos .sav não devem estar na pasta do projeto

2. **Metadados já estão gerados**
   - O arquivo `metadados.py` contém todos os labels e códigos
   - Só precisa ser regenerado quando CETIC atualizar os microdados

3. **Versionamento**
   - Apenas arquivos .py são versionados
   - Arquivos .sav ficam no cache local (gitignore)

---

## 🚀 Próximos Passos

Se quiser reorganizar:

```bash
# Criar pasta para ferramentas auxiliares
mkdir _tools

# Mover scripts de geração
mv explore_sav.py export_*.py parquet_converter.py dicionario_dados.py _tools/

# Adicionar ao .gitignore
echo "cetic/domicilios/_tools/" >> .gitignore
```

