from abc import ABC, abstractmethod
from fastapi import HTTPException
from src.database.models import Rates
from src.repositories.currency_rates_repository import RatesRepository
from src.services.currency_providers.bitcoin import get_bitcoin_price
from src.services.currency_providers.cbr import get_cb


class AbstractCurrencyRatesService(ABC):
    @abstractmethod
    async def get_update(self):
        pass

    @abstractmethod
    async def get_data(self):
        pass


class CurrencyRatesService(AbstractCurrencyRatesService):
    def __init__(self, repository: RatesRepository):
        self.repository = repository

    async def get_data(self) -> Rates:
        try:
            result = await self.repository.get_rates()
            if result is None:
                raise HTTPException(status_code=404, detail="no data in table")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_update(self) -> Rates:
        try:
            get_bitcoin = await get_bitcoin_price()
            get_rates_cb = await get_cb()

            usd = get_rates_cb['usd']
            eur = get_rates_cb['eur']
            eur_usd = eur/usd
            bitcoin = get_bitcoin['bitcoin']

            table = await self.repository.get_rates()
            if table is None:
                rates = await self.repository.save_rates(usd, eur, eur_usd, bitcoin)
                return rates
            else:
                rates = await self.repository.update_rates(usd, eur, eur_usd, bitcoin)
                return rates
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
