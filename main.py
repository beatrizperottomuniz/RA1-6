'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1-6
'''
import sys
import json
from leituraArquivo import lerArquivo
from analisadorLexico import parseExpressao
import globalVars

def exportarTokens(lista_tokens, caminho_exportar="saida_tokens.txt"):
    tokens_serializados = []
    # token -> dicionario
    for token in lista_tokens:
        tokens_serializados.append({
            "type": token.type,
            "line": token.line,
            "column": token.column,
            "symbol_id": token.symbol_id
        })
    # tokens + string pool
    dados = {
        "string_pool": globalVars.string_pool_global.strings,
        "tokens": tokens_serializados
    }

    try:
        with open(caminho_exportar, 'w', encoding='utf-8') as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
        print(f"\nTokens exportados para o arquivo: '{caminho_exportar}'")
    except Exception as e:
        print(f"\nFalha ao salvar o arquivo de tokens: {e}")


# ------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python teste_lerArquivo.py <nome_do_arquivo>")
        sys.exit(1)

    caminho = sys.argv[1]
    linhas = []
    tokens_lista = []

    lerArquivo(caminho, linhas)
    globalVars.total_lines_global = len(linhas)
    for linha in linhas:
        print(linha)
        parseExpressao(linha, tokens_lista)
        globalVars.line_count_global += 1

    print(tokens_lista)
    exportarTokens(tokens_lista)
