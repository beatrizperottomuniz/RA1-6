# Aluno 3 = ler arquivo, recebe uma string de arquivo e devolve as linhas para ParseExpressao
def lerArquivo(nomeArquivo: str):
    try:
        with open(nomeArquivo, encoding='utf-8') as f:
            return [linha.rstrip('\n') for linha in f]
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nomeArquivo}")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return []
