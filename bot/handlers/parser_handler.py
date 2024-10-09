import asyncio
import datetime

from aiogram import Router, types, F
from aiogram.enums import ChatAction, ParseMode
from selenium import webdriver

from bot.keyboards.lead_keyboards import inline_car_details
from bot.utils.bot.filters import URL
from bot.utils.database.requests import create_lead, update_lead
from bot.utils.parser.scripts import get_final_price, get_parse_url, get_data
from bot.utils.parser.scripts import get_parser_options
from main import logger

router = Router()


# Хендлер для парсинга
@router.message(F.text, URL())
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
            url = data.get("url")
        else:
            raise Exception('Parse error')

        bel_price, rus_price = get_final_price(car_price=car_price)

        lead_id = await create_lead(chat_id=message.chat.id,
                                    username=message.chat.username,
                                    car_name=car_name,
                                    url=url)

        text, reply_markup = inline_car_details(car_name=car_name,
                                                car_price=car_price,
                                                bel_price=bel_price,
                                                rus_price=rus_price,
                                                price_type=price_type,
                                                lead_id=lead_id)

        lead_message = await message.answer(text=text,
                                            reply_markup=reply_markup,
                                            parse_mode=ParseMode.MARKDOWN)

        await update_lead(lead_id=lead_id,
                          message_id=lead_message.message_id)

        print(datetime.datetime.now() - time)
    except Exception as Error:
        await message.reply(text="Ошибка! Перепроверьте ссылку!")
        logger.error(Error)
