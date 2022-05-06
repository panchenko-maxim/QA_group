class User:
    users = []

    def __init__(self, bot, chat_id, username='new user', gold=500):
        self.bot = bot
        self.chat_id = chat_id
        self.username = username
        self.gold = gold
        self.message_id = None  # последнее сообщение от бота юзеру
        self._help_message = ''  # для доп информации в текущем меню( любом, где это нужно)
        self.lobby = None
        self.my_smile = None
        self.my_weapon = []
        self.purchase_history = {}

    def clear_help_message(self):
        self._help_message = ''

    @property
    def help_message(self):
        msg = self._help_message
        self.clear_help_message()
        return msg

    @help_message.setter
    def help_message(self, text):  # obj.help_message = 'dfdfds'
        self._help_message = text

    def try_to_save_my_message(self, message):
        if self.message_id is None:
            self.message_id = message.message_id

    def delete_last_message(self):
        if self.message_id:
            self.bot.delete_message(self.chat_id, self.message_id)

    def delete_my_message(self, message):
        self.bot.delete_message(self.chat_id, message.message_id)

    def resend_message(self, text, reply_markup=None):
        self.delete_last_message()
        message = self.bot.send_message(self.chat_id, text, reply_markup=reply_markup)
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

        # не нашли, нужно его создать
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
        if self.lobby is True:
            self.lobby.users.remove(self)
            self.lobby = None
