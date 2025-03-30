import pandas as pd
import logging
from .utils import converter_codigo

try:
    df = pd.read_csv('Relatorio_cadop.csv', sep=';', dtype={'CNPJ': str})
    df['CNPJ'] = df['CNPJ'].apply(converter_codigo)
    df['Razao_Social_Normalizada'] = df['Razao_Social'].str.lower().str.strip().str.replace('  ', ' ').replace('-', '').replace('/', '')
    operadoras = df.to_dict(orient='records')
except FileNotFoundError:
    logging.error("Arquivo CSV não encontrado.")
    operadoras = []
except pd.errors.ParserError as e:
    logging.error(f"Erro ao ler o arquivo CSV: {e}")
    operadoras = []