import os
import re
import PyPDF2
import customtkinter as ctk
from tkinter import filedialog, messagebox


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
        if nome_arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(pasta, nome_arquivo)
            horas = extrairHorasPdf(caminho_pdf)
            print(f"{nome_arquivo}: {horas} horas")
            total += horas
    print(f"\nTotal acumulado: {total} horas")
    messagebox.showinfo("Resultado", f"Total acumulado: {total} horas")
    return total


def escolherArquivo():
    caminho_pdf = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho_pdf:
        horas = extrairHorasPdf(caminho_pdf)
        messagebox.showinfo("Resultado", f"{os.path.basename(caminho_pdf)}: {horas} horas")


def escolherPasta():
    pasta = filedialog.askdirectory()
    if pasta:
        somarHoras(pasta)


# ==== CONFIGURAÇÕES DA JANELA ====
ctk.set_appearance_mode("System")  # opções: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # ou "green", "dark-blue", etc.

janela = ctk.CTk()
janela.title("Leitor de Certificados PDF")
janela.geometry("500x350")

# TÍTULO
titulo = ctk.CTkLabel(
    janela,
    text="Leitor de Certificados PDF",
    font=ctk.CTkFont(size=20, weight="bold")
)
titulo.pack(pady=30)

# BOTÃO: Selecionar PDF
botao_pdf = ctk.CTkButton(
    janela,
    text="Selecionar um PDF",
    command=escolherArquivo,
    width=250,
    height=50
)
botao_pdf.pack(pady=15)

# BOTÃO: Selecionar Pasta
botao_pasta = ctk.CTkButton(
    janela,
    text="Selecionar Pasta de PDFs",
    command=escolherPasta,
    width=250,
    height=50
)
botao_pasta.pack(pady=15)

# RODAPÉ
rodape = ctk.CTkLabel(
    janela,
    text="Desenvolvido por você 😊",
    font=ctk.CTkFont(size=12)
)
rodape.pack(side="bottom", pady=15)

janela.mainloop()
