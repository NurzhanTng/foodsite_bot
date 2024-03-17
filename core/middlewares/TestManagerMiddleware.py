from typing import Any, Awaitable, Callable, Coroutine, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject

from core.utils.OrderTest import OrderTest


class TestManagerMiddleware(BaseMiddleware):
    def __init__(self):
        self.order_test = OrderTest()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Coroutine[Any, Any, Any]:
        data['order_test'] = self.order_test
        return await handler(event, data)
