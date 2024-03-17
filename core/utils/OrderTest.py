import random

from aiogram.filters.callback_data import CallbackData


class Order(CallbackData, prefix='order'):
    products: list[dict]
    client_id: int
    bonus_used: bool
    bonus_amount: int
    user_name: str
    long: float
    lat: float
    exact_address: str
    phone: str
    client_comment: str
    kaspi_phone: str
    is_delivery: bool
    status: str
    id: int


def order_dict_to_object(order: dict) -> Order:
    return Order(
        id=order['id'],
        products=order['products'],
        client_id=order['client_id'],
        bonus_used=order['bonus_used'],
        bonus_amount=order['bonus_amount'],
        user_name=order['user_name'],
        long=order['loc'],
        lat=order['lat'],
        exact_address=order['exact_address'],
        phone=order['phone'],
        client_comment=order['client_comment'],
        kaspi_phone=order['kaspi_phone'],
        is_delivery=order['is_delivery'],
        status=order['status']
    )


def order_to_dict(order: Order) -> dict:
    return {
        "products": order.products,
        "client_id": order.client_id,
        "bonus_used": order.bonus_used,
        "bonus_amount": order.bonus_amount,
        "user_name": order.user_name,
        "loc": order.long,
        "lat": order.lat,
        "exact_address": order.exact_address,
        "phone": order.phone,
        "client_comment": order.client_comment,
        "kaspi_phone": order.kaspi_phone,
        "is_delivery": order.is_delivery,
        "status": order.status,
        "id": order.id
    }


