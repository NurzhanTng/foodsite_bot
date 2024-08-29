from aiogram import Router

from core.handlers.manager import order_statuses, test_new_order, order, mailing

router = Router()

router.include_routers(mailing.router, order.router, order_statuses.router, test_new_order.router)
