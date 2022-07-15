from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.db import connect
from tools.pizza_sizes import pizza_sizes
from tools.order_status import order_status


def examination(admin):
    admin.send_message('Введіть пароль:')
    admin.next_message_handler(admin, text)



def admin_main_menu(admin):
    pass








