from parcing.parcing_settings import *

async def get_info_ozon(product, count=10):
    driver = await init_driver(OZON_url)

    input_window = driver.find_element(By.NAME, 'text')
    input_window.send_keys(product)
    await asyncio.sleep(TIME_SLEEP)

    input_window.send_keys(Keys.ENTER)
    await asyncio.sleep(TIME_SLEEP)

    current_url = f'{driver.current_url}'  # параметр с озона
    await asyncio.sleep(TIME_SLEEP)

    item_links = driver.find_elements(By.CLASS_NAME, 'tile-clickable-element')
    item_links = list(set([f'{item.get_attribute("href")}' for item in item_links]))

    products = []
    for link in range(min(len(item_links), count)):
        products.append(await find_info_item(driver, item_links[link]))
        # print(info_of_product)

    #driver.close()
    # driver.quit()

    return products


async def find_info_item(driver, link):
    driver.switch_to.new_window('tab')
    driver.get(link)

    soup = bs(str(driver.page_source), "html.parser")

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