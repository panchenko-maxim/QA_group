"""
тут что-то не работает
"""
class User:
    name = 'Igor'
    money = 1500
    items = {}
    resultdict = {}

    def run(self):  # не вычитаются деньги, при добавлении одинакового товара - ничего не добавляется, не вывводится False если товар стоит больше - чем есть в money
        while True:
            x = input('enter item: ')
            if x == 'done':
                break
            y = float(input('enter price: '))
            self.items[x] = {"Price": y}

    def get_totals(self):
        for j in self.items.keys():
            self.items[j]["Quantity"] = int(input('enter how many "{}" you want: '.format(j)))
            self.items[j]["Total"] = self.items[j]["Quantity"] * self.items[j]["Price"]
            try:
                self.resultdict[j] += self.items[j]["Total"]
            except KeyError:
                self.resultdict[j] = self.items[j]["Total"]
            a = sum(self.resultdict.values())
            print('amount of purchases -', a)
            w = self.money - a
            if w <= 0:
                print(self.name, 'you need money !!!')
                print('money on the balance', w)
                # break

    def top_up_an_account(self):
        if self.money <= 0:
            s = float(input('Enter the replenishment amount: '))
            g = self.money + s
            print(g)


grocer = User()
grocer.money = 100
grocer.items = {}
grocer.resultdict = {}
grocer.run()
grocer.get_totals()
print(grocer.items)
grocer.top_up_an_account()
print(grocer.money)