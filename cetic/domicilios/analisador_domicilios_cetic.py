import pandas as pd
import pyreadstat
try:
    from cetic.domicilios.metadados import Metadados
except ImportError:
    from metadados import Metadados
 # ignore
class AnalisadorDomiciliosCETIC:
    def __init__(self, data_path=None, ano: int = 2025, df=None, meta=None):
        """
        Inicializa o analisador de domicílios CETIC

        Args:
            data_path: Caminho para arquivo local (opcional, somente para uso direto)
            ano: Ano da pesquisa (default: 2025)
            df: DataFrame já carregado (obrigatório quando usado via data_loader)
            meta: Metadados já carregados (opcional)

        Nota:
            Para uso em aplicações Streamlit, utilize get_analisador_domicilios(ano)
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
                if data_path.endswith('.parquet'):
                    self.df = pd.read_parquet(data_path)
                    self.meta = None
                elif data_path.endswith('.sav'):
                    self.df, self.meta = pyreadstat.read_sav(data_path)
                else:
                    raise ValueError(f"Formato não suportado: {data_path}")
                print(f"✓ Base carregada com {len(self.df):,} registros e {len(self.df.columns)} colunas.")
            except Exception as e:
                print(f"❌ Erro ao carregar arquivo: {e}")
                raise
        else:
            # Sem dados nem arquivo - erro
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_domicilios(ano)\n"
                "Para scripts standalone, passe data_path com caminho do arquivo .sav ou .parquet"
            )

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
            # Análise múltipla
            resumo = []
            for ind in indicador:
                meta_col = getattr(Metadados, ind, None)
                label_col = getattr(meta_col, '_label', ind) if meta_col else ind
                
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

        # Obter metadados da coluna via classe Metadados
        meta_col = getattr(Metadados, indicador, None)
        label_col = getattr(meta_col, '_label', indicador) if meta_col else indicador
        labels_valores = getattr(meta_col, '_map', {}) if meta_col else {}
        
        resumo = []
        for val, count in counts.items():
            label = labels_valores.get(val, "Não categorizado")
            # Pular "Não se aplica" se ainda aparecer
            if label.lower() == 'não se aplica':
                continue
            percent = (count / total) * 100 if total > 0 else 0
            resumo.append({
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
        Metadados.GRAU_INSTRUCAO.FUNDAMENTAL_COMPLETO_MEDIO_INCOMPLETO

    )

    print(app.df.columns.tolist())
    print(resultado)
