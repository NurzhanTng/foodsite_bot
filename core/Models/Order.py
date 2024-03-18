from core.Models.Product import Product, ProductSerializer
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class OrderProduct:
    product: Product
    amount: int
    client_comment: str
    price: int
    product_id: int
    active_modifier: List[Dict[str, Any]]
    additions: List[Dict[str, Any]]


@dataclass
class OrderProductSerializer:
    @staticmethod
    def to_dict(order_product: OrderProduct) -> Dict[str, Any]:
        return {
            "product": ProductSerializer.to_dict(order_product.product),
            "amount": order_product.amount,
            "client_comment": order_product.client_comment,
            "price": order_product.price,
            "product_id": order_product.product_id,
            "active_modifier": order_product.active_modifier,
            "additions": order_product.additions
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> OrderProduct:
        product_dict = data.pop('product')
        product = ProductSerializer.from_dict(product_dict)
        return OrderProduct(
            product=product,
            amount=data['amount'],
            client_comment=data['client_comment'],
            price=data['price'],
            product_id=data['product_id'],
            active_modifier=data['active_modifier'],
            additions=data['additions']
        )


@dataclass
class Order:
    id: int
    status: str
    products: List[OrderProduct]
    client_id: int
    bonus_used: int
    user_name: str
    address: dict
    company_id: int
    exact_address: str
    phone: str
    client_comment: str
    actions: List[dict]


@dataclass
class OrderSerializer:
    @staticmethod
    def to_dict(order: Order) -> Dict[str, Any]:
        return {
            "id": order.id,
            "status": order.status,
            "products": [OrderProductSerializer.to_dict(product) for product in order.products],
            "client_id": order.client_id,
            "bonus_used": order.bonus_used,
            "user_name": order.user_name,
            "address": order.address,
            "company_id": order.company_id,
            "exact_address": order.exact_address,
            "phone": order.phone,
            "client_comment": order.client_comment,
            "actions": order.actions
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Order:
        products_data = data.pop('products', [])
        products = [OrderProductSerializer.from_dict(product_data) for product_data in products_data]
        return Order(
            id=data['id'],
            status=data['status'],
            products=products,
            client_id=data['client_id'],
            bonus_used=data['bonus_used'],
            user_name=data['user_name'],
            address=data['address'],
            company_id=data['company_id'],
            exact_address=data['exact_address'],
            phone=data['phone'],
            client_comment=data['client_comment'],
            actions=data['actions']
        )
