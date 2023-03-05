import pandas as pd
import numpy as np
import re
import nltk
from pymorphy2 import MorphAnalyzer
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import keras
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras import preprocessing
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM

import seaborn as sns
import matplotlib.pyplot as plt


def freqwords(text):                                                            # функция, удаляющая часто встречающиеся слова
    return " ".join([word for word in str(text).split() if word not in freq])

def lemmatize(text):          
    stopwords_ru = stopwords.words("russian")                                                  # функция, выполняющая лемматизацию
    morph = MorphAnalyzer()
    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
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

def class_comments(path):
  with open(path) as file:
    text = str(file.readlines())

  patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
  stopwords_ru = stopwords.words("russian")

  tfidfconverter = TfidfVectorizer(max_features = 845, min_df = 5, max_df = 0.7)
  text = tfidfconverter.transform([lemmatize(freqwords(text))]).toarray()
  prediction = keras.models.load_model('/content/drive/MyDrive/NLP_проект/model').predict(text)

  display(prediction)
  
  print("Прогноз:"+str(float(prediction.max())*100)+"%")
  if (prediction.max() == prediction[0][0]):
    print("Комментарий очень отрицательный")
    return int(-2)
  elif (prediction.max() == prediction[0][1]):
    print("Комментарий отрицательный") 
    return int(-1)
  elif (prediction.max() == prediction[0][2]):
    print("Комментарий нетральный") 
    return int(0)
  elif (prediction.max() == prediction[0][3]):
    print("Комментарий положительный") 
    return int(1)
  elif (prediction.max() == prediction[0][4]):
    print("Комментарий очень положительный") 
    return int(2)

df = pd.read_excel('/content/drive/MyDrive/NLP_проект/parsing_NLP_news_comments.xlsx')

print(df)

freq =  pd.read_csv('freq.csv')
for i in range(0, df.shape[0]):
  class_comm = class_comments(str(df.loc[i]['Comments']))
  df.loc[i]['Class'] = class_comm

writer = pd.ExcelWriter('parsing_NLP_news_comments_class.xlsx')
df.to_excel(writer)
writer.save()

df_teg = pd.DataFrame({'News_head': [], 'Url': [], 'Date': [], 'Tegs': [], 'Comments': [], 'Class': []})
for i in range(0, df.shape[0]):
  teg_news = str(df.loc[i]['Tegs']).split(";")
  for j in teg_news:
      df_teg.loc[len(df_teg.index)] = [str(df.loc[i]['News_head']), str(df.loc[i]['Url']), str(df.loc[i]['Date']), str(j), str(df.loc[i]['Comments']), int(df.loc[i]['Class'])]


df_teg_count = pd.DataFrame({'Tegs': [], 'Count': []})
teg_uniq = df_teg['Tegs'].unique()
for i in teg_uniq:
    teg_count = df_teg[df_teg['Tegs'] == str(i)]
    df_teg_count.loc[len(df_teg_count.index)] = [str(i), int(teg_count)]
    

df_teg_count.sort_values(by=['Count'])

df_teg_top = df_teg_count.head(15)

df_tag_one = df_teg[df_teg['Tegs'] == df_teg_top[0]['Tegs']]


df_tag_one_date = df_tag_one[df_tag_one['Date']].unique()

value_1 = np.array([]).astype(int)
value_2 = np.array([]).astype(int)
value_3 = np.array([]).astype(int)
value_4 = np.array([]).astype(int)
value_5 = np.array([]).astype(int)


for i in df_tag_one_date:

    value_1 = np.append(value_1, int(df_tag_one-[(df_tag_one['Date'] == i and df_tag_one['Class'] == -2)].shape[0]))
    value_2 = np.append(value_2, int(df_tag_one-[(df_tag_one['Date'] == i and df_tag_one['Class'] == -1)].shape[0]))
    value_3 = np.append(value_3, int(df_tag_one-[(df_tag_one['Date'] == i and df_tag_one['Class'] == 0)].shape[0]))
    value_4 = np.append(value_4, int(df_tag_one-[(df_tag_one['Date'] == i and df_tag_one['Class'] == 1)].shape[0]))
    value_5 = np.append(value_5, int(df_tag_one-[(df_tag_one['Date'] == i and df_tag_one['Class'] == 2)].shape[0]))


dates = pd.DatetimeIndex(df_tag_one_date.to_numpy())



sns.set(style='whitegrid')


fig, axs = plt.subplots(nrows=5, figsize=(15, 20))

sns.lineplot(data=pd.DataFrame({'date': dates, 'value': value_1}), x='date', y='value', color='red', ax=axs[0])
axs[0].set_title('\n \n Тег "Нефть" \n Очень негативные комментарии')
axs[0].set_xlabel('Дата публикации новости')
axs[0].set_ylabel('Количество комментариев')

sns.lineplot(data=pd.DataFrame({'date': dates, 'value': value_2}), x='date', y='value', color='#FFB6C1', ax=axs[1])
axs[1].set_title('\n \n Тег "Нефть" \n Негативные комментарии')
axs[1].set_xlabel('Дата публикации новости')
axs[1].set_ylabel('Количество комментариев')

sns.lineplot(data=pd.DataFrame({'date': dates, 'value': value_3}), x='date', y='value', color='gray', ax=axs[2])
axs[2].set_title('\n \n Тег "Нефть" \n Нейтральные комментарии')
axs[2].set_xlabel('Дата публикации новости')
axs[2].set_ylabel('Количество комментариев')

sns.lineplot(data=pd.DataFrame({'date': dates, 'value': value_4}), x='date', y='value', color='#8FD8AA', ax=axs[3])
axs[3].set_title('\n \n Тег "Нефть" \n Позитивные комментарии')
axs[3].set_xlabel('Дата публикации новости')
axs[3].set_ylabel('Количество комментариев')

sns.lineplot(data=pd.DataFrame({'date': dates, 'value': value_5}), x='date', y='value', color='green', ax=axs[4])
axs[4].set_title('\n \n Тег "Нефть" \n Очень позитивные комментарии')
axs[4].set_xlabel('Дата публикации новости')
axs[4].set_ylabel('Количество комментариев')


for ax in axs:
    ax.set_ylim(0, 70)


plt.tight_layout()
plt.show()

