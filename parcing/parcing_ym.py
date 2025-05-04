from parcing_settings import *

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