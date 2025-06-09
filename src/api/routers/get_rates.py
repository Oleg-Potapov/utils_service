from fastapi import APIRouter
from src.api.schemas.rates_schemas import RatesResponse
from src.database.session import get_async_session
from src.repositories.currency_rates_repository import RatesRepository
from src.services.currency_rates_service import CurrencyRatesService

router = APIRouter(
    tags=["exchange_rates"]
)


@router.get("/get_rates", response_model=RatesResponse)
async def get_rates_data():
    async with get_async_session() as db:
        result = await CurrencyRatesService(RatesRepository(db)).get_data()
    return result
