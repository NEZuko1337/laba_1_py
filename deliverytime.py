class DeliverySystem:
    @staticmethod
    def calculate_delivery_time(store_coords: tuple, user_coords: tuple) -> float:
        # Расчет времени доставки
        distance = abs(store_coords[0] - user_coords[0]) + abs(store_coords[1] - user_coords[1])
        delivery_time = distance * 30 + 60 * 2  # Время в секундах
        return delivery_time

    @staticmethod
    def wait_for_return(courier_coords: tuple, store_coords: tuple) -> float:
        # Время возвращения курьера на склад
        distance = abs(store_coords[0] - courier_coords[0]) + abs(store_coords[1] - courier_coords[1])
        return distance * 30 + 60  # Время в секундах
