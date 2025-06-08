import httpx
from fastapi import HTTPException
from src.api.config import RATES_URL
from src.services.currency_providers.bitcoin import get_bitcoin_price
from src.services.currency_providers.cbr import get_cbr_usd_eur_rates
from src.services.currency_providers.t_bank import parse_rates


async def result_rates() -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(RATES_URL)

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Не удалось получить данные с источника")

        rates_tb = parse_rates(response.text)
        if not rates_tb:
            raise HTTPException(status_code=404, detail="Курсы валют не найдены в ответе")

        get_bitcoin = await get_bitcoin_price()
        get_rates_cb = get_cbr_usd_eur_rates()
        print(get_rates_cb)

        usd = get_rates_cb['usd']
        eur = get_rates_cb['eur']
        eur_usd = eur / usd
        eur_usd = round(eur_usd, 4)
        bitcoin = get_bitcoin['bitcoin']
        usd_buy_tb = rates_tb["usd_buy"]
        usd_sell_tb = rates_tb["usd_sell"]
        eur_buy_tb = rates_tb["eur_buy"]
        eur_sell_tb = rates_tb["eur_sell"]
        result_dict = {
            "usd": usd,
            "eur": eur,
            "eur_usd": eur_usd,
            "bitcoin": bitcoin,
            "usd_buy_tb": usd_buy_tb,
            "usd_sell_tb": usd_sell_tb,
            "eur_buy_tb": eur_buy_tb,
            "eur_sell_tb": eur_sell_tb
        }
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
