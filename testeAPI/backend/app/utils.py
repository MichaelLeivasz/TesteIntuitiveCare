import re
import pandas as pd

def converter_codigo(codigo):
    """Converte código de notação científica para 8 dígitos."""
    if isinstance(codigo, str):
        match = re.match(r'([\d,.]+)', codigo)
        if match:
            codigo_base = match.group(1).replace(',', '')
            if len(codigo_base) >= 8:
                return codigo_base[:8]
            else:
                return codigo_base + '0' * (8 - len(codigo_base))
    return codigo

def limpar_dados(operadora):
    """Limpa dados da operadora."""
    operadora_limpa = {k: v for k, v in operadora.items() if k != 'Razao_Social_Normalizada'}
    for key, value in operadora_limpa.items():
        if pd.isna(value):
            operadora_limpa[key] = None
    return operadora_limpa