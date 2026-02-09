import pandas as pd
from .municipios_ibge import adicionar_nome_municipio


class AnalisadorCoberturaMovel:
    """
    Analisador de dados de Cobertura Móvel da ANATEL
    Fornece métodos para análise e ranking de cobertura por município
    """
    
    def __init__(self, df=None):
        """
        Inicializa o analisador de cobertura móvel

        Args:
            df: DataFrame já carregado (obrigatório quando usado via data_loader)

        Nota:
            Para uso em aplicações Streamlit, utilize get_analisador_cobertura_movel()
            do módulo streamlit.utils.data_loader
        """
        if df is None:
            raise ValueError(
                "❌ Analisador requer dados.\n"
                "Para aplicações Streamlit, use: get_analisador_cobertura_movel()\n"
            )
        
        self.df = df.copy()
        self.df_original = df.copy()  # Backup para reset
        
        # Normaliza nomes das colunas (maiúsculas, remove espaços extras)
        self.df.columns = [str(col).strip().upper() for col in self.df.columns]
        
        # Identifica automaticamente colunas importantes
        self._identificar_colunas()
        
        # Se encontrou coluna de código de município, adiciona nome
        if self.col_municipio and 'CÓDIGO' in self.col_municipio.upper():
            print("⏳ Adicionando nomes dos municípios...")
            self.df = adicionar_nome_municipio(self.df, self.col_municipio, 'MUNICÍPIO')
            # Atualiza coluna de município para a nova coluna com nomes
            self.col_municipio_codigo = self.col_municipio
            self.col_municipio = 'MUNICÍPIO'
            print("✓ Nomes dos municípios adicionados!")
        
        print(f"✓ Analisador Cobertura Móvel inicializado com {len(self.df):,} registros")
        print(f"  Colunas disponíveis: {len(self.df.columns)}")
        if self.col_municipio:
            print(f"  Coluna de município: {self.col_municipio}")
        if self.col_cobertura:
            print(f"  Colunas de cobertura: {', '.join(self.col_cobertura)}")
    
    def _identificar_colunas(self):
        """Identifica automaticamente as colunas de interesse nos dados"""
        
        # Identifica coluna de município/localidade
        location_terms = ['MUNICIPIO', 'MUNICÍPIO', 'CIDADE', 'LOCALIDADE', 'NOME', 'ENTIDADE']
        self.col_municipio = None
        for term in location_terms:
            matching = [col for col in self.df.columns if term in col]
            if matching:
                self.col_municipio = matching[0]
                break
        
        # Se não encontrou, tenta busca mais flexível
        if not self.col_municipio:
            # Procura por colunas que tenham "mun" no nome
            matching = [col for col in self.df.columns if 'MUN' in col]
            if matching:
                self.col_municipio = matching[0]
        
        # Identifica colunas de UF/Estado
        uf_terms = ['UF', 'ESTADO', 'SIGLA']
        self.col_uf = None
        for term in uf_terms:
            matching = [col for col in self.df.columns if term in col and 'MUNICIPIO' not in col and 'MUNICÍPIO' not in col]
            if matching:
                self.col_uf = matching[0]
                break
        
        # Se não encontrou UF, tenta "SG"
        if not self.col_uf:
            matching = [col for col in self.df.columns if col == 'SG' or col.startswith('SG_')]
            if matching:
                self.col_uf = matching[0]
        
        # Identifica colunas de cobertura (porcentagem)
        coverage_terms = ['COBERTURA', 'PERCENTUAL', '%', 'PERCENT', 'COB']
        self.col_cobertura = []
        for col in self.df.columns:
            if any(term in col for term in coverage_terms):
                self.col_cobertura.append(col)
        
        # Identifica colunas de tecnologia (2G, 3G, 4G, 5G)
        tech_terms = ['2G', '3G', '4G', '5G', 'TECNOLOGIA']
        self.col_tecnologia = []
        for col in self.df.columns:
            if any(term in col for term in tech_terms):
                self.col_tecnologia.append(col)
    
    def reset_filtros(self):
        """Reseta todos os filtros aplicados, voltando ao DataFrame original"""
        self.df = self.df_original.copy()
        print(f"✓ Filtros resetados. Total de registros: {len(self.df):,}")
        return self.df
    
    def obter_colunas_cobertura(self):
        """Retorna lista de colunas que contêm dados de cobertura"""
        return self.col_cobertura
    
    def obter_coluna_municipio(self):
        """Retorna o nome da coluna que contém municípios"""
        return self.col_municipio
    
    def obter_coluna_uf(self):
        """Retorna o nome da coluna que contém UF"""
        return self.col_uf
    
    def definir_coluna_municipio(self, nome_coluna: str):
        """Define manualmente qual coluna usar para município"""
        if nome_coluna in self.df.columns:
            self.col_municipio = nome_coluna
            print(f"✓ Coluna de município definida: {nome_coluna}")
        else:
            print(f"⚠️ Coluna '{nome_coluna}' não encontrada no DataFrame")
    
    def definir_coluna_uf(self, nome_coluna: str):
        """Define manualmente qual coluna usar para UF"""
        if nome_coluna in self.df.columns:
            self.col_uf = nome_coluna
            print(f"✓ Coluna de UF definida: {nome_coluna}")
        else:
            print(f"⚠️ Coluna '{nome_coluna}' não encontrada no DataFrame")
    
    def filtrar_por_uf(self, uf: str):
        """
        Filtra dados por UF específica
        
        Args:
            uf: Sigla da UF (ex: 'SP', 'RJ', 'PI')
        
        Returns:
            DataFrame filtrado
        """
        if not self.col_uf:
            print("⚠️ Coluna de UF não identificada nos dados")
            return self.df
        
        self.df = self.df[self.df[self.col_uf] == uf.upper()]
        print(f"Filtrado por UF: {uf}. Registros: {len(self.df):,}")
        return self.df
    
    def ranking_cobertura(self, coluna_cobertura=None, top_n=20, bottom_n=20, por_uf=None):
        """
        Gera ranking de municípios por cobertura móvel com análise estatística completa
        
        Args:
            coluna_cobertura: Nome da coluna de cobertura a usar (se None, usa a primeira encontrada)
            top_n: Quantidade de municípios com maior cobertura (padrão: 20)
            bottom_n: Quantidade de municípios com menor cobertura (padrão: 20)
            por_uf: Filtrar por UF específica antes de calcular ranking (ex: 'PI', 'SP')
        
        Returns:
            dict contendo:
                - 'top': DataFrame com os N municípios de maior cobertura
                - 'bottom': DataFrame com os N municípios de menor cobertura
                - 'estatisticas': Dict com métricas estatísticas (média, mediana, min, max, desvio)
                - 'distribuicao': Dict com distribuição por faixas de cobertura
                - 'coluna_usada': Nome da coluna analisada
                - 'completo': DataFrame completo com todos os municípios ranqueados
        """
        if not self.col_municipio:
            raise ValueError("Coluna de município não identificada nos dados")
        
        if not self.col_cobertura:
            raise ValueError("Nenhuma coluna de cobertura identificada nos dados")
        
        # Define qual coluna de cobertura usar
        if coluna_cobertura and coluna_cobertura in self.df.columns:
            col_cob = coluna_cobertura
        else:
            col_cob = self.col_cobertura[0]
        
        # Prepara dados
        df_work = self.df.copy()
        
        # Filtra por UF se solicitado
        if por_uf and self.col_uf:
            df_work = df_work[df_work[self.col_uf] == por_uf.upper()]
        
        # Seleciona colunas necessárias
        colunas = [self.col_municipio, col_cob]
        if self.col_uf and self.col_uf not in colunas:
            colunas.append(self.col_uf)
        
        df_work = df_work[colunas].copy()
        
        # Converte coluna de cobertura para numérico se necessário
        if df_work[col_cob].dtype == 'object':
            df_work[col_cob] = (
                df_work[col_cob]
                .astype(str)
                .str.replace('%', '')
                .str.replace(',', '.')
                .str.replace(' ', '')
            )
            df_work[col_cob] = pd.to_numeric(df_work[col_cob], errors='coerce')
        
        # Remove valores nulos
        df_work = df_work.dropna(subset=[col_cob])
        
        # Agrupa por município e calcula média (caso haja múltiplas entradas)
        group_cols = [self.col_municipio]
        if self.col_uf and self.col_uf in df_work.columns:
            group_cols.append(self.col_uf)
        
        df_grouped = df_work.groupby(group_cols, as_index=False)[col_cob].mean()
        
        # Renomeia colunas para facilitar
        rename_dict = {col_cob: 'Cobertura (%)'}
        if self.col_municipio in df_grouped.columns:
            rename_dict[self.col_municipio] = 'Município'
        if self.col_uf and self.col_uf in df_grouped.columns:
            rename_dict[self.col_uf] = 'UF'
        
        df_grouped = df_grouped.rename(columns=rename_dict)
        
        # Ordena por cobertura (maior para menor)
        df_grouped = df_grouped.sort_values('Cobertura (%)', ascending=False).reset_index(drop=True)
        
        # ===== ANÁLISE ESTATÍSTICA COMPLETA =====
        
        # 1. Estatísticas Descritivas Básicas
        estatisticas = {
            'total_municipios': len(df_grouped),
            'cobertura_media': round(df_grouped['Cobertura (%)'].mean(), 2),
            'cobertura_mediana': round(df_grouped['Cobertura (%)'].median(), 2),
            'cobertura_max': round(df_grouped['Cobertura (%)'].max(), 2),
            'cobertura_min': round(df_grouped['Cobertura (%)'].min(), 2),
            'desvio_padrao': round(df_grouped['Cobertura (%)'].std(), 2),
        }
        
        # 2. Análise de Distribuição por Faixas de Cobertura
        # Ajuda a entender quantos municípios estão em cada nível de conectividade
        distribuicao = {
            'Sem cobertura (0%)': len(df_grouped[df_grouped['Cobertura (%)'] == 0]),
            'Muito Baixa (0-25%)': len(df_grouped[(df_grouped['Cobertura (%)'] > 0) & (df_grouped['Cobertura (%)'] <= 25)]),
            'Baixa (25-50%)': len(df_grouped[(df_grouped['Cobertura (%)'] > 25) & (df_grouped['Cobertura (%)'] <= 50)]),
            'Média (50-75%)': len(df_grouped[(df_grouped['Cobertura (%)'] > 50) & (df_grouped['Cobertura (%)'] <= 75)]),
            'Boa (75-90%)': len(df_grouped[(df_grouped['Cobertura (%)'] > 75) & (df_grouped['Cobertura (%)'] <= 90)]),
            'Excelente (90-100%)': len(df_grouped[df_grouped['Cobertura (%)'] > 90]),
        }
        
        # Adiciona percentuais à distribuição
        total = len(df_grouped)
        distribuicao_percentual = {k: round((v/total)*100, 1) for k, v in distribuicao.items()}
        estatisticas['distribuicao'] = distribuicao
        estatisticas['distribuicao_percentual'] = distribuicao_percentual
        
        # Separa top e bottom rankings
        df_top = df_grouped.head(top_n)
        df_bottom = df_grouped.tail(bottom_n).sort_values('Cobertura (%)', ascending=True)
        
        return {
            'top': df_top,
            'bottom': df_bottom,
            'estatisticas': estatisticas,
            'coluna_usada': col_cob,
            'completo': df_grouped
        }
    
    def comparar_tecnologias(self, municipio=None):
        """
        Compara cobertura de diferentes tecnologias (2G, 3G, 4G, 5G)
        
        Args:
            municipio: Nome do município (se None, retorna agregado geral)
        
        Returns:
            DataFrame com comparação de tecnologias
        """
        if not self.col_tecnologia:
            print("⚠️ Nenhuma coluna de tecnologia identificada")
            return None
        
        df_work = self.df.copy()
        
        if municipio and self.col_municipio:
            df_work = df_work[df_work[self.col_municipio].str.contains(municipio, case=False, na=False)]
        
        # Cria resumo por tecnologia
        resultado = {}
        for col in self.col_tecnologia:
            if col in df_work.columns:
                # Tenta converter para numérico
                valores = df_work[col].copy()
                if valores.dtype == 'object':
                    valores = pd.to_numeric(
                        valores.astype(str).str.replace('%', '').str.replace(',', '.'),
                        errors='coerce'
                    )
                
                resultado[col] = {
                    'media': valores.mean(),
                    'max': valores.max(),
                    'min': valores.min()
                }
        
        return pd.DataFrame(resultado).T
    
    def obter_resumo_por_uf(self, coluna_cobertura=None):
        """
        Gera resumo estatístico completo de cobertura por UF (Unidade Federativa)
        
        Calcula para cada estado:
        - Média: cobertura média de todos os municípios
        - Máxima: melhor cobertura encontrada
        - Mínima: pior cobertura encontrada
        - Mediana: valor central da distribuição
        - Desvio Padrão: dispersão dos valores (quanto maior, mais heterogêneo)
        
        Args:
            coluna_cobertura: Nome da coluna de cobertura (se None, usa primeira encontrada)
        
        Returns:
            DataFrame com estatísticas por UF, ordenado por média (decrescente)
        """
        if not self.col_uf:
            print("⚠️ Coluna de UF não identificada")
            return None
        
        if not self.col_cobertura:
            print("⚠️ Nenhuma coluna de cobertura identificada")
            return None
        
        # Define coluna de cobertura
        col_cob = coluna_cobertura if coluna_cobertura else self.col_cobertura[0]
        
        df_work = self.df[[self.col_uf, col_cob]].copy()
        
        # Converte para numérico
        if df_work[col_cob].dtype == 'object':
            df_work[col_cob] = pd.to_numeric(
                df_work[col_cob].astype(str).str.replace('%', '').str.replace(',', '.'),
                errors='coerce'
            )
        
        # Agrupa por UF e calcula estatísticas
        resumo = df_work.groupby(self.col_uf)[col_cob].agg([
            ('Média', 'mean'),
            ('Máxima', 'max'),
            ('Mínima', 'min'),
            ('Mediana', 'median'),
            ('Desvio Padrão', 'std')
        ]).round(2)
        
        resumo = resumo.sort_values('Média', ascending=False)
        
        return resumo
    
    def obter_distribuicao_cobertura(self, coluna_cobertura=None, por_uf=None):
        """
        Analisa a distribuição de municípios por faixas de cobertura
        
        Retorna quantos municípios estão em cada faixa de conectividade:
        - Sem cobertura (0%)
        - Muito Baixa (0-25%)
        - Baixa (25-50%)
        - Média (50-75%)
        - Boa (75-90%)
        - Excelente (90-100%)
        
        Args:
            coluna_cobertura: Coluna de cobertura a analisar (se None, usa primeira)
            por_uf: Filtrar por UF específica (opcional)
        
        Returns:
            DataFrame com contagem e percentual de municípios por faixa
        """
        if not self.col_cobertura:
            print("⚠️ Nenhuma coluna de cobertura identificada")
            return None
        
        col_cob = coluna_cobertura if coluna_cobertura else self.col_cobertura[0]
        df_work = self.df.copy()
        
        # Filtra por UF se solicitado
        if por_uf and self.col_uf:
            df_work = df_work[df_work[self.col_uf] == por_uf.upper()]
        
        # Converte para numérico
        if df_work[col_cob].dtype == 'object':
            df_work['cobertura_num'] = pd.to_numeric(
                df_work[col_cob].astype(str).str.replace('%', '').str.replace(',', '.'),
                errors='coerce'
            )
        else:
            df_work['cobertura_num'] = df_work[col_cob]
        
        df_work = df_work.dropna(subset=['cobertura_num'])
        
        # Calcula distribuição por faixas
        distribuicao = {
            'Sem cobertura (0%)': len(df_work[df_work['cobertura_num'] == 0]),
            'Muito Baixa (0-25%)': len(df_work[(df_work['cobertura_num'] > 0) & (df_work['cobertura_num'] <= 25)]),
            'Baixa (25-50%)': len(df_work[(df_work['cobertura_num'] > 25) & (df_work['cobertura_num'] <= 50)]),
            'Média (50-75%)': len(df_work[(df_work['cobertura_num'] > 50) & (df_work['cobertura_num'] <= 75)]),
            'Boa (75-90%)': len(df_work[(df_work['cobertura_num'] > 75) & (df_work['cobertura_num'] <= 90)]),
            'Excelente (90-100%)': len(df_work[df_work['cobertura_num'] > 90]),
        }
        
        total = len(df_work)
        
        # Cria DataFrame com resultados
        df_dist = pd.DataFrame({
            'Faixa de Cobertura': distribuicao.keys(),
            'Quantidade de Municípios': distribuicao.values()
        })
        
        df_dist['Percentual (%)'] = (df_dist['Quantidade de Municípios'] / total * 100).round(1)
        
        return df_dist
    
    def interpretar_estatisticas(self, estatisticas):
        """
        Gera interpretações em linguagem clara das estatísticas calculadas
        
        Args:
            estatisticas: Dicionário de estatísticas do método ranking_cobertura
        
        Returns:
            String com interpretação em linguagem acessível
        """
        if not estatisticas:
            return "Estatísticas não disponíveis"
        
        media = estatisticas.get('cobertura_media', 0)
        mediana = estatisticas.get('cobertura_mediana', 0)
        desvio = estatisticas.get('desvio_padrao', 0)
        total = estatisticas.get('total_municipios', 0)
        
        interpretacao = []
        
        # Interpretação da cobertura média
        if media >= 80:
            interpretacao.append(f"✅ **Excelente cobertura média** ({media:.1f}%) - A maioria dos municípios tem boa conectividade")
        elif media >= 60:
            interpretacao.append(f"🟢 **Boa cobertura média** ({media:.1f}%) - Nível satisfatório de conectividade")
        elif media >= 40:
            interpretacao.append(f"🟡 **Cobertura média moderada** ({media:.1f}%) - Há espaço para melhorias")
        else:
            interpretacao.append(f"🔴 **Cobertura média baixa** ({media:.1f}%) - Necessita investimentos urgentes")
        
        # Interpretação da relação média-mediana
        if abs(media - mediana) < 5:
            interpretacao.append(f"📊 **Distribuição equilibrada** - Média ({media:.1f}%) próxima da mediana ({mediana:.1f}%)")
        elif media > mediana:
            interpretacao.append(f"⚠️ **Desigualdade positiva** - Poucos municípios com alta cobertura elevam a média")
        else:
            interpretacao.append(f"ℹ️ **Desigualdade negativa** - Poucos municípios com baixa cobertura reduzem a média")
        
        # Interpretação do desvio padrão
        if desvio < 10:
            interpretacao.append(f"✅ **Baixa variação** ({desvio:.1f}%) - Cobertura homogênea entre municípios")
        elif desvio < 20:
            interpretacao.append(f"🟡 **Variação moderada** ({desvio:.1f}%) - Alguma desigualdade na distribuição")
        else:
            interpretacao.append(f"🔴 **Alta variação** ({desvio:.1f}%) - Grande desigualdade entre municípios")
        
        return "\n\n".join(interpretacao)
    
    def obter_info_geral(self):
        """Retorna informações gerais sobre os dados carregados"""
        return {
            'total_registros': len(self.df),
            'colunas_disponiveis': list(self.df.columns),
            'coluna_municipio': self.col_municipio,
            'coluna_uf': self.col_uf,
            'colunas_cobertura': self.col_cobertura,
            'colunas_tecnologia': self.col_tecnologia,
            'ufs_disponiveis': sorted(self.df[self.col_uf].unique().tolist()) if self.col_uf else []
        }
