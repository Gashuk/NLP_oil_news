import pandas as pd
import numpy as np
import re
import nltk
from pymorphy2 import MorphAnalyzer
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download("stopwords")
nltk.download("punkt")
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import keras
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras import preprocessing
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM


def freqwords(text):                                                            # функция, удаляющая часто встречающиеся слова
    return " ".join([word for word in str(text).split() if word not in freq])

def lemmatize(text):                                                            # функция, выполняющая лемматизацию
    morph = MorphAnalyzer()
    text = re.sub(patterns, ' ', text)
    tokens = []
    for token in text.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]            
            tokens.append(token)
    if len(tokens) > 2:
        return ' '.join(tokens)
    return None


df = pd.read_excel('doc_comment_summary.xlsx')
print(df)

for i in range(0, df.shape[0]):
   df.loc[i]['Text'] = str(df.loc[i]['Text'])

print(df.shape[0])
df = df.dropna()
print(df.shape[0])
df = df[(df['Class']==-2) | (df['Class']==-1) | (df['Class']==-0) | (df['Class']==1)|(df['Class']==2)]
print(df.shape[0])


print("-2 = " + str(df[df['Class']==-2].shape[0]))
print("-1 = " + str(df[df['Class']==-1].shape[0]))
print(" 0 = " + str(df[df['Class']==0].shape[0]))
print(" 1 = " + str(df[df['Class']==1].shape[0]))
print(" 2 = " + str(df[df['Class']==2].shape[0]))
print("all= " + str(df.shape[0]))



print(df)

df['Text'] = df['Text'].str.lower()

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"

for i in range(0, df.shape[0]):
    df.iloc[i]['Text'] = re.sub(patterns, ' ', str(df.iloc[i]['Text']))
print(df)

cnt = Counter()
for text in df["Text"].values:
      for word in text.split():
          cnt[word] += 1
print(cnt)

freq = set([w for (w, wc) in cnt.most_common(15)])
freq.to_csv("freq.csv", index=False)
df["Text"] = df["Text"].apply(freqwords) 

print(df)

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
df['Text'] = df['Text'].apply(lemmatize)
print(df)



df = df.rename(columns = {'Class':'label','Text':'text'})
df.text = df.text.astype(str)
df.label = df.label.astype(int)
df.label[df.label == -1] = 3
df.label[df.label == -2] = 4


df.label.dtype

df.to_csv("text_all.csv", index=False)


X_train, X_val, y_train, y_val = train_test_split(df.index.values, 
                                                  df.label.values, 
                                                  test_size=0.15, 
                                                  random_state=42, 
                                                  stratify=df.label.values)


df.to_csv("X_train.csv", index=False)
df.to_csv("X_val.csv", index=False)
df.to_csv("y_train.csv", index=False)
df.to_csv("y_val.csv", index=False)