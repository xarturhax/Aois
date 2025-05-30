from table import SportHashTable
from prettytable import PrettyTable
import os

def load_sports_terms(file_path):
    terms = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and ':' in line:
                    key, data = line.split(':', 1)
                    terms.append((key.strip(), data.strip()))
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    return terms

def print_table(table, title):
    prettytable = PrettyTable()
    prettytable.field_names = ["№", "ID", "C", "U", "T", "L", "D", "Po", "Pi", "V", "h(V)"]
    for i in range(table.size):
        entry = table.table[i]
        # Показываем только активные (U=1, D=0) или пустые (U=0, D=0) ячейки
        if entry['U'] == 1 and entry['D'] == 0 or (entry['U'] == 0 and entry['D'] == 0):
            v = table.v_function(entry['ID']) if entry['ID'] is not None else ""
            h = table.hash_function(v) if v != "" else ""
            po_value = entry['Po'] if entry['Po'] is not None else ""
            pi_value = entry['Pi'] if entry['Pi'] is not None else ""
            id_value = entry['ID'] if entry['ID'] is not None else "None"
            prettytable.add_row([i, id_value, entry['C'], entry['U'], entry['T'], entry['L'], entry['D'], po_value, pi_value, v, h])
    print(f"\n{title}:")
    print(prettytable)
    print(f"Коэффициент заполнения: {table.get_fill_factor():.2%}")

# Загрузка данных
terms = load_sports_terms('sports.txt')
table = SportHashTable()

# Вставка записей
for key, data in terms:
    success = table[key] = data
    print(f"Вставка ключа '{key}': {'Успешно' if success else 'Ключ уже существует'}")

# Вывод таблицы после вставки
print_table(table, "Хеш-таблица после вставки")

# Операция поиска
print("\nОперация Поиск")
keys_to_search = ["Футбол", "Теннис", "Неизвестный"]
for key in keys_to_search:
    value = table[key]
    print(f"Поиск ключа '{key}': {value}")

# Операция обновления
print("\nОперация Обновление")
updates = [
    ("Футбол", "Командный вид спорта с мячом и двумя командами по 11 игроков"),
    ("Теннис", "Ракеточный вид спорта на корте")
]
for key, data in updates:
    success = table.update(key, data)
    print(f"Обновление ключа '{key}': {'Успешно' if success else 'Не найдено'}")
print_table(table, "Хеш-таблица после обновления")

# Операция удаления
print("\nОперация Удаление")
keys_to_delete = ["Баскетбол", "Плавание", "Неизвестный"]
for key in keys_to_delete:
    success = table.delete(key)
    print(f"Удаление ключа '{key}': {'Успешно' if success else 'Не найдено'}")
print_table(table, "Хеш-таблица после удаления")

