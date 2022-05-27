import telebot
from misc import TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from classes.user import User
from classes.lobby import Lobby


# Можем использовать эти переменные как глобальные
bot = telebot.TeleBot(TOKEN)
# bot.send_message(123, '', parse_mode='')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    if user.next_step_handler:
        user.next_step_handler(message)
    else:
        main_menu(user)


@bot.callback_query_handler(lambda call: True)
def inline_button_handler(call):  # ПРИ НАЖАТИИ НА ИНЛАЙН КНОПОЧКУ
    user = User.find_user_from_message(call.message, bot)
    bot.answer_callback_query(call.id)

    if call.data == 'back':
        return main_menu(user)
    elif call.data == 'create_lobby':
        return create_lobby(user)
    elif call.data == 'delete_lobby':
        return delete_or_edit_lobby(user, 'Удалить лобби')
    elif call.data.startswith('destroy_'):
        return destroy_lobby(call.data, user)
    elif call.data == 'edit_lobby':
        return delete_or_edit_lobby(user, 'Редактировать лобби', flag='edit_')
    elif call.data.startswith('edit'):
        return edit_lobby(call.data[5:], user)
    elif call.data.startswith('name_'):
        return new_name_lobby(user)
    elif call.data.startswith('num_'):
        return new_max_players_lobby(user)

    lobby = Lobby.find_lobby(call.data)
    lobby.enter(user)


def create_lobby(user):
    user.resend_message('Введите количество игроков и название лобби через пробел):')
    user.register_next_step_handler(create_lobby_handler)


def create_lobby_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    text = message.text
    num = 2
    name = 'lobby for Bobby'
    if text.split()[0].isdigit():
        num = int(text.split()[0])
    if len(text.split()) > 1:
        name = ' '.join(text.split()[1:])

    Lobby.lobbies.append(Lobby(name, bot, creator=user, max_players=num, lobbies_menu=lobbies_menu))
    lobbies_menu(user)


def delete_or_edit_lobby(user, text, flag='destroy_'):
    keyboard = InlineKeyboardMarkup()
    for lobby in Lobby.lobbies:
        if user == lobby.__dict__['creator']:
            keyboard.row(InlineKeyboardButton(str(lobby), callback_data=f'{flag}{lobby.name}'))
    keyboard.row(InlineKeyboardButton('назад', callback_data='back'))
    user.resend_message(f'--= {text} =--', keyboard)


def destroy_lobby(name_lobby, user):
    index_for_destroy = None
    for i, lobby in enumerate(Lobby.lobbies):
        if name_lobby[8:] == lobby.__dict__['name']:
            index_for_destroy = i
            break
    Lobby.lobbies.pop(index_for_destroy)
    lobbies_menu(user)


def edit_lobby(name_lobby, user):
    keyboard = InlineKeyboardMarkup()
    for lobby in Lobby.lobbies:
        if name_lobby == lobby.__dict__['name']:
            user.lobby_for_edit = lobby
    keyboard.row(InlineKeyboardButton(f'Изменить имя: {user.lobby_for_edit.name}',
                                      callback_data=f'name_'))
    keyboard.row(InlineKeyboardButton(f'Изменить количество участников: {user.lobby_for_edit.max_players}',
                                      callback_data=f'num_'))
    keyboard.row(InlineKeyboardButton('Назад', callback_data='back'))
    user.resend_message(f'--= Меню редактирования =--', keyboard)


def new_name_lobby(user):
    user.resend_message('Введите новое имя лобби:')
    user.register_next_step_handler(new_name_lobby_handler)


def new_name_lobby_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    new_name = message.text
    if len(new_name) < 100:
        user.lobby_for_edit.name = new_name
    edit_lobby(user.lobby_for_edit.name, user)


def new_max_players_lobby(user):
    user.resend_message('Введите новое количество участников:')
    user.register_next_step_handler(new_max_players_lobby_handler)


def new_max_players_lobby_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    new_numbers = message.text
    if new_numbers.isdigit() and 0 < int(new_numbers) < 10:
        user.lobby_for_edit.max_players = int(new_numbers)
    edit_lobby(user.lobby_for_edit.name, user)


def main_menu(user):
    text = '---= Главное меню =---'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton('Играть'), KeyboardButton('Магазин'))
    keyboard.row(KeyboardButton('Настройки аккаунта'))
    user.resend_message(text, keyboard)
    user.register_next_step_handler(main_handler)


def main_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    text = message.text.lower()
    if 'играть' in text:
        lobbies_menu(user)
    elif 'настройки аккаунта' in text:
        account_settings_menu(user)


def account_settings_menu(user):
    text = '--= Настройки аккаунта =--\n' \
           f'Ваш никнейм: {user.username}\n' \
           f'Ваш аватар: {user.avatar}\n' \
           f'Ваше золото: {user.gold}\n\n' \
           f'{user.help_message}'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton('Изменить никнейм'), KeyboardButton('Изменить аватар'))
    keyboard.row(KeyboardButton('Назад'))
    user.resend_message(text, keyboard)
    user.register_next_step_handler(account_settings_handler)


def account_settings_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    text = message.text.lower()
    if 'изменить никнейм' in text:
        user.resend_message('Введите новый никнейм:')
        user.register_next_step_handler(new_nickname_handler)
    elif 'изменить аватар' in text:
        user.resend_message('Введите новый аватар:')
        user.register_next_step_handler(new_avatar_handler)
    elif 'назад' in text:
        main_menu(user)


def new_avatar_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    new_avatar = message.text  # 'o'
    if len(new_avatar) == 1 and new_avatar.isalpha():
        user.avatar = new_avatar.lower()
        account_settings_menu(user)
    else:
        user.help_message = 'Аватар должен быть 1 буквой.'
        account_settings_menu(user)


def new_nickname_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    new_nickname = message.text
    if 3 <= len(new_nickname) <= 20 and ' ' not in new_nickname:
        user.username = new_nickname
        user.help_message = 'Никнейм обновлен'
        account_settings_menu(user)
    else:
        user.help_message = 'Никнейм не принят'
        account_settings_menu(user)


def lobbies_menu(user):
    keyboard = InlineKeyboardMarkup()
    for lobby in Lobby.lobbies:
        keyboard.row(InlineKeyboardButton(str(lobby), callback_data=lobby.name))
    keyboard.row(InlineKeyboardButton('назад', callback_data='back'))
    keyboard.row(InlineKeyboardButton('Создать лобби', callback_data='create_lobby'),
                 InlineKeyboardButton('Удалить лобби', callback_data='delete_lobby'),
                 InlineKeyboardButton('Редактировать лобби', callback_data='edit_lobby'))
    user.resend_message('--= Лобби =--', keyboard)


def test_handler(call):
    print(call)


Lobby.lobbies.append(Lobby('первое лобби', bot, lobbies_menu=lobbies_menu))
Lobby.lobbies.append(Lobby('второе лобби', bot, lobbies_menu=lobbies_menu))
Lobby.lobbies.append(Lobby('третье лобби', bot, lobbies_menu=lobbies_menu, max_players=3))
bot.polling()
