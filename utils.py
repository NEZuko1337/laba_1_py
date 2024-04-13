import random
from user import User
from deliverytime import DeliverySystem


def get_nearest_store_to_user(stores, user_data: User):
    min_data = float("inf")
    for store in stores:
        min_data = min(min_data,
                       DeliverySystem.calculate_delivery_time(store_coords=store.coords, user_coords=user_data.coords))
    print(min_data)
    for store in stores:
        if float(min_data) == DeliverySystem.calculate_delivery_time(store_coords=store.coords, user_coords=user_data.coords):
            return store.get_store_id()
    return None


def random_cancelled_work():
    number = random.randint(1, 10)
    if number == 1:
        return "Курьер не пришел"
    return None
