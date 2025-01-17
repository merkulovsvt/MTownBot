import os
import zipfile

from dotenv import load_dotenv

load_dotenv()


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


proxies = os.getenv('PROXIES').split(',')
for i in range(len(proxies)):
    make_plugin_zip(proxy=proxies[i], id=i + 1)
