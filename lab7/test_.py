import pytest
from main import AssociativeProcessor
import io
import sys
import argparse
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

@pytest.fixture
def test_processor():
    ap = AssociativeProcessor()
    ap.matrix = [[0] * 16 for _ in range(16)]
    test_words = {
        0: 0b0000000100100000,
        1: 0b0010001101000000,
        2: 0b0100010101100000,
        5: 0b1010001100100000,
        10: 0b1111111111111111
    }
    for k, val in test_words.items():
        ap.write_word(k, val)
    return ap

def test_initialization():
    ap = AssociativeProcessor()
    assert len(ap.matrix) == 16
    assert all(len(row) == 16 for row in ap.matrix)

def test_read_write_word(test_processor):
    assert test_processor.read_word(0) == 288
    test_processor.write_word(0, 0xFFFF)
    assert test_processor.read_word(0) == 0xFFFF

def test_bit_column_operations(test_processor):
    col0 = test_processor.read_bit_column(0)
    assert len(col0) == 16
    assert col0[0] == 0

def test_search_operations():
    ap = AssociativeProcessor()
    ap.matrix = [[0] * 16 for _ in range(16)]
    test_words = {0: 288, 1: 9024, 2: 17760, 5: 41888, 10: 65535}
    for k, val in test_words.items():
        ap.write_word(k, val)
    results = ap.search_in_interval(9000, 10000)
    assert len(results) == 1
    assert results[0] == (1, 9024)

def test_arithmetic_operations():
    ap = AssociativeProcessor()
    ap.matrix = [[0] * 16 for _ in range(16)]
    test_word = (5 << 13) | (3 << 9) | (2 << 5) | 0
    ap.write_word(5, test_word)
    ap.arithmetic_operation("101")
    new_word = ap.read_word(5)
    assert (new_word & 0b11111) == 5

def test_edge_cases():
    ap = AssociativeProcessor()
    ap.matrix = [[0] * 16 for _ in range(16)]
    test_word = (0 << 13) | (15 << 9) | (15 << 5) | 0
    ap.write_word(0, test_word)
    ap.arithmetic_operation("000")
    assert (ap.read_word(0) & 0b11111) == 30

def test_display_functions(test_processor):
    with redirect_stdout(io.StringIO()) as f:
        test_processor.display_matrix()
    assert len(f.getvalue().splitlines()) == 16

def test_invalid_input():
    ap = AssociativeProcessor()
    with redirect_stderr(io.StringIO()) as f:
        ap.arithmetic_operation("01")
    assert "Ошибка" in f.getvalue()

def test_main_program_output():
    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(test=False)):
        with patch('builtins.input', side_effect=["10", "20", "101"]):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                from main import main
                main()

            output = stdout.getvalue()
            # Проверяем ключевые фразы в выводе
            assert "Инициализация ассоциативного процессора" in output
            assert "Матрица 16x16:" in output
            assert "Значения всех слов:" in output

def test_search_input_validation():
    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(test=False)):
        with patch('builtins.input', side_effect=["100", "50", "10", "20", "101"]):
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                from main import main
                main()

            output = stdout.getvalue()
            assert "Ошибка" in output
            assert "Слова в интервале" in output

def test_logical_operations_edge_cases():
    ap = AssociativeProcessor()
    ap.matrix = [[0] * 16 for _ in range(16)]
    empty = [0] * 16
    full = [1] * 16
    assert ap.f2(empty, empty) == empty
    assert ap.f7(full, full) == full

def test_arithmetic_edge_cases():
    ap = AssociativeProcessor()
    ap.matrix = [[0] * 16 for _ in range(16)]
    test_word = (0 << 13) | (15 << 9) | (15 << 5) | 0
    ap.write_word(0, test_word)
    ap.arithmetic_operation("000")
    assert (ap.read_word(0) & 0b11111) == 30