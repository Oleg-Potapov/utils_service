import requests
import xml.etree.ElementTree as ET
from fastapi import HTTPException


async def get_cb() -> dict:
    try:
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        response = requests.get(url)
        response.encoding = 'windows-1251'  # Кодировка сайта ЦБР

        if response.status_code != 200:
            raise Exception("Ошибка при запросе данных ЦБР")

        root = ET.fromstring(response.text)

        rates = {}

        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code in ['USD', 'EUR']:
                nominal = int(valute.find('Nominal').text)
                value_str = valute.find('Value').text.replace(',', '.')
                value = float(value_str)
                # Курс за 1 единицу валюты
                rate = value / nominal
                rates[char_code.lower()] = rate

        return rates

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
