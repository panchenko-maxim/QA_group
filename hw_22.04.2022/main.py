import telebot
from misc import TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Можем использовать эти переменные как глобальные
bot = telebot.TeleBot(TOKEN)
users = []

dct_store = [{'меч': {'золото': 10,
                      'количество': 2,
                      'урон': 10,
                      'количество ударов': 15,
                      'кто может владеть': []}},
             {'сабля': {'золото': 15,
                        'количество': 5,
                        'урон': 15,
                        'количество ударов': 10,
                        'кто может владеть': []}},
             {'дубина': {'золото': 5,
                         'количество': 15,
                         'урон': 2,
                         'количество ударов': '50',
                         'кто может владеть': []}},
             {'лук': {'золото': 25,
                      'количество': 5,
                      'урон': 8,
                      'количество ударов': 30,
                      'кто может владеть': []}},
             {'рогатка': {'золото': 20,
                          'количество': 30,
                          'урон': 5,
                          'количество ударов': 70,
                          'кто может владеть': []}},
             {'кирпич': {'золото': 8,
                         'количество': 100,
                         'урон': 3,
                         'количество ударов': 45,
                         'кто может владеть': []}},
             ]

dct_menu = {'главное меню': ['main menu'],
            'настройка аккаунта': ['account settings', '😵‍💫'],
            "корзина": ['basket'],
            'ваш никнейм': ['your nickname'],
            'ваше золото': ['your gold'],
            "ваши товары": ["your goods"],
            'введите новый никнейм': ['enter a new nickname'],
            'никнейм обновлен': ['nickname updated'],
            'никнейм не принят (длина и пробелы)': ['nickname not accepted (length and spaces)'],
            'настройка меню': ['menu setting', 'Ⓜ'],
            'меню выбора языка': ['language selection menu'],
            'знаки в оглавлении': ['symbols in the title'],
            "введите символы": ['enter symbols'],
            "эмоджи на кнопках": ['emoji on buttons'],
            "введите номер товара": ['enter item number'],
            "покупка успешна": ["purchase successful"],
            "покупка не успешна (проверьте верность номера ввода товара из списка)":
                ["purchase not successful (check the item entry number from the list is correct)"],
            "покупка не успешна (возможно у вас мало золота или данного товара нет)":
                ["the purchase was not successful (maybe you have little gold or this product is not available)"],
            "добавлено в корзину": ["added to basket"],
            "товаров в корзине": ["products in basket"],
            "успешно удалено": ["successfully deleted"],
            "что-то пошло не так": ["something went wrong"],

            'играть': ['game', '🎮'],
            'магазин': ['shop', '🏪'],
            'изменить никнейм': ['change nickname', '🕴'],
            'настройка кнопок': ['button settings', '🧑‍🔧 🎹'],
            'назад': ['back', '🔙'],
            'выбор языка меню': ['menu language selection', '😝'],
            'изменить знаки в оглавлении меню': ['change the characters in the menu table of contents', '🔣'],
            'настройка языка': ['language setting', '🤔'],
            'знаки в начале': ['symbols start', '👈'],
            'знаки в конце': ['symbols end', '👉'],
            'вкл': ['on', '🔛'],
            'выкл': ['off', '📴'],
            'купить': ['buy', '🤑'],
            'добавить в корзину': ['add to basket', '🗑'],
            'перейти в корзину': ['basket watch', '🗄'],
            'удалить из корзины': ['remove from basket', '🙅‍♂'],

            'меч': ['sword'], 'сабля': ['saber'], 'дубина': ['cudgel'],
            'лук': ['bow'], 'рогатка': ['slingshot'], 'кирпич': ['brick'],
            'золото': ['gold'], 'количество': ['amount'], 'урон': ['damage'],
            'количество ударов': ['number of strokes'], 'кто может владеть': ['who can own'],

            }


def translate(text, language=None):
    if language == 'EN':
        return dct_menu[text][0].capitalize()
    return text.capitalize()


