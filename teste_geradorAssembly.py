'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
import unittest
import os
import struct
import geradorAssembly
import globalVars
from Token import Token, TokenType
from analisadorLexico import parseExpressao

def resetar():
    geradorAssembly.constantes.clear()
    geradorAssembly.variaveis.clear()
    geradorAssembly.resultados_linha.clear()
    geradorAssembly.contador_label = 0
    globalVars.string_pool_global.pool.clear()
    globalVars.string_pool_global.strings.clear()
    globalVars.contador_linha_global = 1
    globalVars.total_linhas_global = 2


def gerarTokens(linha, linha_num=1, total_linhas=2):
    globalVars.contador_linha_global = linha_num
    globalVars.total_linhas_global   = total_linhas
    tokens = []
    parseExpressao(linha, tokens)
    return tokens


class TestDoubleParaBits(unittest.TestCase):

    def test_zero(self):
        wb, wa = geradorAssembly.doubleParaBits(0.0)
        self.assertEqual(wb, 0x00000000)
        self.assertEqual(wa, 0x00000000)

    def test_um(self):
        wb, wa = geradorAssembly.doubleParaBits(1.0)
        self.assertEqual(wb, 0x00000000)
        self.assertEqual(wa, 0x3FF00000)

    def test_menos_um(self):
        wb, wa = geradorAssembly.doubleParaBits(-1.0)
        self.assertEqual(wb, 0x00000000)
        self.assertEqual(wa, 0xBFF00000)


    def test_meio(self):
        wb, wa = geradorAssembly.doubleParaBits(0.5)
        self.assertEqual(wb, 0x00000000)
        self.assertEqual(wa, 0x3FE00000)

#falta
class TestNovoLabel(unittest.TestCase):

    def setUp(self):
        geradorAssembly.contador_label = 0

    def tearDown(self):
        geradorAssembly.contador_label = 0

    def test_prefixo(self):
        lbl = geradorAssembly.novoLabel()
        self.assertTrue(lbl.startswith("LBL_"))

    def test_labels_unicos(self):
        lbl1 = geradorAssembly.novoLabel("X")
        lbl2 = geradorAssembly.novoLabel("X")
        self.assertNotEqual(lbl1, lbl2)

class TestResgatarLexema(unittest.TestCase):

    def setUp(self):
        globalVars.string_pool_global.pool.clear()
        globalVars.string_pool_global.strings.clear()

    def tearDown(self):
        globalVars.string_pool_global.pool.clear()
        globalVars.string_pool_global.strings.clear()

    def _tokenComId(self, tipo, lexema):
        id_ = globalVars.string_pool_global.buscarOuAdicionar(lexema)
        return Token(tipo, 1, 1, id_)

    def test_operador_mais(self):
        t = Token(TokenType.PLUS, 1, 1, 0)
        self.assertEqual(geradorAssembly.resgatarLexema(t), "+")

    def test_operador_menos(self):
        t = Token(TokenType.MINUS, 1, 1, 0)
        self.assertEqual(geradorAssembly.resgatarLexema(t), "-")

    def test_operador_mult(self):
        t = Token(TokenType.MULT, 1, 1, 0)
        self.assertEqual(geradorAssembly.resgatarLexema(t), "*")

    def test_operador_div(self):
        t = Token(TokenType.DIV, 1, 1, 0)
        self.assertEqual(geradorAssembly.resgatarLexema(t), "/")

    def test_operador_div_inteira(self):
        t = Token(TokenType.INT_DIV, 1, 1, 0)
        self.assertEqual(geradorAssembly.resgatarLexema(t), "//")

    def test_operador_mod(self):
        t = Token(TokenType.MOD, 1, 1, 0)
        self.assertEqual(geradorAssembly.resgatarLexema(t), "%")

    def test_operador_pot(self):
        t = Token(TokenType.POW, 1, 1, 0)
        self.assertEqual(geradorAssembly.resgatarLexema(t), "^")

    def test_num_int_da_pool(self):
        t = self._tokenComId(TokenType.NUM_INT, "42")
        self.assertEqual(geradorAssembly.resgatarLexema(t), "42")

    def test_num_float_da_pool(self):
        t = self._tokenComId(TokenType.NUM_FLOAT, "3.14")
        self.assertEqual(geradorAssembly.resgatarLexema(t), "3.14")

    def test_id_da_pool(self):
        t = self._tokenComId(TokenType.ID, "X")
        self.assertEqual(geradorAssembly.resgatarLexema(t), "X")

