'''
Aluna : Beatriz Perotto Muniz
Grupo : RA1 6
'''
# Aluno 3 = ler arquivo, recebe uma string de arquivo e devolve as linhas para ParseExpressao
def lerArquivo(nomeArquivo: str, linhas: list) -> None:
    try:
        with open(nomeArquivo, encoding='utf-8') as arquivo:
            for linha in arquivo:
                linhas.append(linha.rstrip('\n'))
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nomeArquivo}")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
