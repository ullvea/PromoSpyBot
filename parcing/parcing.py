#
#
#
#
#
#
#
#
#
#
#
# def get_info_WB(product):
#     driver = init_driver(WB_url)
#
#     input_window = driver.find_element(By.ID, 'searchInput')
#     input_window.send_keys(product)
#     time.sleep(TIME_SLEEP)
#
#     input_window.send_keys(Keys.ENTER)
#     time.sleep(TIME_SLEEP)
#
#     item_links = driver.find_elements(By.CLASS_NAME, 'product-card__link')
#     item_links = list(set([f'{item.get_attribute("href")}' for item in item_links]))
#     print(item_links)
#
#     for link in item_links:
#         info_of_product = find_info_item_wb(driver, link)
#         print(info_of_product)
#         time.sleep(1000)
#         return
#
#     driver.close()
#     driver.quit()
#
#
# def find_info_item_wb(driver, link):
#     driver.switch_to.new_window('tab')
#     driver.get(link)
#
#     soup = bs(str(driver.page_source), "lxml")
#     with open('no commit/one_pr_wb.html', 'w', encoding='utf-8') as f:
#         f.write(str(soup))
#
#     item_name = soup.find('h1', {'class': 'product-page__title'}).get_text(strip=True)
#     time.sleep(10000)
#     print(item_name)
#
#     # item_name = soup.find(attrs={"data-widget": "webProductHeading"}).get_text(strip=True)
#     #
#     # item_article = soup.find('div', string=lambda text: "Артикул:" in text).get_text(strip=True)
#     #
#     # find_data_state = soup.find_all('div', attrs={'data-state': True})
#     # item_price, item_price_with_card = None, None
#     #
#     # for element in find_data_state:
#     #     state_json = json.loads(element['data-state'])
#     #     if 'cardPrice' in state_json:
#     #         #print(state_json)
#     #         item_price = state_json['price']
#     #         item_price_with_card = state_json['cardPrice']
#     #         break
#     #
#     # state_json_2 = json.loads(soup.find('script', type='application/ld+json').string)
#     # item_card = state_json_2["image"]
#     # item_raiting = state_json_2["aggregateRating"]["ratingValue"]
#     # item_number_of_comments = state_json_2["aggregateRating"]["reviewCount"]
#     #
#     # d = {"item_name": item_name,
#     #      "item_article": item_article,
#     #      "link": link,
#     #      "item_price": item_price,
#     #      "item_price_with_card": item_price_with_card,
#     #      "item_raiting": item_raiting,
#     #      "item_number_of_comments": item_number_of_comments,
#     #      "item_card": item_card}
#
#     driver.close()  # закрываем данную вкладку
#     window_handles = driver.window_handles
#     first_tab_handle = window_handles[0]
#     driver.switch_to.window(first_tab_handle)  # возвращаемся на самую первую страницу
#
#     return 'z'
#
#
#
#
#
# #get_info_ozon('тапочки')
# # get_info_WB('тапочки')
# #get_info_Ymarket('самовар')
