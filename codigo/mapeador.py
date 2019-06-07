import os

class Mapeador:

    def __init__(self, caminho_dos_emails):
        self.caminho_dos_emails = caminho_dos_emails
        self.arquivos_mapeados = [];
        self.dicionario = {}


    def criar_mapeamento(self, nome_arquivo_mapeamento):
        arquivos_de_texto = self.listar_todos_os_arquivos_de_texto(self.caminho_dos_emails)
        arquivos_mapeados = self.atribuir_indices(arquivos_de_texto)
        self.salvar_mapeamento(arquivos_mapeados, nome_arquivo_mapeamento)
        self.renomear_arquivos(arquivos_mapeados)


    def listar_todos_os_arquivos_de_texto(self, nome_diretorio):
        arquivos_de_texto = []

        arquivos_diretorio = os.listdir(nome_diretorio)

        for arquivo in arquivos_diretorio:
            if '.txt' in arquivo:
                arquivos_de_texto.append(arquivo)

        return arquivos_de_texto

    def atribuir_indices(self, lista_de_arquivos_de_texto):
        arquivos_mapeados = []

        i = 1
        for arquivo in lista_de_arquivos_de_texto:
            arquivos_mapeados.append((i, arquivo))
            i += 1

        return arquivos_mapeados

    def salvar_mapeamento(self, arquivos_mapeados, nome_do_arquivo):
        arquivo_de_salvamento = open(nome_do_arquivo, "w+")

        for registro in arquivos_mapeados:
            indice, nome_arquivo = registro
            arquivo_de_salvamento.write(str(indice) + " " + nome_arquivo + "\n")

        arquivo_de_salvamento.close()

    def renomear_arquivos(self, arquivos_mapeados):
        for indice, nome_arquivo in arquivos_mapeados:
            novo_nome = self.caminho_dos_emails + str(indice) + ".txt"
            os.rename(self.caminho_dos_emails + nome_arquivo, novo_nome)
            print(nome_arquivo + "\t -> \t" + novo_nome)


    def carregar_mapeamento(self, nome_arquivo_mapeamento):
        self.dicionario = {}

        with open(nome_arquivo_mapeamento, "r") as arquivo_de_mapeamento:
            registro = arquivo_de_mapeamento.readline()

            while(registro != ""):
                indice, nome_antigo = registro.split(' ', 1)
                nome_antigo = nome_antigo.replace('\n', '')
                self.dicionario[nome_antigo] = indice

                registro = arquivo_de_mapeamento.readline()

        arquivo_de_mapeamento.close()

    def obter_novo_nome(self, nome_arquivo_antigo):
        return self.dicionario[nome_arquivo_antigo];



'''def main():
    mapeador = Mapeador("../dados/0_todos_os_emails/")
    #mapeador.mapear("../dados/0_mapeamento.txt") !!!!so executar uma vez!!!!

    mapeador.carregar_mapeamento("../dados/0_mapeamento.txt");

    print(mapeador.obter_novo_nome("20190521-Palestra_”O papel do herdeiro frente aos negócios da família” dia 29_05_19-328.txt"))

main()'''