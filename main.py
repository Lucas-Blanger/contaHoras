import os
import re
import PyPDF2


def extrairHorasPdf(caminho_pdf):
    try:
        with open(caminho_pdf, "rb") as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            texto = ""
            for pagina in leitor.pages:
                texto += pagina.extract_text()
            print(f"\n===== TEXTO DE {os.path.basename(caminho_pdf)} =====")
            print(texto)

            padrao = r"(\d{1,3})\s*(h|hora[s]?)"
            correspondencias = re.findall(padrao, texto.lower())
            print(f"Encontrado: {correspondencias}")
            if correspondencias:
                return sum(int(valor) for valor, _ in correspondencias)
            return 0
    except Exception as e:
        print(f"Erro ao processar {caminho_pdf}: {e}")
        return 0


def somarHoras(pasta):
    total = 0
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, nome_arquivo)
            horas = extrairHorasPdf(caminho_pdf)
            print(f"{nome_arquivo}: {horas} horas")
            total += horas
    print(f"\nTotal acumulado: {total} horas")
    return total


pasta_certificados = r""
somarHoras(pasta_certificados)