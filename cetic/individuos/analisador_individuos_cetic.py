import pandas as pd
import pyreadstat
try:
    from cetic.individuos.metadados_individuos import MetadadosIndividuos
except ImportError:
    from metadados_individuos import MetadadosIndividuos

class AnalisadorIndividuosCETIC:
    def __init__(self, data_path=None, ano: int = 2025, df=None, meta=None):
        """
        Inicializa o analisador de indivíduos CETIC

        Args:
            data_path: Caminho para arquivo local (opcional, somente para uso direto)
            ano: Ano da pesquisa (default: 2025)
            df: DataFrame já carregado (obrigatório quando usado via data_loader)
            meta: Metadados já carregados (opcional)

        Nota:
            Para uso em aplicações Streamlit, utilize get_analisador_individuos(ano)
            do módulo streamlit.utils.data_loader, que busca automaticamente do cache HTTP.
        """
        self.ano = ano

        # Quando usado via data_loader (caso normal no Streamlit)
        if df is not None:
            self.df = df
            self.meta = meta
            print(f"✓ Analisador inicializado com {len(self.df):,} registros e {len(self.df.columns)} colunas.")
        elif data_path is not None:
            # Uso direto com arquivo local (scripts standalone)
            print(f"⚠️ Carregando de arquivo local: {data_path}")
            try:
                if data_path.endswith('.sav'):
                    self.df, self.meta = pyreadstat.read_sav(data_path)
                else:
                    raise ValueError(f"Formato não suportado: {data_path}. Use arquivo .sav")
                print(f"✓ Base carregada com {len(self.df):,} registros e {len(self.df.columns)} colunas.")
            except Exception as e:
                print(f"❌ Erro ao carregar arquivo: {e}")
                raise
        else:
            # Sem dados nem arquivo - erro
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_individuos(ano)\n"
                "Para scripts standalone, passe data_path com caminho do arquivo .sav"
            )

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
        
        if df.empty:
            return None

        # FILTRAR "Não se aplica" (99.0) de TODAS as colunas relevantes no DataFrame
        # Isso garante que independente dos filtros aplicados antes, nunca contaremos 99.0
        if isinstance(indicador, list):
            # Para análise múltipla, filtrar 99.0 de cada indicador da lista
            for ind in indicador:
                if ind in df.columns:
                    df = df[df[ind] != 99.0]
        else:
            # Para análise simples, filtrar 99.0 do indicador específico
            if indicador in df.columns:
                df = df[df[indicador] != 99.0]

        if df.empty:
            print(f"Aviso: Todos os valores são 'Não se aplica' após filtragem.")
            return None

        if isinstance(indicador, list):
            # Análise múltipla (ex: múltiplos dispositivos)
            resumo = []
            for ind in indicador:
                meta_col = getattr(MetadadosIndividuos, ind, None)
                label_col = getattr(meta_col, '_label', ind) if meta_col else ind
                
                # Considera apenas o valor 'Sim' (1.0) para comparação
                sim_count = (df[ind] == 1.0).sum()
                total = len(df)  # Total JÁ sem "Não se aplica"
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

        # Contagem de valores (já filtrado 99.0 acima)
        counts = df[indicador].value_counts().sort_index()
        total = len(df)  # Total JÁ sem "Não se aplica"

        meta_col = getattr(MetadadosIndividuos, indicador, None)
        label_col = getattr(meta_col, '_label', indicador) if meta_col else indicador
        labels_valores = getattr(meta_col, '_map', {}) if meta_col else {}
        
        resumo = []
        for val, count in counts.items():
            label = labels_valores.get(val, "Não categorizado")
            # Pular "Não se aplica" se ainda aparecer (proteção adicional)
            if label.lower() == 'não se aplica':
                continue
            percent = (count / total) * 100 if total > 0 else 0
            resumo.append({
                'Descrição': label,
                'Total': count,
                'Percentual': f"{percent:.2f}%"
            })
            
        return pd.DataFrame(resumo)

    def analisar_com_internet(self, indicador, df_contexto=None):
        """
        Analisa um indicador mostrando também a distribuição de uso da Internet (C1).
        Retorna dois DataFrames: (resultado_indicador, resultado_internet)
        """
        df = df_contexto if df_contexto is not None else self.df

        if df.empty:
            return None, None

        # Analisa o indicador principal
        resultado_indicador = self.analisar_indicador(indicador, df_contexto=df)

        # Analisa o uso da Internet (C1)
        resultado_internet = self.analisar_indicador('C1', df_contexto=df)

        return resultado_indicador, resultado_internet

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