class User:
    def __init__(self, chat_id, username='new user', gold=100, language='RU',
                 title_symbols_start='-==', title_symbols_end='==-', emoji_on_buttons='Выкл'):
        self.chat_id = chat_id
        self.username = username
        self.gold = gold
        self.message_id = None  # последнее сообщение от бота юзеру
        self._help_message = ''  # для доп информации в текущем меню( любом, где это нужно)
        self.language = language
        self.title_symbols_start = title_symbols_start
        self.title_symbols_end = title_symbols_end
        self.emoji_on_buttons = emoji_on_buttons
        self.shopping_basket = []
        self.purchased_goods = []

    def button_with_emoji(self, words):
        if self.emoji_on_buttons in ['On', 'Вкл']:
            return self.text(words) + dct_menu[words][-1]
        return self.text(words)

    def text_with_symbols(self, words):
        return f'{self.title_symbols_start}{self.text(words)}{self.title_symbols_end}'

    def text(self, words):
        return translate(words, self.language)

    def clear_help_message(self):
        self._help_message = ''

    @property
    def help_message(self):
        msg = self._help_message
        self.clear_help_message()
        return msg

    @help_message.setter
    def help_message(self, text):  # obj.help_message = 'klk'
        self._help_message = text

    def try_to_save_my_message(self, message):
        if self.message_id is None:
            self.message_id = message.message_id

    def delete_last_message(self):
        if self.message_id:
            bot.delete_message(self.chat_id, self.message_id)

    def delete_my_message(self, message):
        bot.delete_message(self.chat_id, message.message_id)

    def resend_message(self, text, reply_markup=None):
        self.delete_last_message()
        message = bot.send_message(self.chat_id, text, reply_markup=reply_markup)
        self.message_id = message.message_id

    @classmethod
    def create_user(cls, chat_id):
        user = User(chat_id)
        users.append(user)
        return user

    @classmethod
    def find_user(cls, chat_id) -> 'User':
        for user in users:
            if user.chat_id == chat_id:
                return user

        # не нашли, нужно его создать
        user = cls.create_user(chat_id)
        return user

    @classmethod
    def find_user_from_message(cls, message):
        return cls.find_user(message.chat.id)

    @classmethod
    def find_user_and_delete_message(cls, message):
        user = cls.find_user_from_message(message)
        user.delete_my_message(message)
        return user


@bot.message_handler(content_types=['text'])
def text_handler(message):
    user = User.find_user_and_delete_message(message)
    main_menu(user)


def main_menu(user):
    text = user.text_with_symbols("главное меню")
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton(user.button_with_emoji("играть")),
                 KeyboardButton(user.button_with_emoji('магазин')))
    keyboard.row(KeyboardButton(user.button_with_emoji('настройка аккаунта')))
    # bot.send_message(user.chat_id, text, reply_markup=keyboard)
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, main_handler)


def main_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if user.text('играть') in text:
        pass
    elif user.text('магазин') in text:
        store(user)
    elif user.text('настройка аккаунта') in text:
        account_settings_menu(user)


def store(user):
    text = f'{user.text("ваш никнейм")}: {user.username}\n' \
           f'{user.text("ваше золото")}: {user.gold}\n' \
           f'{user.text("ваши товары")}: {user.purchased_goods}\n' \
           f'{user.text("товаров в корзине")}: {len(user.shopping_basket)}\n' \
           f'{user.help_message}\n\n' \
           f'{user.text_with_symbols("магазин"):}\n'

    for num, products in enumerate(dct_store, start=1):
        text += f'{num}) - '
        for weapon, properties in products.items():
            text += f'{user.text(weapon)}\n' \
                    f'{user.text("золото")}: {properties["золото"]}\n' \
                    f'{user.text("количество")}: {properties["количество"]}\n' \
                    f'{user.text("урон")}: {properties["урон"]}\n' \
                    f'{user.text("количество ударов")}: {properties["количество ударов"]}\n' \
                    f'{user.text("кто может владеть")}: {properties["кто может владеть"]}\n' \
                    f'{"-" * 25}\n'

    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton(user.button_with_emoji('купить')))
    keyboard.row(KeyboardButton(user.button_with_emoji('добавить в корзину')),
                 user.button_with_emoji('перейти в корзину'))
    keyboard.row(KeyboardButton(user.button_with_emoji('назад')))
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, store_handler)


