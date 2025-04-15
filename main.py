import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from data.config import BOT_TOKEN  # импортируем токен
import logging

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

# создаем диспетчер
dp = Dispatcher()


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


@dp.message(Command('start'))  # декоратор для обработчика команды start
async def process_start_command(message: types.Message):
    await message.reply("Привет! Я бот-парсер, готов помочь тебе собрать нужную информацию."
                        " Скажи, что именно ты хочешь найти?")  # отправляет ответ на сообщение


@dp.message(Command('help'))  # декоратор для обработчика команды help
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")


@dp.message()  # декоратор для обработчика прочих сообщений
async def echo_message(message: types.Message):
    await message.answer(message.text)  # отправляет обратно новое сообщение с тем же текстом


if __name__ == '__main__':
    asyncio.run(main())  # начинаем принимать сообщения