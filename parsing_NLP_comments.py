import time
import pandas as pd
from selenium import webdriver
import random
from selenium.webdriver.common.by import By


df_news = pd.read_excel('D:\PycharmProjects\pythonProject_NLP\parsing_NLP.xlsx')
df_news = df_news.drop(columns=['Unnamed: 0'])

driver = webdriver.Chrome()


df_news_url = pd.DataFrame({'News_head': [], 'Url': [], 'Date': [], 'Tegs': [], 'Comments': [], 'Class': []})

try:

    for col in df_news.iloc:
        news_head, url, date, tegs, comments, class_comments = col

        driver.get(f'{url}')
        time.sleep(random.randint(3, 10))
        driver.maximize_window()
        time.sleep(random.randint(3, 10))

        all_tegs = driver.find_elements(By.XPATH, "//a[@class='tags-trends__link link link_underline_color']")
        mas_tegs = []
        for i in range(0, len(all_tegs)):
            mas_tegs.append(str(all_tegs[i].text))

        tegs = ";".join(mas_tegs)
        time.sleep(random.randint(3, 10))

        all_comments = driver.find_elements(By.XPATH, "//div[@class='app-comment__text']")

        for i in range(0, len(all_comments)):
            comment =  all_comments[i].find_elements(By.XPATH,"//span]")[i].text
            df_news_url.loc[len(df_news_url.index)] = [str(news_head), str(url), str(date), str(tegs), str(comment), '']


    driver.quit()

    writer = pd.ExcelWriter('parsing_NLP_news_comments.xlsx')
    df_news_url.to_excel(writer)
    writer.save()
    print('Все хорошо')
except:
    writer = pd.ExcelWriter('parsing_NLP_news_comments.xlsx')
    df_news_url.to_excel(writer)
    writer.save()
    print("Что-то пошло не так")