def store_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if user.text('купить') in text:
        user.resend_message(f'{user.text("введите номер товара")}:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, buy_handler)
    elif user.text('добавить в корзину') in text:
        user.resend_message(f'{user.text("введите номер товара")}:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, add_to_shopping_basket_handler)
    elif user.text('перейти в корзину') in text:
        if len(user.shopping_basket) <= 0:
            user.help_message = 'Корзина пуста'
            store(user)
        else:
            go_to_shopping_basket(user)
    elif user.text('назад') in text:
        main_menu(user)


def go_to_shopping_basket(user):
    text = f'{user.text("ваш никнейм")}: {user.username}\n' \
            f'{user.text("ваше золото")}: {user.gold}\n' \
            f'{user.text("ваши товары")}: {user.purchased_goods}\n' \
            f'{user.text("товаров в корзине")}: {len(user.shopping_basket)}\n' \
            f'{user.help_message}\n\n' \
            f'{user.text_with_symbols("корзина"):}\n'

    for num, products in enumerate(user.shopping_basket, start=1):
        text += f'{num}) - '
        for weapon, properties in products.items():
            text += f'{user.text(weapon)}\n' \
                    f'{user.text("золото")}: {properties["золото"]}\n' \
                    f'{user.text("количество")}: {properties["количество"]}\n' \
                    f'{user.text("урон")}: {properties["урон"]}\n' \
                    f'{user.text("количество ударов")}: {properties["количество ударов"]}\n' \
                    f'{user.text("кто может владеть")}: {properties["кто может владеть"]}\n' \
                    f'{"-" * 25}\n'

        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.row(KeyboardButton(user.button_with_emoji('купить')))
        keyboard.row(KeyboardButton(user.button_with_emoji('удалить из корзины')))
        keyboard.row(KeyboardButton(user.button_with_emoji('назад')))
        user.resend_message(text, keyboard)
        bot.register_next_step_handler_by_chat_id(user.chat_id, go_to_shopping_basket_handler)


def go_to_shopping_basket_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if user.text('купить') in text:
        user.resend_message(f'{user.text("введите номер товара")}:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, buy_from_basket_handler)
    elif user.text('удалить из корзины') in text:   # добавляешь 1 товар - работают все кнопки, если больше - выбивает ошибку api
        user.resend_message(f'{user.text("введите номер товара")}:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, delete_from_basket_handler)
    elif user.text('назад') in text:
        main_menu(user)


def delete_from_basket_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text

    if text.isdigit() and 0 < int(text) <= len(user.shopping_basket):
        purchase = user.shopping_basket[int(text) - 1]
        user.shopping_basket.remove(purchase)

        user.help_message = user.text("успешно удалено")
        store(user)
    else:
        user.help_message = user.text("что-то пошло не так")
        store(user)


def add_to_shopping_basket_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if text.isdigit() and 0 < int(text) <= len(dct_store):
        purchase = dct_store[int(text) - 1].copy()
        user.shopping_basket.append(purchase)

        user.help_message = user.text("добавлено в корзину")
        store(user)
    else:
        user.help_message = user.text("что-то пошло не так")
        store(user)


def buy_from_basket_handler(message):
    pass


def buy_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if text.isdigit() and 0 < int(text) <= len(dct_store):
        purchase = dct_store[int(text) - 1]
        for weapon, properties in purchase.items():

            if properties['золото'] <= user.gold and properties['количество'] > 0:
                properties['количество'] -= 1
                user.gold -= properties['золото']
                user.purchased_goods.append(purchase)

                user.help_message = user.text("покупка успешна")
                store(user)
            else:
                user.help_message = user.text("покупка не успешна (возможно у вас мало золота или данного товара нет)")
                store(user)
    else:
        user.help_message = user.text("покупка не успешна (проверьте верность номера ввода товара из списка)")
        store(user)


def account_settings_menu(user):
    text = f'{user.text_with_symbols("настройка аккаунта")}\n' \
           f'{user.text("ваш никнейм")}: {user.username}\n' \
           f'{user.text("ваше золото")}: {user.gold}\n' \
           f'{user.help_message}'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton(user.button_with_emoji('изменить никнейм')))
    keyboard.row(KeyboardButton(user.button_with_emoji('настройка меню')),
                 KeyboardButton(user.button_with_emoji('настройка кнопок')))
    keyboard.row(KeyboardButton(user.button_with_emoji('настройка языка')))
    keyboard.row(KeyboardButton(user.button_with_emoji('назад')))
    # bot.send_message(user.chat_id, text, reply_markup=keyboard)
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, account_settings_handler)


def account_settings_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if user.text('изменить никнейм') in text:
        # bot.send_message(user.chat_id, 'Введите новый никнейм:')
        user.resend_message(f'{user.text("введите новый никнейм")}:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, new_nickname_handler)
    elif user.text('настройка меню') in text:
        menu_settings(user)
    elif user.text('настройка кнопок') in text:
        button_settings(user)
    elif user.text('настройка языка') in text:
        menu_language(user)
    elif user.text('назад') in text:
        main_menu(user)


def new_nickname_handler(message):
    user = User.find_user_and_delete_message(message)
    new_nickname = message.text
    if 5 <= len(new_nickname) <= 20 and ' ' not in new_nickname:
        user.username = new_nickname
        # bot.send_message(user.chat_id, 'Никнейм обновлен')
        # user.resend_message('Никнейм обновлен')
        user.help_message = user.text("никнейм обновлен")
        account_settings_menu(user)
    else:
        # bot.send_message(user.chat_id, 'Никнейм не принят (длина и пробелы)')
        user.help_message = user.text("никнейм не принят (длина и пробелы)")
        account_settings_menu(user)


def menu_settings(user):
    text = user.text_with_symbols("настройка меню")
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton(user.button_with_emoji("изменить знаки в оглавлении меню")))
    keyboard.row(KeyboardButton(user.button_with_emoji("назад")))
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, menu_settings_handler)


def menu_settings_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if user.text("изменить знаки в оглавлении меню") in text:
        symbols_in_the_title(user)
    elif user.text("назад") in text:
        account_settings_menu(user)


def symbols_in_the_title(user):
    text = f'{user.text_with_symbols("знаки в оглавлении")}'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton(user.button_with_emoji('знаки в начале')),
                 KeyboardButton(user.button_with_emoji('знаки в конце')))
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, symbols_in_the_title_handler)


