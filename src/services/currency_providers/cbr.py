from zeep import Client
from datetime import datetime
from fastapi import HTTPException


wsdl = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
client = Client(wsdl=wsdl)


async def get_cb() -> dict:
    try:
        today = datetime.now().strftime('%Y-%m-%d')  # цб обновляет курс один раз в день
        response = client.service.GetCursOnDate(today)
        rates = {}
        for valute in response['ValuteData']['ValuteCursOnDate']:
            code = valute['VchCode']
            if code in ['USD', 'EUR']:
                nominal = valute['Vnom']
                curs = valute['Vcurs']
                # Курс за 1 единицу валюты
                rates[code.lower()] = curs / nominal
        return rates
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
