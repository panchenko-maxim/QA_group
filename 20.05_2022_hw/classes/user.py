from time import sleep
from config import MAX_I, MAX_J


class User:
    users = []

    def __init__(self, bot, chat_id, username='new user', avatar='n', gold=0):
        self.bot = bot
        self.chat_id = chat_id
        self.username = username
        self.avatar = avatar
        self.gold = gold
        self.message_id = None  # последнее сообщение от бота юзеру
        self._help_message = ''  # для доп информации в текущей меню (любой, где это нужно)

        self.lobby_for_edit = None

        self.next_step_handler = None

        self.i = None
        self.j = None

    def register_next_step_handler(self, handler):
        self.next_step_handler = handler

    def clear_help_message(self):
        self._help_message = ''

    @property
    def help_message(self):
        msg = self._help_message
        self.clear_help_message()
        return msg

    @help_message.setter
    def help_message(self, text):  # obj.help_message = 'afsdgf'
        self._help_message = text

    def try_to_save_my_message(self, message):
        if self.message_id is None:
            self.message_id = message.message_id

    def delete_last_message(self):
        try:
            if self.message_id:
                self.bot.delete_message(self.chat_id, self.message_id)
        except Exception as exc:
            return
            print(f'EXCEPTION1: {exc}')

    def delete_my_message(self, message):
        try:
            self.bot.delete_message(self.chat_id, message.message_id)
        except Exception as exc:
            return
            print(f'EXCEPTION2: {exc}')

    def resend_message(self, text, reply_markup=None):
        self.delete_last_message()
        message = self.bot.send_message(self.chat_id, text, reply_markup=reply_markup, parse_mode='markdown')
        self.message_id = message.message_id

    @classmethod
    def create_user(cls, chat_id, bot):
        user = User(bot, chat_id)
        cls.users.append(user)
        return user

    @classmethod
    def find_user(cls, chat_id, bot) -> 'User':
        for user in cls.users:
            if user.chat_id == chat_id:
                return user

        # не нашли -> нужно создать
        user = cls.create_user(chat_id, bot)
        return user

    @classmethod
    def find_user_from_message(cls, message, bot):
        return cls.find_user(message.chat.id, bot)

    @classmethod
    def find_user_and_delete_message(cls, message, bot):
        user = cls.find_user_from_message(message, bot)
        user.delete_my_message(message)
        return user

    def exit_lobby(self):
        if self.lobby:
            self.lobby.users.remove(self)
            self.lobby = None

    def move(self, dir):
        if dir == 'вверх':
            if self.i != 0:
                self.i -= 1
        elif dir == 'вправо':
            if self.j != MAX_J - 1:
                self.j += 1
        elif dir == 'вниз':
            if self.i != MAX_I - 1:
                self.i += 1
        elif dir == 'влево':
            if self.j != 0:
                self.j -= 1
