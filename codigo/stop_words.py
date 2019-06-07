class ContadorDeStopWords:

    def __init__(self, lista_de_diretorios_com_emails):
        self.lista_de_diretorios_com_emails = lista_de_diretorios_com_emails
        self.dicionario = {}

    def contar_stop_words(self, arquivo_de_saida):

        for diretorio in self.lista_de_diretorios_com_emails:
            for email in diretorio:
                self.contar_stop_words_nom_email(email)

        #TODO escrever dicionario num arquivo

        pass

    #TODO contar stop words
    def contar_stop_words_nom_email(self, nome_do_email):
        pass