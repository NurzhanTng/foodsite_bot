import asyncio
import json
import logging
import websockets
from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import manager, user, basic
from core.middlewares.TestManagerMiddleware import TestManagerMiddleware
from core.middlewares.DeleteMessagesMiddleware import DeleteMessagesMiddleware
from core.middlewares.AppShedulerMiddleware import SchedulerMiddleware
from core.middlewares.RestMiddleware import RestMiddleware
from core.settings import settings
from core.utils.set_commands import set_commands
from core.utils.OrderSender import OrderSender


try:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except RuntimeError:
    print("Can't set event loop policy")


async def create_scheduled_tasks(bot: Bot, scheduler: AsyncIOScheduler):
    order_sender = OrderSender(bot)
    await order_sender.update_settings()
    scheduler.add_job(order_sender.check_order_statuses, trigger='interval', seconds=5)


# async def send_telegram_message(bot: Bot, message: str):
#     # Отправляем сообщение в Telegram
#     # await bot.send_message(bot., message)
#     print(message)
#
#
# async def connect_to_websocket(bot):
#     print("--- connect_to_websocket ---")
#     uri = "wss://back.pizzeria-almaty.kz:8001/ws/orders/"
#     async with websockets.connect(uri) as websocket:
#         print('connection start')
#         while True:
#             message = await websocket.recv()
#             # Отправляем полученное сообщение в Telegram
#             await send_telegram_message(bot, message)



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(settings.bots.bot_token, parse_mode='Markdown')
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Asia/Almaty")
    await create_scheduled_tasks(bot, scheduler)
    scheduler.start()
    await set_commands(bot)

    delete_middleware = DeleteMessagesMiddleware(bot)
    rest_middleware = RestMiddleware(bot)
    test_manager_middleware = TestManagerMiddleware()
    scheduler_middleware = SchedulerMiddleware(scheduler)
    dp.callback_query.middleware.register(delete_middleware)
    dp.callback_query.middleware.register(rest_middleware)
    dp.callback_query.middleware.register(test_manager_middleware)
    dp.callback_query.middleware.register(scheduler_middleware)
    dp.message.middleware.register(delete_middleware)
    dp.message.middleware.register(rest_middleware)
    dp.message.middleware.register(test_manager_middleware)
    dp.message.middleware.register(ChatActionMiddleware())
    dp.message.middleware.register(scheduler_middleware)

    dp.include_routers(manager.router, user.router, basic.router)

    try:
        # event_loop = asyncio.get_event_loop()
        # event_loop.run_until_complete(connect_to_websocket(bot))
        # event_loop.run_until_complete(dp.start_polling(bot))
        # event_loop.run_forever()
        # await asyncio.gather(connect_to_websocket(bot), dp.start_polling(bot))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
