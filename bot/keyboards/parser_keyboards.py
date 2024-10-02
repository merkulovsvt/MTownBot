from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.texts import parser_text


def car_book_request(car_name: str, car_price: str) -> (str, InlineKeyboardBuilder):
    builder = InlineKeyboardBuilder()
    builder.button(text="✉️ Отправить заявку", url="https://www.amocrm.ru/")

    text = parser_text.format(car_name=car_name,
                              car_price=car_price,
                              bel_price=car_price,
                              rus_price=car_price)

    return text, builder.as_markup()
