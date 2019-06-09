import os
import random
import shutil
import math

diretorio_dos_emails = '../dados/0_todos_os_emails/'
nome_arquivo_mapeamento = '../dados/0_mapeamento.txt'

diretorio_dos_emails_google = '../dados/1_classificacao_google/'
diretorio_dos_emails_ricardo = '../dados/2_classificacao_ricardo/'

diretorio_relativo_spam = 'spam/'
diretorio_relativo_nao_spam = 'nao_spam/'

nome_catalogo_spam = 'spam.txt'
nome_catalogo_nao_spam = 'nao_spam.txt'

diretorio_dos_conjuntos = '../dados/3_conjuntos/'

nome_arquivo_saida_de_treino = 'treino.txt'
nome_arquivo_saida_de_teste = 'teste.txt'

class GeradorDeConjunto:

    def __init__(self, nome_arquivo_spam, nome_arquivo_nao_spam):
        self.nome_arquivo_spam = nome_arquivo_spam
        self.nome_arquivo_nao_spam = nome_arquivo_nao_spam

        self.porcentagem_do_conjunto_de_treino = 0.8
        self.porcentagem_do_conjunto_de_teste = 1 - self.porcentagem_do_conjunto_de_treino

    def gerar_conjuntos(self, nome_arquivo_saida_de_treino, nome_arquivo_saida_de_teste):
        lista_de_spam = carregar_arquivo_em_lista(self.nome_arquivo_spam)
        lista_de_nao_spam = carregar_arquivo_em_lista(self.nome_arquivo_nao_spam)

        quantidade_spam_conjunto_de_treino = math.floor(self.porcentagem_do_conjunto_de_treino * len(lista_de_spam))
        spams = dividir_registros_aleatorioamente(lista_de_spam, quantidade_spam_conjunto_de_treino)

        quantidade_nao_spam_conjunto_de_treino = math.floor(self.porcentagem_do_conjunto_de_treino * len(lista_de_nao_spam))
        nao_spams = dividir_registros_aleatorioamente(lista_de_nao_spam, quantidade_nao_spam_conjunto_de_treino)

        conjunto_de_treino = spams['treino'] + nao_spams['treino']
        conjunto_de_teste = spams['teste'] + nao_spams['teste']

        random.shuffle(conjunto_de_treino)
        random.shuffle(conjunto_de_teste)

        salvar_lista_em_arquivo(conjunto_de_treino, nome_arquivo_saida_de_treino)
        salvar_lista_em_arquivo(conjunto_de_teste, nome_arquivo_saida_de_teste)


def carregar_arquivo_em_lista(nome_do_arquivo):
    lista_de_conteudo = []

    with open(nome_do_arquivo, "r") as arquivo:
        registro = arquivo.readline()
        while registro != '':
            registro = registro.replace('\n', '')
            lista_de_conteudo.append(registro)
            registro = arquivo.readline()
    arquivo.close()

    return lista_de_conteudo

def dividir_registros_aleatorioamente(lista_de_registros, quantidade):
    lista_de_indices_embaralhados = gerar_lista_de_numeros_embaralhados(0, len(lista_de_registros) - 1)

    primeira_lista = []
    segunda_lista = []



    for i in range(quantidade):
        indice = lista_de_indices_embaralhados[i]
        registro = lista_de_registros[indice]
        primeira_lista.append(registro)

    for i in range(quantidade, len(lista_de_indices_embaralhados)):
        indice = lista_de_indices_embaralhados[i]
        registro = lista_de_registros[indice]
        segunda_lista.append(registro)

    #print('{}, {}::: {} {}'.format(quantidade, len(lista_de_indices_embaralhados), len(primeira_lista), len(segunda_lista)))

    dicionario = {'treino':primeira_lista, 'teste':segunda_lista}
    return dicionario

def gerar_lista_de_numeros_embaralhados(inicio_intervalo, fim_intervalo):
    lista_de_numeros = []

    for i in range(inicio_intervalo, fim_intervalo + 1):
        lista_de_numeros.append(i)

    random.shuffle(lista_de_numeros)

    return lista_de_numeros

