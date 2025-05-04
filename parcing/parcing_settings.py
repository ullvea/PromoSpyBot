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
TIME_WAIT = 2


async def init_driver(url):
    driver = uc.Chrome()
    driver.implicitly_wait(TIME_WAIT)
    driver.get(url)
    await asyncio.sleep(TIME_SLEEP)

    return driver


async def find_gci(data, v='gci'):
    """Рекурсивно находит значение поля 'v'."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == v:
                return value
            else:
                result = await find_gci(value, v)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = await find_gci(item, v)
            if result is not None:
                return result
    return None