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


def make_plugin_zip(proxy: str, id: int):
    host = proxy.split(':')[0]
    port = proxy.split(':')[1]
    user = proxy.split(':')[2]
    password = proxy.split(':')[3]

    print(host, port, user, password)

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
""" % (host, port, user, password)

    plugin_file = f'bot/utils/proxies/proxy_plugin_{id}.zip'

    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr('manifest.json', manifest_json)
        zp.writestr('background.js', background_js)


proxies = [
    '163.198.109.59:8000:s6phCL:KYPXky',
    '185.76.243.129:8000:PRBZ0f:DyUU5d',
    '168.81.64.20:8000:R981zD:y7PuHE',
]

for i in range(len(proxies)):
    make_plugin_zip(proxy=proxies[i], id=i + 1)
