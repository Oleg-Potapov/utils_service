import requests
from fastapi import HTTPException


async def get_bitcoin_price() -> dict:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return {"bitcoin": data['bitcoin']['usd']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
