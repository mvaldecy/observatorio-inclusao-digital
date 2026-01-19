import requests
import pandas as pd
import io

import os

BASE_URL = "https://cetic.br/pt/tics/domicilios/{year}/individuos/C1/"

def get_url_for_year(year):
    return BASE_URL.format(year=year)

def extract_table_data(year):
    url = get_url_for_year(year)
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        resp.raise_for_status()
        resp.encoding = "utf-8"

        tables = pd.read_html(io.StringIO(resp.text))
        
        if not tables:
            return None
            
        df = tables[0]

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        return df
    except Exception as e:
        print(f"Erro ao extrair dados para o ano {year}: {e}")
        return None

def save_year_data(year):
    df = extract_table_data(year)
    
    if df is not None:
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            

        filename = os.path.join(output_dir, f"individuos_que_ja_acessaram_internet_{year}.csv")
        df.to_csv(filename, index=False, sep=';', encoding="utf-8-sig")

        print(f"Tabela de {year} salva em {filename} com {len(df)} linhas.")
    else:
        print(f"Não foi possível extrair os dados para o ano {year}.")

if __name__ == "__main__":
    anos = [2022, 2023, 2024, 2025]
    for ano in anos:
        save_year_data(ano)
