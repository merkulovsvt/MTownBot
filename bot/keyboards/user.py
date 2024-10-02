from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.texts import parser_text


def car_book_request(car_name: str, car_price: str) -> (str, InlineKeyboardMarkup):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="✉️ Отправить заявку", url="https://www.amocrm.ru/"))

    text = parser_text.format(car_name=car_name,
                              car_price=car_price,
                              bel_price=car_price,
                              rus_price=car_price)

    return text, markup
