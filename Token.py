class TokenType:
    # keyword
    KEYWORD_RES = "KEYWORD_RES"
    # id (variaveis) e tipos literais
    ID = "ID"
    NUM_INT = "NUM_INT"
    NUM_FLOAT = "NUM_FLOAT"
    # operadores
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    DIV = "DIV"
    INT_DIV = "INT_DIV"
    MOD = "MOD"
    POW = "POW"
    # divisor de operacoes
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    # outros
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"

# classe do token com tipo, valor, linha e coluna
class Token:
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.column})"

#token = Token(TokenType.KEYWORD_RES, "RES", 1, 1)