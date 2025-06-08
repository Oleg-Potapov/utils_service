from src.database.session import get_async_session
from src.services.currency_rates_service import CurrencyRatesService
from src.repositories.currency_rates_repository import RatesRepository


async def update_cb_rates_task():
    async with get_async_session() as db:
        service = CurrencyRatesService(RatesRepository(db))
        await service.get_update_cb()


async def update_tb_bitc_rates_task():
    async with get_async_session() as db:
        service = CurrencyRatesService(RatesRepository(db))
        await service.get_update_rates_tb_and_bitcoin()
