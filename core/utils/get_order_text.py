import json

from aiogram.fsm.context import FSMContext

from core.utils.get_address import get_address


async def get_order_text(state: FSMContext) -> str:
    context = await state.get_data()
    text = '*Ваши данные:*\n\n'

    is_delivery = context.get('is_delivery')
    name = context.get('name')
    phone = context.get('phone')
    geo: dict = context.get('geo')
    print(geo)
    if geo is not None:
        print(geo.get('lat'), geo.get('loc'))
    exact_geo = context.get('exact_geo')
    pay_bonus = context.get('pay_bonus')
    order: dict = json.loads(context.get('order'))
    user: dict = context.get('user')

    order_price = 0
    for product in order.get('products'):
        order_price += product['price']
    delivery_price = 1000
    main_price = order_price

    text += f"Номер телефона: {phone}\n"
    text += f"Имя: {name}\n"
    if is_delivery:
        text += f"Адрес: {get_address(geo.get('lat'), geo.get('loc')) }.\nТочный адрес: {exact_geo}\n\n"
    else:
        text += '\n*Вы можете забрать ваш заказ* по адресу:\nАлматы, улица Курмангазы, 54\n\n'
    text += ('*Последний шаг!*\n'
             'Отправьте ваш номер каспи для того чтобы мы могли выставить счет к оплате:\n\n'
             '_Или используйте кнопки_\n\n'
             f'Общая сумма: {order_price} KZT\n')
    if is_delivery:
        text += f'За доставку: {delivery_price} KZT\n'
        main_price += delivery_price
    if pay_bonus:
        text += f'Использовано: ${user.get("bonus")} бонусов\n'
        main_price -= user.get("bonus")

    text += f"\n*Итого, счет к оплате:* {main_price} KZT"

    return text
