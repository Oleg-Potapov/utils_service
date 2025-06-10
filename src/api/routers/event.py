#from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from src.api.scheduler.ini_scheduler import schedule_jobs, scheduler
from src.database.db import async_session_maker
from src.repositories.currency_rates_repository import RatesRepository
from src.services.currency_rates_service import CurrencyRatesService

router = APIRouter()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with async_session_maker() as db:
#         await CurrencyRatesService(RatesRepository(db)).get_update()
#     schedule_jobs()
#     scheduler.start()
#     yield
#     scheduler.shutdown()


@router.on_event("startup")
async def startup_event():
    try:
        async with async_session_maker() as db:
        #async with get_async_session() as db:
            await CurrencyRatesService(RatesRepository(db)).get_update()
        schedule_jobs()
        scheduler.start()

    except Exception as e:
        print(f"Ошибка при создании httpx.AsyncClient: {e}")


@router.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
