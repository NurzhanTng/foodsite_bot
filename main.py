import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware

from core.handlers import user, basic
from core.middlewares.DeleteMessagesMiddleware import DeleteMessagesMiddleware
from core.middlewares.RestMiddleware import RestMiddleware
from core.settings import settings
from core.utils.get_address import get_address
from core.utils.set_commands import set_commands

# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    bot = Bot(settings.bots.bot_token, parse_mode='Markdown')
    dp = Dispatcher()
    await set_commands(bot)

    delete_middleware = DeleteMessagesMiddleware(bot)
    rest_middleware = RestMiddleware(bot)
    dp.callback_query.middleware.register(delete_middleware)
    dp.callback_query.middleware.register(rest_middleware)
    dp.message.middleware.register(delete_middleware)
    dp.message.middleware.register(rest_middleware)
    dp.message.middleware.register(ChatActionMiddleware())

    dp.include_routers(user.router, basic.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
    # print(get_address(43.242977, 76.945621))
