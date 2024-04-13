from pprint import pprint

from provider import Provider
from store import Store
from user import User
from item import Item
from courier import Courier
from storekeeper import Storekeeper

#
# Сделайте систему больше: добавьте несколько складов
# (заказ получает тот склад, который может быстрее обработать заказ и тот склад, который работает),
# добавьте ожидаемое время доставки
#
# Добавьте время работы склада (не все склады могут работать круглосуточно)
#
# Добавьте обработку ожиданий с клиентом: если каких-то товаров на складе нет,
# то клиент может полностью отказаться от заказа (необходимо спросить)
#
# Также курьер с определенной вероятностью может просто не явиться склад (тогда ему надо назначить штраф)


def main():
    store = Store(store_id="73645", coords=(0, 0), stocks=[], work_time="8:00 - 20:00")
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
        Item(store_id="73645", provider_id="9856437", name="Клавиатура", cost=4200),
    ]
    user = User(username="Andrew", coords=(15, 45))
    user_order = user.make_order(items_to_order)
    # Тут идет основное принятие заказа, плюс формирование, того, чего не хвататет
    items_that_we_dont_have_in_store = store.take_order(user_order=user_order, user=user)

    # Пополняемся тем, чего нет в магазине в целом, т.е тем, что было в заказе, но не было в магазине у всех поставщиков(ниже их 2)
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

    # Получаю тут статус, если есть ошибка, т.е курьер не пришел, тогда не доставляю и не плачу
    if store.get_status_of_work(items=items_that_we_dont_have_in_store):
        # Пополняемся старым товаром
        store.send_request(provider=provider, order=items_to_order)
        store.send_request(provider=provider2, order=items_to_order)
        store.delivery_items(user_order=user_order, user=user)

        store.end_shift(worker=user_order.courier, user=user)
        store.end_shift(worker=user_order.picker, user=user)

    print()
    print(user_order)



if __name__ == '__main__':
    main()

