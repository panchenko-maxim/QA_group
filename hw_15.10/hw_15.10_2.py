"""
2. Статистика по онлайн игре Додо
В игре принимают участие много разных игроков, у каждого из которых уникальных никнейм.
В программе необходимо представить, у какого игрока сколько очков.
Пункты меню:
- батл между 2 игроками:
      пользователь вводит никнейм победителя, никнейм проигравшего, и программа добавляет победителю 5 очков, а у
      проигравшего снимает 4 очка. Если такого игрока еще не было в базе, добавить его.
- очистить список игроков
- выход из программы
"""
import json


def game_battle_1_choice(gamers):
    print('\n-==BATTLE=--')
    winner = input('Enter the name of the winner: ')
    loser = input('Enter the name of the loser: ')
    if winner not in gamers:
        gamers[winner] = 5
    else:
        gamers[winner] += 5
    if loser not in gamers:
        gamers[loser] = -4
    else:
        gamers[loser] -= 4

    return gamers


def clear_player_list_2_choice(gamers):
    while True:
        print('\n', *gamers)
        print('\n--=CLEAR=--\n'
              '1. Remove gamer\n'
              '2. Clear all gamers\n'
              '0. Exit Clear\n')
        choice_clear = input('Your choice: ')
        if choice_clear == '1':
            deleting_a_player = input('Write gamer: ')
            if deleting_a_player in gamers:
                del gamers[deleting_a_player]
            else:
                print('\n!!!No player with that name!!!')
        elif choice_clear == '2':
            gamers.clear()
        elif choice_clear == '0':
            return gamers


def main_data():
    gamers = {
        'Bill': 11,
        'Gabriel': 10,
    }
    return gamers


def main_menu(gamers):
    while True:
        print('\n***GAMERS***')
        [print(gamer, ball) for gamer, ball in gamers.items()]
        print('\n--==MENU=--\n'
              '1. The game - battle\n'
              '2. Clear player list\n'
              '0. Exit')
        choice = input('Your choice: ')
        if choice == '1':
            game_battle_1_choice(gamers)
        elif choice == '2':
            clear_player_list_2_choice(gamers)
        elif choice == '0':
            save_data(gamers)
            break


def save_data(gamers):
    with open('saving_gamers.json', 'wt', encoding='utf-8') as file:
        file.write(json.dumps(gamers, indent=4))


def load_data():
    with open('saving_gamers.json', 'rt', encoding='utf-8') as file:
        gamers = json.loads(file.read())
    return gamers


def try_to_load_data():
    try:
        return load_data()
    except Exception as exc:
        print(f'error while loading: {exc}')
        return main_data()


def main():
    gamers = try_to_load_data()
    main_menu(gamers)


main()
