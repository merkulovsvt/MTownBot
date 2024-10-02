import re
from math import ceil
from typing import Union


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


def get_final_price(car_price: str):
    return ("{:,}".format(ceil(int(car_price.replace(".", "")) * 1.58)).
            replace(',', '.'))
