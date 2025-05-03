import asyncio
import requests

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputMediaPhoto, InputFile, FSInputFile
import aiohttp

from app.parcing.parcing import get_info_ozon, get_info_Ymarket


import app.keyboards as kb

router = Router()
BOT_USERNAME = "PromoSpy_bot"
PRODUCT = None


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
                        parse_mode="HTML", reply_markup=kb.start_keyboard)


@router.message(Command('support'))
async def support(message: Message):
    await message.answer('Напишите что пошло не так. Мы постараемся все уладить')


@router.message(F.photo)  # функция для получения фотографий
async def get_photo(message: Message):
    await message.answer(message.photo[1].file_id)


# @router.message(Command('get_photo'))
# async def get_photo(message: Message):
#     await message.answer_photo(
#         photo="AgACAgIAAxkBAANjaAIHz78dRbUq3xqJlQ99XFKSliEAAobrMRsb6BFIK2F21syNTTEBAAMCAANtAAM2BA",
#         caption='так выглядит подпись')
    # где фото можно указать ссылку из гугла


# reply_markup=kb.help_keyboard

@router.message(F.text.contains('Добавить в товар в отслеживание 💸'))
async def common_message(message: Message, bot):
    await thinking_message(message, bot)


@router.message(F.text.contains('Сравнить цены на маркетплейсах 📈'))
async def common_message(message: Message, bot):
    await thinking_message(message, bot)


@router.message(F.text.contains('Узнать цены похожих на товаров в магазине 🛍️'))
async def common_message(message: Message, bot):
    await message.reply('Выберите нужный Вам магазин на клавиатуре',
                        reply_markup=kb.shops_keyboard)


def format_message(mes: dict):
    return (f'<b>{mes['item_name']}</b>\n'
            f'{mes['item_article']}\n'
            f'Цена/цена по карте: {mes['item_price']} / {mes['item_price_with_card']}\n'
            f'Рейтинг/комментарии: {mes['item_raiting']}⭐️ / {mes['item_number_of_comments']}💬\n\n')

async def download_photo(url):
    return InputMediaPhoto(media=url)


@router.message(F.text.contains('Ozon'))
async def common_message(message: Message, bot):
    global PRODUCT
    thinking_message = await message.answer(f'Запрос принят, @{message.from_user.username}!\n'
                         '💭Ещё чуть-чуть, готовлю ответ')
    ans = get_info_ozon(PRODUCT, 3)
    mes = ""
    photos = await asyncio.gather(*[download_photo(url['item_card']) for url in ans])
    for item in ans:
        mes += format_message(item)
    photos[-1].caption = mes
    photos[-1].parse_mode = "HTML"

    await bot.delete_message(thinking_message.chat.id, thinking_message.message_id)
    # Отправляем группу фотографий
    await bot.send_media_group(chat_id=message.chat.id, media=photos)

# @router.message(F.text.contains('Wildberries'))
# async def common_message(message: Message, bot):
#     await thinking_message(message, bot)


@router.message(F.text.contains('ЯндексМаркет'))
async def common_message(message: Message, bot):
    global PRODUCT
    thinking_message = await message.answer(f'Запрос принят, @{message.from_user.username}!\n'
                                            '💭Ещё чуть-чуть, готовлю ответ')

    ans = get_info_Ymarket(PRODUCT, 3)
    mes = ""
    photos = await asyncio.gather(*[download_photo(url['item_card']) for url in ans])
    for item in ans:
        mes += format_message(item)
    photos[-1].caption = mes
    photos[-1].parse_mode = "HTML"

    await bot.delete_message(thinking_message.chat.id, thinking_message.message_id)
    # Отправляем группу фотографий
    await bot.send_media_group(chat_id=message.chat.id, media=photos)


@router.message()  # декоратор для обработчика прочих сообщений
async def common_message(message: Message, bot):
    global PRODUCT
    PRODUCT = message.text
    print(PRODUCT)
    await message.answer(f'Выберите, что Вы хотите сделать с данным товаром на клавиатуре:',
                         reply_markup=kb.help_keyboard)


# async def thinking_message(message: Message, bot):
#     response_message = await message.answer(f'Запрос принят, @{message.from_user.username}!\n'
#                                             '💭Ещё чуть-чуть, готовлю ответ')
#     # отправляет сообщение об обработке запроса, а затем удаляет его пока 5 сек, в дальнейшим пока
#     # не сгенерируется запрос
#     await delete_message(response_message.chat.id, response_message., 5, bot)
#
#
# # Функция для удаления сообщения через заданное время
# async def delete_message(chat_id, message_id, delay, bot):
#     await asyncio.sleep(delay)
#     await bot.delete_message(chat_id, message_id)

# @router.callback_query(F.data == 'catalog')
# async def catalog(callback: CallbackQuery):
#     await callback.answer('')
#     await callback.message.answer('Привет!')
