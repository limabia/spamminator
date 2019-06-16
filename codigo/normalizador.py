import os

class Normalizador:

    def normalizar_emails(self, diretorio_emails):
        for nome_email in os.listdir(diretorio_emails):
            caminho_email = diretorio_emails + nome_email
            self.normalizar_email(caminho_email)

    def normalizar_email(self, caminho_email):
        with open(caminho_email, "r+") as arquivo_email:
            linhas = []
            linha = arquivo_email.readline()
            while linha != '':
                linhas.append(linha)
                linha = arquivo_email.readline()

            conteudo_email = self.remover_cabecalho(linhas)
            arquivo_email.seek(0)
            arquivo_email.write(conteudo_email)
            arquivo_email.truncate()
        arquivo_email.close()

    # TODO
    def remover_cabecalho(self, linhas):

        conteudo_email = ''

        cont = 0
        for linha in linhas:
            if cont < 7:

                if not (linha.startswith('Data:')
                        #or linha.startswith('Assunto')
                        or linha.startswith('Reply-to:')
                        #or linha.startswith('De:')
                        or linha.startswith('Para:')
                        or linha.startswith('BCC:')):
                    conteudo_email += (linha)
                cont += 1
            else:
                conteudo_email += (linha)

        return conteudo_email

c1 = '../dados/2_classificacao_ricardo/nao_spam/'
c2 = '../dados/2_classificacao_ricardo/spam/'

n = Normalizador()
print("Normalizando {}".format(c1))
n.normalizar_emails(c1)
print("Normalizado! {}".format(c1))

print("Normalizando {}".format(c2))
n.normalizar_emails(c2)
print("Normalizado! {}".format(c2))