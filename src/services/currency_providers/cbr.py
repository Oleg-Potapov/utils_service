from zeep import Client
from datetime import datetime
from fastapi import HTTPException
from src.api.config import WSDL

# client = Client(wsdl=WSDL)


# async def get_cb() -> dict:
#     try:
#         today = datetime.now().strftime('%Y-%m-%d')  # цб обновляет курс один раз в день
#         response = client.service.GetCursOnDate(today)
#         print(response)
#         rates = {}
#         for valute in response['ValuteData']['ValuteCursOnDate']:
#             code = valute['VchCode']
#             if code in ['USD', 'EUR']:
#                 nominal = valute['Vnom']
#                 curs = valute['Vcurs']
#                 # Курс за 1 единицу валюты
#                 rates[code.lower()] = curs / nominal
#         return rates
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


import requests
import xml.etree.ElementTree as ET


def get_cbr_usd_eur_rates() -> dict:

    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    params = {}

    response = requests.get(url, params=params)
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
