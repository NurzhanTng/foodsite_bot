from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Product:
    id: int
    category_id: int
    image_url: str
    name: str
    description: Optional[str]
    price: Optional[float]
    currency: str
    modifiers: List[dict]
    additions: List[dict]
    tags: List[dict]
    on_stop: bool


@dataclass
class ProductSerializer:
    @staticmethod
    def to_dict(product: Product) -> Dict[str, Any]:
        return {
            "id": product.id,
            "category_id": product.category_id,
            "image_url": product.image_url,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "currency": product.currency,
            "modifiers": [],  # Convert modifiers to dict if needed
            "additions": [],  # Convert additions to dict if needed
            "tags": [],  # Convert tags to dict if needed
            "on_stop": product.on_stop
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Product:
        return Product(
            id=data['id'],
            category_id=data['category_id'],
            image_url=data['image_url'],
            name=data['name'],
            description=data['description'],
            price=data['price'],
            currency=data['currency'],
            modifiers=data['modifiers'],
            additions=data['additions'],
            tags=data['tags'],
            on_stop=data['on_stop']
        )
