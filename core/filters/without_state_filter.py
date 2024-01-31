from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from aiogram.types import Message


class WithoutStateFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        state_name = await state.get_state()
        if state_name is None:
            return True
        return False
