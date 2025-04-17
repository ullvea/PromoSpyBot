import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from datetime import datetime


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение <{update.message.text}>')


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def time_command(update, context):
    """Отправляет сообщение когда получена команда /time"""
    now = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(now)


async def data_command(update, context):
    """Отправляет сообщение когда получена команда /data"""
    now = datetime.now().strftime("%Y:%m:%d").replace(':', '-')
    await update.message.reply_text(now)


def main():
    application = Application.builder().token('7925593712:AAEh8X0Z3twKdGJJJ4bz1mDxMQ1nAyEKCZM').build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("data", data_command))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()