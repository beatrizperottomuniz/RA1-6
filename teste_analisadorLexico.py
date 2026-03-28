'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
import unittest
from Token import TokenType
from stringPool import StringPool
from analisadorLexico import Lexer
import globalVars

def tokenizar(linha, linha_num=1, total_linhas=1):
    pool = StringPool()
    globalVars.total_linhas_global = total_linhas
    lexer = Lexer(linha, pool, linha_num)
    return lexer.tokenize(), pool


class TestAnalisadorLexicoValidos(unittest.TestCase):

    def test_inteiros_tipos(self):
        tokens, _ = tokenizar("(2 3 +)")
        tipos = [t.tipo for t in tokens]
        self.assertEqual(tipos, [
            TokenType.LPAREN, TokenType.NUM_INT, TokenType.NUM_INT,
            TokenType.PLUS, TokenType.RPAREN, TokenType.EOF
        ])

    def test_inteiro_lexema_na_pool(self):
        tokens, pool = tokenizar("(7 4 -)")
        self.assertEqual(pool.obterString(tokens[1].simbolo_id), "7")
        self.assertEqual(pool.obterString(tokens[2].simbolo_id), "4")

    def test_float_tipos(self):
        tokens, _ = tokenizar("(3.14 2.0 *)")
        tipos = [t.tipo for t in tokens]
        self.assertEqual(tipos, [
            TokenType.LPAREN, TokenType.NUM_FLOAT, TokenType.NUM_FLOAT,
            TokenType.MULT, TokenType.RPAREN, TokenType.EOF
        ])

    def test_float_lexema_na_pool(self):
        tokens, pool = tokenizar("(3.14 2.0 *)")
        self.assertEqual(pool.obterString(tokens[1].simbolo_id), "3.14")
        self.assertEqual(pool.obterString(tokens[2].simbolo_id), "2.0")

    def test_int_e_float_tipos_distintos(self):
        tokens_int, _  = tokenizar("(2 3 +)")
        tokens_flt, _  = tokenizar("(2.0 3.0 +)")
        self.assertEqual(tokens_int[1].tipo, TokenType.NUM_INT)
        self.assertEqual(tokens_flt[1].tipo, TokenType.NUM_FLOAT)

    def test_operador_adicao(self):
        tokens, _ = tokenizar("(1 2 +)")
        self.assertEqual(tokens[3].tipo, TokenType.PLUS)

    def test_operador_subtracao(self):
        tokens, _ = tokenizar("(10 4 -)")
        self.assertEqual(tokens[3].tipo, TokenType.MINUS)

    def test_operador_multiplicacao(self):
        tokens, _ = tokenizar("(3 4 *)")
        self.assertEqual(tokens[3].tipo, TokenType.MULT)

    def test_operador_divisao(self):
        tokens, _ = tokenizar("(10 2 /)")
        self.assertEqual(tokens[3].tipo, TokenType.DIV)

    def test_operador_divisao_inteira(self):
        tokens, _ = tokenizar("(10 3 //)")
        self.assertEqual(tokens[3].tipo, TokenType.INT_DIV)

    def test_operador_modulo(self):
        tokens, _ = tokenizar("(10 3 %)")
        self.assertEqual(tokens[3].tipo, TokenType.MOD)

    def test_operador_potencia(self):
        tokens, _ = tokenizar("(2 8 ^)")
        self.assertEqual(tokens[3].tipo, TokenType.POW)

    def test_keyword_res_tipo(self):
        tokens, _ = tokenizar("(1 RES)")
        self.assertEqual(tokens[2].tipo, TokenType.KEYWORD_RES)

    def test_keyword_res_nao_entra_na_pool(self):
        _, pool = tokenizar("(1 RES)")
        self.assertNotIn("RES", pool.pool)

    def test_variavel_tipo(self):
        tokens, _ = tokenizar("(5.0 VAR)")
        self.assertEqual(tokens[2].tipo, TokenType.ID)

    def test_variavel_lexema_na_pool(self):
        tokens, pool = tokenizar("(5.0 VAR)")
        self.assertEqual(pool.obterString(tokens[2].simbolo_id), "VAR")

    def test_variavel_load_tipo(self):
        tokens, pool = tokenizar("(VAR)")
        self.assertEqual(tokens[1].tipo, TokenType.ID)
        self.assertEqual(pool.obterString(tokens[1].simbolo_id), "VAR")

    def test_variavel_uma_vez_na_pool(self):
        tokens, _ = tokenizar("(X X +)")
        self.assertEqual(tokens[1].simbolo_id, tokens[2].simbolo_id)

    def test_numero_uma_vez_na_pool(self):
        tokens, _ = tokenizar("(3 3 +)")
        self.assertEqual(tokens[1].simbolo_id, tokens[2].simbolo_id)

    def test_parenteses_tipos(self):
        tokens, _ = tokenizar("(2 3 +)")
        self.assertEqual(tokens[0].tipo, TokenType.LPAREN)
        self.assertEqual(tokens[4].tipo, TokenType.RPAREN)

    def test_expressao_aninhada_operadores(self):
        tokens, _ = tokenizar("((2 3 *) (4 5 +) /)")
        tipos = [t.tipo for t in tokens]
        self.assertIn(TokenType.MULT, tipos)
        self.assertIn(TokenType.PLUS, tipos)
        self.assertIn(TokenType.DIV, tipos)

    def test_expressao_aninhada_contagem_parenteses(self):
        tokens, _ = tokenizar("((2 3 *) (4 5 +) /)")
        tipos = [t.tipo for t in tokens]
        self.assertEqual(tipos.count(TokenType.LPAREN), 3)
        self.assertEqual(tipos.count(TokenType.RPAREN), 3)

    def test_eof_aparece_na_ultima_linha(self):
        tokens, _ = tokenizar("(2 3 +)", linha_num=1, total_linhas=1)
        tipos = [t.tipo for t in tokens]
        self.assertIn(TokenType.EOF, tipos)

    def test_eof_ausente_em_linha_intermediaria(self):
        tokens, _ = tokenizar("(2 3 +)", linha_num=1, total_linhas=3)
        tipos = [t.tipo for t in tokens]
        self.assertNotIn(TokenType.EOF, tipos)

    def test_espacos_sao_ignorados(self):
        tokens1, _ = tokenizar("(2 3 +)")
        tokens2, _ = tokenizar("( 2   3  +  )")
        tipos1 = [t.tipo for t in tokens1]
        tipos2 = [t.tipo for t in tokens2]
        self.assertEqual(tipos1, tipos2)


