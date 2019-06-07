class Normalizador:

    def normalizar_emails(self, caminhos_emails):
        for caminho_email in caminhos_emails:
            self.normalizar_email(caminho_email)

    def normalizar_email(self, caminho_email):
        with open(caminho_email, "r+") as arquivo_email:
            conteudo_email = arquivo_email.read()

            conteudo_email = self.remover_pontuacao(conteudo_email)
            conteudo_email = self.remover_cabecalho(conteudo_email)
            conteudo_email = self.substituir_caracteres_acentuados(conteudo_email)
            conteudo_email = self.converter_caracteres_para_minusculo(conteudo_email)

            arquivo_email.seek(0)
            arquivo_email.write(conteudo_email)
            arquivo_email.truncate()
        arquivo_email.close()

    # TODO
    def remover_pontuacao(self, conteudo_email):
        novo_conteudo = conteudo_email
        return novo_conteudo

    # TODO
    def remover_cabecalho(self, conteudo_email):
        novo_conteudo = conteudo_email
        return novo_conteudo

    # TODO
    def substituir_caracteres_acentuados(self, conteudo_email):
        novo_conteudo = conteudo_email
        return novo_conteudo

    def converter_caracteres_para_minusculo(self, conteudo_email):
        novo_conteudo = conteudo_email.lower()
        return novo_conteudo
