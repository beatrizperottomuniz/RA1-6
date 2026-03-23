'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1-6
'''
import sys
import json
from leituraArquivo import lerArquivo
from analisadorLexico import parseExpressao
import globalVars

def exportTokens(list_tokens, path_output="saida_tokens.txt"):
    serialized_tokens = []
    # token -> dicionario
    for token in list_tokens:
        serialized_tokens.append({
            "type": token.type,
            "line": token.line,
            "column": token.column,
            "symbol_id": token.symbol_id
        })
    # tokens + string pool
    data = {
        "string_pool": globalVars.string_pool_global.strings,
        "tokens": serialized_tokens
    }

    try:
        with open(path_output, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"\nTokens exportados para o arquivo: '{path_output}'")
    except Exception as e:
        print(f"\nFalha ao salvar o arquivo de tokens: {e}")


# ------------------------------------------------------------------------------------------------------------------------
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
        parseExpressao(line, tokens_list)
        globalVars.line_count_global += 1
        
    print(tokens_list)
    exportTokens(tokens_list)
