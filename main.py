import os
import re
import PyPDF2
import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging


LANG = "pt"

textos = {
    "pt": {
        "titulo": "Leitor de Certificados PDF",
        "selecionar_pdf": "Selecionar um PDF",
        "selecionar_pasta": "Selecionar Pasta de PDFs",
        "salvar_resultado": "Salvar Resultado em .txt",
        "desenvolvedor": "Desenvolvido por Lucas Blanger 🐺",
        "sucesso": "Resultado exportado com sucesso!",
        "erro_processar": "Erro ao processar o arquivo:\n{}",
        "total_acumulado": "\nTotal acumulado: {:.2f} horas",
        "processamento_concluido": "Processamento concluído",
    },
    "en": {
        "titulo": "PDF Certificate Reader",
        "selecionar_pdf": "Select a PDF",
        "selecionar_pasta": "Select PDF Folder",
        "salvar_resultado": "Save Result as .txt",
        "desenvolvedor": "Developed by Lucas Blanger 🐺",
        "sucesso": "Result exported successfully!",
        "erro_processar": "Error processing file:\n{}",
        "total_acumulado": "\nTotal accumulated: {:.2f} hours",
        "processamento_concluido": "Processing completed",
    },
}

T = textos[LANG]

# === LOG DE ERROS ===
logging.basicConfig(filename="erros.log", level=logging.ERROR)


def extrairHorasPdf(caminho_pdf):
    try:
        with open(caminho_pdf, "rb") as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            texto = ""
            for pagina in leitor.pages:
                texto += pagina.extract_text() or ""
            texto = re.sub(r"\s+", " ", texto.lower())
            padrao = r"(\d{1,3})\s*(h|hora[s]?)|(\d{1,2})\s*(minuto[s]?)"
            total_horas = 0
            for h, _, m, _ in re.findall(padrao, texto):
                if h:
                    total_horas += int(h)
                elif m:
                    total_horas += int(m) / 60
            return total_horas
    except Exception as e:
        logging.error(f"Erro ao processar {caminho_pdf}: {e}")
        messagebox.showerror("Erro", T["erro_processar"].format(caminho_pdf))
        return 0


def escreverResultado(mensagem):
    campoResultado.configure(state="normal")
    campoResultado.delete("1.0", "end")
    campoResultado.insert("1.0", mensagem)
    campoResultado.configure(state="disabled")
    btn_salvar.configure(state="normal")


def escolherArquivo():
    caminho_pdf = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho_pdf:
        horas = extrairHorasPdf(caminho_pdf)
        msg = f"{os.path.basename(caminho_pdf)}: {horas:.2f} horas"
        escreverResultado(msg)
        messagebox.showinfo(T["processamento_concluido"], msg)


def escolherPasta():
    pasta = filedialog.askdirectory()
    if pasta:
        total = 0
        resultado = ""
        for nome_arquivo in os.listdir(pasta):
            if nome_arquivo.lower().endswith(".pdf"):
                caminho_pdf = os.path.join(pasta, nome_arquivo)
                horas = extrairHorasPdf(caminho_pdf)
                resultado += f"{nome_arquivo}: {horas:.2f} horas\n"
                total += horas
        resultado += T["total_acumulado"].format(total)
        escreverResultado(resultado)
        messagebox.showinfo(T["processamento_concluido"], T["processamento_concluido"])


def salvarResultado():
    conteudo = campoResultado.get("1.0", "end").strip()
    if conteudo:
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Arquivo de texto", "*.txt")]
        )
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
            messagebox.showinfo("Salvo", T["sucesso"])


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title(T["titulo"])
janela.geometry("640x580")

try:
    janela.iconbitmap("icon.ico")
except:
    pass

titulo = ctk.CTkLabel(
    janela, text=T["titulo"], font=ctk.CTkFont(size=22, weight="bold")
)
titulo.pack(pady=20)

btn_arquivo = ctk.CTkButton(
    janela, text=T["selecionar_pdf"], command=escolherArquivo, width=300, height=45
)
btn_arquivo.pack(pady=10)
btn_arquivo.focus_set()

btn_pasta = ctk.CTkButton(
    janela, text=T["selecionar_pasta"], command=escolherPasta, width=300, height=45
)
btn_pasta.pack(pady=10)

frame_resultado = ctk.CTkFrame(janela)
frame_resultado.pack(pady=10)

campoResultado = ctk.CTkTextbox(
    frame_resultado, height=200, width=500, state="disabled", font=("Arial", 14)
)
campoResultado.pack(side="left")

scrollbar = ctk.CTkScrollbar(frame_resultado, command=campoResultado.yview)
scrollbar.pack(side="right", fill="y")
campoResultado.configure(yscrollcommand=scrollbar.set)

btn_salvar = ctk.CTkButton(
    janela,
    text=T["salvar_resultado"],
    command=salvarResultado,
    width=200,
    state="disabled",
)
btn_salvar.pack(pady=10)

rodape = ctk.CTkLabel(janela, text=T["desenvolvedor"], font=ctk.CTkFont(size=12))
rodape.pack(side="bottom", pady=10)

janela.mainloop()
