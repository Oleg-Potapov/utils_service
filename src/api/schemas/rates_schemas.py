from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RatesResponse(BaseModel):
    usd: float
    eur: float
    eur_usd: float
    bitcoin: float
    usd_buy_tb: float
    usd_sell_tb: float
    eur_buy_tb: float
    eur_sell_tb: float
    update_cb: datetime
    update_tb_and_bitcoin: datetime

    class Model(BaseModel):
        model_config = ConfigDict(from_attributes=True)

    class Config:
        json_schema_extra = {
            "example": {
                "usb": 89.12,
                "eur": 96.54,
                "eur_usd": 1.084,
                "bitcoin": 110690.00,
                "usd_buy_tb": 88.50,
                "usd_sell_tb": 89.70,
                "eur_buy_tb": 95.80,
                "eur_sell_tb": 97.20,
                "update_cb": "2025-06-07T09:38:00+00:00",
                "update_tb_and_bitcoin": "2025-06-07T11:38:00+00:00"
            }
        }
