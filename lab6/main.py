from prettytable import PrettyTable

# Русский алфавит для вычисления V
rus_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
H = 20  # Размер таблицы

# Инициализация хеш-таблицы
table = [{'ID': '', 'C': 0, 'U': 0, 'D': 0, 'Pi': ''} for _ in range(H)]


# Вычисление значения V по первым двум буквам ключа
def get_V(key):
    try:
        first = key[0].upper()
        second = key[1].upper()
        index1 = rus_letters.index(first)
        index2 = rus_letters.index(second)
        return index1 * 33 + index2
    except (IndexError, ValueError):
        raise ValueError("Ключ должен начинаться с двух русских букв")


# Вычисление хеш-адреса
def get_hash(V):
    return V % H


# Вставка ключа и данных
def insert(key, data):
    V = get_V(key)
    h = get_hash(V)
    i = h
    while True:
        if table[i]['U'] == 0 or (table[i]['U'] == 1 and table[i]['D'] == 1):
            table[i]['ID'] = key
            table[i]['Pi'] = data
            table[i]['U'] = 1
            table[i]['D'] = 0
            table[i]['C'] = 0 if i == h else 1
            print(f"Вставлено: '{key}' в слот {i}, C={table[i]['C']}")
            return
        elif table[i]['U'] == 1 and table[i]['D'] == 0 and table[i]['ID'] == key:
            print("Ошибка: Дубликат ключа")
            return
        i = (i + 1) % H
        if i == h:
            print("Ошибка: Таблица заполнена")
            return


# Поиск ключа
def search(key):
    V = get_V(key)
    h = get_hash(V)
    i = h
    while table[i]['U'] == 1:
        if table[i]['D'] == 0 and table[i]['ID'] == key:
            return table[i]['Pi']
        i = (i + 1) % H
        if i == h:
            break
    return "Не найдено"


# Обновление данных по ключу
def update(key, new_data):
    V = get_V(key)
    h = get_hash(V)
    i = h
    while table[i]['U'] == 1:
        if table[i]['D'] == 0 and table[i]['ID'] == key:
            table[i]['Pi'] = new_data
            print(f"Обновлено: '{key}'")
            return
        i = (i + 1) % H
        if i == h:
            break
    print("Ошибка: Ключ не найден")


# Удаление ключа
def delete(key):
    V = get_V(key)
    h = get_hash(V)
    i = h
    while table[i]['U'] == 1:
        if table[i]['D'] == 0 and table[i]['ID'] == key:
            table[i]['D'] = 1
            print(f"Удалено: '{key}'")
            return
        i = (i + 1) % H
        if i == h:
            break
    print("Ошибка: Ключ не найден")


# Вывод таблицы с нерешёнными коллизиями
def display_unresolved_collisions(entries):
    temp_table = [[] for _ in range(H)]
    for key, data in entries:
        V = get_V(key)
        h = get_hash(V)
        temp_table[h].append((key, data))

    pt = PrettyTable()
    pt.field_names = ["Слот", "ID", "Pi"]
    for i in range(H):
        if temp_table[i]:
            ids = ', '.join([key for key, _ in temp_table[i]])
            pis = ', '.join([data for _, data in temp_table[i]])
            rowdata = [i, ids, pis]
            pt.add_row(rowdata)
        else:
            pt.add_row([i, '', ''])
    print("\nХеш-таблица с нерешёнными коллизиями:")
    print(pt)


# Вывод таблицы с разрешёнными коллизиями
def display_resolved_collisions():
    pt = PrettyTable()
    pt.field_names = ["Слот", "ID", "C", "U", "D", "Pi", "V", "h"]
    for i in range(H):
        slot = table[i]
        # Вычисляем V и h только для занятых слотов с непустым ID
        V = get_V(slot['ID']) if slot['U'] == 1 and slot['ID'] else ''
        h = get_hash(V) if V != '' else ''
        rowdata = [i, slot['ID'], slot['C'], slot['U'], slot['D'], slot['Pi'], V, h]
        pt.add_row(rowdata)
    print("\nХеш-таблица с разрешёнными коллизиями:")
    print(pt)
    load_factor = sum(1 for slot in table if slot['U'] == 1 and slot['D'] == 0) / H
    print(f"Коэффициент заполнения: {load_factor:.2f}")


# Начальные записи
initial_entries = [
    ("Ангина", "Воспаление миндалин"),
    ("Анемия", "Недостаток эритроцитов"),
    ("Анорексия", "Расстройство пищевого поведения"),
    ("Аритмия", "Нарушение ритма сердца"),
    ("Бронхит", "Воспаление бронхов"),
    ("Гастрит", "Воспаление желудка"),
    ("Дерматит", "Воспаление кожи"),
    ("Инфаркт", "Омертвение ткани"),
    ("Ларингит", "Воспаление гортани"),
    ("Пневмония", "Воспаление лёгких"),
    ("Тонзиллит", "Воспаление нёбных миндалин")
]


# Функция для интерактивного меню
def run_menu():
    while True:
        print("\nМеню:")
        print("1. Вставить новую запись")
        print("2. Найти запись")
        print("3. Обновить запись")
        print("4. Удалить запись")
        print("5. Показать хеш-таблицу")
        print("6. Выход")
        choice = input("Выберите опцию: ")
        if choice == '1':
            key = input("Введите ключ (медицинский термин): ")
            data = input("Введите данные (определение): ")
            insert(key, data)
        elif choice == '2':
            key = input("Введите ключ для поиска: ")
            result = search(key)
            print(f"Результат: {result}")
        elif choice == '3':
            key = input("Введите ключ для обновления: ")
            new_data = input("Введите новые данные: ")
            update(key, new_data)
        elif choice == '4':
            key = input("Введите ключ для удаления: ")
            delete(key)
        elif choice == '5':
            display_resolved_collisions()
        elif choice == '6':
            print("Выход")
            break
        else:
            print("Неверный выбор")


# Основной блок
if __name__ == "__main__":
    print("Заполнение хеш-таблицы:")
    for key, data in initial_entries:
        insert(key, data)

    display_unresolved_collisions(initial_entries)
    display_resolved_collisions()

    run_menu()
