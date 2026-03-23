'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1-6
'''
# para ver se a string (variavel) ja esta na pool
class StringPool:
    def __init__(self):
        self.pool = {} # dicionario string = id
        self.strings = [] # lista de strings

    # retorna id se existe/ cria novo se não
    def get_or_add(self, lexeme: str):
        if lexeme in self.pool:
            return self.pool[lexeme]

        next_id = len(self.strings) # id é o índice na lista
        self.pool[lexeme] = next_id
        self.strings.append(lexeme)

        return next_id

    # retorna texto original de id
    def get_string(self, symbol_id: int):
        if 0 <= symbol_id < len(self.strings):
            return self.strings[symbol_id]
        return "unknown"