class OrderTest:
    def __init__(self):
        self.orders: dict[int, list[Order]] = {}
        self.all_product = [
            {'id': 1, 'category_id': 1,
             'image_url': 'https://eda.yandex.ru/images/3490335/6a1ccf7e5ce90b8e3f1a24ff3b1720ff-680x500.jpeg',
             'name': 'Свиные ребра в пивной глазури с салатом и соусом Сальса',
             'description': 'Свиные ребра в пивной глазури с салатом и соусом Сальса', 'price': 3300,
             'currency': 'KZT', 'modifiers': [], 'additions': [],
             'tags': [{'name': '🧑\u200d🍳 Выбор шефа', 'tag_color': '#1B4255'},
                      {'name': '🔥 Острое', 'tag_color': '#000000'}], 'on_stop': False},
            {'id': 2, 'category_id': 1,
             'image_url': 'https://lobsterhouse.ru/wp-content/uploads/2/b/3/2b3e420d76050fa1a1cdfe31be639254.jpeg',
             'name': 'Кальмар в сливочном соусе', 'description': 'Кальмар в сливочном соусе',
             'price': 3300, 'currency': 'KZT', 'modifiers': [], 'additions': [], 'tags': [],
             'on_stop': False},
            {'id': 3, 'category_id': 1,
             'image_url': 'https://sun9-63.userapi.com/zXXNsZm9UcK-w9b9Y_lpWSiN2cHukEOd6vcFGw/fUS2i4QvMpU.jpg',
             'name': 'Филе утиной грудки с соусом из смородины и пюре батата',
             'description': 'Филе утиной грудки с соусом из смородины и пюре батата',
             'price': 2900, 'currency': 'KZT', 'modifiers': [], 'additions': [],
             'tags': [], 'on_stop': False},
            {'id': 4, 'category_id': 1, 'image_url': 'https://sludsky.ru/images/prods/big661.jpg',
             'name': 'Язык с запеченным картофелем', 'description': 'Язык с запеченным картофелем',
             'price': None, 'currency': 'KZT', 'modifiers': [
                {'id': 2, 'price': 3490, 'currency': 'KZT', 'name': 'Маленькая порция 150гр',
                 'on_stop': False},
                {'id': 4, 'price': 4900, 'currency': 'KZT', 'name': 'Большая порция 300гр',
                 'on_stop': False}], 'additions': [
                {'id': 1, 'price': 350, 'currency': 'KZT', 'name': 'Соус тартар', 'on_stop': False},
                {'id': 2, 'price': 250, 'currency': 'KZT', 'name': 'Соус чили', 'on_stop': False}],
             'tags': [{'name': '🔥 Острое', 'tag_color': '#000000'}], 'on_stop': False},
            {'id': 5, 'category_id': 2,
             'image_url': 'https://webassets.cyranecloud.com/dhh/Steak-Burger.jpg.jpg',
             'name': 'Бургер с котлетой из мраморной говядины с томатным джемом', 'description': '',
             'price': 2390, 'currency': 'KZT', 'modifiers': [], 'additions': [],
             'tags': [{'name': '🧑\u200d🍳 Выбор шефа', 'tag_color': '#1B4255'}], 'on_stop': False},
            {'id': 6, 'category_id': 2,
             'image_url': 'https://s3.amazonaws.com/images.ecwid.com/images/29352200/3360832319.jpg',
             'name': 'Бургер с куриной котлетой и свежими овощами', 'description': '', 'price': 2090,
             'currency': 'KZT', 'modifiers': [], 'additions': [], 'tags': [], 'on_stop': False},
            {'id': 7, 'category_id': 3,
             'image_url': 'https://s3.amazonaws.com/images.ecwid.com/images/29352200/3360832319.jpg',
             'name': 'Бургер с куриной котлетой и свежими овощами', 'description': '', 'price': 2090,
             'currency': 'KZT', 'modifiers': [], 'additions': [
                {'id': 1, 'price': 350, 'currency': 'KZT', 'name': 'Соус тартар', 'on_stop': False},
                {'id': 2, 'price': 250, 'currency': 'KZT', 'name': 'Соус чили', 'on_stop': False}],
             'tags': [{'name': '🧑\u200d🍳 Выбор шефа', 'tag_color': '#1B4255'},
                      {'name': '🔥 Острое', 'tag_color': '#000000'}], 'on_stop': False},
            {'id': 8, 'category_id': 3,
             'image_url': 'https://s3.amazonaws.com/images.ecwid.com/images/29352200/3360832319.jpg',
             'name': 'Бургер с куриной котлетой и свежими овощами', 'description': '', 'price': 2090,
             'currency': 'KZT', 'modifiers': [], 'additions': [], 'tags': [], 'on_stop': False},
            {'id': 9, 'category_id': 4,
             'image_url': 'https://s3.amazonaws.com/images.ecwid.com/images/29352200/3360832319.jpg',
             'name': 'Бургер с куриной котлетой и свежими овощами', 'description': '', 'price': 2090,
             'currency': 'KZT', 'modifiers': [], 'additions': [], 'tags': [], 'on_stop': False},
            {'id': 10, 'category_id': 4,
             'image_url': 'https://s3.amazonaws.com/images.ecwid.com/images/29352200/3360832319.jpg',
             'name': 'Бургер с куриной котлетой и свежими овощами', 'description': '', 'price': 2090,
             'currency': 'KZT', 'modifiers': [], 'additions': [], 'tags': [], 'on_stop': False},
            {'id': 11, 'category_id': 4,
             'image_url': 'https://s3.amazonaws.com/images.ecwid.com/images/29352200/3360832319.jpg',
             'name': 'Бургер с куриной котлетой и свежими овощами', 'description': '', 'price': 2090,
             'currency': 'KZT', 'modifiers': [], 'additions': [], 'tags': [], 'on_stop': False}
        ]

    def create_new_order(self, company_id: int, order: dict | None = None) -> int:
        if self.orders.get(company_id) is None:
            self.orders[company_id] = []

        if order is not None:
            new_order = order_dict_to_object(order)
            self.orders[company_id].append(new_order)
            # print(f'Create new order [self.orders null]: {self.orders}')
            return new_order.id

        max_index = -1
        for key, orders in self.orders.items():
            if orders is None:
                continue
            for order in orders:
                if max_index < order.id:
                    max_index = order.id

        orders = [
            {
                "products": [
                    {
                        "amount": 2,
                        "client_comment": "",
                        "price": 7680,
                        "product_id": 4,
                        "active_modifier": 2,
                        "additions": [
                            1
                        ]
                    },
                    {
                        "amount": 3,
                        "client_comment": "",
                        "price": 9900,
                        "product_id": 2,
                        "active_modifier": None,
                        "additions": []
                    },
                    {
                        "amount": 1,
                        "client_comment": "",
                        "price": 2390,
                        "product_id": 5,
                        "active_modifier": None,
                        "additions": []
                    }
                ],
                'id': max_index + 1,
                "client_id": 1234249296,
                "bonus_used": True,
                "bonus_amount": 1000,
                "user_name": "Nurzhan",
                "status": 'manager_await',
                "loc": 76.942911,
                "lat": 43.256321,
                "exact_address": "\u041a\u0432\u0430\u0440\u0442\u0438\u0440\u0430 42",
                "phone": "+77074862447",
                "client_comment": "",
                "kaspi_phone": "+77074862447",
                "is_delivery": True
            },
            {
                "products": [
                    {
                        "amount": 2,
                        "client_comment": "",
                        "price": 7680,
                        "product_id": 4,
                        "active_modifier": 2,
                        "additions": [
                            1
                        ]
                    },
                    {
                        "amount": 1,
                        "client_comment": "",
                        "price": 2390,
                        "product_id": 5,
                        "active_modifier": None,
                        "additions": []
                    }
                ],
                'id': max_index + 1,
                "client_id": 1234249296,
                "bonus_used": False,
                "bonus_amount": 0,
                "user_name": "Nurzhan",
                "status": 'manager_await',
                "loc": 0,
                "lat": 0,
                "exact_address": "",
                "phone": "+77074862447",
                "client_comment": "",
                "kaspi_phone": "+77074862447",
                "is_delivery": False
            },
            {
                "products": [
                    {
                        "amount": 1,
                        "client_comment": "",
                        "price": 2390,
                        "product_id": 5,
                        "active_modifier": None,
                        "additions": []
                    }
                ],
                'id': max_index + 1,
                "client_id": 1234249296,
                "bonus_used": False,
                "bonus_amount": 0,
                "user_name": "Nurzhan",
                "status": 'manager_await',
                "loc": 76.942911,
                "lat": 43.256321,
                "exact_address": "\u041a\u0432\u0430\u0440\u0442\u0438\u0440\u0430 42",
                "phone": "+77074862447",
                "client_comment": "",
                "kaspi_phone": "+77074862447",
                "is_delivery": True
            }
        ]

        new_order = order_dict_to_object(random.choice(orders))
        self.orders[company_id].append(new_order)
        # print(f'Create new order [self.orders]: {self.orders}')
        return new_order.id

    def get_order_by_id(self, order_id: int) -> Order | None:
        for key, orders in self.orders.items():
            for order in orders:
                if order.id == order_id:
                    return order
        return None

    def change_order_status(self, company_id: int, order_id: int, status: str):
        if self.orders.get(company_id) is None:
            return []
        for order in self.orders.get(company_id):
            if order.id == order_id:
                order.status = status

    def get_order_by_status(self, company_id: int, status: str) -> list[Order]:
        # print(f'get order by status for {company_id}: {status}')
        if self.orders.get(company_id) is None:
            # print(f'self.orders.get(company_id) is None')
            return []
        orders = []
        for order in self.orders.get(company_id):
            if order.status == status:
                orders.append(order)
        # print(f'get order by status result: {orders}')
        return orders
