import json
from random import randint, choice, randrange
import time


def main_data():                                                # глобальные данные
    cutlet = {                                                  # котлета
        'name': 'hot friend',
        'health': 50,
        'max health': 100,
        'mood': 10,                                             # настроение
        'satiety': 20,                                          # сытость
        'max satiety': 30,
        'toys': {
            'soldier': 1,
            'paper': 3,
            'tomato': 1
        }
    }
    gamer = {                                                   # игрок
        'player turn': 0,
        'coins': 0
    }
    shop = {}

    with open('shop.csv', 'rt', encoding='utf-8') as file:
        header = file.readline().rstrip().split(',')
        ind_toy = header.index('toy')
        ind_price = header.index('price')
        ind_total = header.index('total')
        ind_mood = header.index('mood')
        for line in file:
            toy = line.rstrip().split(',')
            shop[toy[ind_toy]] = {'price': int(toy[ind_price]),
                                  'total': int(toy[ind_total]),
                                  'mood': int(toy[ind_mood])}
    return cutlet, gamer, shop


def main_choice_1_work_for_coins(gamer):                        # ВЫБОР МЕНЮ 1: Работать за монеты
    while True:
        print('\n---=WORK FOR COINS=---\n'
              f'COINS: {gamer["coins"]}  |  turn: {gamer["player turn"]}\n'
              '1. Care for the environment\n'                   # Забота об окружающей среде
              '2. Do tasks\n'                                   # Делать задачи
              '3. Play for money\n'                             # Играть на деньги
              '4. Steal from people\n'                          # Воровать у людей
              '5. Hard work\n'                                  # Тяжелая работа
              '0. EXIT')                                        # Выход

        work_choice = input('Choose a job: ')

        if work_choice == '1':                                  # Забота об окружающей среде
            main_choice_1_work_1_care_for_the_environment(gamer)
        elif work_choice == '2':                                # Решать задачи
            main_choice_1_work_2_do_tasks(gamer)
        elif work_choice == '3':                                # Играть на деньги
            main_choice_1_work_3_play_for_money(gamer)
        elif work_choice == '4':                                # Воровать у людей
            print('\nIN DEVELOPING...')
            print('Stealing from people is not good!')
            print('¯ \ _ (ツ) _ / ¯')
        elif work_choice == '5':                                # Тяжелая работа
            print('\nIN DEVELOPING...')
            print('HARD JOB NOT FOR US!')
            print('😢')
        elif work_choice == '0':                                # Выход
            return gamer


def main_choice_1_work_1_care_for_the_environment(gamer):       # Забота об окружающей среде
    while True:
        print('\n---=Care for the environment=---\n'
              f'COINS: {gamer["coins"]}  |  turn: {gamer["player turn"]}\n'
              '1. Collect and sell bottles\n'                   # Собирать и продавать бутылки
              '2. Collect and sell paper\n'                     # Собирать и продавать бумагу
              '3. Sort garbage in a landfill\n'                 # Сортировать мусор на свалке 
              '4. Mow the grass\n'                              # Косить травку
              '0. EXIT')                                        # Выход
        choice_care = input('Your choice is a lazy person: ')

        if choice_care == '1':                                  # Собирать и продавать бутылки
            print('\nEnter the number where you are looking for bottles')
            print('1.🗑 urn |  2.🌳 - Bush  | 3.🏠 - Near houses')
            search_for_bottles = input('look in: ')
            num_bottle = str(randint(1, 3))
            if search_for_bottles == num_bottle:
                gamer["coins"] += 1
                print('You found the bottle and sold it for 1 coin!')
            else:
                print('There is no bottle here')

        elif choice_care == '2':                                # Собирать и продавать бумагу
            print('\nEnter the number where you are looking for paper')
            print('1.🗑 urn |  2.🌳 - Bush  | 3.🏠 - Near houses')
            search_for_paper = input('look in: ')
            num_paper = str(randint(1, 3))
            if search_for_paper == num_paper:
                kilograms_of_paper = randint(1, 100)
                paper_price = int(kilograms_of_paper * 0.1)
                print(f"You found {kilograms_of_paper} kilograms of paper - that's {paper_price} coins")
                gamer["coins"] += paper_price
            else:
                print('There is no paper here')

        elif choice_care == '3':                                # Сортировать мусор на свалке
            print('\nSort the trash press ENTER')
            click = randint(5, 20)
            count_clic = 0
            while count_clic != click:
                press_enter = input('Work fast: ')
                if press_enter == '':
                    count_clic += 1
                else:
                    count_clic -= 1
                    print('Do your job man!')
            print("Good job - you earned 1 coin!")
            gamer["coins"] += 1

        elif choice_care == '4':                                # Косить травку
            relax = randint(1, 20)
            relax_count = 0
            sleep = 'z'
            while relax_count != relax:
                print(sleep)
                time.sleep(randint(0, 2))
                relax_count += 1
                sleep += 'z'
            print('Smoking - harm to health!')

        elif choice_care == '0':                                # Выход
            return gamer


