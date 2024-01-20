from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo


def get_main_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text='📕 Меню', web_app=WebAppInfo(url='https://google.com'))
    keyboard_builder.button(text='🛒 Активные заказы', callback_data='show-cart')
    keyboard_builder.button(text='🗃 История заказов', callback_data='show-history')
    keyboard_builder.button(text='👤 Мои данные', callback_data='my-data')
    keyboard_builder.button(text='📞 Контакты', callback_data='contact')
    keyboard_builder.adjust(2, 1, 2)

    return keyboard_builder.as_markup()


def get_back_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🔙 На главную', callback_data='to-back')
    return keyboard_builder.as_markup()

