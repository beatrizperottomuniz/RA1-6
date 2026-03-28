'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
import unittest
import globalVars
from stringPool import StringPool
from analisadorLexico import parseExpressao
from executaExpressao import executarExpressao


def resetar():
    globalVars.string_pool_global.pool.clear()
    globalVars.string_pool_global.strings.clear()
    globalVars.contador_linha_global = 1
    globalVars.total_linhas_global   = 2 


def executar(linha, resultados, memoria, linha_num=1, total_linhas=2):
    globalVars.contador_linha_global = linha_num
    globalVars.total_linhas_global   = total_linhas
    tokens = []
    parseExpressao(linha, tokens)
    executarExpressao(tokens, resultados, memoria)


class TestOperadores(unittest.TestCase):

    def setUp(self):
        resetar()
        self.res = []
        self.mem = {}

    def tearDown(self):
        resetar()

    def test_adicao(self):
        executar("(2.5 3 +)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 5.5)

    def test_subtracao(self):
        executar("(10 4 -)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 6.0)

    def test_multiplicacao(self):
        executar("(3 4 *)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 12.0)

    def test_divisao_real(self):
        executar("(10 4 /)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 2.5)

    def test_divisao_inteira(self):
        executar("(7 2 //)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 3.0)

    def test_modulo(self):
        executar("(10 3 %)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 1.0)

    def test_potenciacao(self):
        executar("(2 8 ^)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 256.0)


class TestCasosEspeciaisOperadores(unittest.TestCase):

    def setUp(self):
        resetar()
        self.res = []
        self.mem = {}

    def tearDown(self):
        resetar()

    def test_potencia_expoente_zero(self):
        executar("(5 0 ^)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 1.0)

    def test_potencia_expoente_um(self):
        executar("(5 1 ^)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 5.0)

    def test_divisao_inteira_exata(self):
        executar("(9 3 //)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 3.0)

    def test_modulo_divisao_exata(self):
        executar("(9 3 %)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 0.0)

    def test_subtracao_resultado_negativo(self):
        executar("(2 5 -)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], -3.0)

class TestVariaveis(unittest.TestCase):

    def setUp(self):
        resetar()
        self.res = []
        self.mem = {}

    def tearDown(self):
        resetar()

    def test_store_salva_na_memoria(self):
        executar("(5.0 X)", self.res, self.mem)
        self.assertAlmostEqual(self.mem.get("X", None), 5.0)

    def test_store_mantem_valor_na_pilha(self):
        executar("(5.0 X)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 5.0)

    def test_load_apos_store(self):
        executar("(5.0 X)", self.res, self.mem, linha_num=1, total_linhas=3)
        resetar()
        executar("(X)", self.res, self.mem, linha_num=2, total_linhas=3)
        self.assertAlmostEqual(self.res[-1], 5.0)

    def test_load_sem_store_retorna_zero(self):
        executar("(Y)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 0.0)

    def test_variavel_usada_em_operacao(self):
        executar("(3.0 A)", self.res, self.mem, linha_num=1, total_linhas=3)
        resetar()
        executar("(A 2 *)", self.res, self.mem, linha_num=2, total_linhas=3)
        self.assertAlmostEqual(self.res[-1], 6.0)

    def test_store_sobrescreve_valor(self):
        executar("(5.0 X)", self.res, self.mem, linha_num=1, total_linhas=3)
        resetar()
        executar("(9.0 X)", self.res, self.mem, linha_num=2, total_linhas=3)
        self.assertAlmostEqual(self.mem.get("X"), 9.0)


class TestRes(unittest.TestCase):

    def setUp(self):
        resetar()
        self.res = []
        self.mem = {}

    def tearDown(self):
        resetar()

    def test_res_linha_anterior_imediata(self):
        executar("(2 3 +)", self.res, self.mem, linha_num=1, total_linhas=3)
        resetar()
        executar("(1 RES)", self.res, self.mem, linha_num=2, total_linhas=3)
        self.assertAlmostEqual(self.res[-1], 5.0)

    def test_res_duas_linhas_atras(self):
        executar("(4 4 *)", self.res, self.mem, linha_num=1, total_linhas=4)
        resetar()
        executar("(1 2 +)", self.res, self.mem, linha_num=2, total_linhas=4)
        resetar()
        executar("(2 RES)", self.res, self.mem, linha_num=3, total_linhas=4)
        self.assertAlmostEqual(self.res[-1], 16.0)

    def test_res_indice_zero_retorna_zero(self):
        executar("(0 RES)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 0.0)

    def test_res_indice_maior_que_historico_retorna_zero(self):
        executar("(10 RES)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 0.0)

    def test_res_em_operacao(self):
        executar("(3 3 +)", self.res, self.mem, linha_num=1, total_linhas=3)
        resetar()
        executar("((1 RES) 2 *)", self.res, self.mem, linha_num=2, total_linhas=3)
        self.assertAlmostEqual(self.res[-1], 12.0)


class TestAninhamento(unittest.TestCase):

    def setUp(self):
        resetar()
        self.res = []
        self.mem = {}

    def tearDown(self):
        resetar()

    def test_aninhamento(self):
        executar("(((2 3 +) 4 *) 5 -)", self.res, self.mem)
        self.assertAlmostEqual(self.res[-1], 15.0)

    def test_aninhamento_com_variavel(self):
        executar("(2.0 N)", self.res, self.mem, linha_num=1, total_linhas=3)
        resetar()
        executar("((N 3 +) 2 *)", self.res, self.mem, linha_num=2, total_linhas=3)
        self.assertAlmostEqual(self.res[-1], 10.0)

if __name__ == '__main__':
    unittest.main()
