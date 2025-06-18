# Conta Horas Certificado

Este é um aplicativo web feito com Flask que permite ao usuário enviar arquivos PDF contendo registros de horas e retorna a soma total das horas encontradas nos documentos.

## Funcionalidades

  - Upload de múltiplos arquivos PDF.

  - Extração automática de horas e minutos do conteúdo dos PDFs.

  - Soma total de horas convertida e exibida.

  - Interface simples via navegador.

## Como usar

1. Clonar o repositório

        git clone https://https://github.com/Lucas-Blanger/contaHoras.git
        cd contaHoras


2. Instalar dependências

        pip install -r requirements.txt

4. Rodar o servidor Flask

         python app.py

## Como funciona

  - O usuário seleciona um ou mais arquivos PDF.

  - O conteúdo textual dos arquivos é extraído com PyPDF2.

  - Um padrão regex localiza ocorrências de horas e minutos.

  - Todos os valores são somados e exibidos ao usuário.

### Exemplos de padrões reconhecidos:

    12h, 5 horas, 1 hora, 30 minutos, 45minutos


## Requisitos

  - Python 3.7+

  - Flask

  - PyPDF2

## Você pode instalar tudo com:

    pip install flask PyPDF2

## Licença

Este projeto está licenciado sob a MIT License.
