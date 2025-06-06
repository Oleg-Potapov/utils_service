import requests
from src.api.config import API_TOKEN_TB

API_TOKEN = API_TOKEN_TB


headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetOrderBook"

payload = {
    "figi": "BBG0013HGFT4",  # FIGI USD/RUB с лотностью 1000
    "depth": 1  # глубина стакана (1 — чтобы получить лучший bid и ask)
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

if response.status_code == 200 and "payload" in data:
    bids = data["payload"].get("bids", [])
    asks = data["payload"].get("asks", [])

    best_bid = bids[0]["price"] if bids else None
    best_ask = asks[0]["price"] if asks else None

    def price_to_float(price):
        return price["units"] + price["nano"] / 1e9

    if best_bid:
        best_bid_price = price_to_float(best_bid)
    else:
        best_bid_price = None

    if best_ask:
        best_ask_price = price_to_float(best_ask)
    else:
        best_ask_price = None

    print(f"Лучший Bid (покупка) USD/RUB: {best_bid_price}")
    print(f"Лучший Ask (продажа) USD/RUB: {best_ask_price}")
else:
    print(f"Ошибка запроса: {response.status_code} {response.text}")