def main_choice_1_work_2_do_tasks(gamer):                       # Решать задачи
    while True:
        print('\n---=Do Tasks=---\n'
              f'COINS: {gamer["coins"]}  |  turn: {gamer["player turn"]}\n'
              '1. Easy level\n'                                 # Легкий уровень
              '2. Middle level\n'                               # Средний уровень
              '3. Hard level\n'                                 # Сложный уровень
              '0. EXIT')                                        # Выход
        level = input('Choose level: ')

        number_1 = randint(10, 100)
        number_2 = randint(1, 10)
        number_3 = randint(1, 20)
        number_4 = randint(1, 30)
        sign_1 = choice('-+/*')
        sign_2 = choice('-+/*')
        sign_3 = choice('-+/*')

        if level == '1':                                            # Легкий уровень
            result = int(operations_on_numbers(number_1, number_2, sign_1))
            print(f'\nAnswer the task (int): {number_1} {sign_1} {number_2} =', end=' ')
            answer = int(input())
            if answer == result:
                gamer["coins"] += 1
                print('GOOD JOB, keep 1 coin')
            else:
                print('Bad, very bad!')
                gamer["coins"] -= 1
        elif level == '2':                                          # Средний уровень
            oper_num1_num2 = int(operations_on_numbers(number_1, number_2, sign_1))
            result = int(operations_on_numbers(oper_num1_num2, number_3, sign_2))
            print(f'\nAnswer the task (int): ({number_1} {sign_1} {number_2}) {sign_2} {number_3} =', end=' ')
            answer = int(input())
            if answer == result:
                gamer["coins"] += 2
                print('GOOD JOB, keep 2 coin')
            else:
                print('Bad, very bad!')
                gamer["coins"] -= 2
        elif level == '3':                                          # Сложный уровень
            oper_num1_num2 = int(operations_on_numbers(number_1, number_2, sign_1))
            oper_num_1_num_2_num_3 = int(operations_on_numbers(oper_num1_num2, number_3, sign_2))
            result = int(operations_on_numbers(oper_num_1_num_2_num_3, number_4, sign_3))
            print(f'\nAnswer the task (int): (({number_1} {sign_1} {number_2}) {sign_2} {number_3}) '
                  f'{sign_3} {number_4} =', end=' ')
            answer = int(input())
            if answer == result:
                gamer["coins"] += 3
                print('GOOD JOB, keep 3 coin')
            else:
                print('Bad, very bad!')
                gamer["coins"] -= 3
        elif level == '0':                                          # Выход
            return gamer


def operations_on_numbers(num_1, num_2, sign):                      # Операция надо двумя числами
    if sign == '-':
        return num_1 - num_2
    elif sign == '+':
        return num_1 + num_2
    elif sign == '/':
        return num_1 / num_2
    elif sign == '*':
        return num_1 * num_2


def main_choice_1_work_3_play_for_money(gamer):                     # Играть на деньги
    while True:
        print('\n---=Play for money=---\n'
              f'COINS: {gamer["coins"]}  |  turn: {gamer["player turn"]}\n'
              '1. Play\n'                                           # Играть
              '0. EXIT')                                            # Выход
        choice_play = input('Your choice: ')
        if choice_play == '1':
            print(f"We play on {choice(['roulette', 'machine', 'leg', 'game cards', 'nerves'])}...")
            time.sleep(randint(0, 5))
            result = randint(0, 3)
            if result == 3:                                         # Победа в игре
                win = randint(0, 2000)
                print(f'\nCONGRATULATIONS! YOU WIN: {win} coins')
                gamer["coins"] += win
            else:
                lose = randint(0, 1000)                             # Проигрыш в игре
                print(f'\n YOU LOSE: {lose} coins')
                gamer["coins"] -= lose

        elif choice_play == '0':
            return gamer


