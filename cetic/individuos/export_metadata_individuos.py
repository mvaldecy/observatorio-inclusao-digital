import pyreadstat
import os
import json

def export_metadata():
    data_path = 'cetic/individuos/tic_domicilios_2025_individuos_base_de_microdados_v1.0.sav'
    output_path = 'cetic/individuos/metadados_individuos.py'
    
    print(f"Lendo metadados de {data_path}...")
    df, meta = pyreadstat.read_sav(data_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("\"\"\"\nMETADADOS DE INDIVÍDUOS GERADOS AUTOMATICAMENTE\n\"\"\"\n\n")
        f.write("class MetaValue(float):\n")
        f.write("    def __new__(cls, value, column):\n")
        f.write("        res = super(MetaValue, cls).__new__(cls, value)\n")
        f.write("        res.column = column\n")
        f.write("        return res\n\n")
        f.write("class MetadadosIndividuos:\n")
        
        for col_name in meta.column_names:
            label = meta.column_names_to_labels.get(col_name, "None")
            f.write(f"    class {col_name}:\n")
            f.write(f"        \"\"\"{label}\"\"\"\n")
            f.write(f"        _label = {repr(label)}\n")
            
            value_labels = meta.variable_value_labels.get(col_name, {})
            if value_labels:
                for val, val_label in value_labels.items():
                    # Criar um nome de variável válido
                    import re
                    # Remove acentos e caracteres especiais
                    import unicodedata
                    var_name = unicodedata.normalize('NFKD', val_label).encode('ascii', 'ignore').decode('ascii')
                    var_name = var_name.upper().replace(' ', '_').replace('/', '_').replace('-', '_').replace('.', '').replace('(', '').replace(')', '').replace(',', '')
                    var_name = re.sub(r'[^A-Z0-9_]', '', var_name)
                    
                    if var_name and var_name[0].isdigit():
                        var_name = 'V_' + var_name
                    if not var_name:
                        var_name = f"VAL_{int(val)}"
                    
                    try:
                        f.write(f"        {var_name} = MetaValue({float(val)}, {repr(col_name)})\n")
                    except:
                        pass
                
                f.write(f"        _map = {repr(value_labels)}\n")
            else:
                f.write("        pass\n")
            f.write("\n")

if __name__ == "__main__":
    export_metadata()
