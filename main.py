from provider import Provider
from store import Store
from user import User
from item import Item
from courier import Courier
from storekeeper import Storekeeper


def main():
    store = Store(store_id="73645", coords=(0, 0), stocks=[])
    provider_35473758_and_9856437_items = [
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="9856437", name="Клавиатура", cost=4200),
    ]
    provider_345_items = [
        Item(store_id=None, provider_id="345", name="Фен", cost=5200),
        Item(store_id=None, provider_id="345", name="Фен", cost=5200),
        Item(store_id=None, provider_id="345", name="Фен", cost=5200),
        Item(store_id=None, provider_id="345", name="Фен", cost=3200),
        Item(store_id=None, provider_id="345", name="Клавиатура", cost=1000),
        Item(store_id=None, provider_id="345", name="Вентилятор", cost=4300),
        Item(store_id=None, provider_id="345", name="Вентилятор", cost=4300),
        Item(store_id=None, provider_id="345", name="Ноутбук", cost=45200),
    ]
    # До пополнения
    # print(store)
    provider = Provider(stock=provider_35473758_and_9856437_items)
    provider2 = Provider(stock=provider_345_items)
    store.send_request(provider=provider, order=provider_35473758_and_9856437_items)
    # После пополнения
    # print(store)

    # Курьер и кладовщик работают независимо друг от друга
    courier = Courier(username="Nilson", shift=2)
    courier1 = Courier(username="Java", shift=3)
    courier2 = Courier(username="Andrew", shift=1)
    courier3 = Courier(username="Anatoly", shift=12)

    storekeeper = Storekeeper(username="Wonderson", shift=7)
    storekeeper1 = Storekeeper(username="Sherlock", shift=5)

    store.take_to_work(storekeeper)
    store.take_to_work(storekeeper1)
    store.take_to_work(courier)
    store.take_to_work(courier1)
    store.take_to_work(courier2)
    store.take_to_work(courier3)
    # Появление пользователя
    items_to_order = [
        Item(store_id="73645", provider_id="35473758", name="Фен", cost=5200),
        Item(store_id="73645", provider_id="35473758", name="Фен", cost=5200),
        Item(store_id="73645", provider_id="9856437", name="Чемодан", cost=4200),
        Item(store_id="73645", provider_id="345", name="Фен", cost=5200),
        Item(store_id="73645", provider_id="345", name="Ноутбук", cost=45200),
    ]
    items_to_order2 = [
        Item(store_id="73645", provider_id="35473758", name="Фен", cost=5200),
        Item(store_id="73645", provider_id="35473758", name="Фен", cost=5200),
        Item(store_id="73645", provider_id="35473758", name="Фен", cost=5200),
        Item(store_id="73645", provider_id="345", name="Вентилятор", cost=4300),
        Item(store_id="73645", provider_id="9856437", name="Клавиатура", cost=4200),

    ]
    user = User(username="Andrew", coords=(15, 45))
    user2 = User(username="Anton", coords=(73, 44))
    user_order = user.make_order(items_to_order)
    user_order2 = user2.make_order(items_to_order2)

    # Тут идет основное принятие заказа, плюс формирование, того, чего не хвататет
    items_that_we_dont_have_in_store = store.take_order(user_order=user_order, user=user)
    items_that_we_dont_have_in_store_for_second_order = store.take_order(user_order=user_order2, user=user2)

    # Если товара нет, то просим у другого провайдера этот товар
    if items_that_we_dont_have_in_store:
        to_buy = []
        for item in items_that_we_dont_have_in_store:
            user_order.items.remove(item)
            to_buy.append(
                Item(
                    store_id=None,
                    provider_id=item.provider_id,
                    name=item.name,
                    cost=item.cost
                )
            )
        pr = Provider(stock=provider_35473758_and_9856437_items)
        prov = Provider(stock=provider_345_items)
        store.send_request(provider=prov, order=to_buy)
        store.send_request(provider=pr, order=to_buy)

    if items_that_we_dont_have_in_store_for_second_order:
        to_buy = []
        for item in items_that_we_dont_have_in_store_for_second_order:
            user_order2.items.remove(item)
            to_buy.append(
                Item(
                    store_id=None,
                    provider_id=item.provider_id,
                    name=item.name,
                    cost=item.cost
                )
            )
        pr = Provider(stock=provider_35473758_and_9856437_items)
        prov = Provider(stock=provider_345_items)
        store.send_request(provider=prov, order=to_buy)
        store.send_request(provider=pr, order=to_buy)

    # Пополняемся старым товаром
    store.send_request(provider=provider, order=items_to_order)
    store.send_request(provider=provider, order=items_to_order2)
    store.send_request(provider=provider2, order=items_to_order)
    store.send_request(provider=provider2, order=items_to_order2)

    store.delivery_items(user_order=user_order, user=user)
    store.delivery_items(user_order=user_order2, user=user2)

    store.end_shift(worker=user_order.courier, user=user)
    store.end_shift(worker=user_order.picker, user=user)
    store.end_shift(worker=user_order2.courier, user=user2)
    store.end_shift(worker=user_order2.picker, user=user2)

    print()
    print(user_order)
    print()
    print(user_order2)
    print()
    user_order3 = user2.make_order(items_to_order2)
    items_that_we_dont_have_for_third_time = store.take_order(user_order=user_order3, user=user2)
    if items_that_we_dont_have_for_third_time:
        to_buy = []
        for item in items_that_we_dont_have_for_third_time:
            user_order.items.remove(item)
            to_buy.append(
                Item(
                    store_id=None,
                    provider_id=item.provider_id,
                    name=item.name,
                    cost=item.cost
                )
            )
        pr = Provider(stock=provider_35473758_and_9856437_items)
        prov = Provider(stock=provider_345_items)
        store.send_request(provider=prov, order=to_buy)
        store.send_request(provider=pr, order=to_buy)

    store.send_request(provider=provider, order=items_to_order2)
    store.send_request(provider=provider2, order=items_to_order2)

    store.delivery_items(user_order=user_order3, user=user2)

    store.end_shift(worker=user_order3.courier, user=user2)
    store.end_shift(worker=user_order3.picker, user=user2)

    print()
    print(user_order3)


if __name__ == '__main__':
    main()
# import time
#
#
# def time_decorator(fn):
#     def inner(*args, **kwargs):
#         start_time = time.time()
#         res = fn(*args, **kwargs)
#         end_time = time.time()
#         dt = end_time - start_time
#         print(dt)
#         return res
#     return inner
#
#
# @time_decorator
# def fn(n):
#     sum = 0
#     for i in range(n):
#         sum += i
#     return sum
#
#
# print("Время работы:")
# fn(10000000)


# def decorator(fn):
#     def wrapper(*args, **kwargs):
#         print(f"{fn.__name__} - Название функции\n{args} - неименнованные аргументы\n{kwargs} - именнованные аргументы")
#         res = fn(*args, **kwargs)
#         return res
#     return wrapper
#
#
# @decorator
# def test_fn(*args, **kwargs):
#     print("Я функция, обернутая в декоратор")
#
#
# test_fn(1,2,3,4,5, a=15, b=17)