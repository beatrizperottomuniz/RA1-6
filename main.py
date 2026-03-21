import sys
from leituraArquivo import lerArquivo

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python teste_lerArquivo.py <nome_do_arquivo>")
        sys.exit(1)

    nome = sys.argv[1]
    linhas = lerArquivo(nome)
