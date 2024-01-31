from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.reply import get_bonus_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States
from .step5 import main_logic as step5_main_logic

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, exact_geo: str | None = None):
    context = await state.get_data()
    if exact_geo is not None:
        await state.update_data(exact_geo=exact_geo)
    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message,
                                    f'В данный момент у вас: ${context.get("user")["bonus"]} бонусов!\nПотратить их?',
                                    reply_markup=get_bonus_reply_keyboard(context.get('order')))
    await state.set_state(States.ORDER_PAY_BONUS)


@router.message(States.ORDER_EXACT_GEO, F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=message.web_app_data.data)
    await step5_main_logic(message, state, chat_handler)


@router.message(States.ORDER_EXACT_GEO, F.text == '❌ Отмена')
async def cancel(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.clear()
    await get_start(message, chat_handler, rest, state, None)


@router.message(States.ORDER_EXACT_GEO, F.text)
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    context = await state.get_data()
    await main_logic(message, state, chat_handler, message.text)


@router.message(States.ORDER_EXACT_GEO, lambda message: True)
async def handle_all_messages(message: Message):
    print('Заглушка [States.ORDER_EXACT_GEO]')
