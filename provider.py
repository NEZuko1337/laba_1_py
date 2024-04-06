from typing import List
from item import Item


# Поставщик
class Provider:
    def __init__(self, stock: List[Item]):
        self.__stock = stock
        self.__current_stock = self.__stock.copy()

    def send_order(self, order_items: List[Item]):
        result = []
        for item in order_items:
            if item in self.__current_stock:
                result.append(item)
                self.__current_stock.remove(item)
        return result

    def update_stocks(self):
        self.__current_stock = self.__stock
