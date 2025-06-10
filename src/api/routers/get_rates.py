from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.rates_schemas import RatesResponse
from src.database.session import get_async_session
from src.repositories.currency_rates_repository import RatesRepository
from src.services.currency_rates_service import CurrencyRatesService

router = APIRouter(
    tags=["exchange_rates"]
)


@router.get("/get_rates", response_model=RatesResponse)
async def get_rates_data(db: AsyncSession = Depends(get_async_session)):
    result = await CurrencyRatesService(RatesRepository(db)).get_data()
    return result
