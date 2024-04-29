import time
from typing import List, Tuple

from courier import Courier
from deliverytime import DeliverySystem
from item import Item
from order import Order
from provider import Provider
from storekeeper import Storekeeper
from user import User
from worker import Worker
from utils import random_cancelled_work


class Store:
    def __init__(self, store_id, coords: Tuple[int, int], stocks: List[Item], work_time: str):
        self.__store_id = store_id
        self.coords = coords
        self.__stocks = stocks
        self.__orders: List[Order] = []
        self.__workers: List[Worker] = []
        self.work_time = work_time
        self.__store_status = "Работает"
        self.predicted_delivery_time = None

    def get_store_id(self):
        return self.__store_id

    def get_store_status(self):
        return self.__store_status

    def set_store_status(self, status):
        self.__store_status = status

    def send_request(self, provider: Provider, order: List[Item]) -> None:
        resp = provider.send_order(order)
        for item in resp:
            item.store_id = self.__store_id
        provider.update_stocks()
        self.__stocks.extend(resp)

    # принять заказ и начать его обрабатывать
    def take_order(self, user_order: Order, user: User):
        # Меняем статус заказа
        if not self.__stocks:
            user_order.delivery_status = "Ошибка, нет товаров у поставщика, нечего заказывать!"
            user_order.items = []
            return
        not_in_store_items = []
        courier, storekeeper = self.get_worker(user_order=user_order, user=user)
        if courier and storekeeper:
            user_order.delivery_status = "Принят"
            for item in user_order.items:
                if item not in self.__stocks:
                    not_in_store_items.append(item)
                else:
                    self.__stocks.remove(item)

            self.set_courier(courier=courier, user_order=user_order)
            self.set_storekeeper(storekeeper=storekeeper, user_order=user_order)
            rndm = random_cancelled_work()
            if not_in_store_items:
                print(
                    f"Доставка {user_order.unique_id}:\n К сожалению некоторых товаров нет в наличии, мы можем доставить к вам все, кроме: {[item for item in not_in_store_items]}")
                user_choise = input(
                    f" Хотите ли вы {user.username}, чтобы мы доставили к вам имеющиеся товары (да/нет)\n")
                while user_choise.lower not in ["нет", "да"]:
                    if user_choise.lower() == "нет":
                        user_order.delivery_status = "Отменен пользователем"
                        user_order.picker = None
                        user_order.courier = None
                        self.__orders.append(user_order)
                        return "ERROR", not_in_store_items
                    elif user_choise.lower() == "да":
                        storekeeper.get_order(user_order)
                        # Считаем время доставки(оверол)
                        # На один товар 45 секунд
                        storekeeper_time = len(user_order.items) * 45

                        # Время доставки по О.У как в ТЗ
                        delivery_time = DeliverySystem.calculate_delivery_time(self.coords, user.coords)
                        if rndm == "Курьер не пришел":
                            print("Курьер не пришел! Мы обязательно примем меры, к сожалению заказ будет отменен")
                            user_order.delivery_status = "Курьер не явился на выдачу"
                            user_order.delivery_time = None
                            courier.set_status("Уволен")
                            self.__orders.append(user_order)
                            return None, None
                        else:
                            courier.get_order(user_order)

                        # Итоговое время доставки переведенное на человеческий вид
                        correct_delivery_time = time.ctime(int(time.time() + delivery_time + storekeeper_time))
                        print(f"Ваш заказ будет доставлен в {correct_delivery_time}")
                        user_order.delivery_time = correct_delivery_time
                        self.__orders.append(user_order)
                        break

                    else:
                        user_choise = input(f"Можно вводить только (да/нет)\n")
            else:
                storekeeper.get_order(user_order)
                # Считаем время доставки(оверол)
                # На один товар 45 секунд
                storekeeper_time = len(user_order.items) * 45

                # Время доставки по О.У как в ТЗ
                delivery_time = DeliverySystem.calculate_delivery_time(self.coords, user.coords)
                if rndm == "Курьер не пришел":
                    print("Курьер не пришел! Мы обязательно примем меры, к сожалению заказ будет отменен")
                    user_order.delivery_status = "Курьер не явился на выдачу"
                    user_order.delivery_time = None
                    courier.set_status("Уволен")
                    self.__orders.append(user_order)
                    return None, None
                else:
                    courier.get_order(user_order)

                # Итоговое время доставки переведенное на человеческий вид
                correct_delivery_time = time.ctime(int(time.time() + delivery_time + storekeeper_time))
                print(f"Ваш заказ будет доставлен в {correct_delivery_time}")
                user_order.delivery_time = correct_delivery_time
                self.__orders.append(user_order)

        else:
            user_order.delivery_status = "Ошибка"
            print(f"На заказ {user_order.unique_id} данный момент нет доступных сотрудников")
            return None, None

        return "Success", not_in_store_items

    # выдать заказ курьеру
    def set_courier(self, courier: Courier, user_order: Order) -> None:
        user_order.courier = courier

    def delivery_items(self, user_order: Order, user: User):
        # Доставка заказа
        if user_order.delivery_status != "Курьер не явился на выдачу":
            if user_order.picker and user_order.courier is not None:
                print(f"Курьер '{user_order.courier}' отправляется к пользователю {user.username}...")
                print(f"Заказ доставлен пользователю {user.username}.")
                user.take_order(user_order)
                user_order.delivery_status = "Доставлен"
                print(f"Курьер '{user_order.courier}' возвращается обратно...")

    # выдать заказ кладовщику
    def set_storekeeper(self, storekeeper: Storekeeper, user_order: Order) -> None:
        user_order.picker = storekeeper

    def take_to_work(self, worker: Worker):
        if worker.get_store_id() != self.__store_id:
            worker.set_store_id(self.__store_id)
        if worker not in self.__workers:
            self.__workers.append(worker)

    # взять работника к себе и дать ему смену
    def get_worker(self, user_order: Order, user: User):
        available_couriers = [worker for worker in self.__workers if
                              isinstance(worker, Courier) and worker.get_status() == "Свободен"]
        available_storekeepers = [worker for worker in self.__workers if
                                  isinstance(worker, Storekeeper) and worker.get_status() == "Свободен"]
        if available_couriers and available_storekeepers:
            time_for_delivery = (DeliverySystem.calculate_delivery_time(store_coords=self.coords,
                                                                        user_coords=user.coords)) / 60
            time_for_return = (DeliverySystem.wait_for_return(courier_coords=user.coords,
                                                              store_coords=self.coords)) / 60
            overall_time_for_courier = time_for_delivery + time_for_return
            courier, storekeeper = None, None
            for cur in available_couriers:
                if cur.get_shift() * 60 < overall_time_for_courier:
                    continue
                else:
                    cur.set_status("Занят")
                    courier = cur
                    break
            for storkep in available_storekeepers:
                if storkep.get_shift() * 60 < (45 * len(user_order.items)) / 60:
                    continue
                else:
                    storkep.set_status("Занят")
                    storekeeper = storkep
                    break

            if courier and storekeeper:
                return courier, storekeeper
            else:
                return None, None
        else:
            return None, None

    def end_shift(self, worker: Worker, user: User):
        if worker is not None and worker.get_status() != "Уволен":
            if isinstance(worker, Courier):
                print("Курьер вернулся на склад")
                time1 = (DeliverySystem.calculate_delivery_time(self.coords, user_coords=user.coords)) / 60
                time2 = (DeliverySystem.wait_for_return(courier_coords=user.coords, store_coords=self.coords)) / 60

                overall_time = time1 + time2
                hours = overall_time // 60
                minutes = overall_time % 60

                if hours != 0:
                    new_h = hours * 60 + minutes
                    worker.set_shift((worker.get_shift() * 60 - new_h) // 60)
                else:
                    worker.set_shift((worker.get_shift() * 60 - minutes) // 60)

                salary = 300 * (overall_time / 60)

                print(
                    f"Время работы курьера {worker.get_username()}: {hours} часов {minutes} минут, за это время он получил {salary} рублей")
                if worker.get_shift() > 0:
                    worker.set_status("Свободен")
                    print(f"На данный момент {worker.get_username()} свободен и готов принимать заказы")
                else:
                    worker.set_status("Закончил рабочий день")
                    print(f"{worker.get_username()} закончил свой рабочий день")
            else:
                orders_handled = [order for order in self.__orders if order.picker == worker]
                total_items = sum(len(order.items) for order in orders_handled)
                time_for_storekeeper = (45 * total_items) / 60
                hours = time_for_storekeeper // 60
                minutes = time_for_storekeeper % 60
                salary = 300 * (time_for_storekeeper / 60)
                print(
                    f"Время работы кладовщика {worker.get_username()}: {hours} часов {minutes} минут, за это время он получил {salary} рублей")
                if hours != 0:
                    new_h = hours * 60 + minutes
                    worker.set_shift((worker.get_shift() * 60 - new_h) // 60)
                else:
                    worker.set_shift((worker.get_shift() * 60 - minutes) // 60)

                if worker.get_shift() > 0:
                    worker.set_status("Свободен")
                    print(f"На данный момент {worker.get_username()} свободен и готов принимать заказы")
                else:
                    worker.set_status("Закончил рабочий день")
                    print(f"{worker.get_username()} закончил свой рабочий день")
        else:
            if worker is not None:
                print(f"Рабочий {worker.get_username()} уволен из-за невыполнения своей работы")

    def replenish_store_with_missing_items(
            self,
            items_that_we_dont_have_in_store: Tuple[str, list],
            user_order: Order,
            provider_stock):
        if items_that_we_dont_have_in_store is not None:
            if items_that_we_dont_have_in_store[0] != "ERROR":
                if items_that_we_dont_have_in_store[1] is not None:
                    # Если товара нет, то просим у другого провайдера этот товар
                    to_buy = []
                    for item in items_that_we_dont_have_in_store[1]:
                        if item in user_order.items:
                            user_order.items.remove(item)
                            to_buy.append(
                                Item(
                                    store_id=None,
                                    provider_id=item.provider_id,
                                    name=item.name,
                                    cost=item.cost
                                )
                            )
                        else:
                            to_buy.append(
                                Item(
                                    store_id=None,
                                    provider_id=item.provider_id,
                                    name=item.name,
                                    cost=item.cost
                                )
                            )
                    provider = Provider(stock=provider_stock)
                    self.send_request(provider=provider, order=to_buy)
            else:
                to_buy = []
                for item in items_that_we_dont_have_in_store[1]:
                    to_buy.append(
                        Item(
                            store_id=None,
                            provider_id=item.provider_id,
                            name=item.name,
                            cost=item.cost
                        )
                    )
                provider = Provider(stock=provider_stock)
                self.send_request(provider=provider, order=to_buy)

    def get_status_of_work(self, items: Tuple[str, list]) -> bool:
        if items is not None:
            return False if items[0] == "ERROR" else True

    def get_orders(self):
        return self.__orders

    def get_stocks(self):
        return self.__stocks

    def pre_order_time(self, user: User) -> None:
        print(
            f"Примерное время доставки заказа от магазина {self.__store_id} - {(DeliverySystem.calculate_delivery_time(store_coords=self.coords, user_coords=user.coords) / 60)} минут")

    def __str__(self):
        return f'{[f"{item.name}/его стоимость: {item.cost}р/айди магазина: {item.store_id}/поставщик: {item.provider_id}/" for item in self.__stocks]}'
