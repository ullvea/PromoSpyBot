import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from datetime import datetime

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def time_command(update, context):
    now = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(now)


async def data_command(update, context):
    now = datetime.now().strftime("%Y:%m:%d").replace(':', '.')
    await update.message.reply_text(now)


def main():
    application = Application.builder().token('7925593712:AAEh8X0Z3twKdGJJJ4bz1mDxMQ1nAyEKCZM').build()
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("data", data_command))
    application.run_polling()


if __name__ == '__main__':
    main()
