'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1-6
'''
from Token import Token, TokenType
from stringPool import StringPool
import globalVars

class Lexer:
    def __init__(self, src: str, string_pool: StringPool,line_count: int):
        self.src = src
        self.string_pool = string_pool
        self.pos = 0
        self.line = line_count
        self.col = 1
        self.buffer = []
        self.tokens = []

        self.start_col = 1
        self.current_state = self.state_start
        self.keywords = {"RES": TokenType.KEYWORD_RES}
        self.operators = "+-*/%^"
        self.symbols = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULT,
            '/': TokenType.DIV,
            '%': TokenType.MOD,
            '^': TokenType.POW,
        }

    # olha proximo sem consumir
    def peek(self): 
        return self.src[self.pos] if self.pos < len(self.src) else None

    def advance(self):
        char = self.peek()
        if char is not None:
            self.pos += 1
            self.col += 1
        return char

    # salva token e limpa buffer
    def emit(self, token_type: str):
        lex_str = "".join(self.buffer)
        symbol_id = None

        if token_type == TokenType.ID:
            if lex_str in self.keywords:
                token_type = self.keywords[lex_str]
            else:
                symbol_id = self.string_pool.get_or_add(lex_str)
        elif token_type in (TokenType.NUM_INT, TokenType.NUM_FLOAT):
            symbol_id = float(lex_str) if token_type == TokenType.NUM_FLOAT else int(lex_str)
            
        elif token_type == TokenType.UNKNOWN:
            str_erro = lex_str 
            print(f"Erro na linha {self.line}, coluna {self.start_col}: {str_erro}\n")

        self.tokens.append(Token(token_type, self.line, self.start_col, symbol_id))
        self.buffer.clear()


    def tokenize(self):
        while self.current_state is not None:
            self.current_state = self.current_state()
        return self.tokens

    # funcoes de estados ------------------------------------

    # estado inicial
    def state_start(self):
        char = self.peek()

        if char is None:
            if self.line == globalVars.total_lines_global:
                self.tokens.append(Token(TokenType.EOF, self.line, self.col))
            return None

        if char.isspace():
            self.advance()
            return self.state_start

        self.start_col = self.col

        # transicao estado de id -> apenas conjunto de letras maiusculas
        if char.isalpha() and char.isupper():
            self.buffer.append(char)
            self.advance()
            return self.state_id

        # transicao estado de num_int
        if char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.state_num_int

        # transicao estado de operadores
        if char in self.operators:
            self.buffer.append(char)
            self.advance()
            return self.state_operator

        # transicao estado de parenteses
        if char in "()":
            self.buffer.append(char)
            self.advance()
            return self.state_paren

        self.buffer.append(char)
        self.advance()
        self.emit(TokenType.UNKNOWN)
        return self.state_start


    def state_operator(self):
        char = self.buffer[0]
        if char == '/' and self.peek() == '/':
            self.buffer.append(self.peek())
            self.advance()
            self.emit(TokenType.INT_DIV)
            return self.state_start

        if char in self.symbols:
            self.emit(self.symbols[char])
        else:
            self.emit(TokenType.UNKNOWN)
            
        return self.state_start


    def state_paren(self):
        char = self.buffer[0]
        if char == '(':
            self.emit(TokenType.LPAREN)
        elif char == ')':
            self.emit(TokenType.RPAREN)
            
        return self.state_start
    

    def state_id(self):
        char = self.peek()
        if char is not None and char.isalpha() and char.isupper():
            self.buffer.append(char)
            self.advance()
            return self.state_id
            
        self.emit(TokenType.ID)
        return self.state_start


    def state_num_int(self):
        char = self.peek()
        if char is not None and char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.state_num_int
            
        if char == '.':
            self.buffer.append(char)
            self.advance()
            return self.state_num_float
            
        self.emit(TokenType.NUM_INT)
        return self.state_start


    def state_num_float(self):
        char = self.peek()
        if char is not None and char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.state_num_float
            
        if char == '.':
            # estado de erro para + de um ponto
            self.buffer.append(char)
            self.advance()
            return self.state_invalid_num
            
        self.emit(TokenType.NUM_FLOAT)
        return self.state_start


    # estado de erro para consumir o resto do numero float errado -> ex : 1.2.34
    def state_invalid_num(self):
        char = self.peek()
        if char is not None and (char.isdigit() or char == '.'):
            self.buffer.append(char)
            self.advance()
            return self.state_invalid_num
            
        self.emit(TokenType.UNKNOWN)
        return self.state_start


def parseExpressao(line: str):
    lexer = Lexer(line, globalVars.string_pool_global, globalVars.line_count_global)
    return lexer.tokenize()
