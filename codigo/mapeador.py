import os

class Mapeador:

    def __init__(self, caminho_dos_emails):
        self.caminho_dos_emails = caminho_dos_emails


    def mapear(self, nome_arquivo_mapeamento):
        arquivos_de_texto = self.listar_todos_os_arquivos_de_texto(self.caminho_dos_emails)
        arquivos_mapeados = self.criar_mapeamento(arquivos_de_texto)
        self.salvar_mapeamento(arquivos_mapeados, nome_arquivo_mapeamento);
        self.renomear_arquivos(arquivos_mapeados)

    def listar_todos_os_arquivos_de_texto(self, nome_diretorio):

        arquivos_de_texto = []

        arquivos_diretorio = os.listdir(nome_diretorio)

        for arquivo in arquivos_diretorio:
            if '.txt' in arquivo:
                arquivos_de_texto.append(arquivo)

        return arquivos_de_texto

    def criar_mapeamento(self, lista_de_arquivos_de_texto):

        arquivos_mapeados = []

        i = 1
        for arquivo in lista_de_arquivos_de_texto:
            arquivos_mapeados.append((i, arquivo))
            i += 1

        return arquivos_mapeados

    def salvar_mapeamento(self, arquivos_mapeados, nome_do_arquivo):

        arquivo_de_salvamento = open(nome_do_arquivo, "w+");

        for registro in arquivos_mapeados:
            indice, nome_arquivo = registro
            arquivo_de_salvamento.write(str(indice) + " " + nome_arquivo + "\n")

        arquivo_de_salvamento.close();

    def renomear_arquivos(self, arquivos_mapeados):

        for indice, nome_arquivo in arquivos_mapeados:
            novo_nome = self.caminho_dos_emails + str(indice) + ".txt"
            os.rename(self.caminho_dos_emails + nome_arquivo, novo_nome)
            print(nome_arquivo + "\t -> \t" + novo_nome)


def main():
    mapeador = Mapeador("../dados/0_todos_os_emails/");
    #mapeador.mapear("../dados/0_mapeamento.txt")

main()