import pytest
from main import get_V, get_hash, insert, search, update, delete, table, H, display_unresolved_collisions, display_resolved_collisions, initial_entries, run_menu
from io import StringIO

# Фикстура для очистки таблицы перед каждым тестом
@pytest.fixture
def clear_table():
    global table
    table[:] = [{'ID': '', 'C': 0, 'U': 0, 'D': 0, 'Pi': ''} for _ in range(H)]
    return table

# Тесты для функции get_V
def test_get_V_valid_key():
    assert get_V("Ангина") == 14  # А=0, н=13, 0*33 + 13 = 14
    assert get_V("Пневмония") == 542  # П=15, н=13, 15*33 + 13 = 542

def test_get_V_invalid_key():
    with pytest.raises(ValueError, match="Ключ должен начинаться с двух русских букв"):
        get_V("А")  # Слишком короткий ключ
    with pytest.raises(ValueError, match="Ключ должен начинаться с двух русских букв"):
        get_V("A1")  # Нерусские буквы

def test_get_V_empty_key():
    with pytest.raises(ValueError, match="Ключ должен начинаться с двух русских букв"):
        get_V("")  # Пустой ключ

# Тесты для функции get_hash
def test_get_hash():
    assert get_hash(14) == 14  # 14 % 20 = 14
    assert get_hash(542) == 2  # 542 % 20 = 2
    assert get_hash(642) == 2  # 642 % 20 = 2

# Тесты для функции insert
def test_insert_no_collision(clear_table):
    insert("Бронхит", "Воспаление бронхов")  # V=50, h=10
    assert table[10]['ID'] == "Бронхит"
    assert table[10]['Pi'] == "Воспаление бронхов"
    assert table[10]['C'] == 0
    assert table[10]['U'] == 1
    assert table[10]['D'] == 0

def test_insert_with_collision(clear_table):
    insert("Ангина", "Воспаление миндалин")  # h=14
    insert("Анемия", "Недостаток эритроцитов")  # h=14
    insert("Анорексия", "Расстройство пищевого поведения")  # h=14
    assert table[14]['ID'] == "Ангина"
    assert table[14]['C'] == 0
    assert table[15]['ID'] == "Анемия"
    assert table[15]['C'] == 1
    assert table[16]['ID'] == "Анорексия"
    assert table[16]['C'] == 1

def test_insert_duplicate_key(clear_table, capsys):
    insert("Ангина", "Воспаление миндалин")
    insert("Ангина", "Другое описание")
    captured = capsys.readouterr()
    assert "Ошибка: Дубликат ключа" in captured.out

def test_insert_full_table(clear_table, capsys):
    for i in range(H):
        key = f"Ка{i:02d}"  # Используем 'Ка' для двух русских букв
        insert(key, f"Данные{i}")
    insert("Новый", "Данные")
    captured = capsys.readouterr()
    assert "Ошибка: Таблица заполнена" in captured.out

def test_insert_over_deleted(clear_table):
    insert("Ангина", "Воспаление миндалин")  # h=14
    delete("Ангина")
    insert("Анемия", "Недостаток эритроцитов")  # h=14
    assert table[14]['ID'] == "Анемия"
    assert table[14]['D'] == 0

# Тесты для функции search
def test_search_existing_key(clear_table):
    insert("Ангина", "Воспаление миндалин")
    assert search("Ангина") == "Воспаление миндалин"

def test_search_non_existing_key(clear_table):
    assert search("Неизвестно") == "Не найдено"

def test_search_deleted_key(clear_table):
    insert("Ангина", "Воспаление миндалин")
    delete("Ангина")
    assert search("Ангина") == "Не найдено"

# Тесты для функции update
def test_update_existing_key(clear_table, capsys):
    insert("Ангина", "Воспаление миндалин")
    update("Ангина", "Новое описание")
    assert table[14]['Pi'] == "Новое описание"
    captured = capsys.readouterr()
    assert "Обновлено: 'Ангина'" in captured.out

def test_update_non_existing_key(clear_table, capsys):
    update("Неизвестно", "Новое описание")
    captured = capsys.readouterr()
    assert "Ошибка: Ключ не найден" in captured.out

def test_update_after_loop(clear_table, capsys):
    for i in range(14, 20):
        insert(f"Та{i:02d}", f"Данные{i}")  # h=7, занимает слоты 7-12
    insert("Ангина", "Воспаление миндалин")  # h=14, вставится в 14
    update("Ангина", "Новое описание")
    assert table[14]['Pi'] == "Новое описание"  # Проверяем слот 14
    captured = capsys.readouterr()
    assert "Обновлено: 'Ангина'" in captured.out

# Тесты для функции delete
def test_delete_existing_key(clear_table, capsys):
    insert("Ангина", "Воспаление миндалин")
    delete("Ангина")
    assert table[14]['D'] == 1
    captured = capsys.readouterr()
    assert "Удалено: 'Ангина'" in captured.out

def test_delete_non_existing_key(clear_table, capsys):
    delete("Неизвестно")
    captured = capsys.readouterr()
    assert "Ошибка: Ключ не найден" in captured.out

