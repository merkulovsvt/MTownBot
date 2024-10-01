from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def car_book_request(car_name: str, car_price: str) -> (str, InlineKeyboardMarkup):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="✉️ Отправить заявку", url="https://www.amocrm.ru/"))

    text = f'''
Привет!
<b>{car_name}</b> будет стоить в Германии <b>{car_price}</b> евро
Доставка - <b>{car_price}</b> евро

Таможня:
Если на белоруссию - <b>{car_price}</b> руб 
На россию - <b>{car_price}</b> руб 

Это предварительный расчет, лучше бы посчитать детально.
    '''

    return text, markup
