"""
Создай класс Слизень, у которого есть два поля. Имя, и вес. Кроме того, у него есть 1 метод: прилепить.
Этот метод принимает self, а также other - другого слизня. И он прилепляет второго слизня к себе,
таким образом вес self увеличивается на величину, равную весу второго слизня. Пример ниже.
"""


class Slime:
    name = ''
    weight = 0

    def prilepit(self, other):
        self.weight += other.weight


slime_1 = Slime()
slime_1.name = "Solly"
slime_1.weight = 14

slime_2 = Slime()
slime_2.name = "Bolly"
slime_2.weight = 4

slime_1.prilepit(slime_2)
print(slime_1.weight)