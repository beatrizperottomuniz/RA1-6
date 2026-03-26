'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1 6
'''
from Token import TokenType
from geradorAssembly import resgatarLexema

def executarExpressao(tokens: list, resultados: list, memoria: dict) -> None:
    pilha = []
    ultimo_foi_val = False
    ultimo_num    = 0.0   # para pegar numero da linha de RES
    for token in tokens:

        if token.type in (TokenType.LPAREN, TokenType.RPAREN, TokenType.EOF):
            continue

        if token.type in (TokenType.NUM_INT, TokenType.NUM_FLOAT):
            valor = float(token.symbol_id)
            pilha.append(valor)
            ultimo_foi_val = True
            ultimo_num    = valor
            continue

        if token.type == TokenType.ID:
            nome_var = resgatarLexema(token)
            if ultimo_foi_val: # caso (Valor VARIAVEL)
                valor = pilha.pop()
                memoria[nome_var] = valor
                pilha.append(valor)
            else:
                valor = memoria.get(nome_var, 0.0)
                pilha.append(valor)
            ultimo_foi_val = True
            continue

        if token.type == TokenType.KEYWORD_RES:
            n = int(ultimo_num)
            pilha.pop()
            linha_atual = len(resultados)
            i = linha_atual - n
            if 0 <= i < len(resultados):
                pilha.append(resultados[i])
            else:
                pilha.append(0.0)   # se a linha nao existe
            ultimo_foi_val = True
            continue

        if token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULT,
                          TokenType.DIV, TokenType.INT_DIV, TokenType.MOD,
                          TokenType.POW):
            num_direita = pilha.pop()
            num_esquerda  = pilha.pop()

            if token.type == TokenType.PLUS:
                pilha.append(num_esquerda + num_direita)
            elif token.type == TokenType.MINUS:
                pilha.append(num_esquerda - num_direita)
            elif token.type == TokenType.MULT:
                pilha.append(num_esquerda * num_direita)
            elif token.type == TokenType.DIV:
                pilha.append(num_esquerda / num_direita)
            elif token.type == TokenType.INT_DIV:
                pilha.append(float(int(num_esquerda / num_direita)))
            elif token.type == TokenType.MOD:
                quociente = float(int(num_esquerda / num_direita))
                pilha.append(num_esquerda - quociente * num_direita)
            elif token.type == TokenType.POW:
                acumulador = 1.0
                expoente   = int(num_direita)
                for _ in range(expoente):
                    acumulador = acumulador * num_esquerda
                pilha.append(acumulador)

            ultimo_foi_val = True
            continue

    resultado_final = pilha[-1] if pilha else 0.0
    resultados.append(resultado_final)
