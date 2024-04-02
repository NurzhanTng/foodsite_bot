from typing import List

from aiogram import Bot, Router, F
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.models.Order import OrderSerializer, Order
from core.handlers.basic import get_start
from core.keyboards.inline import get_back_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States

router = Router()


@router.callback_query(F.data == 'old-orders')
async def get_my_data(callback: CallbackQuery, chat_handler: ChatHistoryHandler, state: FSMContext, rest: RestHandler):
    orders_dict = await rest.get(url=f'food/orders/')
    orders: List[Order] = []
    for order in orders_dict:
        orders.append(OrderSerializer.from_dict(order))

    orders = [order for order in orders if order.client_id == 1234249296 and len(order.products) != 0]

    await chat_handler.delete_messages(callback.message.chat.id)
    await chat_handler.send_message(callback.message, f'Ваши предыдущие заказы',
                                    reply_markup=get_back_inline_keyboard())

    for order in orders:
        string = f"Заказ № {order.id}\nБлюда в заказе:\n"
        price = 0
        for product in order.products:
            string += f"{product.product.name}\n"
            price += product.price
        string += f"\nСумма заказа: {price} KZT"
        await chat_handler.send_message(callback.message, string)
    await state.set_state(States.ORDERS)


@router.callback_query(States.ORDERS, F.data == 'to-back')
async def go_back(callback: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext,
                  command: CommandObject | None = None):
    await chat_handler.delete_messages(callback.message.chat.id)
    await get_start(callback.message, chat_handler, rest, state, command)
