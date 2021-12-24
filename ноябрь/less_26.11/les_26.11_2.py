"""
Задание:
 Написать класс Юзер интернет магазина.
У юзера есть имя, количество денег на счету, и история покупок

Создать для него методы:
- Купить товар - принимает словарь с информацией о товаре, в том числе с ценой.
Должен добавить этот товар в список - историю покупок юзера, а так же снять деньги со счета юзера.
Если денег недостаточно, вернуть False.
- пополнить счет
- метод для получения общей суммы, потраченной пользователем (считать по истории его закупок)
"""


class User:
    name = ''
    money = 0
    purchase_history = {}

    def buy_goods(self, product: dict):
        if product['price'] > self.money:
            return False
        else:
            if product['name'] not in self.purchase_history:
                self.purchase_history[product['name']] = {"price": 0, 'total': 0}

            self.purchase_history[product['name']]['price'] += product['price']
            self.purchase_history[product['name']]['total'] += 1
            self.money -= product['price']

    def add_money_user(self, add_money: int):
        self.money += add_money

    def amount_of_costs(self):
        return sum([self.purchase_history[key]['price'] for key in self.purchase_history])


store = User()
store.name = 'Soloma'
store.money = 6
store.purchase_history = {}

toy = {"name": "toy",
       "price": 2}

potato = {'name': 'potato',
          'price': 3}

"""проверка 1-го метода"""
store.buy_goods(toy)
store.buy_goods(toy)
print(store.money)
store.buy_goods(potato)
print(store.purchase_history, '\n')

"""проверка 2-го метода"""
store.add_money_user(550)
print(store.money, '\n')

"""проверка 3-го метода"""
store.buy_goods(potato)
print(store.purchase_history)
print(store.amount_of_costs())





