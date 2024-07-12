from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Address:
    lat: float
    long: float
    parsed: str
    exact_address: str


@dataclass
class OrderData:
    order_id: int
    client_id: str
    delivery_id: Optional[int]
    status: str
    bonus_used: bool
    user_name: str
    address: Address
    exact_address: str
    phone: str
    kaspi_phone: str
    client_comment: str
    company_id: int
    done_time: Optional[str]
    bonus_amount: int
    delivery_price: str
    updated_at: str
    created_at: str


@dataclass
class NewOrder:
    type: str
    order_data: OrderData


class NewOrderSerializer:
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> NewOrder:
        address_data = data['order_data'].get('address', {})
        address = Address(
            lat=address_data.get('lat'),
            long=address_data.get('long'),
            parsed=address_data.get('parsed'),
            exact_address=address_data.get('exact_address')
        )

        order_data = OrderData(
            order_id=data['order_data'].get('order_id'),
            client_id=data['order_data'].get('client_id'),
            delivery_id=data['order_data'].get('delivery_id'),
            status=data['order_data'].get('status'),
            bonus_used=data['order_data'].get('bonus_used'),
            user_name=data['order_data'].get('user_name'),
            address=address,
            exact_address=data['order_data'].get('exact_address'),
            phone=data['order_data'].get('phone'),
            kaspi_phone=data['order_data'].get('kaspi_phone'),
            client_comment=data['order_data'].get('client_comment'),
            company_id=data['order_data'].get('company_id'),
            done_time=data['order_data'].get('done_time'),
            bonus_amount=data['order_data'].get('bonus_amount'),
            delivery_price=data['order_data'].get('delivery_price'),
            updated_at=data['order_data'].get('updated_at'),
            created_at=data['order_data'].get('created_at')
        )

        return NewOrder(
            type=data.get('type'),
            order_data=order_data
        )

    @staticmethod
    def to_dict(new_order: NewOrder) -> Dict[str, Any]:
        return {
            'type': new_order.type,
            'order_data': {
                'order_id': new_order.order_data.order_id,
                'client_id': new_order.order_data.client_id,
                'delivery_id': new_order.order_data.delivery_id,
                'status': new_order.order_data.status,
                'bonus_used': new_order.order_data.bonus_used,
                'user_name': new_order.order_data.user_name,
                'address': {
                    'lat': new_order.order_data.address.lat,
                    'long': new_order.order_data.address.long,
                    'parsed': new_order.order_data.address.parsed,
                    'exact_address': new_order.order_data.address.exact_address,
                },
                'exact_address': new_order.order_data.exact_address,
                'phone': new_order.order_data.phone,
                'kaspi_phone': new_order.order_data.kaspi_phone,
                'client_comment': new_order.order_data.client_comment,
                'company_id': new_order.order_data.company_id,
                'done_time': new_order.order_data.done_time,
                'bonus_amount': new_order.order_data.bonus_amount,
                'delivery_price': new_order.order_data.delivery_price,
                'updated_at': new_order.order_data.updated_at,
                'created_at': new_order.order_data.created_at
            }
        }