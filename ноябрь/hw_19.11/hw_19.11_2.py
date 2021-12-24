"""
Создай класс Прямоугольник (Rectangle), у которого есть два поля: ширина, и длинна.
А также два метода: первый возвращает площадь прямоугольника (ширина * длинна),
 второй возвращает периметр прямоугольника (ширина * 2 + длинна * 2).
"""


class Rectangle:
    width = 0
    length = 0

    def area_of_a_rectangle(self):
        print(f'Area of a rectangle: {self.width * self.length}')

    def rectangle_perimeter(self):
        print(f'Rectangle perimeter: {(self.width * 2) + (self.length * 2)}')


rectangle_1 = Rectangle()
rectangle_1.width = 5
rectangle_1.length = 8
rectangle_1.area_of_a_rectangle()
rectangle_1.rectangle_perimeter()