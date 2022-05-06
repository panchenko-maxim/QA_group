class Weapon:
    weapons_lst = []

    def __init__(self, name, gold, damage,):
        self.name = name
        self.gold = gold
        self.damage = damage

    @classmethod
    def add_to_weapons_lst(cls, weapon):
        cls.weapons_lst.append(weapon)
