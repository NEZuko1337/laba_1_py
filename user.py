import time
import uuid

from typing import List
from item import Item
from order import Order


class User:
    def __init__(self, username: str, coords: tuple[int, int]):
        self.username = username
        self.coords = coords

    # сделать заказ
    def make_order(self, items: List[Item]):
        return Order(
            unique_id=str(uuid.uuid4()),
            delivery_status="Новый",
            items=items,
            creation_time=time.ctime(int(time.time())),
            delivery_time=None,
            picker=None,
            courier=None
        )

    # забрать заказ
    def take_order(self, user_order: Order):
        print(f"{self.username} забрал заказ {user_order.unique_id}")
