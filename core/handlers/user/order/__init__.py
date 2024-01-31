from aiogram import Router

from core.handlers.user.order import step1, step2, step3, step4, step5, step6, step7, step8

router = Router()
router.include_routers(step1.router, step2.router, step3.router, step4.router, step5.router, step6.router,
                       step7.router, step8.router)
