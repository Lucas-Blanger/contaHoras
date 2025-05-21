import os
import re
from flask import Flask, render_template, request
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extrair_horas_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            texto = ""
            for pagina in reader.pages:
                texto += pagina.extract_text() or ""
            texto = re.sub(r"\s+", " ", texto.lower())
            padrao = r"(\d{1,3})\s*(h|hora[s]?)|(\d{1,2})\s*(minuto[s]?)"
            total_horas = 0
            for h, _, m, _ in re.findall(padrao, texto):
                if h:
                    total_horas += int(h)
                elif m:
                    total_horas += int(m) / 60
            return round(total_horas, 2)
    except Exception as e:
        return f"Erro: {e}"


@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    total = 0
    if request.method == "POST":
        arquivos = request.files.getlist("pdfs")
        for arquivo in arquivos:
            if arquivo and arquivo.filename.endswith(".pdf"):
                filename = secure_filename(arquivo.filename)
                caminho = os.path.join(UPLOAD_FOLDER, filename)
                arquivo.save(caminho)
                horas = extrair_horas_pdf(caminho)
                resultados.append((filename, horas))
                if isinstance(horas, (int, float)):
                    total += horas
        return render_template(
            "index.html", resultados=resultados, total=round(total, 2)
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
