from typing import Union

from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from aiogram.types import Message


class UserRoleFilter(BaseFilter):
    def __init__(self, user_type: Union[str, list[str]]):
        self.user_type = user_type

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        context = await state.get_data()
        user = context.get('user')

        if user is None:
            return False
        if isinstance(self.user_type, str):
            return user['role'] == self.user_type
        else:
            return user['role'] in self.user_type
