"""
1. Электронный магазин
В магазине Необходимо представить информацию про товары:
- название
- стоимость
- тип
Программа должна уметь пополнять список товаров, и удалять товары из списка.
При выходе программа должна сохранять данные. При запуске - выгружать данные из файла.
"""
import json


def data():
    store = {
        'paper': {
            'price': 5,
            'type of': 'stationery'},
        'car': {
            'price': 100,
            'type of': 'scrap metal'
        }
    }
    return store


def main_menu(store):
    while True:
        print()
        [print(name, resume) for name, resume in store.items()]
        print('\n--= MENU =--\n'
              '1. Add products\n'
              '2. Delete products\n'
              '0. Exit')

        choice = input('Enter your choice: ')
        if choice == '1':  # Add products
            product = input('Write a product: ')
            product_price = int(input('Write product price: '))
            type_of_product = input('Write product type: ')
            store[product] = {'price': product_price, 'type of': type_of_product}
        elif choice == '2':  # Delete products
            delete_product = input('Write product to remove: ')
            del store[delete_product]
        elif choice == '0':  # Exit
            save_data(store)
            break


def save_data(store):
    with open('saving.json', 'wt', encoding='utf-8') as file:
        file.write(json.dumps(store, indent=4))


def load_data():
    with open('saving.json', 'rt', encoding='utf-8') as file:
        store = json.loads(file.read())
    return store


def try_to_load_data():
    try:
        return load_data()
    except Exception as exc:
        print(f'error while loading: {exc}')
        return data()


def main():
    store = try_to_load_data()
    main_menu(store)


main()