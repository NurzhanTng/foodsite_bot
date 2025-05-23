import logging
from aiogram import Bot, Router, F
from core.models.Order import Order
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.keyboards.inline import get_rating_inline_keyboard, get_manager_order_inline_keyboard
from core.utils.fetch_users import fetch_users
from core.utils.RestHandler import RestHandler

rest = RestHandler()


async def send_new_order_to_role(company_id: int, order_id: int, bot: Bot, role: str, message_history:
                                 ChatHistoryHandler, send_reply_markup: bool = True):
    ids = await fetch_users(company_id, role)
    for user_id in ids:
        try:
            reply = get_manager_order_inline_keyboard(order_id) if send_reply_markup else None
            message_id = (await bot.send_message(int(user_id), f"Получен новый заказ {order_id}",
                                                 reply_markup=reply)).message_id
            message_history.add_new_message(f'{user_id}|{order_id}', message_id)
        except Exception as e:
            logging.error(f"New order error [{role}]: {e}")


async def order_change(bot: Bot, message_history: ChatHistoryHandler,
                       order: Order):
    order_price = 0
    for product in order.products:
        order_price += product.price

    address_text = ""
    if order.status in ["on_runner", "done"]:
        company: dict = await rest.get(f"service/company_spots/{order.company_id}/")
        company_name = company.get("name", "")
        company_address = company.get("address", {}).get("parsed", "")
        address_link = company.get("address_link", "")
        address_text = f'Ваш заказ готов к выдаче! Пожалуйста, заберите его по адресу: {company_name} ' + \
                       f'[{company_address}]({address_link})'
        print("Address text: ", address_text)

    bonus_amount = 0
    if order.status == 'inactive':
        response: dict = await rest.get(f"food/order_bonus/{order.id}/")
        bonus_amount = response.get("bonus_amount", 0)

    text_by_status = {
        # 'manager_await': 'Ваш заказ находится в обработке нашим менеджером. Благодарим за ожидание и понимание!',
        'manager_await': 'Благодарим за ваш заказ! Вам в скором времени будет отправлен платеж на каспи. После '
                         'подтверждения платежа мы немедленно приступим к выполнению вашего заказа',
        'payment_await': 'Благодарим за ваш заказ! Вам отправлен платеж на каспи. После '
                         'подтверждения платежа мы немедленно приступим к выполнению вашего заказа',
        'active': 'Мы подтвердили получение вашей оплаты. Приступили к подготовке вашего заказа',
        'done': address_text,
        'on_delivery': 'Ваш заказ готов и передан доставщику. Ожидайте доставки в ближайшее время',
        # 'inactive': f'Ваш заказ выполнен успешно! Мы рады сообщить, что на ваш счет было добавлено '
        #             f'{(order_price - (int(order.bonus_amount) if order.bonus_used else 0)) // 20} бонусных баллов',
        'inactive': f'Ваш заказ выполнен успешно! {f"Мы рады сообщить, что на ваш счет было добавлено {bonus_amount} бонусных баллов" if bonus_amount != 0 else "" }',
        'rating': "Пожалуйста, выберите смайлик, который наилучшим образом описывает ваше впечатление от "
                  "заказа:\n\n😞 - Не понравилось\n😐 - Средне\n🙂 - Хорошо\n😊 - Отлично",
        'rejected': f"Ваш заказ был отклонен. Причина: *{order.rejected_text}*",
        'on_runner': address_text
    }
    try:
        if order.status in ["payment_await", "active"]:
            manager_ids = await fetch_users(order.company_id, 'admin')
            for manager_id in manager_ids:
                await message_history.delete_messages(f'{manager_id}|{order.id}', '|')
            manager_ids = await fetch_users(order.company_id, 'manager')
            for manager_id in manager_ids:
                await message_history.delete_messages(f'{manager_id}|{order.id}', '|')
        if order.status in ["on_runner"]:
            manager_ids = await fetch_users(order.company_id, 'cook')
            for manager_id in manager_ids:
                await message_history.delete_messages(f'{manager_id}|{order.id}', '|')
        if order.status in ["inactive"]:
            manager_ids = await fetch_users(order.company_id, 'runner')
            for manager_id in manager_ids:
                await message_history.delete_messages(f'{manager_id}|{order.id}', '|')
    except Exception as e:
        logging.error(f"Error [order_change (message delete)]: {e}")

    try:
        if (order.status == "done" or
                (order.status == "on_runner" and order.is_delivery) or
                (order.status == "manager_await" and order.rejected_text != "")):
            return
        if order.status == "active":
            await send_new_order_to_role(order.company_id, order.id, bot, 'cook', message_history, False)
        if order.status == "on_runner":
            await send_new_order_to_role(order.company_id, order.id, bot, 'runner', message_history, False)
        if order.status == "on_delivery":
            await send_new_order_to_role(order.company_id, order.id, bot, 'delivery', message_history, False)
    except Exception as e:
        logging.error(f"Error [order_change (message send)]: {e}")

    try:
        if order.status == "inactive":
            print(1)
            if isinstance(order.rating, int):
                return
            try:
                await message_history.delete_messages(order.client_id)
            except Exception as e:
                print(f'Huilo ebanoe: ', order.client_id, e)
            print(2)
            message_id = (await bot.send_message(int(order.client_id), text_by_status[
                order.status])).message_id
            print(3)
            rating_id = (await bot.send_message(int(order.client_id), text_by_status['rating'],
                                                reply_markup=get_rating_inline_keyboard(order.id))).message_id
            print(4, order.client_id, message_id)
            message_history.add_new_message(order.client_id, message_id)
            print('websocket message rating: ', order.client_id, type(order.client_id))
            print(5)
            message_history.add_new_message(order.client_id, rating_id)
            return
        print(6)
        if order.status == "on_delivery":
            message_id = (await bot.send_message(int(order.client_id), text_by_status[
                order.status])).message_id
            del_message_id = (await bot.send_message(int(order.delivery_id),
                                                     f"Вам назначили новый заказ № {order.id}")).message_id
            message_history.add_new_message(order.client_id, message_id)
            message_history.add_new_message(order.delivery_id, del_message_id)
            return

        print(7)
        if order.status == 'rejected' and order.bonus_used and order.bonus_amount != 0:
            message_id = (await bot.send_message(
                int(order.client_id),
                f"Вам начислено {order.bonus_amount} бонусов")).message_id
            message_history.add_new_message(order.client_id, message_id)

        print("Pidor")
        message_id = (await bot.send_message(int(order.client_id), text_by_status[order.status])).message_id
        print(8)
        message_history.add_new_message(order.client_id, message_id)
        print(9)
    except Exception as e:
        logging.error(f"Error [order_change]: {e}")
