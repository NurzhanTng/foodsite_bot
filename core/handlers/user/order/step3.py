from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.reply import get_phones_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States
from .step2 import main_logic as step2_main_logic

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, name: str | None = None):
    if name is not None:
        await state.update_data(name=name)

    context = await state.get_data()
    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message, f'Отправьте ваш номер телефона или воспользуйтесь кнопками:',
                                    reply_markup=get_phones_reply_keyboard(context.get('order'), context.get('user')))
    await state.set_state(States.ORDER_PHONE)


@router.message(States.ORDER_NAME, F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=message.web_app_data.data)
    await step2_main_logic(message, state, chat_handler)


@router.message(States.ORDER_NAME, F.text == '❌ Отмена')
async def cancel(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.clear()
    await get_start(message, chat_handler, rest, state, None)


@router.message(States.ORDER_NAME, lambda message: True)
async def handle_all_messages(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await main_logic(message, state, chat_handler, message.text)


@router.message(States.ORDER_NAME, lambda message: True)
async def handle_all_messages(message: Message):
    print('Заглушка [States.ORDER_NAME]')
