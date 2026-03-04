class BaseFiltrosPerfilMixin:
    def filtrar_por_uf(self, uf: str):
        if 'uf' not in self.df.columns:
            print("Coluna 'uf' não encontrada")
            return self

        self.df = self.df[self.df['uf'].str.upper() == uf.upper()]
        print(f"Filtrado para UF {uf.upper()}: {len(self.df):,} registros")
        return self

    def filtrar_por_regiao(self, regiao: str):
        if 'regiao' not in self.df.columns:
            print("Coluna 'regiao' não encontrada")
            return self

        self.df = self.df[self.df['regiao'].str.lower() == regiao.lower()]
        print(f"Filtrado para Região {regiao}: {len(self.df):,} registros")
        return self

    def filtrar_por_area(self, area: str):
        if 'area' not in self.df.columns:
            print("Coluna 'area' não encontrada")
            return self

        self.df = self.df[self.df['area'].str.lower() == area.lower()]
        print(f"Filtrado para Área {area}: {len(self.df):,} registros")
        return self

    def filtrar_por_tipo_deficiencia(self, tipo: str):
        if 'tipo_deficiencia' not in self.df.columns:
            print("Coluna 'tipo_deficiencia' não encontrada")
            return self

        self.df = self.df[self.df['tipo_deficiencia'].str.lower() == tipo.lower()]
        print(f"Filtrado para Deficiência {tipo}: {len(self.df):,} registros")
        return self

    def filtrar_com_deficiencia(self, tem: bool = True):
        if 'tem_deficiencia' not in self.df.columns:
            print("Coluna 'tem_deficiencia' não encontrada")
            return self

        self.df = self.df[self.df['tem_deficiencia'] == tem]
        texto = "COM deficiência" if tem else "SEM deficiência"
        print(f"Filtrado pessoas {texto}: {len(self.df):,} registros")
        return self

    def filtrar_por_grau_deficiencia(self, grau: str):
        if 'grau_deficiencia' not in self.df.columns:
            print("Coluna 'grau_deficiencia' não encontrada")
            return self

        self.df = self.df[self.df['grau_deficiencia'].str.lower() == grau.lower()]
        print(f"Filtrado por grau {grau}: {len(self.df):,} registros")
        return self

    def filtrar_por_faixa_etaria(self, faixa: str):
        if 'faixa_etaria' not in self.df.columns:
            print("Coluna 'faixa_etaria' não encontrada")
            return self

        self.df = self.df[self.df['faixa_etaria'] == faixa]
        print(f"Filtrado para faixa etária {faixa}: {len(self.df):,} registros")
        return self

    def filtrar_por_sexo(self, sexo: str):
        if 'sexo' not in self.df.columns:
            print("Coluna 'sexo' não encontrada")
            return self

        self.df = self.df[self.df['sexo'].str.lower() == sexo.lower()]
        print(f"Filtrado por sexo {sexo}: {len(self.df):,} registros")
        return self

    def filtrar_por_escolaridade(self, escolaridade: str):
        if 'escolaridade' not in self.df.columns:
            print("Coluna 'escolaridade' não encontrada")
            return self

        self.df = self.df[self.df['escolaridade'] == escolaridade]
        print(f"Filtrado por escolaridade {escolaridade}: {len(self.df):,} registros")
        return self

    def filtrar_por_renda(self, faixa_renda: str):
        if 'renda_familiar' not in self.df.columns:
            print("Coluna 'renda_familiar' não encontrada")
            return self

        self.df = self.df[self.df['renda_familiar'] == faixa_renda]
        print(f"Filtrado por renda {faixa_renda}: {len(self.df):,} registros")
        return self

    def filtrar_com_internet(self, tem: bool = True):
        if 'tem_internet' not in self.df.columns:
            print("Coluna 'tem_internet' não encontrada")
            return self

        self.df = self.df[self.df['tem_internet'] == tem]
        texto = "COM" if tem else "SEM"
        print(f"Filtrado pessoas {texto} internet: {len(self.df):,} registros")
        return self

    def filtrar_por_frequencia_uso(self, frequencia: str):
        if 'frequencia_uso' not in self.df.columns:
            print("Coluna 'frequencia_uso' não encontrada")
            return self

        self.df = self.df[self.df['frequencia_uso'].str.lower() == frequencia.lower()]
        print(f"Filtrado por frequência {frequencia}: {len(self.df):,} registros")
        return self
