from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.get_order_text import get_order_text
from core.utils.states import States
from core.keyboards.reply import get_kaspi_phone_reply_keyboard
from .step6 import main_logic as step6_main_logic

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler,
                     pay_bonus: bool | None = None):
    context = await state.get_data()
    if pay_bonus is not None:
        await state.update_data(pay_bonus=pay_bonus)

    order_text = await get_order_text(state)
    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message,
                                    order_text,
                                    reply_markup=get_kaspi_phone_reply_keyboard(
                                        context.get('order'),
                                        context.get('user')))
    await state.set_state(States.ORDER_ACCEPT)


@router.message(States.ORDER_PAY_BONUS, F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=message.web_app_data.data)
    await step6_main_logic(message, state, chat_handler)


@router.message(States.ORDER_PAY_BONUS, F.text == '❌ Отмена')
async def cancel(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.clear()
    await get_start(message, chat_handler, rest, state, None)


@router.message(States.ORDER_PAY_BONUS, F.text == '❌ Нет')
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await main_logic(message, state, chat_handler, False)


@router.message(States.ORDER_PAY_BONUS, F.text == '✔ Да')
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await main_logic(message, state, chat_handler, True)


@router.message(States.ORDER_PAY_BONUS, lambda message: True)
async def handle_all_messages(message: Message):
    print('Заглушка [States.ORDER_EXACT_GEO]')
