"""
Analisador de Dados do INEP - Censo Escolar da Educação Básica
Baseado no AnalisadorDomiciliosCETIC para manter compatibilidade de interface
"""

import pandas as pd

try:
    from inep.metadados_inep import (
        METADADOS_INEP,
        get_label,
        get_valores,
        get_categoria_variavel
    )
except ImportError:
    from metadados_inep import (
        METADADOS_INEP,
        get_label,
        get_valores,
        get_categoria_variavel
    )


class AnalisadorINEP:
    """
    Analisador de dados do INEP (Censo Escolar)
    Interface compatível com AnalisadorDomiciliosCETIC
    """

    def __init__(self, data_path=None, ano: int = 2024, df=None, meta=None):
        """
        Inicializa o analisador de dados do INEP

        Args:
            data_path: Caminho para arquivo local (opcional, somente para uso direto)
            ano: Ano do censo (default: 2024)
            df: DataFrame já carregado (obrigatório quando usado via data_loader)
            meta: Metadados já carregados (opcional, sempre None para INEP)

        Nota:
            Para uso em aplicações Streamlit, utilize get_analisador_inep(ano)
            do módulo streamlit.utils.data_loader, que busca automaticamente do cache HTTP.
        """
        self.ano = ano

        # Quando usado via data_loader (caso normal no Streamlit)
        if df is not None:
            self.df_original = df.copy()  # Guardar cópia do original
            self.df = df.copy()  # DataFrame de trabalho
            self.meta = meta
            print(f"✓ Analisador INEP inicializado com {len(self.df):,} registros e {len(self.df.columns)} colunas.")
        elif data_path is not None:
            # Uso direto com arquivo local (scripts standalone)
            print(f"⚠️ Carregando de arquivo local: {data_path}")
            try:
                if data_path.endswith('.parquet'):
                    self.df_original = pd.read_parquet(data_path)
                    self.df = self.df_original.copy()
                    self.meta = None
                elif data_path.endswith('.csv'):
                    self.df_original = pd.read_csv(data_path, sep=';', encoding='utf-8-sig', low_memory=False)
                    self.df = self.df_original.copy()
                    self.meta = None
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
                "Para aplicações Streamlit, use: get_analisador_inep(ano)\n"
                "Para scripts standalone, passe data_path com caminho do arquivo .parquet ou .csv"
            )

    def renomear_colunas_com_labels(self):
        """
        Renomeia as colunas do DataFrame substituindo os códigos pelas labels dos metadados.
        """
        rename_dict = {}

        # Percorre todas as categorias e variáveis
        for categoria, variaveis in METADADOS_INEP.items():
            for var_name, var_info in variaveis.items():
                if var_name in self.df.columns:
                    rename_dict[var_name] = var_info['label']

        # Renomeia as colunas
        self.df.rename(columns=rename_dict, inplace=True)
        print(f"{len(rename_dict)} colunas renomeadas com suas labels.")
        return self.df

    def filtrar_dados(self, **kwargs):
        """
        Filtra os dados usando kwargs.

        Exemplos:
            analisador.filtrar_dados(TP_DEPENDENCIA=1)  # Federal
            analisador.filtrar_dados(CO_UF=22, TP_LOCALIZACAO=2)  # Piauí Rural
            analisador.filtrar_dados(IN_INTERNET=1, IN_LABORATORIO_INFORMATICA=1)

        Args:
            **kwargs: Pares coluna=valor para filtrar

        Returns:
            DataFrame filtrado
        """
        if self.df.empty:
            return self.df

        # Processa kwargs
        for col, value in kwargs.items():
            if col in self.df.columns:
                if isinstance(value, list):
                    self.df = self.df[self.df[col].isin(value)]
                else:
                    self.df = self.df[self.df[col] == value]
            else:
                print(f"Aviso: Coluna '{col}' não encontrada no DataFrame.")

        print(f"Filtro aplicado. Registros encontrados: {len(self.df):,}")
        return self.df

    def analisar_indicador(self, indicador, df_contexto=None):
        """
        Analisa um indicador específico.

        Args:
            indicador: Nome da coluna ou lista de colunas para análise
            df_contexto: DataFrame filtrado (opcional, usa self.df se não fornecido)

        Returns:
            DataFrame com resumo da análise
        """
        df = df_contexto if df_contexto is not None else self.df

        if df.empty:
            return None

        # Análise múltipla
        if isinstance(indicador, list):
            resumo = []
            for ind in indicador:
                if ind not in df.columns:
                    continue

                label_col = get_label(ind)
                valores = get_valores(ind)

                if valores and '1' in valores:
                    # Indicador binário (0/1)
                    sim_count = (df[ind] == 1).sum()
                    total = df[ind].notna().sum()
                    percent = (sim_count / total) * 100 if total > 0 else 0

                    resumo.append({
                        'Indicador': ind,
                        'Descrição': label_col,
                        'Total': sim_count,
                        'Percentual': f"{percent:.2f}%"
                    })
                else:
                    # Indicador quantitativo
                    total = df[ind].notna().sum()
                    media = df[ind].mean()
                    soma = df[ind].sum()

                    resumo.append({
                        'Indicador': ind,
                        'Descrição': label_col,
                        'Total': int(soma) if pd.notna(soma) else 0,
                        'Média': f"{media:.2f}" if pd.notna(media) else "0.00"
                    })

            return pd.DataFrame(resumo)

        # Análise simples
        if indicador not in df.columns:
            print(f"Erro: Indicador '{indicador}' não encontrado.")
            return None

        label_col = get_label(indicador)
        valores = get_valores(indicador)

        # Se for categórico, faz contagem
        if valores:
            counts = df[indicador].value_counts().sort_index()
            total = df[indicador].notna().sum()

            resumo = []
            for val, count in counts.items():
                if pd.isna(val):
                    continue

                val_str = str(int(val) if isinstance(val, float) and val.is_integer() else val)
                label = valores.get(val_str, f"Valor {val_str}")
                percent = (count / total) * 100 if total > 0 else 0

                resumo.append({
                    'Descrição': label,
                    'Total': count,
                    'Percentual': f"{percent:.2f}%"
                })

            return pd.DataFrame(resumo)
        else:
            # Indicador quantitativo - estatísticas descritivas
            stats = df[indicador].describe()
            return pd.DataFrame({
                'Estatística': ['Total', 'Média', 'Desvio Padrão', 'Mínimo', 'Máximo'],
                'Valor': [
                    int(stats['count']),
                    f"{stats['mean']:.2f}",
                    f"{stats['std']:.2f}",
                    f"{stats['min']:.2f}",
                    f"{stats['max']:.2f}"
                ]
            })

    def analisar_acesso_internet(self, **kwargs):
        """
        Análise específica de acesso à internet nas escolas.
        Aplica filtros e retorna percentual de escolas com internet.

        Args:
            **kwargs: Filtros a aplicar (ex: CO_UF=22, TP_LOCALIZACAO=2)

        Returns:
            DataFrame com percentuais de Sim/Não
        """
        # Aplica os filtros
        self.filtrar_dados(**kwargs)

        # Analisa o indicador IN_INTERNET
        res = self.analisar_indicador('IN_INTERNET')

        if res is not None:
            return res[['Descrição', 'Percentual']]
        return "Nenhum dado encontrado para os filtros aplicados."

    def analisar_por_agregador(self, indicador, campo_agregador: str, df_contexto=None):
        """
        Análise otimizada por agregador usando groupby.
        Retorna resultados agregados para visualização em gráficos.

        Args:
            indicador: Campo ou lista de campos para análise
            campo_agregador: Nome do campo para agregação (ex: 'TP_DEPENDENCIA', 'CO_UF')
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
        label_agregador = get_label(campo_agregador)
        map_agregador = get_valores(campo_agregador) or {}

        # Determinar se é análise simples ou múltipla
        is_multiple = isinstance(indicador, list)
        campos = [indicador] if not is_multiple else indicador

        resultados = []

        # Para cada valor único do agregador
        for valor_agregador in sorted(df[campo_agregador].dropna().unique()):
            # Filtrar dados para este valor
            df_grupo = df[df[campo_agregador] == valor_agregador]

            # Converter valor para string para buscar no mapa
            valor_str = str(int(valor_agregador) if isinstance(valor_agregador, float) and valor_agregador.is_integer() else valor_agregador)
            label_valor_agregador = map_agregador.get(valor_str, str(valor_agregador))

            # Analisar cada campo
            for campo in campos:
                if campo not in df_grupo.columns:
                    continue

                label_campo = get_label(campo)
                map_campo = get_valores(campo) or {}

                # Contar valores
                contagens = df_grupo[campo].value_counts()
                total_grupo = df_grupo[campo].notna().sum()

                for valor_campo, count in contagens.items():
                    if pd.isna(valor_campo):
                        continue

                    valor_campo_str = str(int(valor_campo) if isinstance(valor_campo, float) and valor_campo.is_integer() else valor_campo)
                    label_valor_campo = map_campo.get(valor_campo_str, str(valor_campo))
                    percentual = (count / total_grupo * 100) if total_grupo > 0 else 0

                    resultado = {
                        label_agregador: label_valor_agregador,
                        'Categoria': label_valor_campo,
                        'Percentual': f"{percentual:.1f}%"
                    }

                    resultados.append(resultado)

        if not resultados:
            return None

        return pd.DataFrame(resultados)

    def analisar_por_agregador_quantitativo(self, indicador, campo_agregador: str,
                                              funcao='sum', df_contexto=None):
        """
        Análise quantitativa por agregador usando groupby.
        Para indicadores numéricos (QT_*), aplica uma função de agregação.

        Args:
            indicador: Campo ou lista de campos para análise
            campo_agregador: Nome do campo para agregação
            funcao: Função de agregação: 'sum', 'mean', 'median', 'count'
            df_contexto: DataFrame filtrado (opcional)

        Returns:
            DataFrame com resultados agregados
        """
        df = df_contexto if df_contexto is not None else self.df

        if df.empty:
            return None

        if campo_agregador not in df.columns:
            print(f"Erro: Campo agregador '{campo_agregador}' não encontrado.")
            return None

        label_agregador = get_label(campo_agregador)
        map_agregador = get_valores(campo_agregador) or {}

        is_multiple = isinstance(indicador, list)
        campos = indicador if is_multiple else [indicador]

        # Verificar que os campos existem
        campos = [c for c in campos if c in df.columns]
        if not campos:
            return None

        resultados = []

        for valor_agregador in sorted(df[campo_agregador].dropna().unique()):
            df_grupo = df[df[campo_agregador] == valor_agregador]
            if isinstance(valor_agregador, float) and valor_agregador.is_integer():
                valor_str = str(int(valor_agregador))
            else:
                valor_str = str(valor_agregador)
            label_valor = map_agregador.get(valor_str, str(valor_agregador))

            for campo in campos:
                serie = df_grupo[campo].dropna()
                if serie.empty:
                    continue

                if funcao == 'sum':
                    valor_calc = serie.sum()
                elif funcao == 'mean':
                    valor_calc = serie.mean()
                elif funcao == 'median':
                    valor_calc = serie.median()
                elif funcao == 'count':
                    valor_calc = serie.count()
                else:
                    valor_calc = serie.sum()

                resultado = {
                    label_agregador: label_valor,
                    'Indicador': get_label(campo),
                    'Indicador_Cod': campo,
                    'Total': valor_calc,
                    'Contagem': len(df_grupo),
                }
                resultados.append(resultado)

        if not resultados:
            return None

        return pd.DataFrame(resultados)

    def resumo_infraestrutura(self, **kwargs):
        """
        Gera resumo de infraestrutura de internet e tecnologia.

        Args:
            **kwargs: Filtros a aplicar

        Returns:
            DataFrame com indicadores de infraestrutura
        """
        if kwargs:
            self.filtrar_dados(**kwargs)

        indicadores_tech = [
            'IN_INTERNET',
            'IN_LABORATORIO_INFORMATICA',
            'IN_BANDA_LARGA',
            'IN_INTERNET_ALUNOS',
            'IN_INTERNET_APRENDIZAGEM'
        ]

        # Filtra apenas indicadores que existem no DataFrame
        indicadores_existentes = [ind for ind in indicadores_tech if ind in self.df.columns]

        if not indicadores_existentes:
            print("Nenhum indicador de infraestrutura encontrado no DataFrame.")
            return None

        return self.analisar_indicador(indicadores_existentes)

    def resetar_filtros(self):
        """
        Remove todos os filtros aplicados, retornando ao DataFrame original.
        """
        if hasattr(self, 'df_original'):
            self.df = self.df_original.copy()
            print(f"✓ Filtros resetados. Registros: {len(self.df):,}")
        else:
            print("⚠️ DataFrame original não disponível.")
        return self


# Função auxiliar para uso em Streamlit
def criar_analisador_inep(df, ano=2024):
    """
    Cria uma instância do analisador a partir de um DataFrame.
    Útil para integração com data_loader do Streamlit.

    Args:
        df: DataFrame com dados do INEP
        ano: Ano do censo

    Returns:
        AnalisadorINEP inicializado
    """
    return AnalisadorINEP(df=df, ano=ano)


if __name__ == "__main__":
    print("=" * 80)
    print("EXEMPLO DE USO DO ANALISADOR INEP")
    print("=" * 80)

    print("""
# Para usar em produção, carregue os dados via data_loader:

from streamlit.utils.data_loader import carregar_educacao_basica_inep
from inep.analisador_inep import AnalisadorINEP

# Carregar dados
df = carregar_educacao_basica_inep(ano=2024)

# Criar analisador
analisador = AnalisadorINEP(df=df, ano=2024)

# Filtrar escolas públicas do Piauí na zona rural
analisador.filtrar_dados(CO_UF=22, TP_DEPENDENCIA=[1, 2, 3], TP_LOCALIZACAO=2)

# Analisar acesso à internet
resultado = analisador.analisar_indicador('IN_INTERNET')
print(resultado)

# Analisar por dependência administrativa
resultado_dep = analisador.analisar_por_agregador('IN_INTERNET', 'TP_DEPENDENCIA')
print(resultado_dep)

# Resumo de infraestrutura
resumo = analisador.resumo_infraestrutura(CO_UF=22)
print(resumo)
""")

