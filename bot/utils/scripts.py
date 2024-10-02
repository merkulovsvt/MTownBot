import re
from math import ceil
from typing import Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from main import logger


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
                'price_type': price_type}

    except Exception as Error:
        logger.error(Error)
        return None
    finally:
        driver.close()


def get_final_price(car_price: str) -> str:
    return ("{:,}".format(ceil(int(car_price.replace(".", "")) * 1.58)).
            replace(',', '.'))
