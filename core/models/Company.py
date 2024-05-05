from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Company:
    id: int
    delivery_layers: list
    products_on_stop: list
    additions_on_stop: list
    name: str
    link: str
    open_time: str
    close_time: str
    address: dict
    address_link: str
    updated_at: str
    created_at: str
    manager: str


class CompanySerializer:
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Company:
        address_data = data.get('address', {})
        return Company(
            id=data.get('id'),
            delivery_layers=data.get('delivery_layers', []),
            products_on_stop=data.get('products_on_stop', []),
            additions_on_stop=data.get('additions_on_stop', []),
            name=data.get('name'),
            link=data.get('link'),
            open_time=data.get('open_time'),
            close_time=data.get('close_time'),
            address={
                'lat': address_data.get('lat'),
                'long': address_data.get('long'),
                'parsed': address_data.get('parsed')
            },
            address_link=data.get('address_link'),
            updated_at=data.get('updated_at'),
            created_at=data.get('created_at'),
            manager=data.get('manager')
        )

    @staticmethod
    def to_dict(company: Company) -> Dict[str, Any]:
        return {
            'id': company.id,
            'delivery_layers': company.delivery_layers,
            'products_on_stop': company.products_on_stop,
            'additions_on_stop': company.additions_on_stop,
            'name': company.name,
            'link': company.link,
            'open_time': company.open_time,
            'close_time': company.close_time,
            'address': company.address,
            'address_link': company.address_link,
            'updated_at': company.updated_at,
            'created_at': company.created_at,
            'manager': company.manager
        }
