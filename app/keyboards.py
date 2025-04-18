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