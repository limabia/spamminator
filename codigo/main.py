import string
import csv
import os

from unicodedata import normalize
import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from sklearn.model_selection import StratifiedShuffleSplit

HAM_FILE = '../dados/2_classificacao_ricardo/nao_spam.txt'
SPAM_FILE = '../dados/2_classificacao_ricardo/spam.txt'

dicionario_postugues = {}

def inicializar_dicionario():
    for palavra in stopwords.words('portuguese'):
        dicionario_postugues.update({palavra: True})

def controi_data_frame():
    df = pd.DataFrame(columns=['label', 'texto'])
    f = open(HAM_FILE, 'r')
    for arq in f.readlines():
        email = open('../dados/0_todos_os_emails/' + arq[:-1], 'r')
        text = ' '.join(email.readlines())
        email.close()
        df = df.append({'label': 'HAM', 'texto': text}, ignore_index=True)
    f.close()
    f = open(SPAM_FILE, 'r')
    for arq in f.readlines():
        email = open('../dados/0_todos_os_emails/' + arq[:-1], 'r')
        text = ' '.join(email.readlines())
        email.close()
        df = df.append({'label': 'SPAM', 'texto': text}, ignore_index=True)
    f.close()
    return df

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def pre_processamento(mess):
    nopunc = []
    for char in mess:
        if char not in string.punctuation:
            nopunc.append(char)
        else:
            nopunc.append(' ')
    nopunc = ''.join(nopunc)
    return [word.lower() for word in nopunc.split()]

def pre_processamento_sem_stopwords(mess):
    nopunc = []
    for char in mess:
        if char not in string.punctuation:
            nopunc.append(char)
        else:
            nopunc.append(' ')
    nopunc = ''.join(nopunc)
    return [word.lower() for word in nopunc.split() if not dicionario_postugues.get(word.lower())]

def gerar_conjuntos(df):
    sss = StratifiedShuffleSplit(n_splits=1, train_size=0.8, test_size=0.2)
    for train_index, test_index  in sss.split(df['texto'], df['label']):
        massa_treino, massa_teste = df['texto'][train_index], df['texto'][test_index]
        labels_treino, labels_teste = df['label'][train_index], df['label'][test_index]

        return massa_treino, massa_teste, labels_treino, labels_teste

def main():
    print("Baixando as stopwords")
    nltk.download('stopwords')
    inicializar_dicionario()

    df = controi_data_frame()

    print(df.describe())
    print(df.groupby('label').describe())

    # separa massa de treino e massa de testes
    #massa_treino, massa_teste, labels_treino, labels_teste = train_test_split(df['texto'], df['label'], test_size=0.2)

    nome_arquivo_saida = 'simulacao_09_1000_removendo_stopword.csv'

    if os.path.isfile(nome_arquivo_saida):
        print('[!] O arquivo {} já existe, escolha outro nome'.format(nome_arquivo_saida))
        exit(-1)
    else:
        linha_pt1 = ('N_TESTE', 'HAM_precision', 'HAM_recall', 'HAM_f1-score', 'HAM_support')
        linha_pt2 = ('SPAM_precision', 'SPAM_recall', 'SPAM_f1-score', 'SPAM_support')
        linha_pt3 = ('accuracy', 'weighted avg_precision', 'weighted avg_recall', 'weighted avg_f1-score', 'weighted avg_support')
        linha_pt4 = ('HAM->HAM (HAM classificado como HAM)', 'SPAM->HAM (SPAM classificado como HAM)', 'HAM->SPAM', 'SPAM->SPAM')
        linha = linha_pt1 + linha_pt2 + linha_pt3 +linha_pt4
        with open(nome_arquivo_saida, "w+") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(linha)
        arquivo.close()

    # constroi pipeline
    pipeline = Pipeline([
        ('bow', CountVectorizer(analyzer=pre_processamento_sem_stopwords)),
        # Bag of words - https://en.wikipedia.org/wiki/Bag-of-words_model
        ('tfidf', TfidfTransformer()),  # TF-IDF - https://en.wikipedia.org/wiki/Tf%E2%80%93idf
        ('classifier', MultinomialNB()),  # Naive Bayes - Multinomial
    ])

    for i in range(1000):
        print('Teste {} em execucao'.format(i))

        massa_treino, massa_teste, labels_treino, labels_teste = gerar_conjuntos(df)

        print('  Treinando modelo')
        pipeline.fit(massa_treino, labels_treino)
    
        print('  Testando modelo')
        predictions = pipeline.predict(massa_teste)

        print(classification_report(predictions, labels_teste))
        print('\n')
        #(confusion_matrix(predictions, labels_teste))

        c = classification_report(predictions, labels_teste, output_dict=True)
        m = confusion_matrix(predictions, labels_teste)

        linha_pt1 = (i, c['HAM']['precision'], c['HAM']['recall'], c['HAM']['f1-score'], c['HAM']['support'])
        linha_pt2 = (c['SPAM']['precision'], c['SPAM']['recall'], c['SPAM']['f1-score'], c['SPAM']['support'])
        linha_pt3 = (c['accuracy'], c['weighted avg']['precision'], c['weighted avg']['recall'], c['weighted avg']['f1-score'], c['weighted avg']['support'])
        linha_pt4 = (m[0][0], m[0][1], m[1][0], m[1][1])
        linha = linha_pt1 + linha_pt2 + linha_pt3 + linha_pt4

        with open(nome_arquivo_saida, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(linha)

        csvFile.close()

if __name__ == '__main__':
    main()
