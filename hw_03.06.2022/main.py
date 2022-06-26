from misc import TOKEN
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(TOKEN)


def text_with_keyboard_for_menu_add_and_change(table):
    text = f'| id {" " * 7}| code | activ   | sale | wh_sale | retail |\n'
    for lst in table:
        text += '| '
        for el in lst:
            text += str(el) + ' | '
        text += '\n'
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Присвоить код обуви', callback_data='shoes_code')
    btn2 = InlineKeyboardButton('В продаже(да/нет)', callback_data='active')
    btn3 = InlineKeyboardButton('Описание обуви', callback_data='description')
    btn4 = InlineKeyboardButton('Описание размеров', callback_data='measurements')
    btn5 = InlineKeyboardButton('Распродажная цена', callback_data='sale')
    btn6 = InlineKeyboardButton('Оптовая цена', callback_data='wholesale')
    btn7 = InlineKeyboardButton('Розничная цена', callback_data='retail')
    btn8 = InlineKeyboardButton('Назад', callback_data='back')
    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return text, kb


class UserNotFoundError(BaseException):
    def __init__(self, chat_id):
        super(f'Не был найден пользователь с chat_id = {chat_id} в базе данных')


def connect():
    connection = sqlite3.connect('data_hw.db')
    cursor = connection.cursor()
    return connection, cursor


def conn_cursor_handler_decorator(func):
    def new_func(*args, **kwargs):
        conn, cursor = connect()
        return func(*args, **kwargs, conn=conn, cursor=cursor)
    return new_func


class User:
    columns = ['id', 'username', 'information', 'contact', 'balance',
               'active_cart_id', 'bot_message_id', 'next_message_handler', 'shoes_id_active', 'shoes_position_for_change']

    def __init__(self, id, username, information, contact, balance,
               active_cart_id, bot_message_id, next_message_handler, shoes_id_active, shoes_position_for_change):
        self.id = id
        self.username = username
        self.information = information
        self.contact = contact
        self.balance = balance
        self.active_cart_id = active_cart_id
        self.bot_message_id = bot_message_id
        self.next_message_handler = next_message_handler
        self.shoes_id_active = shoes_id_active
        self.shoes_position_for_change = shoes_position_for_change

    @classmethod
    def get_by_id(cls, chat_id):
        conn, cursor = connect()
        query = f"SELECT {', '.join(cls.columns)} FROM Client WHERE id={chat_id}"
        cursor.execute(query)
        table = cursor.fetchall()
        if len(table) == 0:
            raise UserNotFoundError(chat_id)

        kwargs = {column: value for column, value in zip(cls.columns, table[0])}
        return cls(**kwargs)

    @classmethod
    def create_user_if_it_not_db(cls, chat_id):
        conn, cursor = connect()
        cursor.execute(f'SELECT id FROM Client WHERE id={chat_id}')
        table = cursor.fetchall()
        if len(table) == 0:
            cls.create_default_user(chat_id, conn, cursor)

    @classmethod
    def create_default_user(cls, chat_id, conn, cursor):
        cursor.execute(f'INSERT INTO Client(id, username) VALUES({chat_id}, "new_client")')
        conn.commit()

    def save_next_message_handler(self, handler):
        index = HANDLERS.index(handler)
        query = f"UPDATE Client\n" \
                f"SET next_message_handler={index}\n" \
                f"WHERE id={self.id}"
        conn, cursor = connect()
        cursor.execute(query)
        conn.commit()
        self.next_message_handler = index

    def send_message(self, message, keyboard):
        try:
            if self.bot_message_id is None:
                message = bot.send_message(self.id, message, reply_markup=keyboard)
                self.save_bot_message_id(message.message_id)
            else:
                message = bot.edit_message_text(message, self.id, self.bot_message_id, reply_markup=keyboard)
        except:
            message = bot.send_message(self.id, message, reply_markup=keyboard)
            self.save_bot_message_id(message.message_id)

    def save_bot_message_id(self, bot_message_id):
        query = f"UPDATE Client\n" \
                f"SET bot_message_id = {bot_message_id}\n" \
                f"WHERE id={self.id}"
        conn, cursor = connect()
        cursor.execute(query)
        conn.commit()
        self.bot_message_id = bot_message_id


@bot.message_handler(commands=['start'])
def start(message):
    User.create_user_if_it_not_db(message.chat.id)
    bot.delete_message(message.chat.id, message.message_id)
    main_menu(User.get_by_id(message.chat.id))


