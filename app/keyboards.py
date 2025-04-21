from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Узнать как пользоваться ботом 🤖⚡')]
],
    resize_keyboard=True,
    input_field_placeholder='Нажми кнопку, чтобы узнать всё про этого бота')

help_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Узнай как пользоваться ботом 🤖')]
])

# обязательно дописывать url
settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='где это блять работает', url='https://youtube.com/playlist?list=PLV0FNhq3XMOJ31X9eBWLIZJ4OVjBwb-KM&si=mVrn66eBvb0sFVdh')]
])