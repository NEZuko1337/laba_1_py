import random
import time
from typing import List, Tuple

from item import Item
from user import User
from deliverytime import DeliverySystem


def store_working_now(store) -> bool:
    start_working_time, end_working_time = translate_raw_time_to_minutes(store.work_time)
    raw_time = time.localtime()
    order_time = time.strftime("%H:%M", raw_time)
    translated_order_time = translate_order_time_to_minutes(order_time)
    if start_working_time <= translated_order_time <= end_working_time:
        return True
    return False


def get_nearest_store_id(stores, user_order: List[Item], user_data: User):
    min_delivery_time: List[Tuple[str, float]] = []
    for store in stores:
        if store_working_now(store):
            # Получили время в секундах
            time_for_order = DeliverySystem.calculate_delivery_time(store_coords=store.coords, user_coords=user_data.coords)

            # Текущий товар магазина
            store_stocks = store.get_stocks()
            copy_stock = store_stocks.copy()

            if store_stocks:
                for user_order_item in user_order:
                    for item in copy_stock:
                        if (user_order_item.name == item.name) and (user_order_item.cost == item.cost) and (
                                user_order_item.provider_id == item.provider_id):
                            copy_stock.remove(item)
                            break
                    else:
                        # Решил хоть как-то нивелировать, то что товара нет в магазине,
                        # поэтому если его нет, то + 60 сек к доставке до юзера
                        time_for_order += 60
            else:
                # Случай если стоки вообще пустые
                time_for_order += len(user_order) * 60

            min_delivery_time.append((store.get_store_id(), time_for_order))
    return min(min_delivery_time, key=lambda x: x[1])[0] if min_delivery_time != [] else -1


def set_store_for_order(arg: int, items_to_order) -> None:
    if arg == -1:
        raise "К сожалению все склады сейчас закрыты, невозможно создать заказ"
    for el in items_to_order:
        el.store_id = arg


def random_cancelled_work():
    number = random.randint(1, 10)
    if number == 1:
        return "Курьер не пришел"
    return None


def translate_raw_time_to_minutes(raw_time: str) -> list[int]:
    start_time, end_time = [time.strip() for time in raw_time.split("-")]
    start_hours, start_minutes = map(int, start_time.split(":"))
    end_hours, end_minutes = map(int, end_time.split(":"))

    start_minutes_total = start_hours * 60 + start_minutes
    end_minutes_total = end_hours * 60 + end_minutes

    return [start_minutes_total, end_minutes_total]


def translate_order_time_to_minutes(order_time: str) -> float:
    hours, minutes = map(int, order_time.split(":"))
    minutes_total = hours * 60 + minutes

    return minutes_total


def get_nearest_store_by_nearest_id(list_of_stores, nearest_store_id):
    for store in list_of_stores:
        if store.get_store_id() == nearest_store_id:
            print(f"Ближайший к юзеру магазин - {nearest_store_id}")
            return store
    return None
