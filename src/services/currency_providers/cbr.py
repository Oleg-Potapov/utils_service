import requests
import xml.etree.ElementTree as ET
from src.api.config import CBR_URL


def get_cbr_usd_eur_rates() -> dict:

    params = {}

    response = requests.get(CBR_URL, params=params)
    response.encoding = 'windows-1251'  # важная кодировка для ЦБ РФ

    root = ET.fromstring(response.text)

    rates = {}
    for valute in root.findall('Valute'):
        char_code = valute.find('CharCode').text
        if char_code in ('USD', 'EUR'):
            nominal = int(valute.find('Nominal').text)
            value_str = valute.find('Value').text
            value = float(value_str.replace(',', '.'))
            rates[char_code.lower()] = value / nominal

    if 'usd' not in rates or 'eur' not in rates:
        raise ValueError("Не удалось получить курсы USD и EUR из ответа ЦБ РФ")

    return rates
