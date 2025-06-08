from fastapi import APIRouter
from src.api.scheduler.ini_scheduler import schedule_jobs, scheduler
from src.database.session import get_async_session
from src.repositories.currency_rates_repository import RatesRepository
from src.services.currency_rates_service import CurrencyRatesService
# from src.api.http_client import startup_client, shutdown_client

router = APIRouter()


@router.on_event("startup")
async def startup_event():
    try:
        async with get_async_session() as db:
            await CurrencyRatesService(RatesRepository(db)).get_update()
        schedule_jobs()
        scheduler.start()

    except Exception as e:
        print(f"Ошибка при создании httpx.AsyncClient: {e}")


@router.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
