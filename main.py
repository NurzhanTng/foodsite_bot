import asyncio
import json
import logging
import websockets
from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers import manager, user, basic, pay
from core.handlers.user import rating
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


async def create_scheduled_tasks(bot: Bot, scheduler: AsyncIOScheduler, delete_middleware: DeleteMessagesMiddleware):
    order_sender = OrderSender(bot, delete_middleware.chat_handler)
    await order_sender.update_settings()
    scheduler.add_job(order_sender.check_order_statuses, trigger='interval', seconds=5)


async def main():
    with open('history/bot.log', 'w') as file:
        file.write('')
    logging.basicConfig(
        filemode='a',
        filename=f'history/bot.log',
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(settings.bots.bot_token, parse_mode='Markdown')
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Asia/Almaty")
    delete_middleware = DeleteMessagesMiddleware(bot)
    rest_middleware = RestMiddleware(bot)
    test_manager_middleware = TestManagerMiddleware()
    scheduler_middleware = SchedulerMiddleware(scheduler)

    await set_commands(bot)
    await create_scheduled_tasks(bot, scheduler, delete_middleware)
    scheduler.start()

    dp.callback_query.middleware.register(delete_middleware)
    dp.callback_query.middleware.register(rest_middleware)
    dp.callback_query.middleware.register(test_manager_middleware)
    dp.callback_query.middleware.register(scheduler_middleware)
    dp.message.middleware.register(delete_middleware)
    dp.message.middleware.register(rest_middleware)
    dp.message.middleware.register(test_manager_middleware)
    dp.message.middleware.register(ChatActionMiddleware())
    dp.message.middleware.register(scheduler_middleware)

    dp.include_routers(pay.router, rating.router, manager.router, user.router, basic.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
