from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.reply import get_geo_reply_keyboard, get_bonus_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.is_valid_phone_number import is_valid_phone_number
from core.utils.states import States
from .step3 import main_logic as step3_main_logic

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, rest: RestHandler,
                     phone: str | None = None):
    if not is_valid_phone_number(phone):
        await chat_handler.delete_messages(message.chat.id)
        await chat_handler.send_message(message,
                                        f'*Введите корректный номер телефона!*\n'
                                        f'Либо воспользуйтесь кнопками\n'
                                        f'Формат:\n_87471231212_\n_+77471231212_\n'
                                        f'Или попробуйте еще раз.')
        return

    context = await state.get_data()
    if phone is not None:
        await state.update_data(phone=phone)
    await chat_handler.delete_messages(message.chat.id)

    if context.get('is_delivery'):
        await chat_handler.send_message(message,
                                        f'Отправьте геолокацию c помощью кнопкой "Отправить геолокацию"'
                                        '_Либо воспользуйтесь готовыми адресами указанной вами ранее_'
                                        '_Для отправки геолокацию самому, нажмите на иконку скрепки "📎" и '
                                        'выберите "Локация/Location", затем поделится локацией_',
                                        reply_markup=get_geo_reply_keyboard(order=context.get('order'),
                                                                            user=context.get('user'))
                                        )
        await state.set_state(States.ORDER_GEO)
    else:
        await chat_handler.send_message(message,
                                        f'В данный момент у вас: ${context.get("user")["bonus"]} бонусов!\n'
                                        f'Потратить их?',
                                        reply_markup=get_bonus_reply_keyboard(context.get('order')))
        await state.set_state(States.ORDER_PAY_BONUS)


@router.message(States.ORDER_PHONE, F.contact)
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, rest: RestHandler):
    await main_logic(message, state, chat_handler, rest, phone=message.contact.phone_number)


@router.message(States.ORDER_PHONE, F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=message.web_app_data.data)
    await step3_main_logic(message, state, chat_handler)


@router.message(States.ORDER_PHONE, F.text == '❌ Отмена')
async def cancel(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.clear()
    await get_start(message, chat_handler, rest, state, None)


@router.message(States.ORDER_PHONE, F.text)
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, rest: RestHandler):
    await main_logic(message, state, chat_handler, rest, message.text)


@router.message(States.ORDER_PHONE, lambda message: True)
async def handle_all_messages(message: Message):
    print('Заглушка [States.ORDER_PHONE]')
