import json

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.get_order_text import get_order_text
from core.utils.is_valid_phone_number import is_valid_phone_number
from core.utils.states import States
from .step7 import main_logic as step7_main_logic

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, rest: RestHandler,
                     phone: str):
    if not is_valid_phone_number(phone):
        await chat_handler.delete_messages(message.chat.id)
        await chat_handler.send_message(message,
                                        f'*Введите корректный номер телефона!*\n'
                                        f'Либо воспользуйтесь кнопками\n'
                                        f'Формат:\n_87471231212_\n_+77471231212_\n'
                                        f'Или попробуйте еще раз.')
        return

    context = await state.get_data()
    await state.update_data(kaspi_phone=phone)
    print('Заказ сохранен')
    print(json.dumps(context, indent=2))
    # result = await rest.post(url='/order', data=context['order'])
    #
    # if result.status_code != 200:
    #     await chat_handler.send_message(message,
    #                                     'Произошла ошибка во время отправки заказа. Попробуйте сделать заказ позже\n'
    #                                     'Просим извинения за неудобства')
    # else:
    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message, 'Заказ сохранен')
    # Надо удалить и другие данные


@router.message(States.ORDER_ACCEPT, F.contact)
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, rest: RestHandler):
    await main_logic(message, state, chat_handler, rest, phone=message.contact.phone_number)


@router.message(States.ORDER_ACCEPT, F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=message.web_app_data.data)
    await step7_main_logic(message, state, chat_handler)


@router.message(States.ORDER_ACCEPT, F.text == '❌ Отмена')
async def cancel(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.clear()
    await get_start(message, chat_handler, rest, state, None)


@router.message(States.ORDER_ACCEPT, lambda message: True)
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, rest: RestHandler):
    await main_logic(message, state, chat_handler, rest, message.text)


@router.message(States.ORDER_ACCEPT, lambda message: True)
async def handle_all_messages(message: Message):
    print('Заглушка [States.ORDER_ACCEPT]')
