'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
import unittest
import os
from leituraArquivo import lerArquivo

class TestLeituraArquivo(unittest.TestCase):
    
    # arquivos para teste
    def setUp(self):
        self.arquivo_comum = "teste_sucesso.txt"
        with open(self.arquivo_comum, 'w', encoding='utf-8') as f:
            f.write("(2 3 +)\n")
            f.write("(1 3 -)\n")
            f.write("(1 RES)")
            
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
        resultado = []
        lerArquivo(self.arquivo_comum, resultado)
        esperado = ["(2 3 +)", "(1 3 -)", "(1 RES)"]
        self.assertEqual(resultado, esperado)

    # arq inexistente
    def test_ler_arquivo_inexistente(self):
        resultado = []
        lerArquivo("arquivo_que_nao_existe.txt", resultado)
        self.assertEqual(resultado, [])

    # arq vazio
    def test_ler_arquivo_vazio(self):
        resultado = []
        lerArquivo(self.arquivo_vazio, resultado)
        self.assertEqual(resultado, [])

if __name__ == '__main__':
    unittest.main()