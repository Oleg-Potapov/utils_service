from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, Float
from src.database.db import Base


class Rates(Base):
    __tablename__ = 'rates'

    id = Column(Integer, primary_key=True, index=True)
    usd = Column(Float, nullable=False)
    eur = Column(Float, nullable=False)
    eur_usd = Column(Float, nullable=False)
    bitcoin = Column(Float, nullable=False)
    usd_buy_tb = Column(Float, nullable=False)
    usd_sell_tb = Column(Float, nullable=False)
    eur_buy_tb = Column(Float, nullable=False)
    eur_sell_tb = Column(Float, nullable=False)
    update_cb = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    update_tb_and_bitcoin = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
