from abc import ABC, abstractmethod
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Rates


class AbstractRatesRepository(ABC):
    @abstractmethod
    async def get_rates(self):
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")

    @abstractmethod
    async def save_rates(
            self, usd: float, eur: float, eur_usd: float, bitcoin: float,
            usd_buy_tb: float, usd_sell_tb: float, eur_buy_tb: float, eur_sell_tb: float
    ):
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")

    @abstractmethod
    async def update_rates_cb(self, usd: float, eur: float, eur_usd: float):
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")

    @abstractmethod
    async def update_rates_tb_and_bitcoin(
            self, bitcoin: float, usd_buy_tb: float, usd_sell_tb: float, eur_buy_tb: float, eur_sell_tb: float
    ):
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")


class RatesRepository(AbstractRatesRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rates(self) -> Rates:
        try:
            result = await self.session.execute(select(Rates))
            rates = result.scalars().first()
            return rates
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def save_rates(
            self, usd: float, eur: float, eur_usd: float, bitcoin: float,
            usd_buy_tb: float, usd_sell_tb: float, eur_buy_tb: float, eur_sell_tb: float
    ) -> Rates:
        try:
            new_rates = Rates(
                usd=usd, eur=eur, eur_usd=eur_usd, bitcoin=bitcoin,usd_buy_tb=usd_buy_tb,
                usd_sell_tb=usd_sell_tb, eur_buy_tb=eur_buy_tb, eur_sell_tb=eur_sell_tb
            )
            self.session.add(new_rates)
            await self.session.commit()
            await self.session.refresh(new_rates)
            return new_rates
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

    async def update_rates_cb(self, usd: float, eur: float, eur_usd: float) -> Rates:
        try:
            await self.session.execute(update(Rates).values(
                usd=usd, eur=eur, eur_usd=eur_usd,
                update_cb=datetime.now(timezone.utc))
            )
            await self.session.commit()
            result = await self.session.execute(select(Rates))
            rates = result.scalars().first()
            return rates
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update_rates_tb_and_bitcoin(
            self, bitcoin: float, usd_buy_tb: float, usd_sell_tb: float, eur_buy_tb: float, eur_sell_tb: float
    ):
        try:
            await self.session.execute(update(Rates).values(
                bitcoin=bitcoin, usd_buy_tb=usd_buy_tb, usd_sell_tb=usd_sell_tb,
                eur_buy_tb=eur_buy_tb, eur_sell_tb=eur_sell_tb, update_tb_and_bitcoin=datetime.now(timezone.utc))
            )
            await self.session.commit()
            result = await self.session.execute(select(Rates))
            rates = result.scalars().first()
            return rates
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")




