from dataclasses import dataclass
from typing import List

from storekeeper import Storekeeper
from courier import Courier
from item import Item



@dataclass
class Order:
    # Что находится в заказе? Статус доставки, список товаров, время создания-время доставки, кто собирал-доставлял
    unique_id: int | str
    delivery_status: str
    items: List[Item]
    creation_time: float| int | None | str
    delivery_time: float | None | int | str
    picker: Storekeeper | None
    courier: Courier | None

    def __str__(self):
        return f"Айди доставки: {self.unique_id}\n Статус доставки товара: {self.delivery_status}\n Предметы: {[item.name + '(' + str(item.cost) + 'р.' + ')' + ' - ' + str(item.provider_id) for item in self.items]}\n Время создания заказа: {self.creation_time}\n Время доставки заказа: {self.delivery_time}\n Сборщик: {self.picker}\n Курьер: {self.courier}"
