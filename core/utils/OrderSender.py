from aiogram import Bot, Router, F
import time
from datetime import datetime
import json
import logging
import asyncio
from aiogram.filters import (Command, CommandObject, )
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType

from core.settings import settings
from core.utils.RestHandler import RestHandler
from core.models.Order import Order, OrderSerializer
from core.models.Company import Company, CompanySerializer
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.keyboards.inline import get_rating_inline_keyboard


class OrderSender:
    def __init__(self, bot: Bot, message_history: ChatHistoryHandler):
        self.orders: list[Order] = []
        self.rest = RestHandler(bot)
        self.bot: Bot = bot
        self.serializer = OrderSerializer()
        self.company_serializer = CompanySerializer()
        self.message_history = message_history

    async def update_settings(self):
        self.orders = await self.fetch_orders()
        for order in self.orders:
            if order.status == "inactive":
                self.orders.remove(order)

    async def delete_order(self, order) -> None:
        self.orders.remove(order)

    async def fetch_orders(self):
        dict_orders = await self.rest.get('food/orders/')
        orders = []
        for order in dict_orders:
            orders.append(self.serializer.from_dict(order))
        return orders

    async def fetch_manager(self, company_id: int) -> str:
        company_dict = await self.rest.get(f"service/company_spots/{company_id}")
        company = self.company_serializer.from_dict(company_dict)
        return company.manager

    def find_order(self, order_id: int):
        for order in self.orders:
            if order.id == order_id:
                return order
        return -1

    async def send_new_order(self, order: Order):
        # prices = [LabeledPrice(label=f"{product.product.name}, {product.active_modifier}", amount=product.price * 100)
        #           for
        #           product in
        #           order.products]
        #
        # if order.bonus_used:
        #     prices.append(LabeledPrice(label="Использованный бонус", amount=-100 * order.bonus_amount))
        # if not (order.exact_address is None or order.exact_address == ""):
        #     prices.append(LabeledPrice(label="Доставка", amount=int(order.delivery_price) * 100))

        message_id = (await self.bot.send_message(int(order.client_id), f"Ваш заказ сохранен\n")).message_id
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

        self.message_history.add_new_message(order.client_id, message_id)
        # self.message_history.add_new_message(order.client_id, invoice_id)
        manager_id = await self.fetch_manager(order.company_id)
        await self.bot.send_message(manager_id, f"Получен новый заказ {order.id}")

    async def send_new_status(self, order: Order):
        order_price = 0
        for product in order.products:
            order_price += product.price

        text_by_status = {
            'manager_await': 'Ваш заказ находится в обработке нашим менеджером. Благодарим за ожидание и понимание!',
            'payment_await': 'Благодарим за ваш заказ! Вам отправлен платеж на каспи. После '
                             'подтверждения платежа мы немедленно приступим к выполнению вашего заказа',
            'active': 'Мы подтвердили получение вашей оплаты. Приступили к подготовке вашего заказа',
            'done': 'Ваш заказ готов к выдаче! Пожалуйста, заберите его по адресу: г.Алматы. ТРК Forum. Проспект '
                    'Сейфуллина, 617 / 3 этаж',
            'on_delivery': 'Ваш заказ готов и передан доставщику. Ожидайте доставки в ближайшее время',
            'inactive': f'Ваш заказ выполнен успешно! Мы рады сообщить, что на ваш счет было добавлено '
                        f'{(order_price - (int(order.bonus_amount) if order.bonus_used else 0)) // 20} бонусных баллов',
            'rating': "Пожалуйста, выберите смайлик, который наилучшим образом описывает ваше впечатление от "
                      "заказа:\n\n😞 - Не понравилось\n😐 - Средне\n🙂 - Хорошо\n😊 - Отлично",
            'rejected': f"Ваш заказ был отклонен. Причина: *{order.rejected_text}*"
        }
        # 'Ваш заказ готов. Можете забрать его в выбранной точке' if order.is_delivery else 'Ваш заказ готов. Скоро
        # он будет передан курьеру',
        try:
            if order.status == "done" and order.exact_address:
                return
            if order.status == "inactive":
                await self.message_history.delete_messages(order.client_id)
                message_id = (await self.bot.send_message(int(order.client_id), text_by_status[
                    order.status])).message_id
                rating_id = (await self.bot.send_message(int(order.client_id), text_by_status['rating'],
                                                         reply_markup=get_rating_inline_keyboard())).message_id
                self.message_history.add_new_message(order.client_id, message_id)
                self.message_history.add_new_message(order.client_id, rating_id)
                return
            if order.status == "on_delivery":
                message_id = (await self.bot.send_message(int(order.client_id), text_by_status[
                    order.status])).message_id
                del_message_id = (await self.bot.send_message(int(order.delivery_id),
                                                              f"Вам назначили новый заказ № {order.id}")).message_id
                self.message_history.add_new_message(order.client_id, message_id)
                self.message_history.add_new_message(order.delivery_id, del_message_id)
                return

            message_id = (await self.bot.send_message(int(order.client_id), text_by_status[order.status])).message_id
            self.message_history.add_new_message(order.client_id, message_id)

        except Exception as e:
            print(e)

    async def check_order_statuses(self):
        orders = await self.fetch_orders()
        for order in orders:
            oldOrder = self.find_order(order.id)
            if oldOrder == -1:
                await self.send_new_order(order)
                continue
            if oldOrder.status == 'inactive':
                continue
            if oldOrder.status != order.status:
                await self.send_new_status(order)
                continue
        self.orders = orders