@bot.message_handler(content_types=['text'])
def text(message):
    try:
        user = User.get_by_id(message.chat.id)
        bot.delete_message(message.chat.id, message.message_id)
        HANDLERS[user.next_message_handler](user, message.text)
    except Exception as exc:
        print(f'Произошла ошибка - ввод в строку чата {exc}')


@bot.callback_query_handler(lambda callback: True)
def inline_buttons_handler(callback):
    user = User.get_by_id(callback.message.chat.id)
    HANDLERS[user.next_message_handler](user, callback.data)
    bot.answer_callback_query(callback.id)


def main_menu(user):
    kb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Работа в БД', callback_data='work_in_db_menu')
    btn2 = InlineKeyboardButton('Заказы', callback_data='orders_menu')
    btn3 = InlineKeyboardButton('Клиенты', callback_data='clients_menu')
    kb.add(btn1, btn2, btn3)
    user.send_message('Главное меню', kb)
    user.save_next_message_handler(main_menu_handler)


def main_menu_handler(user, data):
    menus = {
        'work_in_db_menu': work_in_db_menu
    }
    menus[data](user)


def work_in_db_menu(user):
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Добавить позицию', callback_data='add_in_db_menu')
    btn2 = InlineKeyboardButton('Удалить позицию', callback_data='del_in_db_menu')
    btn3 = InlineKeyboardButton('Изменить позицию', callback_data='change_in_db_menu')
    btn4 = InlineKeyboardButton('Назад', callback_data='back')
    kb.add(btn1, btn2, btn3, btn4)
    user.send_message('DB Shoes', kb)
    user.save_next_message_handler(work_in_db_menu_handler)


def work_in_db_menu_handler(user, data):
    menus = {
        'add_in_db_menu': add_in_db_1_step_menu,
        'del_in_db_menu': del_in_db_menu,
        'change_in_db_menu': change_in_db_menu,
        'back': main_menu
    }
    menus[data](user)


def add_new_id_in_db(user, conn, cursor):
    query = "SELECT MAX(id) AS max_id\n" \
            "FROM Shoes"
    cursor.execute(query)
    table = cursor.fetchall()
    last_id = 0 if table[0][0] is None else table[0][0]
    new_id = last_id + 1
    user.shoes_id_active = new_id
    query_new_id_for_add = f"INSERT INTO Shoes(id) VALUES({new_id})"
    query_new_id_user_shoes_id_active = f"UPDATE Client\n" \
                                        f"SET shoes_id_active={user.shoes_id_active}\n" \
                                        f"WHERE id = {user.id}"
    for query in (query_new_id_for_add, query_new_id_user_shoes_id_active):
        cursor.execute(query)
        conn.commit()


def add_in_db_1_step_menu(user):
    conn, cursor = connect()
    add_new_id_in_db(user, conn, cursor)
    add_in_db_menu_2_step(user)


def add_in_db_menu_2_step(user):
    conn, cursor = connect()
    query = "SELECT id, shoes_code, active, sale, wholesale, retail FROM Shoes"
    cursor.execute(query)
    table = cursor.fetchall()
    text, kb = text_with_keyboard_for_menu_add_and_change(table)
    text += f'\nДобавление позиции\n' \
            f'id новой позиции: {user.shoes_id_active}'
    user.send_message(text, kb)
    user.save_next_message_handler(add_in_db_menu_2_step_handler)


def add_in_db_menu_2_step_handler(user, data):
    if data == 'back':
        work_in_db_menu(user)
    else:
        query = f"UPDATE Client\n" \
                f"SET shoes_position_for_change='{data}'\n" \
                f"WHERE id = {user.id}"
        conn, cursor = connect()
        cursor.execute(query)
        conn.commit()
        text = f'Напиши {data} Shoes для добавления'
        user.send_message(text, None)
        user.save_next_message_handler(add_position)


def add_position(user, data):
    text = f"'{data}'" if user.shoes_position_for_change in ['description', 'measurements'] else f"{data}"
    conn, cursor = connect()
    query = f'UPDATE Shoes\n' \
            f'SET {user.shoes_position_for_change}={text}\n' \
            f'WHERE id = {user.shoes_id_active}'
    cursor.execute(query)
    conn.commit()
    add_in_db_menu_2_step(user)


