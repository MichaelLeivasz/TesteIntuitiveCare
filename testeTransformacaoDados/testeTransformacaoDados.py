import pdfplumber
from pathlib import Path
import pandas as pd
import zipfile
import os
import re

def extrair_texto_pdf(pdf_path, start_page=0):
    """Extrai o texto de um arquivo PDF a partir de uma página específica."""
    textos = []
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start_page, len(pdf.pages)):
            page_text = pdf.pages[i].extract_text()
            if page_text:
                textos.append(page_text)
    return "\n".join(textos)

def extrair_dados_tabela(pdf_path):
    """Extrai os dados da tabela do PDF de forma estruturada."""
    dados = []
    cabecalho = None
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })
            for tabela in tabelas:
                if tabela:
                    if not cabecalho:
                        cabecalho, *linhas = tabela 
                        cabecalho = [celula or "" for celula in cabecalho]
                    else:
                        linhas = tabela[1:]
                    dados.extend(linhas)
    return cabecalho or [], dados

def extrair_definicoes_rodape(pdf_path, start_page=2):
    """Extrai as definições de OD e AMB do rodapé de uma página - neste caso, a apartir da terceira."""
    definicoes = {}
    with pdfplumber.open(pdf_path) as pdf:
        if start_page < len(pdf.pages):
            texto = pdf.pages[start_page].extract_text()
            if texto:
                for chave in ["OD", "AMB"]:
                    match = re.search(rf"{chave}:\s*([\S]+\s+[\S]+)", texto)
                    if match:
                        definicoes[chave] = match.group(1)
    return definicoes

def substituir_abreviacoes(df, definicoes_rodape):
    """Substitui as abreviações OD e AMB pelas descrições completas no cabeçalho e nos dados."""
    if not definicoes_rodape:
        return df 
    
    padroes = {re.compile(rf"\b{chave}\b"): definicao for chave, definicao in definicoes_rodape.items()}
    
    def substituir_texto(valor):
        if isinstance(valor, str):
            for padrao, definicao in padroes.items():
                valor = padrao.sub(definicao, valor)
        return valor
    
    df.columns = [substituir_texto(coluna) for coluna in df.columns]
    return df.map(substituir_texto)

def salvar_csv(df, caminho_csv, incluir_cabecalho=True):
    """Salva os dados em um arquivo CSV sem índice e com cabeçalho."""
    df.to_csv(caminho_csv, index=False, encoding='utf-8-sig', sep=';', header=incluir_cabecalho, mode='w')

def compactar_arquivo(caminho_csv, caminho_zip):
    """Compacta o arquivo CSV em um ZIP."""
    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(caminho_csv, os.path.basename(caminho_csv))


caminho_pdf = r"testeWebScraping\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
diretorio_atual = Path(__file__).parent
caminho_csv = diretorio_atual / "Teste_Michael.csv"
caminho_zip = r"testeTransformacaoDados\Teste_Michael.zip"


cabecalho, dados = extrair_dados_tabela(caminho_pdf)
definicoes_rodape = extrair_definicoes_rodape(caminho_pdf)

df = pd.DataFrame(dados, columns=cabecalho) if cabecalho else pd.DataFrame(dados)
df = substituir_abreviacoes(df, definicoes_rodape)

salvar_csv(df, caminho_csv, incluir_cabecalho=True)
compactar_arquivo(caminho_csv, caminho_zip)

print(f"Arquivo ZIP criado: {caminho_zip}")
