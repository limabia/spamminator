import os
import string

import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.naive_bayes import MultinomialNB

DIR_HAM = '../dados/normais/mensagens'
DIR_SPAM = '../dados/spam/mensagens'

print("Baixando as stopwords")
nltk.download('stopwords')

# Constroi o Data Frame
df = pd.DataFrame(columns=['label', 'texto'])
for filename in os.listdir(DIR_HAM):
    if filename.endswith(".txt"):
        file = open('{}/{}'.format(DIR_HAM, filename), 'r')
        text = ' '.join(file.readlines())
        file.close()
        df = df.append({'label': 'HAM', 'texto': text}, ignore_index=True)

for filename in os.listdir(DIR_SPAM):
    if filename.endswith(".txt"):
        file = open('{}/{}'.format(DIR_SPAM, filename), 'r')
        text = ' '.join(file.readlines())
        file.close()
        df = df.append({'label': 'SPAM', 'texto': text}, ignore_index=True)


# Pre processamento
def text_process(mess):
    nopunc = [char for char in mess if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('portuguese')]


print(df.describe())
print(df.groupby('label').describe())

# Bag of Words transformer
print('Criando transforador de bag of words')
bow_transformer = CountVectorizer(analyzer=text_process).fit(df['texto'])

print('Criando bag of words')
messages_bow = bow_transformer.transform(df['texto'])

tfidf_transformer = TfidfTransformer().fit(messages_bow)
print('Calculando TF-IDF')
messages_tfidf = tfidf_transformer.transform(messages_bow)

print('Treinando modelo Multinomial Naive Bayes')
spam_detect_model = MultinomialNB().fit(messages_tfidf, df['label'])

print('Predizendo')
all_predictions = spam_detect_model.predict(messages_tfidf)

print(classification_report(df['label'], all_predictions))
print(confusion_matrix(df['label'], all_predictions))
