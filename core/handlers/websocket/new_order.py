import logging
from core.utils.RestHandler import RestHandler
from aiogram import Bot, Router, F
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.models.Company import CompanySerializer
from core.models.Order import Order
from core.keyboards.inline import get_manager_order_inline_keyboard


rest = RestHandler()
company_serializer = CompanySerializer()


async def fetch_manager(company_id: int) -> str:
    company_dict = await rest.get(f"service/company_spots/{company_id}")
    company = company_serializer.from_dict(company_dict)
    return company.manager


async def new_order(bot: Bot, message_history: ChatHistoryHandler, manager_history: ChatHistoryHandler, order: Order):
    # message_id = (await bot.send_message(int(order.client_id), f"Ваш заказ сохранен\n")).message_id
    # message_history.add_new_message(order.client_id, message_id)
    manager_id = await fetch_manager(order.company_id)
    message_id = (await bot.send_message(manager_id, f"Получен новый заказ {order.id}",
                  reply_markup=get_manager_order_inline_keyboard(order.id))).message_id
    manager_history.add_new_message(f'{manager_id}|{order.id}', message_id)


def invoice_test():
    # prices = [LabeledPrice(label=f"{product.product.name}, {product.active_modifier}", amount=product.price * 100)
    #           for
    #           product in
    #           order.products]
    #
    # if order.bonus_used:
    #     prices.append(LabeledPrice(label="Использованный бонус", amount=-100 * order.bonus_amount))
    # if not (order.exact_address is None or order.exact_address == ""):
    #     prices.append(LabeledPrice(label="Доставка", amount=int(order.delivery_price) * 100))
    # invoice_id = (
    #     await self.bot.send_invoice(
    #         order.client_id,
    #         title="Оплата заказа",
    #         photo_url="https://back.pizzeria-almaty.kz/media/images/pay_low.jpg",
    #         photo_width=400,
    #         photo_height=400,
    #         photo_size=17_648,
    #         # photo_url="https://back.pizzeria-almaty.kz/media/images/pay.jpg",
    #         # photo_width=3000,
    #         # photo_height=3000,
    #         # photo_size=2_211_280,
    #         description="Оплата заказа через карту",
    #         provider_token=settings.bots.payments_token,
    #         currency="kzt",
    #         is_flexible=False,
    #         prices=prices,
    #         start_parameter="order-payment",
    #         payload='Test'
    #     )
    # ).message_id
    # self.message_history.add_new_message(order.client_id, invoice_id)
    pass
