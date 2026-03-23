'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1-6
'''
# Aluno 3 = ler arquivo, recebe uma string de arquivo e devolve as linhas para ParseExpressao
def lerArquivo(path: str):
    try:
        with open(path, encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {path}")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []
