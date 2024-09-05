import datetime
import os
import re
from math import ceil
from random import randint

import validators
from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from telebot import TeleBot
from telebot.types import Message

from bot.config import start_text, proxies

load_dotenv()

bot = TeleBot(os.getenv('BOT_TOKEN'))


# service = Service(executable_path="home/tgbot/chromedriver") linux


# Хендлер на команду /start
@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    bot.send_message(message.chat.id, text=start_text)
    bot.send_message(message.chat.id, text="Пришлите мне ссылку на машину с mobile.de и я выведу расчетную стоимость!")


# Хендлер для парсинга
@bot.message_handler(func=lambda message: validators.url(message.text) and 'mobile.de' in message.text)
def parse_handler(message: Message):
    try:
        id = ""

        id_strings = re.findall(r'[?&]id=\d+&', message.text)
        html_strings = re.findall(r'/\d+\.html', message.text)

        if id_strings:
            id = id_strings[0][4:]
            id = id[:-1]

        if html_strings:
            id = html_strings[0][1:]
            id = id[:-5]

        if not id:
            raise Exception

        url = f'https://suchen.mobile.de/fahrzeuge/details.html?id={id}'

    except Exception as e:
        bot.reply_to(message, "Что-то не так с этой ссылкой")
        print(e)
        return None

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--blink-settings=imagesEnabled=False')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.page_load_strategy = 'none'
    # options.add_argument('--headless')

    prefs = {
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.plugins": 2,
        # "profile.managed_default_content_settings.stylesheet": 2,
        # "profile.managed_default_content_settings.javascript": 2,
    }
    options.add_experimental_option("prefs", prefs)

    # options.add_argument("--no-sandbox") linux

    while True:

        userAgent = UserAgent()
        options.add_argument(f'user-agent={userAgent.random}')

        plugin = f'proxies/proxy_plugin_{randint(1, len(proxies))}.zip'
        options.add_extension(plugin)

        # driver = webdriver.Chrome(service=service, options=options) linux
        driver = webdriver.Chrome(options=options)

        try:
            print(f'GET {datetime.datetime.now().strftime("%d.%m %H:%M:%S")}')

            bot.send_chat_action(message.chat.id, 'typing')

            driver.get(url=url)
            driver.implicitly_wait(5)

            bot.send_chat_action(message.chat.id, 'typing')

            try:
                car_price = driver.find_element(by=By.CSS_SELECTOR, value='span.Q7YSy.ZD2EM').text.split(" ")[0]
            except:
                print('No Netto price')
                car_price = driver.find_element(by=By.CLASS_NAME, value='zgAoK.dNpqi').text.split(" ")[0]

            car_price = ("{:,}".format(ceil(int(car_price.replace(".", "")) * 1.58)).
                         replace(',', '.'))

            bot.send_chat_action(message.chat.id, 'typing')

            if "suchen" in driver.current_url:
                value = "h2.dNpqi"
            else:
                value = 'h1.fpviJ.U9mat[data-testid="vip-ad-title"]'

            car_name = driver.find_element(by=By.CSS_SELECTOR, value=value).text

            print(f"{car_name} - €{car_price}\n")

            bot.send_chat_action(message.chat.id, 'typing')

            bot.reply_to(message, f"{car_name} - €{car_price}")

            driver.quit()
            break

        except Exception as e:
            bot.reply_to(message, "Что-то не так с этой ссылкой или сервис блокирует парсер.\n"
                                  "Перепроверьте ссылку и повторите запрос через некоторое время!")
            print(e)
            break


# Хендлер для остальных сообщений
@bot.message_handler(func=lambda message: not (validators.url(message.text) and 'mobile.de' in message.text))
def else_handler(message: Message):
    bot.reply_to(message, "Это не ссылка на машину с mobile.de!")


if __name__ == "__main__":
    bot.infinity_polling()
