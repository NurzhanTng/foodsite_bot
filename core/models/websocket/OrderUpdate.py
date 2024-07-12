from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class OrderUpdate:
    type: str
    order_id: int
    status: str
    delivery_id: int
    rejected_text: str


class OrderUpdateSerializer:
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> OrderUpdate:
        return OrderUpdate(
            type=data.get('type'),
            order_id=data.get('order_id'),
            status=data.get('status'),
            delivery_id=data.get('delivery_id'),
            rejected_text=data.get('rejected_text')
        )

    @staticmethod
    def to_dict(order_update: OrderUpdate) -> Dict[str, Any]:
        return {
            'type': order_update.type,
            'order_id': order_update.order_id,
            'status': order_update.status,
            'delivery_id': order_update.delivery_id,
            'rejected_text': order_update.rejected_text
        }