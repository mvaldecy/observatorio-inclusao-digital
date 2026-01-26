import pyreadstat
import os
import re
import unicodedata

def slugify(text):
    """
    Transforma uma string em um identificador válido para Python.
    Ex: 'PIAUÍ' -> 'PIAUI', 'Até 1 SM' -> 'ATE_1_SM'
    """
    if not text:
        return "NÃO_IDENTIFICADO"
    
    # Remove acentos
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Para maiúsculas
    text = text.upper()
    # Substitui caracteres não alfanuméricos por underscore
    text = re.sub(r'[^A-Z0-9]', '_', text)
    # Remove underscores duplicados
    text = re.sub(r'_+', '_', text)
    # Remove underscores no início e fim
    text = text.strip('_')
    
    # Garante que não comece com número (se começar, adiciona prefixo)
    if text and text[0].isdigit():
        text = 'V_' + text
        
    return text if text else "NÃO_IDENTIFICADO"

def export_sav_metadata_to_py(sav_path, output_py):
    print(f"Lendo metadados de {sav_path}...")
    try:
        _, meta = pyreadstat.read_sav(sav_path, metadataonly=True)
        
        with open(output_py, 'w', encoding='utf-8') as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write('"""\nMETADADOS GERADOS AUTOMATICAMENTE\n"""\n\n')
            f.write("class MetaValue(float):\n")
            f.write("    def __new__(cls, value, column):\n")
            f.write("        res = super(MetaValue, cls).__new__(cls, value)\n")
            f.write("        res.column = column\n")
            f.write("        return res\n\n")

            f.write("class Metadados:\n")
            
            # Primeiro nível: Colunas
            for col in meta.column_names:
                label_coluna = meta.column_names_to_labels.get(col, "")
                valores = meta.variable_value_labels.get(col, {})
                
                if not valores:
                    # Se não tem valores mapeados, apenas cria uma classe vazia ou com o label
                    f.write(f"    class {col}:\n")
                    f.write(f'        """{label_coluna}"""\n')
                    f.write("        _label = " + repr(label_coluna) + "\n")
                    f.write("        pass\n\n")
                    continue

                f.write(f"    class {col}:\n")
                f.write(f'        """{label_coluna}"""\n')
                f.write("        _label = " + repr(label_coluna) + "\n")
                
                # Segundo nível: Valores
                for val, desc in valores.items():
                    slug = slugify(desc)
                    # Se houver colisão de nomes ou slug vazio, precisamos tratar
                    # Mas por enquanto vamos confiar no slugify
                    f.write(f"        {slug} = MetaValue({repr(val)}, {repr(col)})\n")
                
                # Adiciona um mapeamento reverso para facilitar tradução de código -> descrição
                f.write("        _map = {\n")
                for val, desc in valores.items():
                    f.write(f"            {repr(val)}: {repr(desc)},\n")
                f.write("        }\n\n")

        print(f"Metadados exportados com sucesso para {output_py}")
        
    except Exception as e:
        print(f"Erro ao exportar metadados: {e}")

if __name__ == "__main__":
    sav_file = "cetic/tic_domicilios_2025_domicilios_base_de_microdados_v1.0.sav"
    output = "cetic/metadados.py"
    export_sav_metadata_to_py(sav_file, output)
