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
import asyncio
import requests

import time
import json

OZON_url = "https://ozon.ru"
WB_url = "https://www.wildberries.ru/"
YMarket_url = "https://market.yandex.ru/"

TIME_SLEEP = 3
TIME_WAIT = 5
page_scroll_down_times = 10


class ParcingError(Exception):
    pass


def scroll(driver):
    for _ in range(page_scroll_down_times):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.1)


def init_driver(url):
    driver = uc.Chrome()
    driver.implicitly_wait(TIME_WAIT)
    driver.get(url)
    time.sleep(TIME_SLEEP)

    return driver


def get_info_Ymarket(product, count=10):
    driver = init_driver(YMarket_url)

    input_window = driver.find_element(By.NAME, 'text')
    input_window.send_keys(product)
    time.sleep(TIME_SLEEP)

    input_window.send_keys(Keys.ENTER)
    time.sleep(TIME_SLEEP)

    # <div data-cs-name="navigate"

    item_links = driver.find_elements(By.CSS_SELECTOR, '[data-auto="galleryLink"]')
    item_links = list(set([f'{item.get_attribute("href")}' for item in item_links]))
    products = []

    for link in range(min(len(item_links), count)):
        products.append(find_info_item_ymarket(driver, item_links[link]))


    driver.close()
    driver.quit()

    return products


def find_info_item_ymarket(driver, link):
    driver.switch_to.new_window('tab')
    driver.get(link)

    soup = bs(str(driver.page_source), "lxml")

    jsons = soup.find_all('script', type='application/ld+json')
    for js in jsons:
        if "Product" in json.loads(js.string).values():
            state_json = json.loads(js.string)
            item_name = state_json['name']
            item_card = state_json['image']
            item_statistic = state_json['offers']
            item_price_with_card = item_statistic['price']
            item_raiting = state_json['aggregateRating']['ratingValue']
            item_number_of_comments = state_json['aggregateRating']['ratingCount']
            item_price = None
            item_article = None

            noframes_tags = soup.find_all('noframes', attrs={'data-apiary': 'patch'})

            # Перебираем найденные теги
            for tag in noframes_tags:
                content = tag.string.strip()
                data = json.loads(content)
                if "@card/VerifiedBadge" in data["widgets"].keys():
                    item_article = find_gci(data)
                if "@market/Ecommerce" in data["widgets"].keys() and item_price is None:
                    item_price = find_gci(data, 'price')

            d = {"item_name": item_name,
                 "item_article": item_article,
                 "link": link,
                 "item_price": item_price,
                 "item_price_with_card": item_price_with_card,
                 "item_raiting": item_raiting,
                 "item_number_of_comments": item_number_of_comments,
                 "item_card": item_card}
            return d


def find_gci(data, v='gci'):
    """Рекурсивно находит значение поля 'v'."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == v:
                return value
            else:
                result = find_gci(value, v)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_gci(item, v)
            if result is not None:
                return result
    return None


def get_info_WB(product):
    driver = init_driver(WB_url)

    input_window = driver.find_element(By.ID, 'searchInput')
    input_window.send_keys(product)
    time.sleep(TIME_SLEEP)

    input_window.send_keys(Keys.ENTER)
    time.sleep(TIME_SLEEP)

    item_links = driver.find_elements(By.CLASS_NAME, 'product-card__link')
    item_links = list(set([f'{item.get_attribute("href")}' for item in item_links]))
    print(item_links)

    for link in item_links:
        info_of_product = find_info_item_wb(driver, link)
        print(info_of_product)
        time.sleep(1000)
        return

    driver.close()
    driver.quit()


def find_info_item_wb(driver, link):
    driver.switch_to.new_window('tab')
    driver.get(link)

    soup = bs(str(driver.page_source), "lxml")
    with open('no commit/one_pr_wb.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))

    item_name = soup.find('h1', {'class': 'product-page__title'}).get_text(strip=True)
    time.sleep(10000)
    print(item_name)

    # item_name = soup.find(attrs={"data-widget": "webProductHeading"}).get_text(strip=True)
    #
    # item_article = soup.find('div', string=lambda text: "Артикул:" in text).get_text(strip=True)
    #
    # find_data_state = soup.find_all('div', attrs={'data-state': True})
    # item_price, item_price_with_card = None, None
    #
    # for element in find_data_state:
    #     state_json = json.loads(element['data-state'])
    #     if 'cardPrice' in state_json:
    #         #print(state_json)
    #         item_price = state_json['price']
    #         item_price_with_card = state_json['cardPrice']
    #         break
    #
    # state_json_2 = json.loads(soup.find('script', type='application/ld+json').string)
    # item_card = state_json_2["image"]
    # item_raiting = state_json_2["aggregateRating"]["ratingValue"]
    # item_number_of_comments = state_json_2["aggregateRating"]["reviewCount"]
    #
    # d = {"item_name": item_name,
    #      "item_article": item_article,
    #      "link": link,
    #      "item_price": item_price,
    #      "item_price_with_card": item_price_with_card,
    #      "item_raiting": item_raiting,
    #      "item_number_of_comments": item_number_of_comments,
    #      "item_card": item_card}

    driver.close()  # закрываем данную вкладку
    window_handles = driver.window_handles
    first_tab_handle = window_handles[0]
    driver.switch_to.window(first_tab_handle)  # возвращаемся на самую первую страницу

    return 'z'


def get_info_ozon(product, count=10):
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

    products = []
    for link in range(min(len(item_links), count)):
        products.append(find_info_item(driver, item_links[link]))
        # print(info_of_product)

    driver.close()
    driver.quit()

    return products


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
            # print(state_json)
            item_price = state_json['price']
            item_price_with_card = state_json['cardPrice']
            break

    state_json_2 = json.loads(soup.find('script', type='application/ld+json').string)
    item_card = state_json_2["image"]

    try:
        item_raiting = state_json_2["aggregateRating"]["ratingValue"]
    except KeyError:
        item_raiting = None

    try:
        item_number_of_comments = state_json_2["aggregateRating"]["reviewCount"]
    except KeyError:
        item_number_of_comments = None

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


#get_info_ozon('тапочки')
# get_info_WB('тапочки')
#get_info_Ymarket('самовар')
