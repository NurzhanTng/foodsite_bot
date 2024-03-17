from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.OrderTest import OrderTest, Order
from core.keyboards.inline import get_orders_inline_keyboard, get_back_inline_keyboard
from core.handlers.manager.order import show_order
from core.utils.states import States

router = Router()
order_text_statuses = ['❗ Новые заказы', 'Ожидающие оплаты заказы', 'Активные заказы', 'Готовые заказы',
                       'Ожидающие доставки заказы', 'Выполненные заказы']


@router.message(lambda m: m.text in order_text_statuses)
async def order_callback_query(message: Message, chat_handler: ChatHistoryHandler, state: FSMContext,
                               order_test: OrderTest):
    order_statuses = ['manager_await', 'payment_await', 'active', 'done', 'on_delivery', 'inactive']

    status_key = ''
    for index, status in enumerate(order_text_statuses):
        if status == message.text:
            status_key = order_statuses[index]
            break

    context = await state.get_data()
    # orders = await rest.get('', params={'type': 'new'})
    orders = order_test.get_order_by_status(context.get('company')['id'], status_key)
    await chat_handler.delete_messages(message.chat.id)

    await state.set_state(States.ORDER_SHOW)
    if len(orders) == 0:
        await chat_handler.send_message(message, 'Нет заказов', reply_markup=get_back_inline_keyboard())
    else:
        await chat_handler.send_message(message, 'Список заказов:', reply_markup=get_orders_inline_keyboard(
            order_test.get_order_by_status(context.get('company')['id'], status_key)))
