class Node:
    def __init__(self, prev, next_, value):
        self.prev = prev
        self.next = next_
        self.value = value

def el_(struct):
    for i in range(len(struct)):
        el = ''.join(struct[i])
        if type(struct[i]) is list:
            struct[i].append([el[:len(el) // 2]])
            struct[i].append([el[len(el) // 2:]])
    return struct


# def list_or_str(element):
#     result = []
#     if type(element) is str and len(str) > 1:
#         result.append(element)
#         result.append(element[len(element)//2:])
#         result.append(element[:len(element) // 2])
#     return result

class Tree:
    def __init__(self, head='aбвгдеёклмн'):
        self.head = head



    def structure(self):
        a = self.head
        struct = [self.head, [a[:len(a)//2]], [a[len(a)//2:]]]
        struct = el_(struct)
        struct = [[el_(i) for i in el_(el)] for el in struct]
        return struct


print(*Tree().structure(), sep='\n')







