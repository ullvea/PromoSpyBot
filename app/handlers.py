import asyncio
from aiogram import F, Router
from aiogram.enums import parse_mode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()
BOT_USERNAME = "PromoSpy_bot"


@router.message(CommandStart())  # декоратор для обработчика команды start
async def process_start_command(message: Message):
    await message.reply(
        f"Привет, @{message.from_user.username}! 👋 \n Я бот-парсер, готов помочь тебе собрать нужную информацию."
        " Скажи, что именно ты хочешь найти? \n Ниже представлены ссылки на сайты, в которых мы ищем нужный Вам товар",
        reply_markup=await kb.inline_web()
)  # отправляет ответ на сообщение


@router.message(F.text.contains("Узнать как пользоваться ботом 🤖⚡"))
@router.message(Command('help'))  # декоратор для обработчика команды help
async def help_cmd(message: Message):
    await message.reply(f"<b>Что может этот бот?</b>\n"
                        "📌 помочь тебе сравнить цены товаров на различных маркетплейсах.\n"
                        "📌 узнать как изменялась цена товар последнее время\n"
                        "📌 узнать какие ещё есть похожие товары по этому запросу\n\n"

                        "<b>Какие есть быстрые команды?</b>\n"
                        f"/help - помощь по боту\n"
                        f"/my_goods - товары, добавленные для отслеживания цен\n"
                        "/support - написать сообщение в случае некорректной работы бота\n"
                        "\n"

                        "<b>Что же можешь сделать ты:</b>\n"
                        "📌 можешь отправить мне название товара или же скинуть его фотку, "
                        "в ответ я скину тебе информацию об этом товаре из разных источников.",
                        parse_mode="HTML", reply_markup=kb.settings)


@router.message(Command('support'))
async def support(message: Message):
    await message.answer('Напишите что пошло не так. Мы постараемся все уладить')


@router.message(F.photo)  # функция для получения фотографий
async def get_photo(message: Message):
    await message.answer(message.photo[1].file_id)


@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(
        photo="AgACAgIAAxkBAANjaAIHz78dRbUq3xqJlQ99XFKSliEAAobrMRsb6BFIK2F21syNTTEBAAMCAANtAAM2BA",
        caption='так выглядит подпись')
    # где фото можно указать ссылку из гугла




@router.message()  # декоратор для обработчика прочих сообщений
async def common_message(message: Message, bot):
    response_message = await message.answer(f'Запрос принят, @{message.from_user.username}!\n'
                                            '💭Ещё чуть-чуть, готовлю ответ')
    # отправляет сообщение об обработке запроса, а затем удаляет его пока 5 сек, в дальнейшим пока
    # не сгенерируется запрос
    await delete_message(response_message.chat.id, response_message.message_id, 5, bot)


# Функция для удаления сообщения через заданное время
async def delete_message(chat_id, message_id, delay, bot):
    await asyncio.sleep(delay)
    await bot.delete_message(chat_id, message_id)

# @router.callback_query(F.data == 'catalog')
# async def catalog(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.answer('Привет!')