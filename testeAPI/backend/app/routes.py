from flask import jsonify, request
from .data import operadoras
from .utils import limpar_dados
from fuzzywuzzy import fuzz
import pandas as pd

def buscar_operadoras():
    termo = request.args.get('termo')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    if not termo:
        return jsonify({'erro': 'O parâmetro "termo" é obrigatório.'}), 400

    termo_busca = termo.lower().strip().replace('  ', ' ').replace('-', '').replace('/', '')
    resultados = []
    for operadora in operadoras:
        razao_social_normalizada = operadora['Razao_Social_Normalizada']
        pontuacao = fuzz.partial_ratio(termo_busca, razao_social_normalizada)
        if pontuacao > 90:
            operadora_limpa = limpar_dados(operadora)
            resultados.append({**operadora_limpa, 'pontuacao': pontuacao})
    resultados = sorted(resultados, key=lambda x: x['pontuacao'], reverse=True)

    resultados_limpos = [limpar_dados(r) for r in resultados]

    start = (page - 1) * per_page
    end = start + per_page
    resultados_paginados = resultados_limpos[start:end]

    return jsonify({
        'total': len(resultados_limpos),
        'resultados': resultados_paginados
    })