def main_choice_2_buy_a_toy_for_your_cutlet(cutlet, gamer, shop):         # Купить игрушку котлете
    while True:
        print('\nThe cutlet is very happy 😍! She really wants a toy 🧸\n'
              '\nYou are looking for a toy 🔍:\n'
              '1. In the shop\n'                                    # Искать в магазине
              '2. In the market\n'                                  # Искать на рынке
              '3. In the second-hand\n'                             # Искать в секонд-хенда
              '4. In a dumpster\n'                                  # Порыться в мусорном контейнере
              '0. Exit and leave the cutlet without a toy\n')       # Выйти и оставить котлету без игрушки(
        search_in = input('Search in: ')

        if search_in == '1':                                        # Искать в магазине
            main_choice_2_buy_a_toy_1_in_the_shop(cutlet, gamer, shop)
        elif search_in == '2':                                      # Искать на рынке
            main_choice_2_buy_a_toy_2_in_the_market(cutlet, gamer, shop)
        elif search_in == '3':                                      # Искать в секонд-хенде
            main_choice_2_buy_a_toy_3_in_the_second_hand(cutlet, gamer)
        elif search_in == '4':                                      # Порыться в мусорном контейнере
            main_choice_2_buy_a_toy_4_in_a_dumpster(cutlet, gamer)
        elif search_in == '0':                                      # Выйти и оставить котлету без игрушки(
            return cutlet, gamer, shop


def main_choice_2_buy_a_toy_1_in_the_shop(cutlet, gamer, shop):           # Искать в магазине
    while True:
        print('\n---------------------\n'
              f'name: {cutlet["name"]}\n'
              f'❤: {cutlet["health"]}/(max{cutlet["max health"]})\n'
              f'😊: {cutlet["mood"]}\n'
              f'💋: {cutlet["satiety"]}/(max{cutlet["max satiety"]})\n'
              f'toys: {cutlet["toys"]}')
        print('---=Shop=---\n'
              f'COINS: {gamer["coins"]}  |  turn: {gamer["player turn"]}\n'
              '1. Choose a toy randomly\n'                          # Выбрать игрушку рандомом
              '2. Ask the cutlet what she wants\n'                  # Спросить у котлеты, что она хочет
              '3. I will choose a toy\n'                            # Самому выбрать игрушку
              '0. Leave the store in tears')                        # Покинуть магазин в слезах

        shop_key_lst = list(shop)
        choice_shop = input('Your choice:')

        if choice_shop == '1':                                      # Выбрать игрушку рандомом
            rand_toy = choice(shop_key_lst)
            print(rand_toy)
            print(f"Congratulations, now the cutlet has a toy: {rand_toy}. "
                  f"Its cost is {shop[rand_toy]['price']} coins!")
            if gamer['coins'] > shop[rand_toy]['price']:
                print(f'Attention: you have coins for this purchase')
                gamer['coins'] -= shop[rand_toy]['price']
                if rand_toy not in cutlet['toys']:
                    cutlet['toys'][rand_toy] = 1
                    cutlet['mood'] += shop[rand_toy]['mood']
                else:
                    cutlet['toys'][rand_toy] += 1
                    cutlet['mood'] += shop[rand_toy]['mood']
            else:
                print(f'Attention: you have no money for this purchase. Leave the shop!')

        elif choice_shop == '2':                                    # Спросить у котлеты, что она хочет
            print(f"\nTOYS: {', '.join(shop_key_lst)}")
            print('--=Ask the cutlet what she wants=--\n'
                  '1. Suggest toys by name\n'                       # предлагать игрушки по названию
                  '2. Let the cutlet tell itself\n'                 # пусть котлета сама скажет
                  '0. Exit. Bad idea!')                             # выйти
            choice_toy = input('Your choice, papa: ')
            if choice_toy == '1':                                   # предлагать игрушки по названию
                name_toy = input('Write a toy: ').lower()
                if name_toy in shop and gamer['coins'] > shop[name_toy]['price']:
                    print(f"Congratulations, now the cutlet has a toy: {name_toy}. "
                          f"Its cost is {shop[name_toy]['price']} coins!")
                    print(f'Attention: you have coins for this purchase')
                    gamer['coins'] -= shop[name_toy]['price']
                    if name_toy not in cutlet['toys']:
                        cutlet['toys'][name_toy] = 1
                        cutlet['mood'] += shop[name_toy]['mood']
                    else:
                        cutlet['toys'][name_toy] += 1
                        cutlet['mood'] += shop[name_toy]['mood']
                else:
                    print(f'Attention: you have no money for this purchase. Leave the shop!')

            elif choice_toy == '2':                                 # пусть котлета сама скажет
                for_cutlet = choice(shop_key_lst)
                print(f'Cutlet says: "I wont a {for_cutlet}, '
                      f'and I know that it costs {shop[for_cutlet]["price"]} coins !!!"')
                choice_for_cutlet = input("Your answer(YES or NOT): ").lower()
                if choice_for_cutlet == 'yes':
                    if gamer['coins'] > shop[for_cutlet]['price']:
                        if for_cutlet not in cutlet['toys']:
                            cutlet['toys'][for_cutlet] = 1
                            cutlet['mood'] += shop[for_cutlet]['mood']
                        else:
                            cutlet['toys'][for_cutlet] += 1
                            cutlet['mood'] += shop[for_cutlet]['mood']
                    else:
                        print(f'Attention: you have no money for this purchase. Leave the shop!')

                else:
                    print('Very strange answer!')
            elif choice_toy == '0':
                print('Cutlet: "No, papa, I do not love you!"')
                break
        elif choice_shop == '3':                                    # Самому выбрать игрушку
            print('\n--=The store has these toys=--')
            [print(f"{el}({shop[el]['price']} coins); ", end=' ') for el in shop_key_lst]
            i_choose = input('\nI choose: ').lower()
            if i_choose in shop and gamer['coins'] > shop[i_choose]['price']:
                print(f"Congratulations, now the cutlet has a toy: {i_choose}. "
                      f"Its cost is {shop[i_choose]['price']} coins!")
                print(f'Attention: you have coins for this purchase')
                gamer['coins'] -= shop[i_choose]['price']
                if i_choose not in cutlet['toys']:
                    cutlet['toys'][i_choose] = 1
                    cutlet['mood'] += shop[i_choose]['mood']
                else:
                    cutlet['toys'][i_choose] += 1
                    cutlet['mood'] += shop[i_choose]['mood']
            else:
                print(f'Attention: you have no money for this purchase. Leave the shop!')
        elif choice_shop == '0':                                  # Покинуть магазин в слезах
            return cutlet, gamer, shop


