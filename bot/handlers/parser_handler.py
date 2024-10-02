import asyncio
import datetime
from random import randint

from aiogram import Router, types
from aiogram.enums import ChatAction, ParseMode
from fake_useragent import UserAgent
from selenium import webdriver

from bot.keyboards.parser_keyboards import car_book_request
from bot.utils.filters import URL
from bot.utils.parser_config import get_parser_options
from bot.utils.proxy_config import proxies
from bot.utils.scripts import get_final_price, get_parse_url, get_data
from main import logger

router = Router()
userAgent = UserAgent()


# Хендлер для парсинга
@router.message(URL())
async def web_parsing_handler(message: types.Message):
    print(datetime.datetime.now())

    url = get_parse_url(message_text=message.text)

    options = get_parser_options()
    options.add_argument(f'user-agent={userAgent.random}')
    options.add_extension(f'bot/utils/proxies/proxy_plugin_{randint(1, len(proxies))}.zip')

    driver = webdriver.Chrome(options=options)
    try:
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

        data = await asyncio.to_thread(get_data, driver, url)

        if data:
            car_name = data.get("car_name")
            car_price = data.get("car_price")
            price_type = data.get("price_type")
        else:
            raise Exception('Parse error')

        final_price = get_final_price(car_price=car_price)
        text, reply_markup = car_book_request(car_name=car_name,
                                              car_price=final_price)

        await message.answer(text=text,
                             reply_markup=reply_markup,
                             parse_mode=ParseMode.MARKDOWN)

        print(f"{car_name} - €{final_price}")
        print(datetime.datetime.now(), '\n')

    except Exception as Error:
        await message.reply(text="Ошибка! Перепроверьте ссылку!")
        logger.error(Error)
