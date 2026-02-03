import pandas as pd


class AnalisadorAnatel:
    def __init__(self, df=None, ano: int = 2025):
        """
        Inicializa o analisador de dados ANATEL

        Args:
            df: DataFrame já carregado (obrigatório quando usado via data_loader)
            ano: Ano da pesquisa (default: 2025)

        Nota:
            Para uso em aplicações Streamlit, utilize get_analisador_anatel(ano)
            do módulo streamlit.utils.data_loader, que busca automaticamente do cache HTTP.
        """
        self.ano = ano
        
        if df is None:
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_anatel(ano)\n"
            )
        
        self.df = df.copy()
        self.df_original = df.copy()  # Backup para reset
        
        # Normaliza nomes das colunas (maiúsculas, remove espaços extras)
        self.df.columns = [str(col).strip().upper() for col in self.df.columns]
        
        print(f"✓ Analisador ANATEL inicializado com {len(self.df):,} registros do ano {ano}")
        print(f"  Colunas disponíveis: {len(self.df.columns)}")
    
    def reset_filtros(self):
        """Reseta todos os filtros aplicados, voltando ao DataFrame original"""
        self.df = self.df_original.copy()
        print(f"✓ Filtros resetados. Total de registros: {len(self.df):,}")
        return self.df
    
    def filtrar(self, **kwargs):
        """
        Filtra os dados usando kwargs.
        
        Exemplos:
            analisador.filtrar(UF='PI', LOCALIZACAO='URBANA')
            analisador.filtrar(REGIAO='NORDESTE')
        
        Args:
            **kwargs: Pares coluna=valor para filtrar
        
        Returns:
            DataFrame filtrado
        """
        if self.df.empty:
            print("⚠️ DataFrame vazio, nenhum filtro aplicado.")
            return self.df
        
        for col, value in kwargs.items():
            col_upper = col.upper()
            
            # Procura pela coluna (exato ou similar)
            if col_upper in self.df.columns:
                if isinstance(value, list):
                    self.df = self.df[self.df[col_upper].isin(value)]
                else:
                    self.df = self.df[self.df[col_upper] == value]
            else:
                # Tenta busca flexível (contém o termo)
                matching_cols = [c for c in self.df.columns if col_upper in c]
                if matching_cols:
                    print(f"⚠️ Coluna '{col}' não encontrada. Colunas similares: {matching_cols}")
                else:
                    print(f"⚠️ Coluna '{col}' não encontrada no DataFrame.")
        
        print(f"Filtro aplicado. Registros encontrados: {len(self.df):,}")
        return self.df
    
    def filtrar_por_uf(self, *ufs):
        """
        Filtra por UF(s) específica(s)
        
        Args:
            *ufs: Siglas das UFs (ex: 'PI', 'CE', 'BA')
        
        Returns:
            DataFrame filtrado
        """
        col_uf = self._encontrar_coluna(['UF', 'SIGLA_UF', 'COD_UF'])
        
        if col_uf:
            self.df = self.df[self.df[col_uf].isin([uf.upper() for uf in ufs])]
            print(f"Filtrado por UF(s): {', '.join(ufs)}. Registros: {len(self.df):,}")
        else:
            print("⚠️ Coluna de UF não encontrada.")
        
        return self.df
    
    def filtrar_por_regiao(self, regiao: str):
        """
        Filtra por região (Norte, Nordeste, Sul, Sudeste, Centro-Oeste)
        
        Args:
            regiao: Nome da região
        
        Returns:
            DataFrame filtrado
        """
        col_regiao = self._encontrar_coluna(['REGIAO', 'REGIAO_GEOGRAFICA', 'REG'])
        
        if col_regiao:
            self.df = self.df[self.df[col_regiao].str.upper() == regiao.upper()]
            print(f"Filtrado por região: {regiao}. Registros: {len(self.df):,}")
        else:
            print("⚠️ Coluna de região não encontrada.")
        
        return self.df
    
    def filtrar_por_localizacao(self, localizacao: str):
        """
        Filtra por localização (Urbana, Rural)
        
        Args:
            localizacao: 'URBANA' ou 'RURAL'
        
        Returns:
            DataFrame filtrado
        """
        col_loc = self._encontrar_coluna(['LOCALIZACAO', 'LOCAL', 'AREA'])
        
        if col_loc:
            self.df = self.df[self.df[col_loc].str.upper() == localizacao.upper()]
            print(f"Filtrado por localização: {localizacao}. Registros: {len(self.df):,}")
        else:
            print("⚠️ Coluna de localização não encontrada.")
        
        return self.df
    
    def _encontrar_coluna(self, candidatos: list) -> str:
        """
        Busca por uma coluna no DataFrame usando lista de candidatos
        
        Args:
            candidatos: Lista de possíveis nomes de coluna
        
        Returns:
            Nome da coluna encontrada ou None
        """
        for candidato in candidatos:
            if candidato.upper() in self.df.columns:
                return candidato.upper()
            # Busca parcial
            for col in self.df.columns:
                if candidato.upper() in col:
                    return col
        return None
    
    def resumo_geral(self, coluna: str = None):
        """
        Retorna um resumo estatístico dos dados
        
        Args:
            coluna: Coluna específica para resumo (opcional)
        
        Returns:
            Dict com estatísticas
        """
        if self.df.empty:
            return {"erro": "DataFrame vazio"}
        
        if coluna:
            col_upper = coluna.upper()
            if col_upper in self.df.columns:
                return self.df[col_upper].describe().to_dict()
            else:
                return {"erro": f"Coluna '{coluna}' não encontrada"}
        
        return {
            "total_registros": len(self.df),
            "total_colunas": len(self.df.columns),
            "ano": self.ano,
            "colunas": list(self.df.columns)
        }
    
    def contar_por(self, coluna: str, top: int = None):
        """
        Conta valores únicos de uma coluna
        
        Args:
            coluna: Nome da coluna para contar
            top: Limitar aos N primeiros resultados (opcional)
        
        Returns:
            Series com contagens
        """
        col_upper = coluna.upper()
        
        # Busca flexível de coluna
        col_encontrada = None
        if col_upper in self.df.columns:
            col_encontrada = col_upper
        else:
            # Busca parcial
            for c in self.df.columns:
                if col_upper in c:
                    col_encontrada = c
                    break
        
        if not col_encontrada:
            print(f"⚠️ Coluna '{coluna}' não encontrada.")
            return pd.Series()
        
        contagem = self.df[col_encontrada].value_counts()
        
        if top:
            contagem = contagem.head(top)
        
        return contagem
    
    def distribuicao_percentual(self, coluna: str, top: int = None):
        """
        Calcula distribuição percentual de uma coluna
        
        Args:
            coluna: Nome da coluna
            top: Limitar aos N primeiros resultados (opcional)
        
        Returns:
            DataFrame com contagens e percentuais
        """
        contagem = self.contar_por(coluna, top)
        
        if contagem.empty:
            return pd.DataFrame()
        
        total = contagem.sum()
        
        resultado = pd.DataFrame({
            'Valor': contagem.index,
            'Contagem': contagem.values,
            'Percentual': (contagem.values / total * 100).round(2)
        })
        
        resultado['Percentual_Formatado'] = resultado['Percentual'].apply(lambda x: f"{x:.2f}%")
        
        return resultado
    
    def agrupar_por(self, *colunas):
        """
        Agrupa dados por uma ou mais colunas e conta registros
        
        Args:
            *colunas: Nomes das colunas para agrupamento
        
        Returns:
            DataFrame agrupado
        """
        colunas_upper = [c.upper() for c in colunas]
        
        # Valida se colunas existem
        colunas_validas = []
        for col in colunas_upper:
            if col in self.df.columns:
                colunas_validas.append(col)
            else:
                print(f"⚠️ Coluna '{col}' não encontrada.")
        
        if not colunas_validas:
            return pd.DataFrame()
        
        resultado = self.df.groupby(colunas_validas).size().reset_index(name='Total')
        return resultado.sort_values('Total', ascending=False)
    
    def comparar_localizacao(self, coluna: str):
        """
        Compara uma métrica entre áreas urbanas e rurais
        
        Args:
            coluna: Coluna para comparar
        
        Returns:
            DataFrame com comparação
        """
        col_loc = self._encontrar_coluna(['LOCALIZACAO', 'LOCAL', 'AREA'])
        
        if not col_loc:
            print("⚠️ Coluna de localização não encontrada.")
            return pd.DataFrame()
        
        col_upper = coluna.upper()
        if col_upper not in self.df.columns:
            print(f"⚠️ Coluna '{coluna}' não encontrada.")
            return pd.DataFrame()
        
        resultado = self.df.groupby(col_loc)[col_upper].agg(['count', 'mean', 'median']).reset_index()
        resultado.columns = ['Localização', 'Total', 'Média', 'Mediana']
        
        return resultado
    
    def escolas_por_regiao(self):
        """
        Conta escolas por região geográfica
        
        Returns:
            DataFrame com contagem por região
        """
        col_regiao = self._encontrar_coluna(['REGIAO', 'REGIAO_GEOGRAFICA', 'REG'])
        
        if not col_regiao:
            print("⚠️ Coluna de região não encontrada.")
            return pd.DataFrame()
        
        return self.distribuicao_percentual(col_regiao)
    
    def escolas_por_uf(self, top: int = None):
        """
        Conta escolas por UF
        
        Args:
            top: Limitar aos N primeiros resultados (opcional)
        
        Returns:
            DataFrame com contagem por UF
        """
        col_uf = self._encontrar_coluna(['UF', 'SIGLA_UF', 'COD_UF'])
        
        if not col_uf:
            print("⚠️ Coluna de UF não encontrada.")
            return pd.DataFrame()
        
        return self.distribuicao_percentual(col_uf, top)
    
    def get_dataframe(self):
        """Retorna o DataFrame atual (com filtros aplicados)"""
        return self.df.copy()
    
    def get_colunas(self):
        """Retorna lista de colunas disponíveis"""
        return list(self.df.columns)


if __name__ == "__main__":
    # Exemplo de uso standalone
    print("Para usar o AnalisadorAnatel em scripts Streamlit:")
    print("from utils.data_loader import get_analisador_anatel")
    print("analisador = get_analisador_anatel(ano=2024)")
