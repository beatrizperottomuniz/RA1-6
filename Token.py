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

# classe do token com tipo,linha, coluna, id do simbolo na string pool
class Token:
    def __init__(self, token_type: TokenType, line: int, column: int, symbol_id=None):
        self.type = token_type
        self.line = line
        self.column = column
        self.symbol_id = symbol_id

    def __repr__(self):
        return f"Token({self.type}, {self.symbol_id}, {self.line}, {self.column})"

