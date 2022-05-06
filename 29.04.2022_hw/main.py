import telebot
from misc import TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from classes.user import User
from classes.lobby import Lobby
from classes.weapon import Weapon

# Можем использовать эти переменные как глобальные
bot = telebot.TeleBot(TOKEN)
Lobby.lobbies.append(Lobby('первое лобби'))
Lobby.lobbies.append(Lobby('второе лобби'))

Weapon.add_to_weapons_lst(Weapon('сабля', 10, 25))
Weapon.add_to_weapons_lst(Weapon('мотыга', 12, 19))
Weapon.add_to_weapons_lst(Weapon('нунчаки', 50, 1))


@bot.message_handler(content_types=['text'])
def text_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    main_menu(user)


@bot.callback_query_handler(lambda message: True)
def inline_button_handler(call):    # при нажатии на инлайн кнопку
    user = User.find_user_from_message(call.message, bot)
    bot.answer_callback_query(call.id)

    if call.data == 'back':
        main_menu(user)

    if 'smile' in call.data:
        smiles = {'smile_happy': '😀', 'smile_neutral': '😐', 'smile_sad': '☹'}
        user.my_smile = smiles[call.data]
        user.help_message = f'смайл обновлен на {user.my_smile}'
        account_settings_menu(user)

    if 'weapon' in call.data:
        print(call.data[7:])
        for weapon in Weapon.weapons_lst:
            if call.data[7:] == weapon.name:
                if user.gold >= weapon.gold:
                    user.gold -= weapon.gold
                    user.my_weapon.append(weapon)
                    user.help_message = f'Удачная покупка - <{weapon.name}>!!!'
                    if weapon.name not in user.purchase_history:
                        user.purchase_history[weapon.name] = 0
                    user.purchase_history[weapon.name] += 1
                    main_menu(user)
                else:
                    user.help_message = 'Мало золота!!!'
                    main_menu(user)

    if 'лобби' in call.data.lower():
        lobby = Lobby.find_lobby(call.data)
        result = lobby.enter(user)

        if result:
            for user in lobby.users:
                lobby_menu(user)
        else:
            user.resend_message('Не удалось войти, так как лобби заполнено')


def main_menu(user):
    text = f'---= Главное меню =---\n' \
           f'{user.help_message}'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton("Играть"), KeyboardButton('Магазин'))
    keyboard.row(KeyboardButton('Настройки аккаунта'))
    # bot.send_message(user.chat_id, text, reply_markup=keyboard)
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, main_handler)


def main_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    text = message.text.lower()
    if 'играть' in text:
        lobbies_menu(user)
    elif 'магазин' in text.lower():
        store_menu(user)
    elif 'настройки аккаунта' in text.lower():
        account_settings_menu(user)


def account_settings_menu(user):
    text = '--= Настройки аккаунта =--\n' \
           f'Ваш никнейм {user.username}\n' \
           f'Ваше золото {user.gold}\n' \
           f'{user.help_message}'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton('Изменить никнейм'), KeyboardButton('Изменить мой смайл'))
    keyboard.row((KeyboardButton('Статистика покупок')))
    keyboard.row(KeyboardButton('Назад'))
    # bot.send_message(user.chat_id, text, reply_markup=keyboard)
    user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(user.chat_id, account_settings_handler)


def account_settings_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    text = message.text.lower()
    if 'изменить никнейм' in text:
        # bot.send_message(user.chat_id, 'Введите новый никнейм:')
        user.resend_message('Введите новый никнейм:')
        bot.register_next_step_handler_by_chat_id(user.chat_id, new_nickname_handler)
    elif 'изменить мой смайл' in text:
        my_smile_menu(user)
    elif 'статистика покупок' in text:
        purchase_history_menu(user)
    elif 'назад' in text:
        main_menu(user)


def new_nickname_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    new_nickname = message.text
    if 5 <= len(new_nickname) <= 20 and ' ' not in new_nickname:
        user.username = new_nickname
        # bot.send_message(user.chat_id, 'Никнейм обновлен')
        # user.resend_message('Никнейм обновлен')
        user.help_message = 'Никнейм обновлен'
        account_settings_menu(user)
    else:
        # bot.send_message(user.chat_id, 'Никнейм не принят (длина и пробелы)')
        user.help_message = 'Никнейм не принят (длина и пробелы)'
        account_settings_menu(user)


def store_menu(user):
    keyboard = InlineKeyboardMarkup()
    for weapon in Weapon.weapons_lst:
        keyboard.row(InlineKeyboardButton(weapon.name, callback_data='weapon_' + weapon.name))
    keyboard.row(InlineKeyboardButton('назад', callback_data='back'))
    user.resend_message('--=Магазин=--', keyboard)


def my_smile_menu(user):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('веселый', callback_data='smile_happy'))
    keyboard.row(InlineKeyboardButton('нейтральный', callback_data='smile_neutral'))
    keyboard.row(InlineKeyboardButton('грустный', callback_data='smile_sad'))
    keyboard.row(InlineKeyboardButton('назад', callback_data='back'))
    user.resend_message('--=Выбор своего смайла=--', keyboard)


def purchase_history_menu(user):
    keyboard = InlineKeyboardMarkup()
    text = f'Ваши покупки:\n'
    for weapon in user.purchase_history:
        text += f'-{weapon} - {user.purchase_history[weapon]} шт\n'
    keyboard.row(InlineKeyboardButton('назад', callback_data='back'))
    user.resend_message(text, keyboard)


def lobbies_menu(user):
    keyboard = InlineKeyboardMarkup()
    for lobby in Lobby.lobbies:
        keyboard.row(InlineKeyboardButton(str(lobby), callback_data=lobby.name))
    keyboard.row(InlineKeyboardButton('назад', callback_data='back'))
    user.resend_message('--=Лобби=--', keyboard)


def lobby_menu(main_user):
    text = f'--= Лобби {main_user.lobby.name}=--\n'
    for user in main_user.lobby.users:
        text += f'- {user.username}\n'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.row(KeyboardButton('выход'))
    main_user.resend_message(text, keyboard)
    bot.register_next_step_handler_by_chat_id(main_user.chat_id, lobby_menu_handler)


def lobby_menu_handler(message):
    user = User.find_user_and_delete_message(message, bot)
    if message.text == 'выход':
        user.exit_lobby()
        lobbies_menu(user)


bot.polling()