class TestGerarAssembly(unittest.TestCase):

    def setUp(self):
        resetar()

    def tearDown(self):
        resetar()
        if os.path.exists("saida.s"):
            os.remove("saida.s")

    def _asm(self, linha):
        tokens = gerarTokens(linha)
        asm = []
        geradorAssembly.gerarAssembly(tokens, asm)
        return "\n".join(asm)

    def test_adicao_gera_vadd(self):
        self.assertIn("VADD.F64", self._asm("(2 3 +)"))

    def test_subtracao_gera_vsub(self):
        self.assertIn("VSUB.F64", self._asm("(5 2 -)"))

    def test_multiplicacao_gera_vmul(self):
        self.assertIn("VMUL.F64", self._asm("(3 4 *)"))

    def test_divisao_gera_vdiv(self):
        self.assertIn("VDIV.F64", self._asm("(10 2 /)"))

    def test_divisao_inteira_gera_vcvt(self):
        asm = self._asm("(10 3 //)")
        self.assertIn("VCVT.S32.F64", asm)
        self.assertIn("VCVT.F64.S32", asm)

    def test_modulo_gera_sequencia_correta(self):
        asm = self._asm("(10 3 %)")
        self.assertIn("VDIV.F64", asm)
        self.assertIn("VCVT.S32.F64", asm)
        self.assertIn("VMUL.F64", asm)
        self.assertIn("VSUB.F64", asm)

    def test_potencia_gera_loop(self):
        asm = self._asm("(2 3 ^)")
        self.assertIn("POW_LOOP", asm)
        self.assertIn("POW_FIM", asm)
        self.assertIn("BLE", asm)

    def test_variavel_store_gera_vstr(self):
        asm = self._asm("(5.0 X)")
        self.assertIn("VSTR", asm)
        self.assertIn("X_MEM", asm)

    def test_variavel_store_registrada(self):
        self._asm("(5.0 X)")
        self.assertIn("X", geradorAssembly.variaveis)

    def test_variavel_load_gera_vldr(self):
        asm = self._asm("(X)")
        self.assertIn("VLDR", asm)
        self.assertIn("X_MEM", asm)

    def test_variavel_nao_duplicada_no_set(self):
        self._asm("(5.0 X)")
        resetar()
        self._asm("(3.0 X)")
        self.assertEqual(list(geradorAssembly.variaveis).count("X"), 1)

    def test_constante_adicionada_ao_dict(self):
        self._asm("(7.0 3.0 +)")
        self.assertIn("7.0", geradorAssembly.constantes)
        self.assertIn("3.0", geradorAssembly.constantes)

    def test_constante_aparece_uma_vez(self):
        self._asm("(2.0 2.0 +)")
        entradas = [k for k in geradorAssembly.constantes if k == "2.0"]
        self.assertEqual(len(entradas), 1)

    def test_resultado_armazenado_em_memoria(self):
        asm = self._asm("(1 2 +)")
        self.assertIn("RES_LINHA_1", asm)
        self.assertIn("VSTR d0", asm)

    def test_print_res_hex_chamado(self):
        asm = self._asm("(1 2 +)")
        self.assertIn("BL PRINT_RES_HEX", asm)

    def test_res_referencia_linha_anterior(self):
        tokens1 = gerarTokens("(2 3 +)", linha_num=1, total_linhas=3)
        asm1 = []
        geradorAssembly.gerarAssembly(tokens1, asm1)
        globalVars.contador_linha_global = 2
        tokens2 = gerarTokens("(1 RES)", linha_num=2, total_linhas=3)
        asm2 = []
        geradorAssembly.gerarAssembly(tokens2, asm2)
        self.assertIn("RES_LINHA_1", "\n".join(asm2))

    def test_res_indice_invalido_retorna_zero(self):
        tokens = gerarTokens("(5 RES)", linha_num=1, total_linhas=2)
        asm = []
        geradorAssembly.gerarAssembly(tokens, asm)
        self.assertIn("0.0", geradorAssembly.constantes)

    def test_finalizar_gera_arquivo_saida(self):
        tokens = gerarTokens("(2 3 +)", linha_num=1, total_linhas=1)
        asm = []
        geradorAssembly.gerarAssembly(tokens, asm)
        self.assertTrue(os.path.exists("saida.s"))

    def test_saida_contem_cabecalho_arm(self):
        tokens = gerarTokens("(2 3 +)", linha_num=1, total_linhas=1)
        asm = []
        geradorAssembly.gerarAssembly(tokens, asm)
        with open("saida.s", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn(".arch armv7-a", conteudo)
        self.assertIn(".fpu vfpv3-d16", conteudo)
        self.assertIn("_start:", conteudo)
        self.assertIn("_end:", conteudo)

    def test_saida_contem_uart(self):
        tokens = gerarTokens("(2 3 +)", linha_num=1, total_linhas=1)
        asm = []
        geradorAssembly.gerarAssembly(tokens, asm)
        with open("saida.s", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn("UART_PUTCHAR", conteudo)
        self.assertIn("PRINT_RES_HEX", conteudo)

    def test_saida_contem_constantes_em_data(self):
        tokens = gerarTokens("(2.0 3.0 +)", linha_num=1, total_linhas=1)
        asm = []
        geradorAssembly.gerarAssembly(tokens, asm)
        with open("saida.s", encoding="utf-8") as f:
            conteudo = f.read()
        self.assertIn(".data", conteudo)
        self.assertIn(".word", conteudo)


if __name__ == '__main__':
    unittest.main()
