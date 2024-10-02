import asyncio
import datetime

from aiogram import Router, types
from aiogram.enums import ChatAction, ParseMode
from selenium import webdriver

from bot.keyboards.parser_keyboards import car_book_request
from bot.utils.filters import URL
from bot.utils.parser_config import get_parser_options
from bot.utils.scripts import get_final_price, get_parse_url, get_data
from main import logger

router = Router()


# Хендлер для парсинга
@router.message(URL())
async def web_parsing_handler(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    time = datetime.datetime.now()
    driver = webdriver.Chrome(options=get_parser_options())
    try:
        data = await asyncio.to_thread(get_data, driver, get_parse_url(message_text=message.text))
        print(datetime.datetime.now())
        if data:
            car_name = data.get("car_name")
            car_price = data.get("car_price")
            price_type = data.get("price_type")
        else:
            raise Exception('Parse error')

        text, reply_markup = car_book_request(car_name=car_name,
                                              car_price=get_final_price(car_price=car_price))
        await message.answer(text=text,
                             reply_markup=reply_markup,
                             parse_mode=ParseMode.MARKDOWN)
        print(datetime.datetime.now() - time)
    except Exception as Error:
        await message.reply(text="Ошибка! Перепроверьте ссылку!")
        logger.error(Error)
