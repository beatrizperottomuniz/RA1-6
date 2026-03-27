'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1 6
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
        self.current_state = self.stateStart
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
            symbol_id = self.string_pool.get_or_add(lex_str)
            
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
    def stateStart(self):
        char = self.peek()

        if char is None:
            if self.line == globalVars.total_lines_global:
                self.tokens.append(Token(TokenType.EOF, self.line, self.col))
            return None

        if char.isspace():
            self.advance()
            return self.stateStart

        self.start_col = self.col

        # transicao estado de id -> apenas conjunto de letras maiusculas
        if char.isalpha() and char.isupper():
            self.buffer.append(char)
            self.advance()
            return self.stateId

        # transicao estado de num_int
        if char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.stateNumInt

        # transicao estado de operadores
        if char in self.operators:
            self.buffer.append(char)
            self.advance()
            return self.stateOperator

        # transicao estado de parenteses
        if char in "()":
            self.buffer.append(char)
            self.advance()
            return self.stateParen

        self.buffer.append(char)
        self.advance()
        self.emit(TokenType.UNKNOWN)
        return self.stateStart


    def stateOperator(self):
        char = self.buffer[0]
        if char == '/' and self.peek() == '/':
            self.buffer.append(self.peek())
            self.advance()
            self.emit(TokenType.INT_DIV)
            return self.stateStart

        if char in self.symbols:
            self.emit(self.symbols[char])
        else:
            self.emit(TokenType.UNKNOWN)
            
        return self.stateStart


    def stateParen(self):
        char = self.buffer[0]
        if char == '(':
            self.emit(TokenType.LPAREN)
        elif char == ')':
            self.emit(TokenType.RPAREN)
            
        return self.stateStart
    

    def stateId(self):
        char = self.peek()
        if char is not None and char.isalpha() and char.isupper():
            self.buffer.append(char)
            self.advance()
            return self.stateId
            
        self.emit(TokenType.ID)
        return self.stateStart


    def stateNumInt(self):
        char = self.peek()
        if char is not None and char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.stateNumInt
            
        if char == '.':
            self.buffer.append(char)
            self.advance()
            return self.stateNumFloat
            
        self.emit(TokenType.NUM_INT)
        return self.stateStart


    def stateNumFloat(self):
        char = self.peek()
        if char is not None and char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.stateNumFloat
            
        if char == '.':
            # estado de erro para + de um ponto
            self.buffer.append(char)
            self.advance()
            return self.stateInvalidNum
            
        self.emit(TokenType.NUM_FLOAT)
        return self.stateStart


    # estado de erro para consumir o resto do numero float errado -> ex : 1.2.34
    def stateInvalidNum(self):
        char = self.peek()
        if char is not None and (char.isdigit() or char == '.'):
            self.buffer.append(char)
            self.advance()
            return self.stateInvalidNum
            
        self.emit(TokenType.UNKNOWN)
        return self.stateStart


# _tokens_ vem por referencia
def parseExpressao(linha: str, _tokens_ : list) -> None:
    lexer = Lexer(linha, globalVars.string_pool_global, globalVars.line_count_global)
    #return lexer.tokenize()
    tokens = lexer.tokenize()
    _tokens_.extend(tokens)
