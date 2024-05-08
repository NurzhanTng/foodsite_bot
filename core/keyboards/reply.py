import json
from urllib.parse import quote

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

from core.utils.get_address import get_address


def get_web_url(order: str = None, path: str = '') -> str:
    web_url = 'https://www.pizzeria-almaty.kz' + path
    if order is not None:
        web_url += f'/?cart={quote(json.dumps(json.loads(order)["products"]))}'
    return web_url


def get_main_reply_keyboard(order: dict | None):
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Проверка оформления заказа', callback_data='test')
    keyboard_builder.button(text='📕 Меню', web_app=WebAppInfo(url=get_web_url(order)))
    keyboard_builder.button(text='🛒 Корзина', web_app=WebAppInfo(url=get_web_url(order, path='/cart')))
    keyboard_builder.button(text='🚖 Активные заказы', callback_data='show-cart')
    keyboard_builder.button(text='🗃 История заказов', callback_data='show-history')
    keyboard_builder.button(text='👤 Мои данные', callback_data='my-data')
    keyboard_builder.button(text='📞 Контакты', callback_data='contact')
    keyboard_builder.adjust(1, 2, 2, 2)

    return keyboard_builder.as_markup(
        input_field_placeholder='Выберите действие',
        resize_keyboard=True,
    )

def get_delivery_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='🚖 Активные заказы', callback_data='show-cart')
    keyboard_builder.button(text='👤 Мои данные', callback_data='my-data')

    return keyboard_builder.as_markup(
        input_field_placeholder='Выберите действие',
        resize_keyboard=True,
    )


def get_manager_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Создать тестовый заказ', callback_data='contact')
    keyboard_builder.button(text='❗ Новые заказы', callback_data='contact')
    keyboard_builder.button(text='Ожидающие оплаты заказы', callback_data='contact')
    keyboard_builder.button(text='Активные заказы', callback_data='contact')
    keyboard_builder.button(text='Готовые заказы', callback_data='contact')
    keyboard_builder.button(text='Ожидающие доставки заказы', callback_data='contact')
    keyboard_builder.button(text='Выполненные заказы', callback_data='contact')

    keyboard_builder.adjust(1, 1, 2, 2, 1)

    return keyboard_builder.as_markup(
        input_field_placeholder='Выберите действие',
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_back_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='🔙 На главную', callback_data='to-back')

    return keyboard_builder.as_markup(
        input_field_placeholder='⏬ Нажмите кнопку, чтобы перейти на главную страницу',
        resize_keyboard=True,
        # one_time_keyboard=True
    )


def order_reply_keyboard(order: dict | None, placeholder: str, additional_buttons=None, adjust=None):
    keyboard_builder = ReplyKeyboardBuilder()

    if additional_buttons is None:
        additional_buttons = []

    if isinstance(additional_buttons, dict):
        for key, value in additional_buttons.items():
            if key == 'geo':
                keyboard_builder.button(text=value, request_location=True)
            if key == 'contact':
                keyboard_builder.button(text=value, request_contact=True)
            else:
                keyboard_builder.button(text=value, callback_data=value)
    elif isinstance(additional_buttons, list):
        for button in additional_buttons:
            keyboard_builder.button(text=button, callback_data=f"{button}")
    else:
        raise KeyError(f"Unknown additional buttons type: {additional_buttons}\nType: {type(additional_buttons)}")

    keyboard_builder.button(text='📕 Добавить еще', web_app=WebAppInfo(url=get_web_url(order)))
    keyboard_builder.button(text='🛒 Перейти в корзину', web_app=WebAppInfo(url=get_web_url(order, '/cart')))
    keyboard_builder.button(text='❌ Отмена', callback_data='cancel')

    if adjust is not None and isinstance(adjust, list):
        keyboard_builder.adjust(*(adjust + [1, 1, 1]))
    else:
        keyboard_builder.adjust(
            *[len(additional_buttons.keys() if isinstance(additional_buttons, dict) else additional_buttons),
              1, 1, 1]
        )

    return keyboard_builder.as_markup(
        input_field_placeholder=placeholder,
        resize_keyboard=True,
        # one_time_keyboard=True
    )


# def get_delivery_reply_keyboard(order: dict | None):
#     return order_reply_keyboard(order,
#                                 placeholder='Выберите способ получения заказа',
#                                 additional_buttons=['🛵 Доставить', '🚶🏼 Самовывоз'])


def get_usernames_reply_keyboard(order: dict | None, user: dict):
    return order_reply_keyboard(order,
                                placeholder='Выберите прошлое имя или впишите вручную',
                                additional_buttons=[user['telegram_fullname']])


def get_phones_reply_keyboard(order: dict | None, user: dict):
    return order_reply_keyboard(order,
                                placeholder='Выберите прошлый номер или впишите вручную',
                                additional_buttons={'': user['phone'], 'contact': 'Отправить свой номер'})


def get_geo_reply_keyboard(order: dict | None, user: dict):
    address = user['address']
    loc = address['loc']
    lat = address['lat']
    text_address = get_address(lat, loc)

    return order_reply_keyboard(order,
                                placeholder='Выберите прошлый адрес доставки или отправьте свой адрес через кнопку',
                                additional_buttons={"": text_address, 'geo': 'Отправить свой адрес'})


def get_exact_geo_reply_keyboard(order: dict | None, user: dict):
    return order_reply_keyboard(order,
                                placeholder='Выберите адрес или впишите вручную',
                                additional_buttons=[user['exact_address']])


def get_bonus_reply_keyboard(order: dict | None):
    return order_reply_keyboard(order,
                                placeholder='Выберите потратить бонусы или нет',
                                additional_buttons=['❌ Нет', '✔ Да'])


def get_kaspi_phone_reply_keyboard(order: dict | None, user: dict):
    return order_reply_keyboard(order,
                                placeholder='Выберите прошлый номер каспи или впишите вручную',
                                additional_buttons={'': user['phone'], 'contact': 'Отправить свой номер'})


