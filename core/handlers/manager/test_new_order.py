from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.OrderTest import OrderTest

router = Router()


@router.message(F.text == 'Создать тестовый заказ')
async def order_callback_query(message: Message, chat_handler: ChatHistoryHandler, order_test: OrderTest,
                               state: FSMContext):
    context = await state.get_data()
    order_id = order_test.create_new_order(context.get('company')['id'])
    await chat_handler.send_message(message, f'Заказ создан. Номер заказа: {order_id}')


# @router.message(lambda message: True)
# async def handle_all_messages(message: Message):
#     print('Заглушка [new_orders]')
