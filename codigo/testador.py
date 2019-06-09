import unittest

import os
from codigo import tratador_de_dados

def diferenca_de_listas(p, s):
    s = set(s)
    return [i for i in p if i not in s]

class TesteDeFuncoes(unittest.TestCase):
    def test_carregar_arquivo_em_lista(self):
        nome_arquivo = 'arquivo_de_teste_temporario_01.txt'
        with open(nome_arquivo, 'w+') as arquivo:
            for i in range(0, 5):
                arquivo.write(str(i) + '\n')
        arquivo.close()

        lista = tratador_de_dados.carregar_arquivo_em_lista(nome_arquivo)

        for i in range(0, 5):
            assert int(lista[i]) == i, "os valores devem bater: {} e {}".format(lista[i], i)

        os.remove(nome_arquivo)

    def test_dividir_registros_aleatorioamente(self):
        for t in range(50):
            lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            dicionario = tratador_de_dados.dividir_registros_aleatorioamente(lista, 7)

            for elemento in dicionario['teste']:
                assert not elemento in dicionario['treino'], 'os conjuntos devem ser diferentes'

            for elemento in dicionario['treino']:
                assert not elemento in dicionario['teste'], 'os conjuntos devem ser diferentes'

            uniao = dicionario['teste'] + dicionario['treino']

            assert set(uniao) == set(lista), 'a uniao dos conjuntos deve gerar a lista original'
            assert len(uniao) == len(lista), 'a uniao dos conjuntos deve gerar a lista original'

    def test_gerar_lista_de_numeros_embaralhados(self):
        for t in range(50):

            lista = tratador_de_dados.gerar_lista_de_numeros_embaralhados(0, 11)
            for i in (0, 11):
                assert i in lista, 'elemento {} nao contido na lista {}'.format(i, lista)

            lista = tratador_de_dados.gerar_lista_de_numeros_embaralhados(1, 10)
            assert len(lista) == len(set(lista)), 'a lista nao pode possuir duplicatas:\nlista1: {}\nlista2: {}'.format(lista, set(lista))

    def test_salvar_lista_em_arquivo(self):
        lista_original = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '545', '10']
        nome_do_arquivo = 'arquivo_de_teste_temporario_02.txt'

        tratador_de_dados.salvar_lista_em_arquivo(lista_original, nome_do_arquivo)

        lista_de_conteudo_lida = []

        with open(nome_do_arquivo, "r") as arquivo:
            registro = arquivo.readline()
            while registro != '':
                lista_de_conteudo_lida.append(registro)
                registro = arquivo.readline()
        arquivo.close()

        lista_de_conteudo_lida = tratador_de_dados.carregar_arquivo_em_lista(nome_do_arquivo)

        assert lista_de_conteudo_lida == lista_original, 'as listas nao podem ser diferentes, lista_lida: {}\nlista_original: {}'.format(lista_de_conteudo_lida, lista_original)

        os.remove(nome_do_arquivo)

class TesteDeConsistenciaDeDados(unittest.TestCase):
    def conjuntos(self):

        for diretorio_teste in os.listdir(tratador_de_dados.diretorio_dos_conjuntos):
            caminho = tratador_de_dados.diretorio_dos_conjuntos + diretorio_teste
            arquivo_treino = caminho + tratador_de_dados.nome_arquivo_saida_de_treino
            arquivo_teste = caminho + tratador_de_dados.nome_arquivo_saida_de_teste

            emails_treino = tratador_de_dados.carregar_arquivo_em_lista(arquivo_treino)
            emails_teste = tratador_de_dados.carregar_arquivo_em_lista(arquivo_teste)

            diferenca1 = diferenca_de_listas(emails_treino, emails_teste)
            diferenca2 = diferenca_de_listas(emails_teste, emails_treino)

            assert (diferenca1 == len(emails_treino)), 'Nao pode haver elementos comuns em ambas as listas'
            assert (diferenca2 == len(emails_teste)), 'Nao pode haver elementos comuns em ambas as listas'

            uniao = emails_treino + emails_teste

            emails_orginais = os.listdir(tratador_de_dados.diretorio_dos_emails)
            assert len(uniao) == len(emails_orginais), 'Existem {} emails no diretorio, mas {}+{} = {} na soma dos dois conjuntos'.format(len(emails_orginais), len(emails_treino), len(emails_teste), len(uniao))

if __name__ == '__main__':
    unittest.main()