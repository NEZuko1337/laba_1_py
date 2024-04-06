import uuid
from abc import ABC, abstractmethod


class Worker(ABC):
    def __init__(self, username: str, shift: int):
        self.__user_id = uuid.uuid4()
        self.username = username
        self.shift = shift
        self.__status = ""
        self.__store_id = ""

    @abstractmethod
    def get_order(self, order):
        pass

    @abstractmethod
    def get_username(self):
        pass

    # принять заказ, если возможно
    @abstractmethod
    def get_shift(self):
        pass

    @abstractmethod
    def set_shift(self, minutes):
        pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def set_status(self, status):
        pass

    @abstractmethod
    def get_store_id(self):
        pass

    @abstractmethod
    def set_store_id(self, store_id):
        pass

    def __str__(self):
        return f"Юзернейм рабочего: {self.username}"
