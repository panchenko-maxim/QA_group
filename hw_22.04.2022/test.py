# dct_menu = {'главное меню': 'main menu', 'настройки аккаунта': 'account settings',
#             'ваш никнейм': 'your nickname', 'ваше золото': 'your gold', 'настройка меню': 'menu setting',
#             'меню выбора языка': 'language selection menu'}
# print([el for el in dct_menu.keys()])
# print([el for el in dct_menu.values()])


# dct_menu = {'главное меню': ['главное меню', 'main menu'],
#             'настройки аккаунта': ['настройки аккаунта', 'account settings'],
#             'ваш никнейм': ['ваш никнейм', 'your nickname'],
#             'ваше золото': ['ваше золото', 'your gold'],
#             'введите новый никнейм': ['введите новый никнейм', 'enter a new nickname'],
#             'никнейм обновлен': ['никнейм обновлен', 'nickname updated'],
#             'никнейм не принят (длина и пробелы)': ['никнейм не принят (длина и пробелы)',
#                                                     'nickname not accepted (length and spaces)'],
#             'настройка меню': ['настройка меню', 'menu setting'],
#             'меню выбора языка': ['меню выбора языка', 'language selection menu'],
#
#             'играть': ['играть', 'game'],
#             'магазин': ['магазин', 'shop'],
#             'изменить никнейм': ['изменить никнейм', 'change nickname'],
#             'настройка кнопок': ['настройка кнопок', 'button settings'],
#             'назад': ['назад', 'back'],
#             'выбор языка меню': ['выбор языка меню', 'menu language selection'],
#             'изменить знаки в оглавлении меню': ['изменить знаки в оглавлении меню',
#                                                  'change the characters in the menu table of contents'],
#             }


# def translate(text, language=None):
#     if language == 'EN':
#         return dct_menu[text.lower()][1].capitalize()
#     return dct_menu[text.lower()][0].capitalize()
#
#
# print(translate('настройки аккаунта', 'RU'))


# dct_store = {'меч': 10, 'сабля': 15, 'дубина': 5, 'лук': 25, 'рогатка': 20, 'кирпич': 8}
# for product, price in enumerate(dct_store.items(), start=1):
#     print(product, price)


a = ['a', 'b']
a.remove('a')
print(a)
