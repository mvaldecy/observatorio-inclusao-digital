import json
import os
from cetic.domicilios.dicionario_dados import COLUNAS, VALORES

def export_to_json():
    # Estrutura: { "COLUNA": { "label": "Descrição", "valores": { "1.0": "Valor 1", ... } } }
    metadados = {}
    
    for col, label in COLUNAS.items():
        metadados[col] = {
            "label": label.strip() if label else None,
            "valores": VALORES.get(col, {})
        }
    
    output_dir = "../output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "metadados.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadados, f, indent=4, ensure_ascii=False)
        
    print(f"Metadados exportados para {output_path}")

if __name__ == "__main__":
    export_to_json()
