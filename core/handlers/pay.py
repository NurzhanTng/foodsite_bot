from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, PreCheckoutQuery

from core.keyboards.inline import get_main_inline_keyboard, get_manager_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.filters.without_state_filter import WithoutStateFilter

router = Router()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    # data = message.successful_payment
    ...
