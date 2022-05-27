from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from classes.user import User
from config import MAX_I, MAX_J
import random
import datetime


class Lobby:
    lobbies = []

    def __init__(self, name, bot, creator=None, users=None, max_players=2, lobbies_menu=None):
        self.name = name
        self.bot = bot
        self.creator = creator

        if users is None:
            users = []
        self.users = users
        self.max_players = max_players

        self.active_hero_index = 0
        self.lobbies_menu = lobbies_menu

    def __str__(self):
        return f"Лобби '{self.name}' ({len(self.users)}/{self.max_players})"

    @classmethod
    def find_lobby(cls, name):
        for lobby in cls.lobbies:
            if lobby.name == name:
                return lobby

    def enter(self, user):
        if len(self.users) < self.max_players:
            self.users.append(user)
            user.lobby = self

            for user in self.users:
                self.lobby_menu(user)

            if len(self.users) == self.max_players:
                self.start_game()
        else:
            user.resend_message('Не удалось войти, так как лобби заполнено')

    def set_users_coords(self):
        for user in self.users:
            user.i = random.randint(0, MAX_I - 1)
            user.j = random.randint(0, MAX_J - 1)

    def start_game(self):
        # for user in self.users:
        #     user.resend_message('Игра началась')

        self.set_users_coords()
        self.active_hero_index = 0

        self.main_iter()

    def create_matrix(self):
        matrix = [['-' for j in range(MAX_J)] for i in range(MAX_I)]
        for user in self.users:
            matrix[user.i][user.j] = user.avatar
        return matrix

    def draw_matrix(self, matrix):
        text = ''
        for row in matrix:
            text += '|'
            for sprite in row:
                text += sprite + ' '
            text = text[:-1] + '|\n'
        return text

    def game_menu(self, i, user):
        text = self.draw_matrix(self.create_matrix())

        if i == self.active_hero_index:
            keyboard = ReplyKeyboardMarkup()
            keyboard.row(KeyboardButton('_'), KeyboardButton('вверх'), KeyboardButton('_'))
            keyboard.row(KeyboardButton('влево'), KeyboardButton('_'), KeyboardButton('вправо'))
            keyboard.row(KeyboardButton('_'), KeyboardButton('вниз'), KeyboardButton('закончить'))
        else:
            keyboard = None
        user.resend_message('```\n' + text + '\n```', keyboard)
        user.register_next_step_handler(self.game_menu_handler)

    def game_menu_handler(self, message):
        print(f"{datetime.datetime.now().time()}: Handler call: {message.text} ")
        user = User.find_user_and_delete_message(message, self.bot)
        if self.users.index(user) == self.active_hero_index:
            if message.text in ['вверх', 'вниз', 'влево', 'вправо']:
                user.move(message.text)
                self.main_iter()
            elif message.text.lower() == 'закончить':
                self.end_turn()

    def end_turn(self):
        self.active_hero_index += 1
        if self.active_hero_index == len(self.users):
            self.active_hero_index = 0
        self.main_iter()

    def main_iter(self):
        for i, user in enumerate(self.users):
            self.game_menu(i, user)

    def lobby_menu(self, main_user):
        text = f'---= Лобби {main_user.lobby.name} =---\n'
        for user in main_user.lobby.users:
            text += f"- {user.username}\n"
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.row(KeyboardButton('выход'))
        main_user.resend_message(text, keyboard)
        main_user.register_next_step_handler(self.lobby_menu_handler)

    def lobby_menu_handler(self, message):
        user = User.find_user_and_delete_message(message, self.bot)
        if message.text == 'выход':
            lobby = user.lobby
            user.exit_lobby()
            for l_user in lobby.users:
                self.lobby_menu(l_user)
            self.lobbies_menu(user)
