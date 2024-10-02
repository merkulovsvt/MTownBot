from random import randint

from fake_useragent import UserAgent
from selenium import webdriver

from bot.utils.proxy_config import proxies

userAgent = UserAgent()


def get_parser_options():
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
