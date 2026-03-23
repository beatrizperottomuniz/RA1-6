import sys
from leituraArquivo import lerArquivo
from analisadorLexico import parseExpressao
import globalVars

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python teste_lerArquivo.py <nome_do_arquivo>")
        sys.exit(1)

    path = sys.argv[1]
    lines = lerArquivo(path)
    tokens_list = []
    globalVars.total_lines_global = len(lines)
    for line in lines:
        print(line)
        tokens = parseExpressao(line)
        print(tokens)
        tokens_list.append(tokens)
        globalVars.line_count_global += 1
