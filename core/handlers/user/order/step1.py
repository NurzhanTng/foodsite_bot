import json

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.filters.without_state_filter import WithoutStateFilter
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.keyboards.reply import get_delivery_reply_keyboard
from core.utils.states import States

router = Router()


async def main_logic(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    context = await state.get_data()
    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message,
                                    f'Давайте перейдем к оформлению заказа.\n'
                                    f'✅ Выберите способ получения заказа:',
                                    reply_markup=get_delivery_reply_keyboard(context.get('order')))
    await state.set_state(States.ORDER_IS_DELIVERY)


@router.message(WithoutStateFilter(), F.web_app_data)
async def show_menu(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=message.web_app_data.data)
    await main_logic(message, state, chat_handler)


@router.message(F.text == "Проверка оформления заказа")
async def test(message: Message, state: FSMContext, chat_handler: ChatHistoryHandler):
    await state.update_data(order=json.dumps({"products": [
        {"amount": 2, "client_comment": "", "price": 7680, "product_id": 4, "active_modifier": 2, "additions": [1]},
        {"amount": 1, "client_comment": "", "price": 3300, "product_id": 2, "active_modifier": None, "additions": []},
        {"amount": 1, "client_comment": "", "price": 2390, "product_id": 5, "active_modifier": None, "additions": []}],
        "client_id": 0,
        "bonus_used": False,
        "user_name": "",
        "loc": 0,
        "lat": 0,
        "exact_address": "",
        "phone": "",
        "client_comment": ""
    }))
    await state.set_state(States.ORDER_IS_DELIVERY)
    await main_logic(message, state, chat_handler)
