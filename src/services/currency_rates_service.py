from abc import ABC, abstractmethod
from fastapi import HTTPException
import requests

from datetime import datetime


class AbstractCurrencyRatesService(ABC):
    @abstractmethod
    async def send_message(self, data: ChatIdMess):
        pass


class CurrencyRatesService(AbstractCurrencyRatesService):
    def __init__(self, repository: ChatRepository):
        self.repository = repository


