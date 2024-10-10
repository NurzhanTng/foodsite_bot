import logging
import websockets
import asyncio
import json
from aiogram import Bot
from core.middlewares.DeleteMessagesMiddleware import DeleteMessagesMiddleware
from core.handlers.websocket.order_main import order_main
from core.models.websocket.OrderUpdate import OrderUpdateSerializer

from core.settings import settings


async def connect(bot: Bot, delete_middleware: DeleteMessagesMiddleware):
    serializer = OrderUpdateSerializer()

    while True:
        try:
            async with websockets.connect(f"{settings.bots.ws_path}orders/") as websocket:
                logging.info("websocket started")
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                    except Exception as e:
                        logging.error(f"WebSocket not connected to server: {e}")
                        break
                    try:
                        order_update = serializer.from_dict(data)
                        await order_main(bot, delete_middleware.chat_handler, order_update)
                    except Exception as e:
                        logging.error(f"WebSocket error: {e}")
                        await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"WebSocket connection error: {e}")
            await bot.send_message(1234249296, 'Websocket перестал работу')
            await bot.send_message(1770261144, 'Websocket перестал работу')
            await asyncio.sleep(5)
