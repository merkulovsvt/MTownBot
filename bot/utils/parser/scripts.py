import re
from math import ceil
from random import randint
from typing import Union

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bot.utils.proxy.scripts import proxies
from main import logger


def get_parser_options():
    userAgent = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--blink-settings=imagesEnabled=False')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--disable-popup-blocking')
    # options.add_argument('--start-maximized')
    # options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    options.page_load_strategy = 'none'

    options.add_argument(f'user-agent={userAgent.random}')
    options.add_extension(f'bot/utils/proxies/proxy_plugin_{randint(1, len(proxies))}.zip')

    prefs = {
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.stylesheet": 2,
        # "profile.managed_default_content_settings.javascript": 2,
    }
    options.add_experimental_option("prefs", prefs)
    return options


def get_parse_url(message_text: str) -> str:
    id_strings = re.findall(pattern=r'[?&]id=\d+&',
                            string=message_text)

    html_strings = re.findall(pattern=r'/\d+\.html',
                              string=message_text)
    id = ""
    if id_strings:
        id = id_strings[0][4:]
        id = id[:-1]
    elif html_strings:
        id = html_strings[0][1:]
        id = id[:-5]

    if id:
        return f'https://suchen.mobile.de/fahrzeuge/details.html?id={id}'
    else:
        return message_text


def get_data(driver: webdriver.Chrome, url: str) -> Union[dict, None]:
    try:
        driver.get(url)
        car_name = WebDriverWait(driver=driver, timeout=15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h2.dNpqi"))
        ).text

        try:
            price_type = 'Netto'
            car_price = driver.find_element(by=By.CSS_SELECTOR,
                                            value='span.Q7YSy.ZD2EM').text.split(" ")[0]
        except Exception as Error:
            price_type = 'Brutto'
            car_price = driver.find_element(by=By.CLASS_NAME,
                                            value='zgAoK.dNpqi').text.split(" ")[0]

        return {'car_name': car_name,
                'car_price': car_price,
                'price_type': price_type,
                'url': url}

    except Exception as Error:
        logger.error(Error)
        return None
    finally:
        driver.close()


def get_final_price(car_price: str) -> (str, str):
    bel_price = ("{:,}".format(ceil(int(car_price.replace(".", "")) * 1.58)).
                 replace(',', '.'))

    rus_price = ("{:,}".format(ceil(int(car_price.replace(".", "")) * 1.68)).
                 replace(',', '.'))

    return bel_price, rus_price
