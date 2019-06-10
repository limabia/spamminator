import string

import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

HAM_FILE = '../dados/2_classificacao_ricardo/nao_spam.txt'
SPAM_FILE = '../dados/2_classificacao_ricardo/spam.txt'

print("Baixando as stopwords")
nltk.download('stopwords')

# Constroi o Data Frame
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

print(df.describe())
print(df.groupby('label').describe())


def pre_processamento(mess):
    nopunc = [char for char in mess if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('portuguese')]


# separa massa de treino e massa de testes
massa_treino, massa_teste, labels_treino, labels_teste = train_test_split(df['texto'], df['label'], test_size=0.2)

# constroi pipeline
pipeline = Pipeline([
    ('bow', CountVectorizer(analyzer=pre_processamento)),
    # Bag of words - https://en.wikipedia.org/wiki/Bag-of-words_model
    ('tfidf', TfidfTransformer()),  # TF-IDF - https://en.wikipedia.org/wiki/Tf%E2%80%93idf
    ('classifier', MultinomialNB()),  # Naive Bayes - Multinomial
])

print('treinando modelo')
pipeline.fit(massa_treino, labels_treino)

print('testando modelo')
predictions = pipeline.predict(massa_teste)

print(classification_report(predictions, labels_teste))
print(confusion_matrix(predictions, labels_teste))
