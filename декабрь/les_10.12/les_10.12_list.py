class Node:  # узел
    def __init__(self, prev, next_, value):
        self.prev = prev
        self.next = next_
        self.value = value


class List:  # список
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def append(self, value):  # метод добавления в список
        new_node = Node(None, None, value)
        if self.head:
            new_node.next = None
            new_node.prev = self.tail

            self.tail.next = new_node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = new_node

    def __getitem__(self, i):  # []                     # метод - достать по индексу
        cur_i = 0
        node = self.head

        while True:
            if cur_i == i:
                return node.value
            else:
                node = node.next
                cur_i += 1

    def __str__(self):  # метод печать списка
        string = '['
        node = self.head
        while True:
            if node is None:
                break
            else:
                string += node.value.__repr__() + ", "
                node = node.next
        if string[-2:] == ', ':
            string = string[:-2]
        return string + ']'

    def __len__(self):  # len()                     # метод len для списка
        node = self.head
        l = 0
        while True:
            if node is None:
                return l
            else:
                l += 1
                node = node.next

    def maximum(self, flag=False):          # метод max для списка
        node = self.head

        if type(node.value) is str:         # Проверка элемента на str
            max_node = ord(node.value[0])
            while True:
                if node is None:
                    return chr(max_node)
                else:
                    if flag is True:
                        if max_node > ord(node.value[0]):
                            max_node = ord(node.value[0])
                    elif max_node < ord(node.value[0]):
                        max_node = ord(node.value[0])
                    node = node.next
        elif type(node.value) is int:       # Проверка элемента на int
            max_node = node.value
            while True:
                if node is None:
                    return max_node
                else:
                    if flag is True:
                        if max_node > node.value:
                            max_node = node.value
                    elif max_node < node.value:
                        max_node = node.value
                    node = node.next
        else:
            return 'Error: for int or str!'

    def minimum(self):                      # метод min для списка
        return self.maximum(True)

    def clear(self):
        return self.__init__(None, None)

    def copy(self):
        node = self.head
        new_self = List()
        while True:
            if node is None:
                return new_self
            else:
                new_self.append(node.value)
                node = node.next

    def count(self, el):
        node = self.head
        count = 0
        while True:
            if node is None:
                return count
            else:
                if node.value == el:
                    count += 1
                node = node.next

    def extend(self, some_list):
        node = some_list.head
        while True:
            if node is None:
                return self
            else:
                self.append(node.value)
                node = node.next

    def index(self, search_value):
        index = 0
        node = self.head
        while True:
            if node is None and search_value != node.value:
                return 'index not found'
            elif search_value == node.value:
                return index
            else:
                index += 1
                node = node.next

    def insert(self, index_insert, el_for_insert):
        """
        выводит только кортеж или заменяет элемент на новый
        наверно нужно создать новый узел с даннными и внедрить его в lst
        """
        count_index = 0
        node = self.head
        while True:

            if node is None:
                return self
            elif count_index == index_insert:

                node.value = el_for_insert, node.value
                count_index += 1

            else:

                count_index += 1
                node = node.next

    def pop(self, pop_el=None):   # возвращает только новый список, если присвоить переменной pop - не вернет эл-т
        """
        как сделать чтобы возвращало измененный self, а не новый список?
        как сделать, чтобы возвращало эл-т при присваивании pop переменной
        """
        node = self.head
        new_self = List()
        count = 0
        if pop_el is not None and pop_el > self.__len__():
            return 'this is el not found'
        else:
            if pop_el is None:
                index_for_pop = self.__len__() - 1
                while count < index_for_pop:
                    new_self.append(node.value)
                    node = node.next
                    count += 1
            else:
                while True:
                    if node is None:
                        break
                    elif count == pop_el:
                        node = node.next
                    new_self.append(node.value)
                    node = node.next
                    count += 1

            return new_self

    def remove(self, pop_el = None): # возвращает новый список, как вернуть измененный self
        node = self.head
        new_self = List()
        if pop_el is None:
            return 'Error: input element for remove'
        else:
            while True:
                if node is None:
                    return new_self
                elif pop_el == node.value:
                    node = node.next
                new_self.append(node.value)
                node = node.next

    def reverse(self):  # переворачивает список, вроде все норм
        node = self.tail
        new_self = List()
        while True:
            if node is None:
                return new_self
            else:
                new_self.append(node.value)
                node = node.prev

    def sort_(self): # ничего не вышло;(
        node = self.head
        new_self = List()
        min_el = node.value
        count = self.__len__()
        if type(node.value) is str:
            pass
        elif type(node.value) is int:
            pass
        else:
            return 'error'

# n1 = Node(None, None, 'a')
# n2 = Node(None, None, 'b')
# n3 = Node(None, None, 'c')
#
# lst = List(n1, n3)
#
# n1.next = n2
# n2.next = n3
# n3.next = None
#
# n1.prev = None
# n2.prev = n1
# n3.prev = n2
#
# lst.append('d')
# lst.append('e')

#
# print(lst.head.next.next.next.next.value)
# print(lst.tail.value)


lst = List()
lst.append('y')
lst.append('c')
lst.append('s')
lst.append('z')

print(lst.remove('z').head.value)

#
# i = 0
# while i < len(lst):
#     print(lst[i])
#     i += 1
