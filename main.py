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
            padrao = r"(\d{1,3})\s*(h|hora[s]?)"
            correspondencias = re.findall(padrao, texto.lower())
            if correspondencias:
                return sum(int(valor) for valor, _ in correspondencias)
            return 0
    except Exception as e:
        print(f"Erro ao processar {caminho_pdf}: {e}")
        return 0

def escreverResultado(mensagem):
    campoResultado.configure(state="normal")
    campoResultado.delete("1.0", "end")
    campoResultado.insert("1.0", mensagem)
    campoResultado.configure(state="disabled")


def escolherArquivo():
    caminho_pdf = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho_pdf:
        horas = extrairHorasPdf(caminho_pdf)
        msg = f"{os.path.basename(caminho_pdf)}: {horas} horas"
        escreverResultado(msg)

def escolherPasta():
    pasta = filedialog.askdirectory()
    if pasta:
        total = 0
        resultado = ""
        for nome_arquivo in os.listdir(pasta):
            if nome_arquivo.lower().endswith(".pdf"):
                caminho_pdf = os.path.join(pasta, nome_arquivo)
                horas = extrairHorasPdf(caminho_pdf)
                resultado += f"{nome_arquivo}: {horas} horas\n"
                total += horas
        resultado += f"\nTotal acumulado: {total} horas"
        escreverResultado(resultado)

def salvarResultado():
    conteudo = campoResultado.get("1.0", "end").strip()
    if conteudo:
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de texto", "*.txt")])
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
            messagebox.showinfo("Salvo", "Resultado exportado com sucesso!")


ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

janela = ctk.CTk()
janela.title("Leitor de Certificados PDF")
janela.geometry("600x550")

try:
    janela.iconbitmap("icone.ico")
except:
    pass

titulo = ctk.CTkLabel(janela, text="Leitor de Certificados PDF", font=ctk.CTkFont(size=22, weight="bold"))
titulo.pack(pady=20)


btn_arquivo = ctk.CTkButton(janela, text="Selecionar um PDF", command=escolherArquivo, width=300, height=45)
btn_arquivo.pack(pady=10)

btn_pasta = ctk.CTkButton(janela, text="Selecionar Pasta de PDFs", command=escolherPasta, width=300, height=45)
btn_pasta.pack(pady=10)

campoResultado = ctk.CTkTextbox(janela, height=200, width=500, state="disabled", font=("Arial", 14))
campoResultado.pack(pady=20)

btn_salvar = ctk.CTkButton(janela, text="Salvar Resultado em .txt", command=salvarResultado, width=200)
btn_salvar.pack(pady=10)


rodape = ctk.CTkLabel(janela, text="Desenvolvido por Lucas Blanger", font=ctk.CTkFont(size=12))
rodape.pack(side="bottom", pady=10)

janela.mainloop()
