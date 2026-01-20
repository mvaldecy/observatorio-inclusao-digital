import pandas as pd
import pyreadstat
import os
try:
    from cetic.individuos.metadados_individuos import MetadadosIndividuos
except ImportError:
    from metadados_individuos import MetadadosIndividuos

class AnalisadorIndividuosCETIC:
    def __init__(self, data_path=None):
        base_path = os.path.dirname(__file__)
        
        if data_path is None:
            data_path = os.path.join(base_path, 'tic_domicilios_2025_individuos_base_de_microdados_v1.0.sav')
        
        print(f"Carregando dados de: {data_path}...")
        try:
            self.df, self.meta = pyreadstat.read_sav(data_path)
            print(f"Base carregada com {len(self.df)} registros e {len(self.df.columns)} colunas.")
        except Exception as e:
            print(f"Erro ao carregar arquivo .sav: {e}")
            self.df = pd.DataFrame()
            self.meta = None

    def filtrar_dados(self, *args, **kwargs):
        """
        Filtra os dados usando args (objetos de MetadadosIndividuos) ou kwargs.
        """
        if self.df.empty:
            return self.df

        for arg in args:
            if hasattr(arg, 'column'):
                col = arg.column
                if col in self.df.columns:
                    self.df = self.df[self.df[col] == arg]
                else:
                    print(f"Aviso: Coluna '{col}' não encontrada.")
            else:
                print(f"Aviso: Argumento '{arg}' não possui informação de coluna.")

        for col, value in kwargs.items():
            if col in self.df.columns:
                if isinstance(value, list):
                    self.df = self.df[self.df[col].isin(value)]
                else:
                    self.df = self.df[self.df[col] == value]
            else:
                print(f"Aviso: Coluna '{col}' não encontrada.")
        
        print(f"Filtro aplicado. Registros encontrados: {len(self.df)}")
        return self.df

    def analisar_indicador(self, indicador, df_contexto=None):
        df = df_contexto if df_contexto is not None else self.df
        
        if isinstance(indicador, list):
            # Análise múltipla (ex: múltiplos dispositivos)
            resumo = []
            for ind in indicador:
                meta_col = getattr(MetadadosIndividuos, ind, None)
                label_col = getattr(meta_col, '_label', ind) if meta_col else ind
                
                # Considera apenas o valor 'Sim' (1.0) para comparação
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
            
        counts = df[indicador].value_counts().sort_index()
        total = len(df)
        
        meta_col = getattr(MetadadosIndividuos, indicador, None)
        label_col = getattr(meta_col, '_label', indicador) if meta_col else indicador
        labels_valores = getattr(meta_col, '_map', {}) if meta_col else {}
        
        resumo = []
        for val, count in counts.items():
            label = labels_valores.get(val, "Não categorizado")
            percent = (count / total) * 100 if total > 0 else 0
            resumo.append({
                'Descrição': label,
                'Total': count,
                'Percentual': f"{percent:.2f}%"
            })
            
        return pd.DataFrame(resumo)

    def analisar_uso_internet(self, *args, **kwargs):
        """
        Analisa o indicador C1 (Indivíduos que já acessaram a Internet).
        """
        self.filtrar_dados(*args, **kwargs)
        res = self.analisar_indicador('C1')
        if res is not None:
            return res[['Descrição', 'Percentual']]
        return "Nenhum dado encontrado."

if __name__ == "__main__":
    app = AnalisadorIndividuosCETIC()
    print("\n--- Analisando Uso de Internet (Indicador C1) ---")
    # Tenta usar o metadado gerado (sem acentos agora)

    resultado = app.analisar_uso_internet(
        MetadadosIndividuos.COD_UF.PIAUI,
        MetadadosIndividuos.AREA.RURAL,
        MetadadosIndividuos.RENDA_FAMILIAR.DE_R_455401_ATE_R_759000
    )
    print(resultado)

