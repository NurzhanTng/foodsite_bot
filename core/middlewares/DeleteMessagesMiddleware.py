from typing import Any, Awaitable, Callable, Coroutine, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject
import json

from core.utils.ChatHistoryHandler import ChatHistoryHandler


class DeleteMessagesMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.chat_handler = ChatHistoryHandler(bot)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Coroutine[Any, Any, Any]:
        if isinstance(event, Message):
            self.chat_handler.add_new_message(event.chat.id, event.message_id)
        data['chat_handler'] = self.chat_handler
        return await handler(event, data)
