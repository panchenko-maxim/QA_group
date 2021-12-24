class Bottle:
    v = 5
    material = 'пластик'
    liquids = {}

    def add_liquid(self, liquid, v) -> float:  # добавление жидкости(liquid) c обьемом(v) в словарь - self
        if liquid not in self.liquids:
            self.liquids[liquid] = 0

        free_v = self.v - self.filled_v() # свободный объем в бутылке
        if v > free_v:
            v = free_v
        self.liquids[liquid] += v

    def poor_out(self, v) -> dict: # вылить жидкость обьемом(v)
        filled_v = self.filled_v()
        remaining_v = filled_v - v if v < filled_v else 0

        k = remaining_v / filled_v  # 0.6

        return_dict = {}
        for liquid in list(self.liquids):
            v = self.liquids[liquid]
            self.liquids[liquid] = v * k
            return_dict[liquid] = v * (1 - k)
            if self.liquids[liquid] == 0:  # удаление нулевых жидкостей
                self.liquids.pop(liquid)
        return return_dict

    def calculate_in_percents(self) -> dict: # посчитать сколько в процентах каждой жидкости(от заполненного обьема)
        """
        бутылка: 8
        {
            'вода': 4,
            "молоко": 1
        }
        ->
        {
            'вода': 80,
            "молоко": 20
        }
        :return:
        """
        v_bottle = sum([value for value in self.liquids.values()])
        # new_liquids = {}
        # for key, value in self.liquids.items():
        #     new_liquids[key] = value / v_bottle * 100
        return [f'{key}: {self.liquids[key] / v_bottle * 100} %' for key in self.liquids]

    def how_much(self, liquid) -> float: # возвращает обьем конкретной жидкости
        """
        Обязательно!
        бутылка: 8
        {
            'вода': 4,
            "молоко": 1
        }
        b.how_much('вода') -> 4
        b.how_much('слизь') -> 0
        """
        return self.liquids[liquid]

    def filled_v(self) -> float: # сумма заполненной жидкоста
        return sum(self.liquids.values())

    def add_liquids(self, liquids: dict): # залитие словаря с жидкостями( при переполнении часть вылить
        # (сейчас код работает до переполнения), а часть смеси залить)
        # нужно предусомтреть вариант с переполнением бутылки и пропорционально вылить часть каждой из жидкостей из
        # liquids перед заливанием в self.liquids
        sum_liquids_values = sum([value for value in liquids.values()])
        free_v_self = self.v - self.filled_v()
        coef = free_v_self / sum_liquids_values
        if coef == 0:
            pass
        else:
            for key, value in liquids.items():
                if key not in self.liquids:
                    self.liquids[key] = 0
                self.liquids[key] += value * coef
            liquids.clear()


b1 = Bottle()
b1.v = 9
b1.liquids = {}

b1.add_liquid('вода', 3)
b1.add_liquid('молоко', 3)
b1.add_liquid('слизь', 1)


b2 = Bottle()
b2.v = 10
b2.add_liquid('сера', 2)
b2.add_liquid('вода', 2)


print(*b1.calculate_in_percents(), sep='\n')
print()
print(b1.how_much('вода'))
print()
b1.add_liquids(b2.liquids)
print(b1.liquids)
print(b2.liquids)
