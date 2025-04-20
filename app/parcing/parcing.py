# пока здесь парсится озон, но не очень активно ((

# Веб-скрейпинг — это технология получения веб-данных путём извлечения
# их со страниц веб-ресурсов.

# https://www.selenium.dev/documentation/webdriver/interactions/


from selenium.webdriver.common.by import By  # selenium - инструмент для автоматизации приложений
from selenium.webdriver.common.keys import Keys  # содержит константы, представляющие различные клавиши клавиатуры
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc  # расширение библиотеки Selenium

from bs4 import BeautifulSoup as bs
import requests

import time
import json

OZON_url = "https://ozon.ru"
WB_url = "https://www.wildberries.ru/"
YMarket_url = "https://market.yandex.ru/"

TIME_SLEEP = 2
TIME_WAIT = 5
page_scroll_down_times = 10


def scroll(driver):
    for _ in range(page_scroll_down_times):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.1)


class ParcingError(Exception):
    pass


def get_info_Ymarket(product):
    driver = init_driver(YMarket_url)

    input_window = driver.find_element(By.NAME, 'text')
    input_window.send_keys(product)
    time.sleep(TIME_SLEEP)

    input_window.send_keys(Keys.ENTER)
    time.sleep(TIME_SLEEP)

    driver.close()
    driver.quit()


def get_info_WB(product):
    driver = init_driver(WB_url)

    input_window = driver.find_element(By.ID, 'searchInput')
    input_window.send_keys(product)
    time.sleep(TIME_SLEEP)

    input_window.send_keys(Keys.ENTER)
    time.sleep(TIME_SLEEP)

    driver.close()
    driver.quit()


def init_driver(url):
    driver = uc.Chrome()
    driver.implicitly_wait(TIME_WAIT)
    driver.get(url)
    time.sleep(TIME_SLEEP)

    return driver


def find_info_item(driver, link):
    driver.switch_to.new_window('tab')
    driver.get(link)

    soup = bs(str(driver.page_source), "lxml")

    item_name = soup.find(attrs={"data-widget": "webProductHeading"}).get_text(strip=True)

    item_article = soup.find('div', string=lambda text: "Артикул:" in text).get_text(strip=True)

    find_data_state = soup.find_all('div', attrs={'data-state': True})
    item_price, item_price_with_card = None, None

    for element in find_data_state:
        state_json = json.loads(element['data-state'])
        if 'cardPrice' in state_json:
            #print(state_json)
            item_price = state_json['price']
            item_price_with_card = state_json['cardPrice']
            break

    state_json_2 = json.loads(soup.find('script', type='application/ld+json').string)
    item_card = state_json_2["image"]
    item_raiting = state_json_2["aggregateRating"]["ratingValue"]
    item_number_of_comments = state_json_2["aggregateRating"]["reviewCount"]

    d = {"item_name": item_name,
         "item_article": item_article,
         "link": link,
         "item_price": item_price,
         "item_price_with_card": item_price_with_card,
         "item_raiting": item_raiting,
         "item_number_of_comments": item_number_of_comments,
         "item_card": item_card}

    driver.close()  # закрываем данную вкладку
    window_handles = driver.window_handles
    first_tab_handle = window_handles[0]
    driver.switch_to.window(first_tab_handle)  # возвращаемся на самую первую страницу

    return d


def get_info_ozon(product):
    driver = init_driver(OZON_url)

    input_window = driver.find_element(By.NAME, 'text')
    input_window.send_keys(product)
    time.sleep(TIME_SLEEP)

    input_window.send_keys(Keys.ENTER)
    time.sleep(TIME_SLEEP)

    current_url = f'{driver.current_url}'  # параметр с озона
    time.sleep(TIME_SLEEP)

    item_links = driver.find_elements(By.CLASS_NAME, 'tile-clickable-element')
    item_links = list(set([f'{item.get_attribute("href")}' for item in item_links]))

    products_dict = dict()
    for link in item_links:
        info_of_product = find_info_item(driver, link)
        print(info_of_product)
        return

    driver.close()
    driver.quit()


get_info_ozon('тапочки')
