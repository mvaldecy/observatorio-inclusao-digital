import pandas as pd
import pyreadstat
try:
    from cetic.individuos.metadados_individuos import MetadadosIndividuos
except ImportError:
    from metadados_individuos import MetadadosIndividuos

class AnalisadorIndividuosCETIC:
    # Códigos especiais que representam respostas não válidas para análise estatística:
    # 97 = Não sabe, 98 = Não respondeu, 99 = Não se aplica, 999999999 = Não se aplica (campos de quantidade)
    _CODIGOS_SISTEMA = {97.0, 98.0, 99.0, 999999999.0}

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
                if data_path.endswith('.parquet'):
                    self.df = pd.read_parquet(data_path)
                    self.meta = None
                elif data_path.endswith('.sav'):
                    self.df, self.meta = pyreadstat.read_sav(data_path)
                else:
                    raise ValueError(f"Formato não suportado: {data_path}. Use arquivo .sav ou .parquet")
                print(f"✓ Base carregada com {len(self.df):,} registros e {len(self.df.columns)} colunas.")
            except Exception as e:
                print(f"❌ Erro ao carregar arquivo: {e}")
                raise
        else:
            # Sem dados nem arquivo - erro
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_individuos(ano)\n"
                "Para scripts standalone, passe data_path com caminho do arquivo .sav ou .parquet"
            )

    def renomear_colunas_com_labels(self):
        """
        Renomeia as colunas do DataFrame substituindo os códigos pelas labels dos metadados.
        """
        rename_dict = {}

        for attr_name in dir(MetadadosIndividuos):
            if not attr_name.startswith('_'):
                meta_attr = getattr(MetadadosIndividuos, attr_name, None)
                if meta_attr and hasattr(meta_attr, '_label'):
                    if attr_name in self.df.columns:
                        rename_dict[attr_name] = meta_attr._label

        self.df.rename(columns=rename_dict, inplace=True)
        print(f"{len(rename_dict)} colunas renomeadas com suas labels.")
        return self.df

    def filtrar_dados(self, *args, **kwargs):
        """
        Filtra os dados usando args (objetos de MetadadosIndividuos) ou kwargs.
        Retorna uma cópia filtrada sem modificar o DataFrame original.
        """
        df = self.df.copy()

        if df.empty:
            return df

        for arg in args:
            if hasattr(arg, 'column'):
                col = arg.column
                if col in df.columns:
                    df = df[df[col] == arg]
                else:
                    print(f"Aviso: Coluna '{col}' não encontrada.")
            else:
                print(f"Aviso: Argumento '{arg}' não possui informação de coluna.")

        for col, value in kwargs.items():
            if col in df.columns:
                if isinstance(value, list):
                    df = df[df[col].isin(value)]
                else:
                    df = df[df[col] == value]
            else:
                print(f"Aviso: Coluna '{col}' não encontrada.")
        
        print(f"Filtro aplicado. Registros encontrados: {len(df)}")
        return df

    def analisar_indicador(self, indicador, df_contexto=None):
        """
        Analisa um indicador específico.
        Códigos de sistema (97=Não sabe, 98=Não respondeu, 99=Não se aplica,
        999999999=Não se aplica) são excluídos do denominador para que os
        percentuais reflitam apenas as respostas válidas.
        """
        df = df_contexto if df_contexto is not None else self.df
        
        if df.empty:
            return None

        if isinstance(indicador, list):
            # Análise múltipla: para cada indicador, exclui seus próprios códigos de sistema
            resumo = []
            for ind in indicador:
                if ind not in df.columns:
                    continue
                meta_col = getattr(MetadadosIndividuos, ind, None)
                label_col = getattr(meta_col, '_label', ind) if meta_col else ind

                df_valido = df[~df[ind].isin(self._CODIGOS_SISTEMA)]
                sim_count = (df_valido[ind] == 1.0).sum()
                total = len(df_valido)
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

        # Exclui códigos de sistema do denominador para percentuais corretos
        df_valido = df[~df[indicador].isin(self._CODIGOS_SISTEMA)]
        counts = df_valido[indicador].value_counts().sort_index()
        total = len(df_valido)

        meta_col = getattr(MetadadosIndividuos, indicador, None)
        label_col = getattr(meta_col, '_label', indicador) if meta_col else indicador
        labels_valores = getattr(meta_col, '_map', {}) if meta_col else {}
        
        resumo = []
        for val, count in counts.items():
            label = labels_valores.get(val, str(val))
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
        df_filtrado = self.filtrar_dados(*args, **kwargs)
        res = self.analisar_indicador('C1', df_contexto=df_filtrado)
        if res is not None:
            return res[['Descrição', 'Percentual']]
        return "Nenhum dado encontrado."

    def analisar_por_agregador(self, indicador, campo_agregador: str, df_contexto=None):
        """
        Análise otimizada por agregador usando groupby.
        Retorna resultados agregados para visualização em gráficos.

        Args:
            indicador: Campo ou lista de campos para análise
            campo_agregador: Nome do campo para agregação (ex: 'RENDA_FAMILIAR', 'GRAU_INSTRUCAO')
            df_contexto: DataFrame filtrado (opcional)

        Returns:
            DataFrame com resultados agregados por categoria do agregador
        """
        df = df_contexto if df_contexto is not None else self.df

        if df.empty:
            return None

        if campo_agregador not in df.columns:
            print(f"Erro: Campo agregador '{campo_agregador}' não encontrado.")
            return None

        # Obter metadados do agregador
        meta_agregador = getattr(MetadadosIndividuos, campo_agregador, None)
        if not meta_agregador:
            print(f"Erro: Metadados para '{campo_agregador}' não encontrados.")
            return None

        label_agregador = getattr(meta_agregador, '_label', campo_agregador)
        map_agregador = getattr(meta_agregador, '_map', {})

        # Determinar se é análise simples ou múltipla
        is_multiple = isinstance(indicador, list)
        campos = [indicador] if not is_multiple else indicador

        resultados = []

        # Para cada valor único do agregador
        for valor_agregador in sorted(df[campo_agregador].unique()):
            # Filtrar dados para este valor
            df_grupo = df[df[campo_agregador] == valor_agregador]
            label_valor_agregador = map_agregador.get(valor_agregador, str(valor_agregador))

            # Analisar cada campo
            for campo in campos:
                if campo not in df_grupo.columns:
                    continue

                meta_campo = getattr(MetadadosIndividuos, campo, None)
                label_campo = getattr(meta_campo, '_label', campo) if meta_campo else campo
                map_campo = getattr(meta_campo, '_map', {}) if meta_campo else {}

                # Contar valores excluindo códigos de sistema
                df_grupo_valido = df_grupo[~df_grupo[campo].isin(self._CODIGOS_SISTEMA)]
                contagens = df_grupo_valido[campo].value_counts()
                total_grupo = len(df_grupo_valido)

                for valor_campo, count in contagens.items():
                    label_valor_campo = map_campo.get(valor_campo, str(valor_campo))
                    percentual = (count / total_grupo * 100) if total_grupo > 0 else 0

                    resultado = {
                        label_agregador: label_valor_agregador,
                        'Agregador_Valor': valor_agregador,
                        'Total_Grupo': total_grupo,
                    }

                    if is_multiple:
                        resultado['Indicador'] = label_campo

                    resultado.update({
                        'Categoria': label_valor_campo,
                        'Valor': valor_campo,
                        'Total': count,
                        'Percentual': f"{percentual:.1f}%",
                        'Percentual_Num': percentual
                    })

                    resultados.append(resultado)

        if not resultados:
            return None

        return pd.DataFrame(resultados)

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

