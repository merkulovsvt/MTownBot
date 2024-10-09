from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.callbacks.lead_callbacks import LeadStartUpload, RetrySearch
from bot.utils.bot.texts import parser_text


def inline_car_details(car_name: str, car_price: str, bel_price: str, rus_price: str, price_type: str, lead_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✉️ Отправить заявку", callback_data=LeadStartUpload(lead_id=lead_id))
    builder.button(text="🔄 Повторить поиск", callback_data=RetrySearch(lead_id=lead_id))

    text = parser_text.format(car_name=car_name,
                              car_price=car_price,
                              bel_price=bel_price,
                              rus_price=rus_price,
                              price_type_text="(без НДС)" if price_type == "Netto" else "(включая НДС)")
    builder.adjust(1, repeat=True)

    return text, builder.as_markup()


def inline_lead_canceled():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Заявка отменена", callback_data='inactive')

    return builder.as_markup()


def inline_lead_in_progress():
    builder = InlineKeyboardBuilder()
    builder.button(text="🚀 Заявка в процессе", callback_data='inactive')

    return builder.as_markup()


def inline_lead_uploaded():
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Заявка отправлена", callback_data='inactive')

    return builder.as_markup()


def reply_lead_in_progress():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='📞 Поделиться контактом', request_contact=True))
    builder.add(KeyboardButton(text='❌ Отменить заявку'))
    builder.adjust(1, repeat=True)

    text = "Поделитесь контактом для связи!"
    return text, builder.as_markup(resize_keyboard=True)
