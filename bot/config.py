import os
import zipfile

from dotenv import load_dotenv

load_dotenv()

start_text = '''
*Стоимость расчета через бот носит справочный характер.


В стоимость включен следующий состав услуг:

- Проверка автомобиля перед покупкой в Европе
- Перевод денег
- Оплата автомобиля
- Оформление экспортных документов
- Возврат немецкого НДС (вы покупаете автомобиль сразу по цене НЕТТО, вам не нужно ждать пока вернут немецкий НДС)
- Доставка автомобиля автовозом
- Страхование автомобиля на время перевозки
- Оплата таможенной пошлины
- Финальная проверка авто после доставки
- Предпродажная подготовка перед выдачей автомобиля


Оформление СБКТС и ЭПТС, списание утильсбора - являются отдельной услугой и не включены в стоимость расчета.


Осуществить заказ и узнать об автомобиле подробнее : @i1kuch'''


def make_plugin_zip(id: int):
    manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxies",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

    background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxies.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (os.getenv('PROXY_HOST'), os.getenv('PROXY_PORT'), os.getenv('PROXY_USER'),
       os.getenv('PROXY_PASS'))

    plugin_file = f'proxies/proxy_plugin_{id}.zip'

    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr('manifest.json', manifest_json)
        zp.writestr('background.js', background_js)


for i in range(1, 2):
    make_plugin_zip(i)
