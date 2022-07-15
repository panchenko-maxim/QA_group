from db.db import connect
from tools.pizza_sizes import pizza_sizes
from tools.order_status import order_status


class Admin:
    password = 'admin'

    def __init__(self, bot, bot_message_id, next_message_handler):
        self.bot = bot
        self.bot_message_id = bot_message_id
        self.next_message_handler = next_message_handler

    @classmethod
    def set_bot(cls, bot, bot_message_id):
        return cls(bot, bot_message_id)

    def send_message(self, message, keyboard=None):
        if self.bot_message_id is None:
            message = self.bot.send_message(message.chat.id, message, reply_markup=keyboard)
            self.save_bot_message_id(message.message_id)
        else:
            try:
                message = self.bot.edit_message_text(message, message.chat.id, self.bot_message_id,
                                                     reply_markup=keyboard)
            except Exception as exc:
                if not 'message is not modified' in exc.description.lower():
                    raise exc

    def save_bot_message_id(self, bot_message_id):
        self.bot_message_id = bot_message_id