def del_in_db_menu(user):
    conn, cursor = connect()
    query = "SELECT id, shoes_code, active, sale, wholesale, retail FROM Shoes"
    cursor.execute(query)
    table = cursor.fetchall()
    # table = [list(str(table[i][j]) for j in range(len(table[i]))) for i in range(len(table))]
    text = '|id|sh_code|activ|sale|wh_sale|retail|\n'
    for lst in table:
        text += '| '
        for el in lst:
            text += str(el) + ' | '
        text += '\n'
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Удалить позицию', callback_data='delete_position')
    btn2 = InlineKeyboardButton('Назад', callback_data='back')
    kb.add(btn1, btn2)
    user.send_message(text, kb)
    user.save_next_message_handler(del_in_db_menu_handler)


def del_in_db_menu_handler(user, data):
    menus = {
        'delete_position': delete_position,
        'back': work_in_db_menu
    }
    menus[data](user)


def delete_position(user):
    text = 'Напиши id Shoes для удаления'
    user.send_message(text, None)
    user.save_next_message_handler(delete_position_handler)


def delete_position_handler(user, data):
    conn, cursor = connect()
    query = f"DELETE FROM Shoes\n" \
            f"WHERE id={data}"
    cursor.execute(query)
    conn.commit()
    del_in_db_menu(user)


def change_in_db_menu(user):
    conn, cursor = connect()
    query = "SELECT id, shoes_code, active, sale, wholesale, retail FROM Shoes"
    cursor.execute(query)
    table = cursor.fetchall()
    text = f'| id {" " * 7}| code | activ   | sale | wh_sale | retail |\n'
    for lst in table:
        text += '| '
        for el in lst:
            text += str(el) + ' | '
        text += '\n'
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Ввести номер позиции для изменеия', callback_data='shoes_id_active')
    btn2 = InlineKeyboardButton('Назад', callback_data='back')
    kb.add(btn1,btn2)
    user.send_message(text, kb)
    user.save_next_message_handler(change_in_db_menu_handler)


def change_in_db_menu_handler(user, data):
    if data == 'back':
        work_in_db_menu(user)
    else:
        change_position_1_step(user)


def change_position_1_step(user):
    text = 'Напиши id Shoes для изменения'
    user.send_message(text, None)
    user.save_next_message_handler(change_position_2_step)


def change_position_2_step(user, data):
    conn, cursor = connect()
    query = f'UPDATE Client ' \
            f'SET shoes_id_active = {int(data)} ' \
            f'WHERE id = {user.id}'
    cursor.execute(query)
    conn.commit()
    change_position_3_step(user)


def change_position_3_step(user):
    conn, cursor = connect()
    query = f"SELECT id, shoes_code, active, sale, wholesale, retail FROM Shoes WHERE id={user.shoes_id_active}"
    cursor.execute(query)
    table = cursor.fetchall()
    text, kb = text_with_keyboard_for_menu_add_and_change(table)
    text += f'\nИзменение позиции\n' \
            f'id позиции: {user.shoes_id_active}'
    user.send_message(text, kb)
    user.save_next_message_handler(add_in_db_menu_3_step_handler)


def add_in_db_menu_3_step_handler(user, data):
    if data == 'back':
        change_in_db_menu(user)
    else:
        query = f"UPDATE Client\n" \
                f"SET shoes_position_for_change='{data}'\n" \
                f"WHERE id = {user.id}"
        conn, cursor = connect()
        cursor.execute(query)
        conn.commit()
        text = f'Напиши {data} Shoes для добавления'
        user.send_message(text, None)
        user.save_next_message_handler(add_position)


# @conn_cursor_handler_decorator
# def set_id(message, conn, cursor):
#     '''
#     создать в БД Юзера, куда передавать месседж обрабатываем в данный момент
#     и его достаем для изменения
#     надо перенести в БД класс Юзер(сделать хранилище функций и ссылки по названиям)
#     '''
#     text = f'INSERT INTO Shoes(id) VALUES({message.text})'
#     cursor.execute(text)
#     conn.commit()
#     edit_menu(message.chat.id, message.id)


HANDLERS = [main_menu_handler, work_in_db_menu_handler, add_in_db_menu_2_step_handler, del_in_db_menu_handler,
            delete_position_handler, add_position, change_in_db_menu_handler, change_position_2_step, add_in_db_menu_3_step_handler]


bot.polling()





