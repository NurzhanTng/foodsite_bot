import json
from aiogram import Bot, Router, F
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.reply import get_usernames_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States
from .step1 import main_logic as step1_main_logic

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    context = await state.get_data()
    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message,
                                    f'Введите ваше имя:\n'
                                    f'_Либо используйте текущее имя указанной вами ранее_',
                                    reply_markup=get_usernames_reply_keyboard(
                                        context.get('order'),
                                        context.get('user')))
    await state.set_state(States.ORDER_NAME)


@router.message(States.ORDER_IS_DELIVERY, F.text == '🛵 Доставить')
async def order_callback_query(message: Message, chat_handler: ChatHistoryHandler, state: FSMContext):
    await state.update_data(is_delivery=True)
    await main_logic(message, state, chat_handler)


@router.message(States.ORDER_IS_DELIVERY, F.text == '🚶🏼 Самовывоз')
async def order_callback_query(message: Message, chat_handler: ChatHistoryHandler, state: FSMContext):
    await state.update_data(is_delivery=False)
    await main_logic(message, state, chat_handler)


@router.message(States.ORDER_IS_DELIVERY, F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=message.web_app_data.data)
    await step1_main_logic(message, state, chat_handler)


@router.message(States.ORDER_IS_DELIVERY, F.text == '❌ Отмена')
async def cancel(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.clear()
    await get_start(message, chat_handler, rest, state, None)


@router.message(States.ORDER_IS_DELIVERY, lambda message: True)
async def handle_all_messages(message: Message):
    print('Заглушка [States.ORDER_IS_DELIVERY]')
