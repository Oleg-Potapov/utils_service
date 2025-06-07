from datetime import datetime
from pydantic import BaseModel


class RatesResponse(BaseModel):
    usb: float
    eur: float
    eur_usd: float
    bitcoin: float
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "usb": 89.12,
                "eur": 96.54,
                "eur_usd": 1.084,
                "bitcoin": 110690.00,
                "created_at": "2025-06-07T09:38:00+00:00"
            }
        }
