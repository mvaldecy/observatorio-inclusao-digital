from conectividade_escolas.conectividade_escolas import AnalisadorConectividadeEscolas
from pathlib import Path

path = Path('conectividade_escolas')
analisador = AnalisadorConectividadeEscolas(data_path=path)

print('Dados carregados:', len(analisador.df), 'linhas')
print('\nColunas com internet:')
print(analisador.df[['Data', 'SG_UF', 'NO_REGIAO', 'CONECT_POSSUI_INTERNET']].head(10))
print('\nValores de CONECT_POSSUI_INTERNET:')
print(analisador.df['CONECT_POSSUI_INTERNET'].value_counts())
print('\nDados do Brasil:')
print('Total:', len(analisador.df))
print('Com internet:', len(analisador.df[analisador.df['CONECT_POSSUI_INTERNET'] == 1]))
print('Percentual:', (len(analisador.df[analisador.df['CONECT_POSSUI_INTERNET'] == 1]) / len(analisador.df) * 100))
