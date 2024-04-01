from aiogram import Bot
import time
import logging

from core.utils.RestHandler import RestHandler
from core.models.Order import Order, OrderSerializer
from core.utils.ChatHistoryHandler import ChatHistoryHandler


class OrderSender:
    def __init__(self, bot: Bot):
        self.orders: list[Order] = []
        self.manager_id: int = 0
        self.rest = RestHandler(bot)
        self.bot: Bot = bot
        self.serializer = OrderSerializer()
        self.message_history = ChatHistoryHandler(bot)

    async def update_settings(self):
        # logging.info("[update_settings] started")
        self.orders = await self.fetch_orders()

    async def fetch_orders(self):
        # logging.info("[fetch_orders] started")
        dict_orders = await self.rest.get('food/orders/')
        orders = []
        for order in dict_orders:
            orders.append(self.serializer.from_dict(order))
        return orders

    async def fetch_manager(self):
        ...

    def find_order(self, order_id: int):
        for order in self.orders:
            if order.id == order_id:
                return order
        return -1

    async def send_new_order(self, order: Order):
        client_text = f"Ваш заказ сохранен\nБлюда в заказе:\n"
        price = 0
        for product in order.products:
            price += product.price
            client_text += f'{product.product.name} - {product.amount} шт | {product.price} тенге\n'
        if order.bonus_used:
            client_text += f'\nОбщая стоимость: {price - order.bonus_amount}'
        else:
            client_text += f'\nОбщая стоимость: {price}'

        message_id = (await self.bot.send_message(order.client_id, client_text)).message_id
        self.message_history.add_new_message(order.client_id, message_id)
        await self.bot.send_message(1234249296, f"Получен новый заказ {order.id}")

    async def send_new_status(self, order: Order):
        text_by_status = {
            'manager_await': 'Ваш заказ находится в обработке нашим менеджером. Благодарим за ожидание и понимание!',
            'payment_await': 'Благодарим за ваш заказ! Вам отправлен платеж на каспи. После '
                             'подтверждения платежа мы немедленно приступим к выполнению вашего заказа',
            'active': 'Мы подтвердили получение вашей оплаты. Приступили к подготовке вашего заказа',
            'done': 'Ваш заказ готов к выдаче! Пожалуйста, заберите его по адресу: г.Алматы. ТРК Forum. Проспект '
                    'Сейфуллина, 617 / 3 этаж',
            'on_delivery': 'Ваш заказ готов и передан доставщику. Ожидайте доставки в ближайшее время',
            'inactive': 'Ваш заказ выполнен успешно! Мы рады сообщить, что на ваш счет было добавлено 2000 бонусных '
                        'баллов'
        }
        # 'Ваш заказ готов. Можете забрать его в выбранной точке' if order.is_delivery else 'Ваш заказ готов. Скоро
        # он будет передан курьеру',
        try:
            if order.status == "done" and order.exact_address: return
            if order.status == "inactive":
                await self.message_history.delete_messages(order.client_id)
            message_id = (await self.bot.send_message(order.client_id, text_by_status[order.status])).message_id
            self.message_history.add_new_message(order.client_id, message_id)
            if order.status == "inactive":
                await asyncio.sleep(10)
                await self.message_history.delete_messages(order.client_id)
        except Exception as e:
            print(e)

    async def check_order_statuses(self):
        start_time = time.time()
        orders = await self.fetch_orders()
        print(f'[{time.time() - start_time}s] Order statuses fetched: {orders}')
        for order in orders:
            oldOrder = self.find_order(order.id)
            if oldOrder == -1:
                await self.send_new_order(order)
                continue
            if oldOrder.status != order.status:
                await self.send_new_status(order)
                continue
        self.orders = orders
