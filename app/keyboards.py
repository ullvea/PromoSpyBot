from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Узнай как пользоваться ботом 🤖⚡')]
],
    resize_keyboard=True,
    input_field_placeholder='Нажми кнопку, чтобы узнать всё про этого бота')

help_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сравнить цены на маркетплейсах 📈'), KeyboardButton(text='Добавить в товар в отслеживание 💸')],
    [KeyboardButton(text='Узнать цены похожих на товаров в магазине 🛍️')],
    [KeyboardButton(text='Узнай как пользоваться ботом 🤖')]
], resize_keyboard=True)

shops_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Ozon')],
    [KeyboardButton(text='Wildberries')],
    [KeyboardButton(text='ЯндексМаркет')]
],
    resize_keyboard=True)



# инлайны в сообщении при start
websites = ['OZON', 'WB', 'YandexMarket']
links = ['https://www.ozon.ru/?__rr=1', 'https://www.wildberries.ru/',
         'https://market.yandex.ru/?ysclid=m9yp7s0d8e142034555&wprid=1745700852778117-6767317144964461245-balancer-l7leveler-kubr-yp-sas-62-BAL&utm_source_service=web&src_pof=703&icookie=k7MJrkMIGRZrw7XKfaE3SGQRHsFgVMw39V1iKXVox%2BuzaVrxjdUK8h%2BwTdRquwgTH%2FoW0XoDG6i3be51WvkgU%2FvtnZ8%3D&baobab_event_id=m9yp7s0d8e']

async def inline_web():
    keyboard = InlineKeyboardBuilder()
    for i in range(len(websites)):
        keyboard.add(InlineKeyboardButton(text=websites[i], url=links[i]))
    return keyboard.adjust(2).as_markup()