class TestAnalisadorLexicoInvalidos(unittest.TestCase):

    def test_float_dois_pontos(self):
        tokens, _ = tokenizar("(3.14.5 2 +)")
        tipos = [t.tipo for t in tokens]
        self.assertIn(TokenType.UNKNOWN, tipos)

    def test_virgula_como_decimal(self):
        tokens, _ = tokenizar("(3,14 2 +)")
        tipos = [t.tipo for t in tokens]
        self.assertIn(TokenType.UNKNOWN, tipos)

    def test_caractere_nao_reconhecido(self):
        tokens, _ = tokenizar("(! @ # $ & |)")
        tipos = [t.tipo for t in tokens]
        self.assertEqual(tipos.count(TokenType.UNKNOWN), 6)

    def test_letra_minuscula(self):
        tokens, _ = tokenizar("(x 2 +)")
        tipos = [t.tipo for t in tokens]
        self.assertIn(TokenType.UNKNOWN, tipos)

    def test_identificador_misto(self):
        tokens, _ = tokenizar("(Abc 2 +)")
        tipos = [t.tipo for t in tokens]
        self.assertIn(TokenType.UNKNOWN, tipos)

    def test_tokens_validos_antes_do_invalido(self):
        tokens, _ = tokenizar("(3 & 2)")
        tipos = [t.tipo for t in tokens]
        self.assertIn(TokenType.NUM_INT, tipos)
        self.assertIn(TokenType.UNKNOWN, tipos)


if __name__ == '__main__':
    unittest.main()
