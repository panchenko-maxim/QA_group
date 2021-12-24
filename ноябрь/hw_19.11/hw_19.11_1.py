"""
Создай класс Child - дитина. У него будет 2 поля: имя, и возраст. Напиши два метода.
Первый - выводит на экран всю информацию про одного ребенка.
Второй - возвращает число, сколько осталось этому ребенку лет до совершеннолетия (18)
"""


class Child:
    name = ''
    age = 0

    def output_on_display_all_information(self):
        print(f"Information about {self.name}\n"
              f"Name: {self.name}\n"
              f"Age: {self.age}")

    def years_left_until_adulthood(self):
        print("Age information:")
        if self.age < 18:
            print(f'{self.name} up to 18 {18 - self.age} years left!')
        else:
            print(f'{self.name} is already an adult! He is {self.age} years old!')


child_1 = Child()
child_1.name = 'Robinson'
child_1.age = 17
child_1.output_on_display_all_information()
print()
child_1.years_left_until_adulthood()