def symbols_in_the_title_handler(message):
    user = User.find_user_and_delete_message(message)
    text = message.text
    if user.text('знаки в начале') in text:
        bot.send_message(user.chat_id, f'{user.text("введите символы")}:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, symbols_in_the_start_handler)
    elif user.text('знаки в конце') in text:
        bot.send_message(user.chat_id, f'{user.text("введите символы")}:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, symbols_in_the_end_handler)


def symbols_in_the_start_handler(message):
    user = User.find_user_and_delete_message(message)
    user.title_symbols_start = message.text
    account_settings_menu(user)


def symbols_in_the_end_handler(message):
    user = User.find_user_and_delete_message(message)
    user.title_symbols_end = message.text
    account_settings_menu(user)


def menu_language(user):
    text = user.text_with_symbols("меню выбора языка")
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton('RU'), KeyboardButton('EN'))
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, menu_language_handler)


def menu_language_handler(message):
    user = User.find_user_and_delete_message(message)
    user.language = message.text
    account_settings_menu(user)


def button_settings(user):
    text = user.text_with_symbols("эмоджи на кнопках")
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton(user.text('вкл')), KeyboardButton(user.text('выкл')))
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, button_settings_handler)


def button_settings_handler(message):
    user = User.find_user_and_delete_message(message)
    user.emoji_on_buttons = message.text
    account_settings_menu(user)


bot.polling()
