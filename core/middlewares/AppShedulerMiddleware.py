from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerMiddleware(BaseMiddleware):
  def __init__(self, scheduler: AsyncIOScheduler) -> None:
    self.scheduler = scheduler

  async def __call__(
    self,
    handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
    event: TelegramObject,
    data: Dict[str, Any]
  ) -> Any:
    data['apscheduler'] = self.scheduler
    return await handler(event, data)