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
                order_update = serializer.from_dict(data)
                logging.info(f"New message from websocket: {order_update}")
                await order_main(bot, delete_middleware.chat_handler, manager_chat_history, order_update)
                # chat_id = data.get("chat_id")  # Предполагается, что chat_id содержится в сообщении
                # text = data.get("text")  # Предполагается, что text содержится в сообщении
                # if chat_id and text:
                #     await bot.send_message(chat_id, text)
            except Exception as e:
                logging.error(f"WebSocket error: {e}")
                await asyncio.sleep(5)
