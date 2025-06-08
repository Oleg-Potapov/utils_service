from abc import ABC, abstractmethod
from fastapi import HTTPException
from src.database.models import Rates
from src.repositories.currency_rates_repository import RatesRepository
from src.services.currency_providers.result_data import result_rates


class AbstractCurrencyRatesService(ABC):
    @abstractmethod
    async def get_update(self):
        pass

    @abstractmethod
    async def get_data(self):
        pass

    @abstractmethod
    async def get_update_cb(self):
        pass

    @abstractmethod
    async def get_update_rates_tb_and_bitcoin(self) -> Rates:
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
            rates = await result_rates()

            table = await self.repository.get_rates()
            if table is None:
                rates = await self.repository.save_rates(
                    rates["usd"], rates["eur"], rates["eur_usd"], rates["bitcoin"],
                    rates["usd_buy_tb"], rates["usd_sell_tb"], rates["eur_buy_tb"], rates["eur_sell_tb"]
                )
                return rates
            else:
                await self.repository.update_rates_cb(rates["usd"], rates["eur"], rates["eur_usd"])
                await self.repository.update_rates_tb_and_bitcoin(
                    rates["bitcoin"], rates["usd_buy_tb"], rates["usd_sell_tb"],
                    rates["eur_buy_tb"], rates["eur_sell_tb"]
                )
                return await self.repository.get_rates()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_update_cb(self) -> Rates:
        try:
            rates = await result_rates()
            await self.repository.update_rates_cb(rates["usd"], rates["eur"], rates["eur_usd"])
            return await self.repository.get_rates()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_update_rates_tb_and_bitcoin(self) -> Rates:
        try:
            rates = await result_rates()
            await self.repository.update_rates_tb_and_bitcoin(
                rates["bitcoin"], rates["usd_buy_tb"], rates["usd_sell_tb"],
                rates["eur_buy_tb"], rates["eur_sell_tb"]
            )
            return await self.repository.get_rates()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
