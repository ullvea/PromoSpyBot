from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Узнай как пользоваться ботом 🤖⚡')]
],
    resize_keyboard=True,
    input_field_placeholder='Нажми кнопку, чтобы узнать всё про этого бота')

help_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сравнить цены на маркетплейсах 📈'),
     KeyboardButton(text='Добавить в товар в отслеживание 💸')],
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
links = ['https://www.ozon.ru/', 'https://www.wildberries.ru/',
         'https://market.yandex.ru/']

async def inline_web():
    keyboard = InlineKeyboardBuilder()
    for i in range(len(websites)):
        keyboard.add(InlineKeyboardButton(text=websites[i], url=links[i]))
    return keyboard.adjust(2).as_markup()