import json
from urllib.parse import quote

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

from core.utils.OrderTest import Order



def get_web_url(order: str = None, path: str = '') -> str:
    web_url = 'https://www.pizzeria-almaty.kz' + path
    if order is not None:
        web_url += f'/?cart={quote(json.dumps(json.loads(order)["products"]))}'
    return web_url


def get_main_reply_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    # keyboard_builder.button(text='Проверка оформления заказа', callback_data='test')
    # keyboard_builder.button(text='🛒 Корзина', web_app=WebAppInfo(url="https://www.pizzeria-almaty.kz/cart"))
    # keyboard_builder.button(text='🚖 Активные заказы', callback_data='show-cart')
    # keyboard_builder.button(text='🗃 История заказов', callback_data='show-history')
    keyboard_builder.button(text='📕 Меню', web_app=WebAppInfo(url="https://www.pizzeria-almaty.kz"))
    keyboard_builder.button(text='👤 Мои данные', callback_data='my-data')
    keyboard_builder.button(text='📞 Контакты', callback_data='contact')
    keyboard_builder.adjust(1, 1, 1)

    return keyboard_builder.as_markup(
        input_field_placeholder='Выберите действие',
        resize_keyboard=True,
    )


def get_orders_inline_keyboard(orders: list[Order] | None):
    keyboard_builder = InlineKeyboardBuilder()

    for order in orders:
        print(f'Order: {order}')
        keyboard_builder.button(text=f'Заказ №{order.id}', callback_data=str(order.id))
    keyboard_builder.button(text='Назад', callback_data='back')

    keyboard_builder.adjust(*([1] * (len(orders) + 1)))

    return keyboard_builder.as_markup(
        input_field_placeholder='Выберите заказ',
        resize_keyboard=True,
    )


def get_change_order_type_inline_keyboard(order: Order):
    keyboard_builder = InlineKeyboardBuilder()

    text_by_status = {
        'manager_await': 'Нажмите после отправки платежа клиенту',
        'payment_await': 'Нажмите после получения оплаты заказа',
        'active': 'Нажмите после готовности заказа',
        'done': 'Нажмите после получение заказа клиентом' if order.is_delivery
                else 'Нажмите после передачи заказа доставщику',
        'on_delivery': 'Нажмите после получение заказа клиентом',
        'inactive': ''
    }

    if order.status != 'inactive':
        keyboard_builder.button(text=text_by_status[order.status], callback_data=str(order.id))
    keyboard_builder.button(text='Назад', callback_data='back')

    keyboard_builder.adjust(1, 1)

    return keyboard_builder.as_markup(
        resize_keyboard=True
    )


def get_back_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Назад', callback_data='back')
    return keyboard_builder.as_markup(resize_keyboard=True)
