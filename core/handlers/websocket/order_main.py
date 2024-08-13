import logging
from core.utils.RestHandler import RestHandler
from core.handlers.websocket.order_change import order_change
from core.handlers.websocket.new_order import new_order
from aiogram import Bot, Router, F
from core.models.Order import Order, OrderSerializer
from core.models.websocket.OrderUpdate import OrderUpdate
from core.utils.ChatHistoryHandler import ChatHistoryHandler


rest = RestHandler()
serializer = OrderSerializer()


async def order_main(bot: Bot, message_history: ChatHistoryHandler, manager_history: ChatHistoryHandler,
                     request: OrderUpdate):
    try:
        order_dict = await rest.get(f'food/order/{request.order_id}')
        order = serializer.from_dict(order_dict)

        if order.status == "manager_await":
            await new_order(bot, message_history, manager_history, order)
        else:
            await order_change(bot, message_history, manager_history, order)
    except Exception as e:
        logging.error(f"Error order_main: {e}")
