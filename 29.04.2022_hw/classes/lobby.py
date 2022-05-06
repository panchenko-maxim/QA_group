class Lobby:
    lobbies = []

    def __init__(self, name, users=None, max_players=3):
        self.name = name

        if users is None:
            users = []
        self.users = users
        self.max_players = max_players

    def __str__(self):
        return f'Лобби "{self.name}" ({len(self.users)}/{self.max_players})'

    @classmethod
    def find_lobby(cls, name):
        for lobby in cls.lobbies:
            if lobby.name == name:
                return lobby

    def enter(self, user):
        if len(self.users) < self.max_players:
            self.users.append(user)
            user.lobby = self
            return True
        else:
            return False

