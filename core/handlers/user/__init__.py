from aiogram import Router

from core.handlers.user import my_data, contacts, order
from core.filters import UserRoleFilter

router = Router()
router.message.filter(UserRoleFilter('user'))

router.include_routers(my_data.router, contacts.router, order.router)
