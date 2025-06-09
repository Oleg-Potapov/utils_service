import requests
from fastapi import HTTPException
from src.api.config import BITCOIN_URL


async def get_bitcoin_price() -> dict:
    try:
        response = requests.get(BITCOIN_URL)
        data = response.json()
        print(data)
        return {"bitcoin": data['bitcoin']['usd']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
