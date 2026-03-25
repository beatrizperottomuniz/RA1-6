'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1-6
'''
import struct
from Token import TokenType
from globalVars import string_pool_global

constantes = {}        # valor -> label no assembly
variaveis = set()      # nomes das variaveis salvas
resultados_linha = []  # lbl dos resultados de cada linha para RES
contador_label = 0


def novoLabel(prefixo="LBL"):
    global contador_label
    contador_label += 1
    return f"{prefixo}_{contador_label}"

def doubleParaBits(valor):
    #string para duas palavras de 32 b (IEEE 754 64 b little-endian)
    packed = struct.pack('<d', float(valor))
    word_baixo = struct.unpack('<I', packed[0:4])[0]
    word_alto = struct.unpack('<I', packed[4:8])[0]
    return word_baixo, word_alto

def resgatarLexema(token):
    if token.type in (TokenType.NUM_INT, TokenType.NUM_FLOAT):
        return str(token.symbol_id)
    operadores = {TokenType.PLUS: "+", TokenType.MINUS: "-", TokenType.MULT: "*", 
                  TokenType.DIV: "/", TokenType.INT_DIV: "//", TokenType.MOD: "%", TokenType.POW: "^"}
    if token.type in operadores:
        return operadores[token.type]
    if token.symbol_id is not None:
        return string_pool_global.get_string(token.symbol_id)
    return ""


def gerarAssembly(tokens: list, codigoAssembly: list) -> None:
    global contador_label
    asm = []
    
    linha_atual = len(resultados_linha) + 1
    ultimo_foi_valor = False
    ultimo_numero = "0"
    tem_eof = False

    asm.append(f"\n    @ --- linha {linha_atual} ---")

    for token in tokens:
        if token.type == TokenType.EOF:
            tem_eof = True
            continue

        if token.type in (TokenType.LPAREN, TokenType.RPAREN):
            continue

        lex = resgatarLexema(token)

        if token.type in (TokenType.NUM_INT, TokenType.NUM_FLOAT):
            lex = str(float(lex)) # para n duplicar (tipo 2.0 e 2)
            
            if lex not in constantes:
                constantes[lex] = novoLabel("CONST")
            
            lbl = constantes[lex]
            
            asm.append(f"    LDR r0, ={lbl}")
            asm.append(f"    VLDR d0, [r0]")
            asm.append(f"    VSTMDB sp!, {{d0}}")
            
            ultimo_foi_valor = True
            ultimo_numero = lex

        elif token.type == TokenType.ID:
            variaveis.add(lex)
            if ultimo_foi_valor:
                # Store
                asm.append(f"    VLDMIA sp!, {{d0}}")
                asm.append(f"    LDR r1, ={lex}_MEM")
                asm.append(f"    VSTR d0, [r1]")
                asm.append(f"    VSTMDB sp!, {{d0}}")
            else:
                # Load -> carrega p/ pilha)
                asm.append(f"    LDR r0, ={lex}_MEM")
                asm.append(f"    VLDR d0, [r0]")
                asm.append(f"    VSTMDB sp!, {{d0}}")
            ultimo_foi_valor = True

        elif token.type == TokenType.KEYWORD_RES:
            n = int(ultimo_numero)
            asm.append(f"    ADD sp, sp, #8")

            idx = (linha_atual - 1) - n

            # n=0 ou indice invalido: retorna 0.0
            if n == 0 or idx < 0 or idx >= len(resultados_linha):
                #asm.append(f"    @ ({n} RES) invalido -> retorna 0.0")
                if "0.0" not in constantes:
                    constantes["0.0"] = novoLabel("CONST")
                asm.append(f"    LDR r0, ={constantes['0.0']}")
                asm.append(f"    VLDR d0, [r0]")
                asm.append(f"    VSTMDB sp!, {{d0}}")
                ultimo_foi_valor = True
                continue

            lbl_res = resultados_linha[idx]
            asm.append(f"    LDR r0, ={lbl_res}")
            asm.append(f"    VLDR d0, [r0]")
            asm.append(f"    VSTMDB sp!, {{d0}}")
            ultimo_foi_valor = True

        elif token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV, 
                            TokenType.INT_DIV, TokenType.MOD, TokenType.POW):
            
            # desempilhar operandos (d1 = direita, d0 = esquerda)
            asm.append(f"    VLDMIA sp!, {{d1}}")
            asm.append(f"    VLDMIA sp!, {{d0}}")

            if token.type == TokenType.PLUS:
                asm.append("    VADD.F64 d0, d0, d1")
            elif token.type == TokenType.MINUS:
                asm.append("    VSUB.F64 d0, d0, d1")
            elif token.type == TokenType.MULT:
                asm.append("    VMUL.F64 d0, d0, d1")
            elif token.type == TokenType.DIV:
                asm.append("    VDIV.F64 d0, d0, d1")
                
            elif token.type == TokenType.INT_DIV:
                asm.append("    VDIV.F64 d2, d0, d1")
                asm.append("    VCVT.S32.F64 s4, d2")
                asm.append("    VCVT.F64.S32 d0, s4")
                
            elif token.type == TokenType.MOD:
                asm.append("    VDIV.F64 d2, d0, d1")
                asm.append("    VCVT.S32.F64 s4, d2")
                asm.append("    VCVT.F64.S32 d2, s4")
                asm.append("    VMUL.F64 d2, d2, d1")
                asm.append("    VSUB.F64 d0, d0, d2")
                
            elif token.type == TokenType.POW:
                lbl_loop = novoLabel("POW_LOOP")
                lbl_fim  = novoLabel("POW_FIM")
                
                asm.append("    VMOV.F64 d2, d0")
                asm.append("    VCVT.S32.F64 s0, d1")
                asm.append("    VMOV r2, s0")
                
                if "1.0" not in constantes: constantes["1.0"] = novoLabel("CONST")
                asm.append(f"    LDR r0, ={constantes['1.0']}")
                asm.append("    VLDR d0, [r0]")
                
                asm.append(f"{lbl_loop}:")
                asm.append("    CMP r2, #0")
                asm.append(f"    BLE {lbl_fim}")
                asm.append("    VMUL.F64 d0, d0, d2")
                asm.append("    SUB r2, r2, #1")
                asm.append(f"    B {lbl_loop}")
                asm.append(f"{lbl_fim}:")

            asm.append("    VSTMDB sp!, {d0}")
            ultimo_foi_valor = True

    lbl_linha = f"RES_LINHA_{linha_atual}"
    resultados_linha.append(lbl_linha)
    
    if ultimo_foi_valor:
        asm.append(f"    VLDMIA sp!, {{d0}}")
        asm.append(f"    LDR r3, ={lbl_linha}")
        asm.append(f"    VSTR d0, [r3]")

    codigoAssembly.extend(asm)
    if tem_eof:
        finalizarAssembly(codigoAssembly)



def finalizarAssembly(codigo: list) -> None:
    out = [
        "    .syntax unified",
        "    .arch armv7-a",
        "    .fpu vfpv3-d16",
        "",
        "    .data"
    ]

    # vars 8 bytes
    for v in variaveis:
        out.append(f"{v}_MEM: .space 8")
    for res in resultados_linha:
        out.append(f"{res}: .space 8")

    # consts
    for val, lbl in constantes.items():
        wb, wa = doubleParaBits(val)
        out.append(f"{lbl}: .word 0x{wb:08X}, 0x{wa:08X} @ valor: {val}")

    out.extend([
        "",
        "    .text",
        "    .global _start",
        "_start:",
        "    MRC p15, 0, r1, c1, c0, 2",
        "    ORR r1, r1, #(0xF << 20)",
        "    MCR p15, 0, r1, c1, c0, 2",
        "    MOV r1, #0x40000000",
        "    FMXR FPEXC, r1"
    ])

    out.extend(codigo)

    out.extend([
        "",
        "_end:",
        "    B _end"
    ])

    # return "\n".join(out)

    # assembly_final = finalizarAssembly(linhas_assembly)
    # with open("saida.s", "w") as f:
    #     f.write(assembly_final)

    texto_final = "\n".join(out)
    with open("saida.s", "w") as f:
        f.write(texto_final)