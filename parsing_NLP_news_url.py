import time
import pandas as pd
from selenium import webdriver
import random
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://russian.rt.com/tag/neft')
driver.maximize_window()

BOOL_PARSING = True
df_news = pd.DataFrame({'News_head':[], 'Url':[], 'Date':[], 'Tegs':[],'Comments':[],'Class':[]})


def get_new():

    time.sleep(random.randint(3, 10))

    all_news = driver.find_elements(By.XPATH,"//li[@class='listing__column listing__column_all-new listing__column_js']")

    for i in range(df_news.shape[0],len(all_news)):
        news_head = all_news[i].find_elements(By.XPATH,"//a[@class='link link_color']")[i].text
        news_url = all_news[i].find_elements(By.XPATH,"//a[@class='link link_color']")[i].get_attribute("href")
        news_date = all_news[i].find_elements(By.XPATH,"//time[@class='date']")[i].get_attribute("datetime")

        split_date = str(news_date).split('-')

        if split_date[1] == '02' and split_date[0] == '2022':
            print("ЗАШЛО")
            return len(all_news),False

        df_news.loc[len(df_news.index)] = [str(news_head), str(news_url), str(news_date), '', '', '']

    time.sleep(random.randint(3, 10))
    driver.execute_script("window.scrollTo(300, document.body.scrollHeight);")
    time.sleep(random.randint(3, 10))
    driver.find_element(By.XPATH,"//div[@class='listing__button listing__button_js']//a[@class='button__item button__item_listing']").click()

    return len(all_news),True





try:
    while(BOOL_PARSING):
        plus_new, bool_parseng = get_new()
        BOOL_PARSING = bool_parseng

    writer = pd.ExcelWriter('parsing_NLP_news_url.xlsx')
    df_news.to_excel(writer)
    writer.save()
    print('Все хорошо')
except:
    writer = pd.ExcelWriter('parsing_NLP_news_url.xlsx')
    df_news.to_excel(writer)
    writer.save()
    print('Что-то пошло не так')

driver.quit()



