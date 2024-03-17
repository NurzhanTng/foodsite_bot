from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.utils.RestHandler import RestHandler
from core.utils.get_address import get_address
from core.keyboards.inline import get_change_order_type_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.OrderTest import OrderTest, Order
from core.utils.states import States

router = Router()


async def show_order(order: Order, message: Message, chat_handler: ChatHistoryHandler):
    text = f'Заказ: *{order.id}*\n'
    text += f'Продукты:\n'
    price = 0
    for product in order.products:
        # print(product)
        text += f'  {product["product_id"]}\n'
        price += int(product["price"])
    text += f'Имя: *{order.user_name}*\n'
    text += f'Номер: *{order.phone}*\n'
    if order.is_delivery:
        text += f'Адрес: *{get_address(order.lat, order.long)}*\n'
        text += f'Дом: *{order.exact_address}*\n'
    text += f'Каспи номер: *{order.kaspi_phone}*\n'
    text += '\n\n'
    text += f'Общая цена без скидок: *{price}*\n'
    if order.bonus_used:
        text += f'Бонус: *{order.bonus_amount}*\n'
        text += f'Итоговая цена: *{price - order.bonus_amount}*'
    else:
        text += f'Итоговая цена: *{price}*'

    text += '\n\nЧтобы сменить статус заказа, нажмите кнопку снизу:'
    # print(text)

    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message, text, reply_markup=get_change_order_type_inline_keyboard(order))


@router.callback_query(States.ORDER_SHOW)
async def order_callback_query_handler(call: CallbackQuery, chat_handler: ChatHistoryHandler, order_test: OrderTest,
                                       state: FSMContext, rest: RestHandler):
    if call.data == 'back':
        await state.set_state(None)
        await get_start(call.message, chat_handler, rest, state, None)
        await call.answer()
        return

    order = order_test.get_order_by_id(int(call.data))
    await chat_handler.delete_messages(call.message.chat.id)
    await show_order(order, call.message, chat_handler)
    await state.set_state(States.ORDER_STATUS_CHANGE)
    await call.answer()


@router.callback_query(States.ORDER_STATUS_CHANGE)
async def order_callback_query_handler(call: CallbackQuery, chat_handler: ChatHistoryHandler, order_test: OrderTest,
                                       state: FSMContext, rest: RestHandler):
    if call.data == 'back':
        await state.set_state(None)
        await get_start(call.message, chat_handler, rest, state, None)
        await call.answer()
        return

    context = await state.get_data()
    order = order_test.get_order_by_id(int(call.data))

    order_statuses = ['manager_await', 'payment_await', 'active', 'done', 'on_delivery', 'inactive']
    order_index = len(order_statuses) - 1
    for index, status in enumerate(order_statuses):
        if order.status == status and index < len(order_statuses) - 1:
            order_index = index + 1

    if not order.is_delivery and order.status == 'done':
        order_index = 5

    order_test.change_order_status(context.get('company')['id'], order.id, order_statuses[order_index])
    await state.set_state(None)
    await chat_handler.delete_messages(call.message.chat.id)
    await get_start(call.message, chat_handler, rest, state, None)
    await call.answer()
