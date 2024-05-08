from aiogram import Router

from core.handlers.delivery import my_data, order_list

router = Router()

router.include_routers(my_data.router, order_list.router)
