from aiogram import Router

from core.handlers.user import my_data, contacts, order

router = Router()

router.include_routers(my_data.router, contacts.router, order.router)
