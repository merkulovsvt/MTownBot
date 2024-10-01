import datetime
from random import randint

import validators
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from telebot import TeleBot
from telebot.types import Message

from bot.keyboards.user import car_book_request
from bot.utils.parser_config import get_parser_options
from bot.utils.proxy_config import proxies
from bot.utils.scripts import get_error_or_parse_url, get_final_price


def register_parser_handlers(bot: TeleBot):
    userAgent = UserAgent()

    # Хендлер для парсинга
    @bot.message_handler(func=lambda message: validators.url(message.text) and 'mobile.de' in message.text)
    def web_parsing_handler(message: Message):
        print(1, datetime.datetime.now())

        try:
            url = get_error_or_parse_url(message_text=message.text)
            if not url:
                raise Exception("Invalid URL")
        except Exception as e:
            bot.reply_to(message, "Что-то не так с этой ссылкой")
            print(e)
            return None

        options = get_parser_options()
        options.add_argument(f'user-agent={userAgent.random}')
        options.add_extension(f'bot/utils/proxies/proxy_plugin_{randint(1, len(proxies))}.zip')

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(url=url)
            print(2, datetime.datetime.now())
            bot.send_chat_action(chat_id=message.chat.id,
                                 action='typing')

            car_name = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.dNpqi"))
            ).text
            print(3, datetime.datetime.now())

            try:
                car_price = driver.find_element(by=By.CSS_SELECTOR,
                                                value='span.Q7YSy.ZD2EM').text.split(" ")[0]
            except Exception as e:
                print(e)
                car_price = driver.find_element(by=By.CLASS_NAME,
                                                value='zgAoK.dNpqi').text.split(" ")[0]

            final_price = get_final_price(car_price=car_price)

            text, reply_markup = car_book_request(car_name=car_name,
                                                  car_price=final_price)

            bot.send_message(chat_id=message.chat.id,
                             text=text,
                             reply_markup=reply_markup,
                             parse_mode="HTML")
            print(4, datetime.datetime.now())
            print(f"{car_name} - €{final_price}\n")

        except Exception as e:
            bot.reply_to(message, "Ошибка! Перепроверьте ссылку!")
            print(e)
        finally:
            driver.quit()
