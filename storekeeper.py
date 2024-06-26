from worker import Worker


class Storekeeper(Worker):
    def __init__(self, username, shift):
        super().__init__(username=username, shift=shift)
        self.__status = "Свободен"
        self.__store_id = ""

    def get_shift(self):
        return self.shift

    def get_username(self):
        return self.username

    def set_shift(self, minutes):
        self.shift = minutes

    def get_order(self, order):
        print(f"Ваш заказ принят, кладовщик {self.username} собирает ваш заказ")
        print("...")
        print("Кладовщик собрал ваш заказ и ждет курьера, чтобы выдать заказ")

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_store_id(self):
        return self.__store_id

    def set_store_id(self, store_id):
        self.__store_id = store_id