def main_choice_2_buy_a_toy_2_in_the_market(cutlet, gamer, shop):       # Искать на рынке
    if randint(0, 1) == 0:
        print('Quarantine! Go home!')
    else:
        while True:
            print('\n---------------------\n'
                  f'name: {cutlet["name"]}\n'
                  f'❤: {cutlet["health"]}/(max{cutlet["max health"]})\n'
                  f'😊: {cutlet["mood"]}\n'
                  f'💋: {cutlet["satiety"]}/(max{cutlet["max satiety"]})\n'
                  f'toys: {cutlet["toys"]}')
            print('---=Market "LONELY NERD"=---\n'
                  f'COINS: {gamer["coins"]}  |  turn: {gamer["player turn"]}\n'
                  '1. Look for a toy\n'                          # Искать игрушку
                  '0. Exit. The market is not for me\n')         # Выход. Рынок не для меня

            market_choice = input()
            if market_choice == '1':                             # Искать игрушку
                search_in_market = ['fresh fish', 'pig feed', 'aquarium', 'kvass', 'cigarettes', 'boots']
                print('Search...')
                time.sleep(randint(1, 5))
                if randint(0, 1) == 0:
                    not_toy = choice(search_in_market)
                    print(f'You found a {not_toy}, but the {not_toy} is not a toy')
                else:
                    print('BOARD: 1 row - goods for children, 2 row - goods from children')
                    wich_row = input('Which row will you choose?: ')
                    if wich_row == '1':                         # Товары для детей
                        while True:
                            print('--=Some kind of boutique=--\n'
                                  f''
                                  '1. To bargain\n'               # Торговаться
                                  '2. Seller advice\n'            # Совет продавца
                                  '3. Watch and walk by\n'        # Смотреть и идти мимо
                                  '0. Exit. I got lost and frozen!')

                            sellers = ['Ashot', 'Olga', 'ankle Vanya', 'Valya']
                            boutique_choice = input('Your choice: ')
                            if boutique_choice == '1':            # Торговаться
                                print(f'{choice(sellers)}: how much money is there?')
                                answer = int(input('Write how much money you will give: '))
                                if answer > gamer['coins']:
                                    print("You're a liar!")
                                else:
                                    sellers_offer = choice(list(shop))
                                    print(f'Here is a {sellers_offer}, buy for {(shop[sellers_offer]["price"]) + 100}')
                                    answer_2 = input('YES or NOT?: ').lower()
                                    if answer_2 == 'yes':
                                        if gamer['coins'] > (shop[sellers_offer]["price"]) + 100:
                                            print(f'Attention: you have coins for this purchase')
                                            gamer['coins'] -= (shop[sellers_offer]["price"]) + 100
                                            if sellers_offer not in cutlet['toys']:
                                                cutlet['toys'][sellers_offer] = 1
                                                cutlet['mood'] += shop[sellers_offer]['mood']
                                            else:
                                                cutlet['toys'][sellers_offer] += 1
                                                cutlet['mood'] += shop[sellers_offer]['mood']
                                        else:
                                            print(f'Attention: you have no money for this purchase. '
                                                  f'Leave the boutique!')
                                    else:
                                        print('Go HOME')

                            elif boutique_choice == '2':          # Совет продавца
                                sellers_offer = choice(list(shop))
                                print(f'Here is a {sellers_offer}, buy for {(shop[sellers_offer]["price"]) + - 100},'
                                      f'but you have to bargain')
                            elif boutique_choice == '3':          # Смотреть и идти мимо
                                for el in list(shop):
                                    print(f'{el}...')
                                    time.sleep(randint(0,2))
                            else:
                                break

                    elif wich_row == '2':                       # Товары от детей
                        print('Goods from children not for our country!')
            else:                                               # Выход. Рынок не для меня
                return cutlet, gamer, shop


