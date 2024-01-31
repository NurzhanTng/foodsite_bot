from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.reply import get_exact_geo_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States
from core.utils.get_address import get_address
from .step4 import main_logic as step4_main_logic

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler,
                     loc: float | None = None, lat: float | None = None):
    if loc is not None and lat is not None:
        await state.update_data(geo={"loc": loc, "lat": lat})

    context = await state.get_data()

    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message, f'Введите номер квартиры / офиса):',
                                    reply_markup=get_exact_geo_reply_keyboard(context.get('order'), context.get('user')))
    await state.set_state(States.ORDER_EXACT_GEO)


@router.message(States.ORDER_GEO, F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler, rest_handler: RestHandler):
    await state.update_data(order=message.web_app_data.data)
    await step4_main_logic(message, state, chat_handler, rest_handler)


@router.message(States.ORDER_GEO, F.text == '❌ Отмена')
async def cancel(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.clear()
    await get_start(message, chat_handler, rest, state, None)


@router.message(States.ORDER_GEO, F.text)
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    context = await state.get_data()
    address = context.get('user')['address']
    if message.text == get_address(address['lat'], address['loc']):
        await main_logic(message, state, chat_handler, address['lat'], address['loc'])
    else:
        await chat_handler.send_message(message, f"Адрес не найден. Попробуйте еще")


@router.message(States.ORDER_GEO, F.location)
async def get_order(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    lat = message.location.latitude
    loc = message.location.longitude
    await main_logic(message, state, chat_handler, loc, lat)


@router.message(States.ORDER_GEO, lambda message: True)
async def handle_all_messages(message: Message):
    print('Заглушка [States.ORDER_PHONE]')
