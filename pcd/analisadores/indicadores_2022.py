import pandas as pd


class IndicadoresPCDTEA2022Mixin:
    """Indicadores agregados de deficiência/autismo para base territorial 2022."""

    def _resolver_coluna(self, nome: str):
        candidatos = [nome, nome.lower(), nome.upper()]
        for candidato in candidatos:
            if candidato in self.df.columns:
                return candidato
        return None

    def _somar_coluna(self, nome: str) -> float:
        col = self._resolver_coluna(nome)
        if not col:
            return 0.0
        return pd.to_numeric(self.df[col], errors='coerce').fillna(0).sum()

    def get_indicadores_deficiencia_2mais(self) -> dict:
        total = self._somar_coluna('TOTAL_PESSOAS_2_MAIS')
        com_def = self._somar_coluna('PESSOAS_COM_DEFICIENCIA_2_MAIS')
        sem_def = self._somar_coluna('PESSOAS_SEM_DEFICIENCIA_2_MAIS')
        perc_com = (com_def / total * 100) if total > 0 else 0
        perc_sem = (sem_def / total * 100) if total > 0 else 0
        return {
            'total_2_mais': total,
            'com_deficiencia': com_def,
            'sem_deficiencia': sem_def,
            'perc_com_deficiencia': perc_com,
            'perc_sem_deficiencia': perc_sem
        }

    def get_comparativo_com_sem_deficiencia(self) -> pd.DataFrame:
        info = self.get_indicadores_deficiencia_2mais()
        return pd.DataFrame({
            'Categoria': ['Pessoa com deficiência', 'Pessoa sem deficiência'],
            'Quantidade': [info['com_deficiencia'], info['sem_deficiencia']],
            'Percentual': [info['perc_com_deficiencia'], info['perc_sem_deficiencia']]
        })

    def get_deficiencia_por_idade(self) -> pd.DataFrame:
        mapeamento = {
            '2 a 4 anos': 'PCD_IDADE_2_4',
            '5 a 9 anos': 'PCD_IDADE_5_9',
            '10 a 14 anos': 'PCD_IDADE_10_14',
            '15 a 19 anos': 'PCD_IDADE_15_19',
            '20 a 24 anos': 'PCD_IDADE_20_24',
            '25 a 29 anos': 'PCD_IDADE_25_29',
            '30 a 34 anos': 'PCD_IDADE_30_34',
            '35 a 39 anos': 'PCD_IDADE_35_39',
            '40 a 44 anos': 'PCD_IDADE_40_44',
            '45 a 49 anos': 'PCD_IDADE_45_49',
            '50 a 54 anos': 'PCD_IDADE_50_54',
            '55 a 59 anos': 'PCD_IDADE_55_59',
            '60 a 64 anos': 'PCD_IDADE_60_64',
            '65 a 69 anos': 'PCD_IDADE_65_69',
            '70 a 74 anos': 'PCD_IDADE_70_74',
            '75 a 79 anos': 'PCD_IDADE_75_79',
            '80 a 84 anos': 'PCD_IDADE_80_84',
            '85 a 89 anos': 'PCD_IDADE_85_89',
            '90 a 94 anos': 'PCD_IDADE_90_94',
            '95 a 99 anos': 'PCD_IDADE_95_99',
            '100 anos ou mais': 'PCD_IDADE_100_MAIS'
        }

        dados = []
        for faixa, coluna in mapeamento.items():
            valor = self._somar_coluna(coluna)
            if valor > 0:
                dados.append({'Faixa Etária': faixa, 'Quantidade': valor})

        return pd.DataFrame(dados)

    def get_deficiencia_por_cor(self) -> pd.DataFrame:
        return pd.DataFrame({
            'Cor/Raça': ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
            'Quantidade': [
                self._somar_coluna('PCD_COR_BRANCA'),
                self._somar_coluna('PCD_COR_PRETA'),
                self._somar_coluna('PCD_COR_AMARELA'),
                self._somar_coluna('PCD_COR_PARDA'),
                self._somar_coluna('PCD_COR_INDIGENA')
            ]
        })

    def get_tipos_dificuldades(self) -> pd.DataFrame:
        return pd.DataFrame({
            'Tipo de Dificuldade': [
                'Enxergar',
                'Ouvir',
                'Andar/Subir degraus',
                'Pegar pequenos objetos',
                'Funções mentais/comunicação'
            ],
            'Quantidade': [
                self._somar_coluna('PCD_DIFICULDADE_ENXERGAR'),
                self._somar_coluna('PCD_DIFICULDADE_OUVIR'),
                self._somar_coluna('PCD_DIFICULDADE_ANDAR'),
                self._somar_coluna('PCD_DIFICULDADE_PEGAR_OBJETOS'),
                self._somar_coluna('PCD_DIFICULDADE_MENTAL')
            ]
        })

    def get_taxa_analfabetismo_por_cor(self) -> pd.DataFrame:
        return pd.DataFrame({
            'Cor/Raça': ['Total', 'Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
            'Taxa (%)': [
                self._somar_coluna('TAXA_ANALFABETISMO_PCD_TOTAL') / max(len(self.df), 1),
                self._somar_coluna('TAXA_ANALFABETISMO_PCD_BRANCA') / max(len(self.df), 1),
                self._somar_coluna('TAXA_ANALFABETISMO_PCD_PRETA') / max(len(self.df), 1),
                self._somar_coluna('TAXA_ANALFABETISMO_PCD_AMARELA') / max(len(self.df), 1),
                self._somar_coluna('TAXA_ANALFABETISMO_PCD_PARDA') / max(len(self.df), 1),
                self._somar_coluna('TAXA_ANALFABETISMO_PCD_INDIGENA') / max(len(self.df), 1)
            ]
        })

    def get_instrucao_pessoas_deficientes(self) -> pd.DataFrame:
        return pd.DataFrame({
            'Nível de Instrução': [
                'Sem instrução e fund. incompleto',
                'Fund. completo e médio incompleto',
                'Médio completo e superior incompleto',
                'Superior completo'
            ],
            'Quantidade': [
                self._somar_coluna('PCD_INSTRUCAO_SEM_INSTR_FUND_INCOMP'),
                self._somar_coluna('PCD_INSTRUCAO_FUND_COMP_MEDIO_INCOMP'),
                self._somar_coluna('PCD_INSTRUCAO_MEDIO_COMP_SUP_INCOMP'),
                self._somar_coluna('PCD_INSTRUCAO_SUPERIOR_COMP')
            ]
        })

    def get_indicadores_autismo(self) -> dict:
        pop_residente = self._somar_coluna('POPULACAO_RESIDENTE_TOTAL')
        com_autismo = self._somar_coluna('POPULACAO_RESIDENTE_DIAGNOSTICADA_COM_AUTISMO')
        taxa = (com_autismo / pop_residente * 100) if pop_residente > 0 else 0
        return {
            'populacao_residente': pop_residente,
            'diagnosticada_autismo': com_autismo,
            'taxa_autismo_percentual': taxa
        }

    def get_autismo_por_cor(self) -> pd.DataFrame:
        return pd.DataFrame({
            'Cor/Raça': ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena'],
            'Quantidade': [
                self._somar_coluna('AUTISMO_COR_BRANCA'),
                self._somar_coluna('AUTISMO_COR_PRETA'),
                self._somar_coluna('AUTISMO_COR_AMARELA'),
                self._somar_coluna('AUTISMO_COR_PARDA'),
                self._somar_coluna('AUTISMO_COR_INDIGENA')
            ]
        })

    def get_autismo_homens_mulheres(self) -> pd.DataFrame:
        return pd.DataFrame({
            'Sexo': ['Homens', 'Mulheres'],
            'Valor': [
                self._somar_coluna('AUTISMO_HOMENS'),
                self._somar_coluna('AUTISMO_MULHERES')
            ]
        })

    def get_autismo_25mais_instrucao(self) -> pd.DataFrame:
        return pd.DataFrame({
            'Nível de Instrução': [
                'Sem instrução e fund. incompleto',
                'Fund. completo e médio incompleto',
                'Médio completo e superior incompleto',
                'Superior completo'
            ],
            'Quantidade': [
                self._somar_coluna('AUTISMO_25_MAIS_SEM_INSTR_FUND_INCOMP'),
                self._somar_coluna('AUTISMO_25_MAIS_FUND_COMP_MEDIO_INCOMP'),
                self._somar_coluna('AUTISMO_25_MAIS_MEDIO_COMP_SUP_INCOMP'),
                self._somar_coluna('AUTISMO_25_MAIS_SUPERIOR_COMP')
            ]
        })

    def get_domicilios_com_morador_autismo(self) -> dict:
        total = self._somar_coluna('DOMICILIOS_TOTAL')
        com_autismo = self._somar_coluna('DOMICILIOS_COM_MORADOR_AUTISMO')
        percentual = (com_autismo / total * 100) if total > 0 else 0
        return {
            'domicilios_total': total,
            'domicilios_com_morador_autismo': com_autismo,
            'percentual': percentual
        }
