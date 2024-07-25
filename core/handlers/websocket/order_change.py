import logging
from aiogram import Bot, Router, F
from core.models.Order import Order
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.keyboards.inline import get_rating_inline_keyboard
from core.utils.fetch_managers import fetch_managers


async def order_change(bot: Bot, message_history: ChatHistoryHandler, manager_history: ChatHistoryHandler, order: Order):
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
    try:
        manager_ids = await fetch_managers(order.company_id)
        for manager_id in manager_ids:
            await manager_history.delete_messages(f'{manager_id}|{order.id}', '|')

        if order.status == "done" and order.exact_address:
            return
        if order.status == "inactive":
            await message_history.delete_messages(order.client_id)
            message_id = (await bot.send_message(int(order.client_id), text_by_status[
                order.status])).message_id
            rating_id = (await bot.send_message(int(order.client_id), text_by_status['rating'],
                                                reply_markup=get_rating_inline_keyboard())).message_id
            message_history.add_new_message(order.client_id, message_id)
            message_history.add_new_message(order.client_id, rating_id)
            return
        if order.status == "on_delivery":
            message_id = (await bot.send_message(int(order.client_id), text_by_status[
                order.status])).message_id
            del_message_id = (await bot.send_message(int(order.delivery_id),
                                                     f"Вам назначили новый заказ № {order.id}")).message_id
            message_history.add_new_message(order.client_id, message_id)
            message_history.add_new_message(order.delivery_id, del_message_id)
            return

        if order.status == 'rejected' and order.bonus_used and order.bonus_amount != 0:
            message_id = (await bot.send_message(
                int(order.client_id),
                f"Вам начислено {order.bonus_amount} бонусов")).message_id
            message_history.add_new_message(order.client_id, message_id)

        message_id = (await bot.send_message(int(order.client_id), text_by_status[order.status])).message_id
        message_history.add_new_message(order.client_id, message_id)

    except Exception as e:
        print(e)
