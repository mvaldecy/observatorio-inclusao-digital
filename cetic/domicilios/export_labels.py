import pandas as pd
from cetic.domicilios.dicionario_dados import COLUNAS, VALORES
import os

def generate_labels_csv():
    rows = []
    for col, label in COLUNAS.items():
        vals = VALORES.get(col, {})
        if vals:
            for code, val_label in vals.items():
                rows.append({
                    'coluna': col, 
                    'label_coluna': label.strip(), 
                    'valor': code, 
                    'label_valor': val_label
                })
        else:
            rows.append({
                'coluna': col, 
                'label_coluna': label.strip(), 
                'valor': None, 
                'label_valor': None
            })
    
    df = pd.DataFrame(rows)
    output_path = os.path.join('../output', 'metadados_labels.csv')
    if not os.path.exists('../output'):
        os.makedirs('../output')
    df.to_csv(output_path, index=False, sep=';', encoding='utf-8-sig')
    print(f'Arquivo de labels gerado em {output_path}')

if __name__ == "__main__":
    generate_labels_csv()
