import pytest
from table import SportHashTable
import os
import tempfile
from main import load_sports_terms, print_table


@pytest.fixture
def empty_table():
    return SportHashTable()


@pytest.fixture
def filled_table():
    table = SportHashTable()
    test_data = [
        ("Футбол", "Описание футбола"),
        ("Баскетбол", "Описание баскетбола"),
        ("Теннис", "Описание тенниса"),
        ("Плавание", "Описание плавания"),
        ("Волейбол", "Описание волейбола"),
    ]
    for key, value in test_data:
        table.insert(key, value)
    return table


def test_v_function_valid(empty_table):
    """Тест функции v_function с корректными ключами"""
    alphabet = empty_table.alphabet
    index_f = alphabet.index('Ф')
    index_u = alphabet.index('У')
    assert empty_table.v_function("Футбол") == index_f * 33 + index_u
    assert empty_table.v_function("Баскетбол") == alphabet.index('Б') * 33 + alphabet.index('А')


def test_v_function_invalid(empty_table):
    """Тест функции v_function с некорректными ключами"""
    with pytest.raises(ValueError):
        empty_table.v_function("Ф")
    with pytest.raises(ValueError):
        empty_table.v_function("Football")


def test_hash_function(empty_table):
    """Тест функции hash_function"""
    assert empty_table.hash_function(100) == 0
    assert empty_table.hash_function(123) == 3


def test_insert(empty_table):
    """Тест вставки элементов"""
    assert empty_table.insert("Футбол", "Описание") is True
    assert empty_table.insert("Футбол", "Другое описание") is False
    assert empty_table.search("Футбол") == "Описание"


def test_insert_with_collision(filled_table):
    """Тест вставки с коллизиями"""
    original_size = filled_table.size
    for i in range(original_size * 2):
        key = f"Спорт{i}"
        filled_table.insert(key, f"Описание {i}")
    assert filled_table.size > original_size
    assert filled_table.search("Футбол") is not None


def test_search(filled_table):
    """Тест поиска элементов"""
    assert filled_table.search("Футбол") == "Описание футбола"
    assert filled_table.search("Несуществующий") is None


def test_update(filled_table):
    """Тест обновления элементов"""
    assert filled_table.update("Футбол", "Новое описание") is True
    assert filled_table.search("Футбол") == "Новое описание"
    assert filled_table.update("Несуществующий", "Описание") is False


def test_delete(filled_table):
    """Тест удаления элементов"""
    assert filled_table.delete("Футбол") is True
    assert filled_table.search("Футбол") is None
    assert filled_table.delete("Несуществующий") is False
    assert filled_table.search("Баскетбол") is not None


def test_delete_with_collision():
    """Тест удаления с коллизиями"""
    table = SportHashTable()
    table.insert("Футбол", "Описание 1")
    table.insert("Фтбол", "Описание 2")  # Должен создать коллизию

    assert table.delete("Футбол") is True
    assert table.search("Футбол") is None
    assert table.search("Фтбол") == "Описание 2"


def test_get_fill_factor(empty_table, filled_table):
    """Тест коэффициента заполнения"""
    assert empty_table.get_fill_factor() == 0.0
    assert filled_table.get_fill_factor() == 0.25
    filled_table.insert("Гимнастика", "Описание")
    assert filled_table.get_fill_factor() == 0.30


def test_rehash(filled_table):
    """Тест рехеширования"""
    original_size = filled_table.size
    for i in range(original_size * 2):
        key = f"Спорт{i}"
        filled_table.insert(key, f"Описание {i}")
    assert filled_table.size > original_size
    assert filled_table.get_fill_factor() < 0.75


def test_magic_methods(empty_table):
    """Тест магических методов"""
    empty_table["Футбол"] = "Описание"
    assert empty_table["Футбол"] == "Описание"
    assert empty_table["Несуществующий"] is None



