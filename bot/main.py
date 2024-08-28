import logging
import os
import re
import time
from random import randint

import validators
from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from telebot import TeleBot
from telebot.types import Message

load_dotenv()

bot = TeleBot(os.getenv('BOT_TOKEN'))
logging.basicConfig(level=logging.INFO)


# Хендлер на команду /start
@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    bot.send_message(message.chat.id,
                     "Это бот-парсер для MTown!\n"
                     "Пришлите мне ссылку на машину с mobile.de и я выведу нужные данные!")


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

        # if "suchen" in message.text:
        #     data = re.findall(r'[?&]id=\d+&', message.text)[0][4:]
        #     id = data[:-1]
        #
        # else:
        #     data = re.findall(r'/\d+\.html', message.text)[0][1:]
        #     id = data[:-5]

        url = f'https://suchen.mobile.de/fahrzeuge/details.html?id={id}'
        print(url)

    except Exception as e:
        bot.reply_to(message, "Что-то не так с этой ссылкой")
        print(e)
        return None

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless')

    while True:

        userAgent = UserAgent()
        options.add_argument(f'user-agent={userAgent.random}')

        plugin = f'bot/proxies/proxy_plugin_{randint(1, 5)}.zip'
        options.add_extension(plugin)

        driver = webdriver.Chrome(options=options)

        try:
            print('GET')

            bot.send_chat_action(message.chat.id, 'typing')

            driver.get(url=url)
            time.sleep(3)

            bot.send_chat_action(message.chat.id, 'typing')

            car_price = WebDriverWait(driver=driver, timeout=2).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, 'dNpqi'))
            )
            parts = car_price.text[:-2].split('.')
            result = "{:.2f}".format(round(int(parts[0] + parts[1]) * 1.58, 2))

            bot.send_chat_action(message.chat.id, 'typing')

            if "suchen" in driver.current_url:
                car_name = WebDriverWait(driver=driver, timeout=1).until(
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, "h2.dNpqi"))
                )

            else:
                car_name = WebDriverWait(driver=driver, timeout=1).until(
                    expected_conditions.presence_of_element_located(
                        (By.CSS_SELECTOR, 'h1.fpviJ.U9mat[data-testid="vip-ad-title"]'))
                )

            bot.reply_to(message, f"{car_name.text} - €{result}")

            driver.quit()
            break

        except Exception as e:
            bot.reply_to(message, "Что-то не так с этой ссылкой или сервис блокирует парсер.\n"
                                  "Проверьте ссылку и повторите запрос через некоторое время!")
            print(e)
            break


# Хендлер для остальных сообщений
@bot.message_handler(func=lambda message: not (validators.url(message.text) and 'mobile.de' in message.text))
def else_handler(message: Message):
    bot.reply_to(message, "Это не ссылка на машину с mobile.de!")


if __name__ == "__main__":
    bot.infinity_polling()