def main_choice_2_buy_a_toy_3_in_the_second_hand(cutlet, gamer):  # Искать в секонд-хенде
    pass


def main_choice_2_buy_a_toy_4_in_a_dumpster(cutlet, gamer):       # Порыться в мусорном контейнере
    pass


def main_menu(cutlet, gamer, shop):                                     # главное меню
    while True:
        print('\n---WHEN YOUR FRIEND IS A CUTLET---\n'
              f'name: {cutlet["name"]}\n'
              f'❤: {cutlet["health"]}/(max{cutlet["max health"]})\n'
              f'😊: {cutlet["mood"]}\n'
              f'💋: {cutlet["satiety"]}/(max{cutlet["max satiety"]})\n'
              f'toys: {cutlet["toys"]}\n')
        print('---=MAIN MENU=---\n'
              f'COINS: {gamer["coins"]}  |  turn: {gamer["player turn"]}\n'
              '1. Work for coins for your cutlet\n'             # Работать за монеты
              '2. Buy a toy for your cutlet\n'                  # Купить игрушку котлете
              '3. Play with a cutlet\n'                         # Играть с котлетой
              '4. Treat a cutlet\n'                             # Полечить котлету   
              '5. Feed the cutlet\n'                            # Покормить котлету
              '0. EXIT')                                        # Выход

        main_choice = input('YOUR CHOICE: ')

        if main_choice == '1':                                  # Работать за монеты
            main_choice_1_work_for_coins(gamer)
        elif main_choice == '2':                                # Купить игрушку котлете
            main_choice_2_buy_a_toy_for_your_cutlet(cutlet, gamer, shop)
        elif main_choice == '3':                                # Играть с котлетой
            pass
        elif main_choice == '4':                                # Полечить котлету
            pass
        elif main_choice == '5':                                # Покормить котлету
            pass
        elif main_choice == '0':                                # Выход
            save_data(cutlet, gamer, shop)
            break


def save_data(cutlet, gamer, shop):                                   # Сохранение
    with open('cutlet.json', 'wt', encoding='utf-8') as file:
        file.write('{ "cutlet":' + (json.dumps(cutlet, indent=4)) + ', "gamer":' + (json.dumps(gamer, indent=4)))
        file.write(', "shop":' + (json.dumps(shop, indent=4)) + '}')


def load_data():                                                # Загрузка
    with open('cutlet.json', 'rt', encoding='utf-8') as file:
        data = json.loads(file.read())
        return data["cutlet"], data["gamer"], data["shop"]


def try_to_load_data():                                         # Загрузка при ошибке
    try:
        return load_data()
    except Exception as exc:
        print(f'Error while loading: {exc}')
        return main_data()


def main():
    cutlet, gamer, shop = try_to_load_data()
    main_menu(cutlet, gamer, shop)


main()