def salvar_lista_em_arquivo(lista, nome_do_arquivo):
    with open(nome_do_arquivo, "w+") as arquivo:
        for elemento in lista:
            arquivo.write(str(elemento) + '\n')
    arquivo.close()


def listar_todos_os_arquivos_de_texto(nome_diretorio):
    arquivos_de_texto = []

    arquivos_diretorio = os.listdir(nome_diretorio)

    for arquivo in arquivos_diretorio:
        if '.txt' in arquivo:
            arquivos_de_texto.append(arquivo)

    return arquivos_de_texto

'''def atribuir_indices(lista_de_arquivos_de_texto):
    arquivos_mapeados = []

    i = 1
    for arquivo in lista_de_arquivos_de_texto:
        arquivos_mapeados.append((i, arquivo))
        i += 1

    return arquivos_mapeados'''


# A funcao carregar_mapeamento deve ser chamada antes desta funcao
def gerar_catalogo_de_emails(diretorio_dos_emails, nome_arquivo_de_catalogo):
    emails_listados = []

    emails = listar_todos_os_arquivos_de_texto(diretorio_dos_emails)
    for nome_email in emails:
        emails_listados.append(nome_email)

    salvar_lista_em_arquivo(emails_listados, nome_arquivo_de_catalogo)


def criar_catalogos():
    diretorios = [diretorio_dos_emails_google, diretorio_dos_emails_ricardo]
    for diretorio in diretorios:
        if not os.path.isfile(diretorio + nome_catalogo_spam):
            print('Criando catálogo do diretorio {}'.format(diretorio + nome_catalogo_spam))
            gerar_catalogo_de_emails(diretorio + diretorio_relativo_spam, diretorio + nome_catalogo_spam)
        else:
            print('Catálogo do diretorio {} já criado'.format(diretorio + nome_catalogo_spam))

        if not os.path.isfile(diretorio + diretorio_relativo_nao_spam):
            print('Criando catálogo do diretorio {}'.format(diretorio + diretorio_relativo_nao_spam))
            gerar_catalogo_de_emails(diretorio + diretorio_relativo_nao_spam, diretorio + nome_catalogo_nao_spam)
        else:
            print('Catálogo do diretorio {} já criado'.format(diretorio + diretorio_relativo_nao_spam))
    print()

def apagar_conjuntos(apagar):

    if apagar:
        print('[!] Apagando conjuntos')
        for item in os.listdir(diretorio_dos_conjuntos):
            caminho = diretorio_dos_conjuntos + item
            if os.path.isfile(caminho):
                os.remove(caminho)
            elif os.path.isdir(caminho):
                shutil.rmtree(caminho, ignore_errors=True)
            else:
                print('[!] Nao foi possivel excluir o item: {} '.format(item))

def gerar_conjuntos(gerar, quantidade):
    if gerar:

        for i in range(1, quantidade + 1):
            subdiretorio = str(i) + '_conjunto/'
            caminho = diretorio_dos_conjuntos + subdiretorio

            if os.path.isdir(caminho):
                print('[!] Conjunto de treino já existente!!')
                return
            else:
                os.mkdir(caminho)
                print('[!] Gerando {} conjuntos'.format(quantidade))

            arquivo_spam = diretorio_dos_emails_ricardo + nome_catalogo_spam
            arquivo_nao_spam = diretorio_dos_emails_ricardo + nome_catalogo_nao_spam

            gerador_de_conjunto = GeradorDeConjunto(arquivo_spam, arquivo_nao_spam)

            arquivo_treino = caminho + nome_arquivo_saida_de_treino
            arquivo_teste = caminho + nome_arquivo_saida_de_teste
            gerador_de_conjunto.gerar_conjuntos(arquivo_treino, arquivo_teste)


def tratar():
    criar_catalogos()

    apagar_conjuntos(False)
    gerar_conjuntos(True, 100)

def main():
    tratar()
    pass

main()