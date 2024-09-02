from math import ceil

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_by_class_name(driver: WebDriver, class_name: str, timeout: int) -> WebElement:
    price = WebDriverWait(driver=driver, timeout=timeout).until(
        expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, class_name))
    )
    return price


def get_by_css(driver: WebDriver, name: str, timeout: int) -> WebElement:
    price = WebDriverWait(driver=driver, timeout=timeout).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, name))
    )
    return price


def get_final_price(car_price: str) -> str:
    return "{:,}".format(ceil(int(car_price.replace(".", "")[:-2]) * 1.58)).replace(',', '.')
