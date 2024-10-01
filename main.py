import os

from dotenv import load_dotenv
from telebot import TeleBot

from bot.handlers.parser import register_parser_handlers
from bot.handlers.user import register_user_handlers

load_dotenv()

if __name__ == "__main__":
    bot = TeleBot(os.getenv('BOT_TOKEN'))

    register_user_handlers(bot=bot)
    register_parser_handlers(bot=bot)

    bot.infinity_polling(skip_pending=True)
