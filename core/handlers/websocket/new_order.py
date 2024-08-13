import logging
from aiogram import Bot, Router, F
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.models.Order import Order
from core.keyboards.inline import get_manager_order_inline_keyboard
from core.utils.fetch_users import fetch_users


async def send_new_order_to_role(company_id: int, order_id: int, bot: Bot, role: str):
    ids = await fetch_users(company_id, role)
    for user_id in ids:
        try:
            message_id = (await bot.send_message(int(user_id), f"Получен новый заказ {order_id}",
                                                 reply_markup=get_manager_order_inline_keyboard(order_id))).message_id
            manager_history.add_new_message(f'{user_id}|{order_id}', message_id)
        except Exception as e:
            logging.error(f"New order error [{role}]: {e}")


async def new_order(bot: Bot, message_history: ChatHistoryHandler, manager_history: ChatHistoryHandler, order: Order):
    try:
        message_id = (await bot.send_message(int(order.client_id), f"Ваш заказ сохранен\n")).message_id
        message_history.add_new_message(order.client_id, message_id)
        await send_new_order_to_role(order.company_id, order.id, bot, 'manager')
        await send_new_order_to_role(order.company_id, order.id, bot,  'admin')
    except Exception as e:
        logging.error(f"Error new_order: {e}")


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
