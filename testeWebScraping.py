import requests
from bs4 import BeautifulSoup
import os
import zipfile

def baixar_compactar_anexos_url(url, pasta_destino="anexos"):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        links_pdf = []
        for link in soup.find_all("a", href=lambda href: href and href.endswith(".pdf")):
            if "Anexo_I" in link["href"] or "Anexo_2" in link["href"]:
                links_pdf.append(link["href"])

        if not links_pdf:
            print("Nenhum PDF com ANEXO_I ou ANEXO_2 na URL encontrado.")
            return

        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        arquivos_baixados = []

        for link_pdf in links_pdf:
            nome_arquivo = os.path.basename(link_pdf)
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

            response_pdf = requests.get(link_pdf)
            response_pdf.raise_for_status()

            with open(caminho_arquivo, "wb") as arquivo_pdf:
                arquivo_pdf.write(response_pdf.content)

            arquivos_baixados.append(caminho_arquivo)
            print(f"PDF '{nome_arquivo}' baixado.")

        nome_zip = "anexos.zip"
        with zipfile.ZipFile(nome_zip, "w") as arquivo_zip:
            for arquivo in arquivos_baixados:
                arquivo_zip.write(arquivo, os.path.basename(arquivo))

        print(f"Anexos com ANEXO_I e ANEXO_2 compactados em '{nome_zip}'.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site ou baixar os arquivos: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
baixar_compactar_anexos_url(url)