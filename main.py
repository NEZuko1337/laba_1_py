import utils

from provider import Provider
from store import Store
from user import User
from item import Item
from courier import Courier
from storekeeper import Storekeeper


def main():
    store1 = Store(store_id="73645", coords=(0, 0), stocks=[], work_time="8:00 - 21:01")
    store2 = Store(
        store_id="746573645",
        coords=(53, 22),
        stocks=[
            Item(store_id="746573645", provider_id="35473758", name="Фен", cost=5200),
            Item(store_id="746573645", provider_id="35473758", name="Фен", cost=5200),
            Item(store_id="746573645", provider_id="9856437", name="Чемодан", cost=4200),
            Item(store_id="746573645", provider_id="9856437", name="Клавиатура", cost=4200),
        ],
        work_time="8:00 - 22:00"
    )
    store3 = Store(
        store_id="7364757875",
        coords=(0, 21),
        stocks=[
            Item(store_id="7364757875", provider_id="345", name="Фен", cost=5200),
        ],
        work_time="8:00 - 22:00"
    )
    store4 = Store(store_id="73649839845", coords=(88, 21), stocks=[], work_time="8:00 - 22:00")

    # Появление пользователя
    user = User(username="Andrew", coords=(15, 45))
    items_to_order = [
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="9856437", name="Чемодан", cost=4200),
        Item(store_id=None, provider_id="345", name="Фен", cost=5200),
        Item(store_id=None, provider_id="345", name="Ноутбук", cost=45200),
        Item(store_id=None, provider_id="9856437", name="Клавиатура", cost=4200),
    ]

    # Список магазинов
    list_of_stores = [store1, store2, store3, store4]
    # Получаю самый лучший id магазина
    nearest_store_id = utils.get_nearest_store_id(
        stores=list_of_stores,
        user_data=user,
        user_order=items_to_order
    )
    # Меняю id магазина у товаров
    utils.set_store_for_order(arg=nearest_store_id, items_to_order=items_to_order)
    # Назначаю магазин
    store: Store = utils.get_nearest_store_by_nearest_id(list_of_stores=list_of_stores,
                                                         nearest_store_id=nearest_store_id)
    store.pre_order_time(user=user)
    # До пополнения
    # print(store)

    # Поставщики
    provider_35473758_and_9856437_items = [
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="35473758", name="Фен", cost=5200),
        Item(store_id=None, provider_id="9856437", name="Клавиатура", cost=4200),
        # Item(store_id=None, provider_id="9856437", name="Чемодан", cost=4200),
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
    provider_9856437_items = [
        Item(store_id=None, provider_id="9856437", name="Чемодан", cost=4200),
        Item(store_id=None, provider_id="9856437", name="Чемодан", cost=4200),
        Item(store_id=None, provider_id="9856437", name="Чемодан", cost=4200),
        Item(store_id=None, provider_id="9856437", name="Чемодан", cost=4200),
        Item(store_id=None, provider_id="9856437", name="Чемодан", cost=4200),
    ]
    provider = Provider(stock=provider_35473758_and_9856437_items)
    provider2 = Provider(stock=provider_345_items)
    store.send_request(provider=provider, order=provider_35473758_and_9856437_items)
    store.send_request(provider=provider2, order=provider_345_items)

    # После пополнения
    # print(store)

    # Курьер и кладовщик работают независимо друг от друга
    courier = Courier(username="Nilson", shift=2)
    courier1 = Courier(username="Java", shift=3)
    courier2 = Courier(username="Andrew", shift=1)
    courier3 = Courier(username="Anatoly", shift=12)

    storekeeper = Storekeeper(username="Wonderson", shift=7)
    storekeeper1 = Storekeeper(username="Sherlock", shift=5)

    # Берем ребят на работу
    store.take_to_work(storekeeper)
    store.take_to_work(storekeeper1)
    store.take_to_work(courier)
    store.take_to_work(courier1)
    store.take_to_work(courier2)
    store.take_to_work(courier3)

    # Делаем заказ
    user_order = user.make_order(items_to_order)

    # Тут идет основное принятие заказа, плюс формирование, того, чего не хвататет
    items_that_we_dont_have_in_store = store.take_order(user_order=user_order, user=user)

    # Пополняемся тем, чего нет в магазине в целом, т.е тем, что было в заказе,
    # но не было в магазине у всех поставщиков(ниже их 3)
    store.replenish_store_with_missing_items(
        items_that_we_dont_have_in_store=items_that_we_dont_have_in_store,
        user_order=user_order,
        provider_stock=provider_345_items
    )
    store.replenish_store_with_missing_items(
        items_that_we_dont_have_in_store=items_that_we_dont_have_in_store,
        user_order=user_order,
        provider_stock=provider_35473758_and_9856437_items
    )
    store.replenish_store_with_missing_items(
        items_that_we_dont_have_in_store=items_that_we_dont_have_in_store,
        user_order=user_order,
        provider_stock=provider_9856437_items
    )

    # Получаю тут статус, если есть ошибка, т.е отказ от товара, тогда не доставляю и не плачу
    if store.get_status_of_work(items=items_that_we_dont_have_in_store):
        # Пополняемся старым товаром
        store.send_request(provider=provider, order=items_to_order)
        store.send_request(provider=provider2, order=items_to_order)
        store.delivery_items(user_order=user_order, user=user)

        store.end_shift(worker=user_order.courier, user=user)
        store.end_shift(worker=user_order.picker, user=user)

    print()
    print(user_order)
    # Магазин в самом конце
    # print(store)


if __name__ == '__main__':
    main()
