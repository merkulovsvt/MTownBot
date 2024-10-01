import validators
from telebot import TeleBot
from telebot.types import Message

from bot.utils.proxy_config import start_text


def register_user_handlers(bot: TeleBot):
    # Хендлер на команду /start
    @bot.message_handler(commands=['start'])
    def start_handler(message: Message):
        bot.send_message(chat_id=message.chat.id,
                         text=start_text)

        bot.send_message(chat_id=message.chat.id,
                         text="Пришлите мне ссылку на машину с mobile.de и я выведу расчетную стоимость!")

    # Хендлер для остальных сообщений
    @bot.message_handler(func=lambda message: not (validators.url(message.text) and 'mobile.de' in message.text))
    def else_handler(message: Message):
        bot.reply_to(message, "Это не ссылка на машину с mobile.de!")
