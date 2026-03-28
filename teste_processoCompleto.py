'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
import unittest
import os
import globalVars
import geradorAssembly
from stringPool import StringPool
from Token import TokenType
from analisadorLexico import parseExpressao
from executaExpressao import executarExpressao
from geradorAssembly import gerarAssembly
from main import verificacaoParentesesDesbalanceados


def resetar():
    geradorAssembly.constantes.clear()
    geradorAssembly.variaveis.clear()
    geradorAssembly.resultados_linha.clear()
    geradorAssembly.contador_label = 0
    globalVars.string_pool_global.pool.clear()
    globalVars.string_pool_global.strings.clear()
    globalVars.contador_linha_global = 1
    globalVars.total_linhas_global = 1


def executarPipeline(linha, resultados, memoria): # simula a main
    globalVars.contador_linha_global = 1
    globalVars.total_linhas_global = 1 

    tokens = []
    parseExpressao(linha, tokens)

    tem_erro = any(t.tipo == TokenType.UNKNOWN for t in tokens)

    if not tem_erro and not verificacaoParentesesDesbalanceados(linha):
        tem_erro = True

    if not tem_erro:
        executarExpressao(tokens, resultados, memoria)
        gerarAssembly(tokens, [])

    return not tem_erro


class TestPipelineValido(unittest.TestCase):

    def setUp(self):
        resetar()
        if os.path.exists("saida.s"):
            os.remove("saida.s")

    def tearDown(self):
        resetar()
        if os.path.exists("saida.s"):
            os.remove("saida.s")

    def test_pipeline_valido_gera_assembly(self):
        resultados, memoria = [], {}
        sucesso = executarPipeline("(2 3 +)", resultados, memoria)
        self.assertTrue(sucesso)
        self.assertTrue(os.path.exists("saida.s"))

    def test_pipeline_resultado_correto(self):
        resultados, memoria = [], {}
        executarPipeline("(2 3 +)", resultados, memoria)
        self.assertAlmostEqual(resultados[0], 5.0)


class TestPipelineInvalido(unittest.TestCase):

    def setUp(self):
        resetar()
        if os.path.exists("saida.s"):
            os.remove("saida.s")

    def tearDown(self):
        resetar()
        if os.path.exists("saida.s"):
            os.remove("saida.s")

    def test_token_invalido_nao_gera_assembly(self):
        resultados, memoria = [], {}
        sucesso = executarPipeline("(3 2 &)", resultados, memoria)
        self.assertFalse(sucesso)
        self.assertFalse(os.path.exists("saida.s"))

    def test_parenteses_desbalanceados_nao_gera_assembly(self):
        resultados, memoria = [], {}
        sucesso = executarPipeline("(3 2 +", resultados, memoria)
        self.assertFalse(sucesso)
        self.assertFalse(os.path.exists("saida.s"))


if __name__ == '__main__':
    unittest.main()
