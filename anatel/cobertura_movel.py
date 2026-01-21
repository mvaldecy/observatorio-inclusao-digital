# ... existing code ...
    def filtrar_dados(self, **kwargs):
        """
        Filtra o DataFrame dinamicamente com base nos critérios fornecidos.
        Ignora colunas inexistentes e valores de placeholder ('Todos', 'Brasil', etc).
        """
        if self.df.empty:
            return self.df

        # Criamos uma cópia inicial para não mutar o DataFrame original da classe
        df_filtrado = self.df.copy()
        
        # Valores que indicam que nenhum filtro deve ser aplicado naquela coluna
        ignore_values = {"Todos", "Todas as UFs", "Todas", "Brasil", "Todos os Municípios"}

        for coluna, valor in kwargs.items():
            # 1. Pular se a coluna não existir
            if coluna not in df_filtrado.columns:
                continue
            
            # 2. Pular se o valor for nulo ou um placeholder de "ignorar"
            if valor is None or valor in ignore_values:
                continue

            # 3. Aplicar o filtro (suporta valor único ou lista de valores)
            if isinstance(valor, list):
                df_filtrado = df_filtrado[df_filtrado[coluna].isin(valor)]
            else:
                df_filtrado = df_filtrado[df_filtrado[coluna] == valor]

        return df_filtrado
# ... existing code ...