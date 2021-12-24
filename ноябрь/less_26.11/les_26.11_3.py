"""
Просто для тренировки алгоритмов (не ООП, но полезно):
Написать функцию для сортировки только чётных элементов списка. Нечётные должны остаться на своих местах.
"""
my_lst = [9, 55, 88, 4, 45, 6, 53, 2, 1, 10, 0]


def sorting_even_list_items(list):
    index_even = [i for i in range(len(my_lst)) if my_lst[i] != 0 and my_lst[i] % 2 == 0]
    even_numbers = sorted([el for el in my_lst if el != 0 and el % 2 == 0])
    for i in range(len(index_even)):
        list[index_even[i]] = even_numbers[i]


sorting_even_list_items(my_lst)
print(*my_lst)






