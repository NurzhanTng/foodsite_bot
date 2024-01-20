from typing import Any, Awaitable, Callable, Coroutine, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject

from core.utils.RestHandler import RestHandler


class RestMiddleware(BaseMiddleware):
    """
    Example of using:

    >>> from aiogram import types, Dispatcher
    >>> from aiogram.utils import markdown as md

    >>> dp = Dispatcher()

    >>> @dp.message(commands=['get_data_with_params'])
    >>> async def get_data_with_params_handler(message: types.Message, rest: RestHandler):
    >>>     response = await rest.get('/api/data', params={
    >>>         'param1': 'value1',
    >>>         'param2': 'value2'
    >>>     })
    >>>     await message.answer(md.text(f"Received data with parameters: {response}"))

    >>> @dp.message(commands=['update_data'])
    >>> async def update_data_handler(message: types.Message, rest: RestHandler):
    >>>     response = await rest.update('/api/update', data={'key': 'new_value'})
    >>>     await message.answer(md.text(f"Update response: {response}"))

    >>> @dp.message(commands=['delete_data'])
    >>> async def delete_data_handler(message: types.Message, rest: RestHandler):
    >>>     response = await rest.delete('/api/delete')
    >>>     await message.answer(md.text(f"Delete response: {response}"))

    >>> @dp.message(commands=['post_data'])
    >>> async def post_data_handler(message: types.Message, data: dict, rest: RestHandler):
    >>>     response = await rest.post('/api/data', data={'key': 'value'})
    >>>     await message.answer(f"Received data from backend: {response}")
    """

    def __init__(self, bot: Bot):
        self.rest_handler = RestHandler(bot)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Coroutine[Any, Any, Any]:
        data['rest'] = self.rest_handler
        return await handler(event, data)