def test_delete_after_loop(clear_table, capsys):
    for i in range(14, 20):
        insert(f"Та{i:02d}", f"Данные{i}")  # h=7, занимает слоты 7-12
    insert("Ангина", "Воспаление миндалин")  # h=14, вставится в 14
    delete("Ангина")
    assert table[14]['D'] == 1  # Проверяем слот 14
    captured = capsys.readouterr()
    assert "Удалено: 'Ангина'" in captured.out

# Тесты для функции display_unresolved_collisions
def test_display_unresolved_collisions(capsys):
    entries = [
        ("Ангина", "Воспаление миндалин"),
        ("Анемия", "Недостаток эритроцитов"),
        ("Бронхит", "Воспаление бронхов")
    ]
    display_unresolved_collisions(entries)
    captured = capsys.readouterr()
    assert "Ангина, Анемия" in captured.out
    assert "Бронхит" in captured.out
    assert "14" in captured.out
    assert "10" in captured.out

def test_display_unresolved_collisions_empty(capsys):
    display_unresolved_collisions([])
    captured = capsys.readouterr()
    assert "Хеш-таблица с нерешёнными коллизиями" in captured.out

# Тесты для функции display_resolved_collisions
def test_display_resolved_collisions(clear_table, capsys):
    insert("Ангина", "Воспаление миндалин")  # V=14, h=14
    insert("Анемия", "Недостаток эритроцитов")  # V=14, h=14, слот 15
    display_resolved_collisions()
    captured = capsys.readouterr()
    assert "Ангина" in captured.out
    assert "Анемия" in captured.out
    assert "14" in captured.out  # Проверяем слоты и значения V/h
    assert "15" in captured.out
    assert "Коэффициент заполнения: 0.10" in captured.out
    assert "V" in captured.out  # Проверяем наличие столбца V
    assert "h" in captured.out  # Проверяем наличие столбца h
    assert "14" in captured.out  # Проверяем значения V=14, h=14 для Ангина

def test_display_resolved_collisions_with_deleted(clear_table, capsys):
    insert("Ангина", "Воспаление миндалин")
    delete("Ангина")
    display_resolved_collisions()
    captured = capsys.readouterr()
    assert "Коэффициент заполнения: 0.00" in captured.out
    assert "V" in captured.out  # Проверяем наличие столбца V
    assert "h" in captured.out  # Проверяем наличие столбца h
    assert "14" in captured.out  # V=14, h=14 для удалённой записи

# Тест для начальной загрузки initial_entries
def test_initial_entries_load(clear_table, capsys):
    for key, data in initial_entries:
        insert(key, data)
    captured = capsys.readouterr()
    assert "Вставлено: 'Ангина'" in captured.out
    assert "Вставлено: 'Пневмония'" in captured.out
    assert table[14]['ID'] == "Ангина"
    assert table[2]['ID'] == "Пневмония"

# Тест для вставки после нескольких удалений
def test_insert_after_multiple_deletes(clear_table):
    insert("Ангина", "Воспаление миндалин")  # h=14
    insert("Анемия", "Недостаток эритроцитов")  # h=14, слот 15
    delete("Ангина")
    delete("Анемия")
    insert("Анорексия", "Расстройство пищевого поведения")  # h=14
    assert table[14]['ID'] == "Анорексия"
    assert table[14]['D'] == 0

# Тесты для интерактивного меню
def test_menu_insert(monkeypatch, capsys, clear_table):
    inputs = ["1", "Ангина", "Воспаление миндалин", "6"]
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(inputs)))
    run_menu()
    captured = capsys.readouterr()
    assert "Вставлено: 'Ангина'" in captured.out
    assert "Выход" in captured.out

def test_menu_search(monkeypatch, capsys, clear_table):
    insert("Ангина", "Воспаление миндалин")
    inputs = ["2", "Ангина", "6"]
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(inputs)))
    run_menu()
    captured = capsys.readouterr()
    assert "Результат: Воспаление миндалин" in captured.out

def test_menu_update(monkeypatch, capsys, clear_table):
    insert("Ангина", "Воспаление миндалин")
    inputs = ["3", "Ангина", "Новое описание", "6"]
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(inputs)))
    run_menu()
    captured = capsys.readouterr()
    assert "Обновлено: 'Ангина'" in captured.out

def test_menu_delete(monkeypatch, capsys, clear_table):
    insert("Ангина", "Воспаление миндалин")
    inputs = ["4", "Ангина", "6"]
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(inputs)))
    run_menu()
    captured = capsys.readouterr()
    assert "Удалено: 'Ангина'" in captured.out

def test_menu_display(monkeypatch, capsys, clear_table):
    insert("Ангина", "Воспаление миндалин")
    inputs = ["5", "6"]
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(inputs)))
    run_menu()
    captured = capsys.readouterr()
    assert "Хеш-таблица с разрешёнными коллизиями" in captured.out

def test_menu_invalid_choice(monkeypatch, capsys, clear_table):
    inputs = ["7", "6"]
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(inputs)))
    run_menu()
    captured = capsys.readouterr()
    assert "Неверный выбор" in captured.out
