import csv
import os

def remover_zeros_esquerda(input_file, output_file):
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
             open(output_file, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.reader(infile, delimiter=';')  
            writer = csv.writer(outfile, delimiter=';')

            header = next(reader)  
            writer.writerow(header)  

            for row in reader:
                reg_ans = row[1].lstrip('0')  
                row[1] = reg_ans
                writer.writerow(row)

        print(f"Arquivo CSV modificado com sucesso: {output_file}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

arquivos_csv = [
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\1T2023.csv',
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\1T2024.csv',
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\2t2023.csv',
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\2T2024.csv',
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\3T2023.csv',
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\3T2024.csv',
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\4T2023.csv',
    r'C:\Users\Michael\Documents\TestesIntuitiveCare\testeBancoDeDados\4T2024.csv',
]

for arquivo_csv in arquivos_csv:
    nome_arquivo = os.path.basename(arquivo_csv)
    nome_arquivo_modificado = nome_arquivo.replace('.csv', '_modificado.csv')
    caminho_arquivo_modificado = os.path.join(os.path.dirname(arquivo_csv), nome_arquivo_modificado)
    remover_zeros_esquerda(arquivo_csv, caminho_arquivo_modificado)

    os.remove(arquivo_csv)
    os.rename(caminho_arquivo_modificado, arquivo_csv)

    print(f"Arquivo '{nome_arquivo}' substituído com sucesso.")