import pandas as pd
import pyreadstat
import os
try:
    from cetic.domicilios.metadados import Metadados
except ImportError:
    from metadados import Metadados

class AnalisadorDomiciliosCETIC:
    def __init__(self, data_path=None):
        base_path = os.path.dirname(__file__)
        
        if data_path is None:
            data_path = os.path.join(base_path, 'tic_domicilios_2025_domicilios_base_de_microdados_v1.0.parquet')
        
        print(f"Carregando dados de: {data_path}...")
        try:
            # Usando pyreadstat para ler o arquivo .sav diretamente em um DataFrame pandas
            self.df = pd.read_parquet(data_path)
            self.meta = None

            print(f"Base carregada com {len(self.df)} registros e {len(self.df.columns)} colunas.")
        except Exception as e:
            print(f"Erro ao carregar arquivo .sav: {e}")
            self.df = pd.DataFrame()
            self.meta = None

    def renomear_colunas_com_labels(self):
        """
        Renomeia as colunas do DataFrame substituindo os códigos pelas labels dos metadados.
        """
        rename_dict = {}

        # Percorre todos os atributos da classe Metadados
        for attr_name in dir(Metadados):
            if not attr_name.startswith('_'):  # Ignora atributos privados
                meta_attr = getattr(Metadados, attr_name, None)
                if meta_attr and hasattr(meta_attr, '_label'):
                    # Se a coluna existe no DataFrame, adiciona ao dicionário de rename
                    if attr_name in self.df.columns:
                        rename_dict[attr_name] = meta_attr._label

        # Renomeia as colunas
        self.df.rename(columns=rename_dict, inplace=True)
        print(f"{len(rename_dict)} colunas renomeadas com suas labels.")
        return self.df

    def filtrar_dados(self, *args, **kwargs):
        """
        Filtra os dados usando args (objetos de Metadados) ou kwargs.
        Exemplo: app.filtrar_dados(Metadados.COD_UF.PIAUI, AREA=Metadados.AREA.RURAL)
        """
        if self.df.empty:
            return self.df

        # Processa args (ex: Metadados.COD_UF.PIAUI)
        for arg in args:
            if hasattr(arg, 'column'):
                col = arg.column
                if col in self.df.columns:
                    self.df = self.df[self.df[col] == arg]
                else:
                    print(f"Aviso: Coluna '{col}' (de {arg}) não encontrada no DataFrame.")
            else:
                print(f"Aviso: Argumento posicional '{arg}' não possui informação de coluna. Use kwargs para este caso.")

        # Processa kwargs (ex: AREA=Metadados.AREA.RURAL)
        for col, value in kwargs.items():
            if col in self.df.columns:
                if isinstance(value, list):
                    self.df = self.df[self.df[col].isin(value)]
                else:
                    self.df = self.df[self.df[col] == value]
            else:
                print(f"Aviso: Coluna '{col}' não encontrada no DataFrame.")
        # print(pd.DataFrame(self.df))
        print(f"Filtro aplicado. Registros encontrados: {len(self.df)}")
        return self.df

    def analisar_indicador(self, indicador, df_contexto=None):
        """
        Analisa um indicador específico.
        Se df_contexto for passado, usa ele; senão usa o df principal (auto-filtrado).
        """
        df = df_contexto if df_contexto is not None else self.df
        
        if df.empty:
            return None

        if isinstance(indicador, list):
            # Análise múltipla
            resumo = []
            for ind in indicador:
                meta_col = getattr(Metadados, ind, None)
                label_col = getattr(meta_col, '_label', ind) if meta_col else ind
                
                sim_count = (df[ind] == 1.0).sum()
                total = len(df)
                percent = (sim_count / total) * 100 if total > 0 else 0
                
                resumo.append({
                    'Indicador': ind,
                    'Descrição': label_col,
                    'Total': sim_count,
                    'Percentual': f"{percent:.2f}%"
                })
            return pd.DataFrame(resumo)

        if indicador not in df.columns:
            print(f"Erro: Indicador '{indicador}' não encontrado.")
            return None
            
        # Contagem de valores
        counts = df[indicador].value_counts().sort_index()
        total = len(df)
        
        # Obter metadados da coluna via classe Metadados
        meta_col = getattr(Metadados, indicador, None)
        label_col = getattr(meta_col, '_label', indicador) if meta_col else indicador
        labels_valores = getattr(meta_col, '_map', {}) if meta_col else {}
        
        resumo = []
        for val, count in counts.items():
            label = labels_valores.get(val, "Não categorizado")
            percent = (count / total) * 100 if total > 0 else 0
            resumo.append({
                'Código': val,
                'Descrição': label,
                'Total': count,
                'Percentual': f"{percent:.2f}%"
            })
            
        return pd.DataFrame(resumo)

    def analisar_inclusao_digital(self, *args, **kwargs):
        """
        Realiza a filtragem e a análise do indicador de acesso à internet (A4) em uma única chamada.
        Retorna apenas as porcentagens de Sim/Não.
        """
        # Aplica os filtros
        self.filtrar_dados(*args, **kwargs)
        
        # Analisa o indicador A4 (Acesso à Internet)
        res = self.analisar_indicador('A4')
        
        if res is not None:
            # Filtra apenas Sim e Não (ignorando 'Não sabe', etc, se houver, ou apenas formatando melhor)
            # Geralmente 1.0 = Sim, 2.0 = Não
            return res[['Descrição', 'Percentual']]
        return "Nenhum dado encontrado para os filtros aplicados."

if __name__ == "__main__":
    # Inicializa o analisador
    app = AnalisadorDomiciliosCETIC()
    
    # Exemplo de uso direto: Tudo em uma chamada só
    print("\n--- Analisando Inclusão Digital (Acesso à Internet) ---")
    resultado = app.analisar_inclusao_digital(
        Metadados.COD_UF.PIAUI,
        Metadados.AREA.RURAL,

    )

    print(app.df.columns.tolist())
    print(resultado)
