import unittest
import os
from leituraArquivo import lerArquivo

class TestLeituraArquivo(unittest.TestCase):
    
    # arquivos para teste
    def setUp(self):
        self.arquivo_comum = "teste_sucesso.txt"
        with open(self.arquivo_comum, 'w', encoding='utf-8') as f:
            f.write("a = 10\n")
            f.write("b = 20\n")
            f.write("c = a + b")
            
        self.arquivo_vazio = "teste_vazio.txt"
        with open(self.arquivo_vazio, 'w', encoding='utf-8') as f:
            pass

    # apaga arquivos de teste
    def tearDown(self):
        if os.path.exists(self.arquivo_comum):
            os.remove(self.arquivo_comum)
        if os.path.exists(self.arquivo_vazio):
            os.remove(self.arquivo_vazio)

    # funcs de teste

    # arq lido corretamente e \n é removido
    def test_ler_arquivo_com_sucesso(self):
        resultado = lerArquivo(self.arquivo_comum)
        esperado = ["a = 10", "b = 20", "c = a + b"]
        self.assertEqual(resultado, esperado)

    # arq inexistente
    def test_ler_arquivo_inexistente(self):
        resultado = lerArquivo("arquivo_que_nao_existe.txt")
        self.assertEqual(resultado, [])

    # arq vazio
    def test_ler_arquivo_vazio(self):
        resultado = lerArquivo(self.arquivo_vazio)
        self.assertEqual(resultado, [])

if __name__ == '__main__':
    unittest.main()