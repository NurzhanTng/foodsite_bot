import json
from random import randint
from aiogram import Bot, Router, F
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.inline import get_order_inline_keyboard, get_back_inline_keyboard, get_order_end_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States
from core.models.Order import Order, OrderSerializer

router = Router()
serializer = OrderSerializer()

order_keys = {}


async def fetch_orders(user_id: str, rest: RestHandler) -> list[Order]:
    dict_orders = await rest.get('food/orders/')
    orders = []
    for order in dict_orders:
        order = serializer.from_dict(order)
        if order.delivery_id == user_id and order.status != 'inactive':
            orders.append(order)
    return orders


@router.message(F.text == '🚖 Активные заказы')
async def active_orders(message: Message, chat_handler: ChatHistoryHandler, state: FSMContext, rest: RestHandler):
    dict_orders = await fetch_orders(user_id=str(message.chat.id), rest=rest)

    await chat_handler.delete_messages(message.chat.id)

    if len(dict_orders) == 0:
        await chat_handler.send_message(message, f"Нет активных заказов",
                                        reply_markup=get_back_inline_keyboard())
        await state.set_state(States.EMPTY_ORDER_LIST)
        return

    for order in dict_orders:
        await chat_handler.send_message(message,
                                        f"Текст заказа № {order.id}",
                                        reply_markup=get_order_inline_keyboard(order))
        await state.set_state(States.DELIVERY_ORDER)


@router.callback_query(States.DELIVERY_ORDER, F.data.startswith('delivery'))
async def order_text(callback: CallbackQuery, chat_handler: ChatHistoryHandler, state: FSMContext):
    await chat_handler.send_message(callback.message,
                                    f"Полный текст заказа",
                                    reply_markup=get_order_end_inline_keyboard(callback.data.split('-')[1]))
    await state.set_state(States.ORDER_END)
    await callback.answer()


@router.callback_query(States.ORDER_END, F.data.startswith('order_end'))
async def order_end(callback: CallbackQuery, chat_handler: ChatHistoryHandler, state: FSMContext, rest: RestHandler):
    order = serializer.from_dict(
        await rest.get(f'food/order/{int(callback.data.split("-")[1])}')
    )

    order_keys[order.delivery_id] = {'token': randint(100000, 999999), "order_id": order.id}

    client_message_id = (
        (await callback.message.bot.send_message(int(order.delivery_id),
                                                 f"Для завершения заказа, вам необходимо передать "
                                                 f"пароль доставщику: {order_keys[order.delivery_id].get('token')}"))
        .message_id)
    chat_handler.add_new_message(order.client_id, client_message_id)
    await chat_handler.send_message(callback.message,
                                    f"Введите код для завершения:",
                                    reply_markup=get_back_inline_keyboard())
    await state.set_state(States.ORDER_WRITE_TOKEN)


@router.message(States.ORDER_WRITE_TOKEN, F.text)
async def write_order(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext,
                      command: CommandObject | None = None):
    order_token: dict = order_keys.get(str(message.chat.id))
    if str(message.text) == str(order_token.get('token')):
        await state.set_state(None)
        await chat_handler.delete_messages(message.chat.id)
        await chat_handler.send_message(message, 'Пароль введен верно')
        order = serializer.from_dict(await rest.get(f'food/orders/{order_token.get("order_id")}/'))
        await rest.update(f'food/orders/{order_token.get("order_id")}/',
                          {"status": "inactive", "user_name": order.user_name, "phone": order.phone, "client_id":
                              order.client_id})
        await get_start(message, chat_handler, rest, state, command)
    else:
        await chat_handler.send_message(message, 'Пароль введен неверно')


@router.callback_query(F.data == 'to-back')
async def go_back(callback: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext,
                  command: CommandObject | None = None):
    await chat_handler.delete_messages(callback.message.chat.id)
    await get_start(callback.message, chat_handler, rest, state, command)
