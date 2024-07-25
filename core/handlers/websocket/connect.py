import logging
import websockets
import asyncio
import json
from aiogram import Bot
from core.middlewares.DeleteMessagesMiddleware import DeleteMessagesMiddleware
from core.handlers.websocket.order_main import order_main
from core.models.websocket.OrderUpdate import OrderUpdateSerializer, OrderUpdate
from core.utils.ChatHistoryHandler import ChatHistoryHandler


async def connect(bot: Bot, delete_middleware: DeleteMessagesMiddleware):
    serializer = OrderUpdateSerializer()
    manager_chat_history = ChatHistoryHandler(bot)
    async with websockets.connect("wss://pizza.pizzeria-almaty.kz:443/ws/orders/") as websocket:
        logging.info("websocket started")
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                logging.info(f"New message from websocket: {data}")
                order_update = serializer.from_dict(data)
                logging.info(f"New message from websocket: {order_update}")
                await order_main(bot, delete_middleware.chat_handler, manager_chat_history, order_update)
            except Exception as e:
                logging.error(f"WebSocket error: {e}")
                await asyncio.sleep(5)
