import random
import sys
import argparse


class AssociativeProcessor:
    def __init__(self, test_mode=False):
        if test_mode:
            # Детерминированная матрица для тестов
            self.matrix = [[0] * 16 for _ in range(16)]
            # Заполняем тестовые данные
            for k in range(16):
                if k % 2 == 0:
                    self.write_word(k, 0b1010101010101010)  # Четные слова (0xAAAA)
                else:
                    self.write_word(k, 0b0101010101010101)  # Нечетные слова (0x5555)
        else:
            # Случайная матрица для нормального режима
            self.matrix = [
                [random.randint(0, 1) for _ in range(16)]
                for _ in range(16)
            ]

    def read_word(self, k):
        """Чтение слова S_k (диагональная адресация)"""
        word = 0
        for m in range(16):
            i = (m + k) % 16
            bit = self.matrix[i][k]
            word |= (bit << (15 - m))
        return word

    def write_word(self, k, value):
        """Запись слова S_k (диагональная адресация)"""
        for m in range(16):
            i = (m + k) % 16
            bit = (value >> (15 - m)) & 1
            self.matrix[i][k] = bit

    def read_bit_column(self, m):
        """Чтение столбца m (диагональная адресация)"""
        return [self.matrix[(m + k) % 16][k] for k in range(16)]

    # Логические функции
    def f2(self, col1, col2):
        """Запрет 1-го аргумента (x1 AND NOT x2)"""
        return [1 if x1 == 1 and x2 == 0 else 0 for x1, x2 in zip(col1, col2)]

    def f7(self, col1, col2):
        """Дизъюнкция (x1 OR x2)"""
        return [1 if x1 == 1 or x2 == 1 else 0 for x1, x2 in zip(col1, col2)]

    def f8(self, col1, col2):
        """Операция Пирса (NOT (x1 OR x2))"""
        return [1 if not (x1 == 1 or x2 == 1) else 0 for x1, x2 in zip(col1, col2)]

    def f13(self, col1, col2):
        """Импликация (NOT x1 OR x2)"""
        return [1 if x1 == 0 or x2 == 1 else 0 for x1, x2 in zip(col1, col2)]

    def search_in_interval(self, A, B):
        """Поиск слов в интервале [A, B]"""
        results = []
        for k in range(16):
            word_val = self.read_word(k)
            if A <= word_val <= B:
                results.append((k, word_val))
        return results

    def arithmetic_operation(self, V_binary):
        """Сложение полей A и B для слов с заданным V"""
        error_msg = "Ошибка: V должно быть 3-битным двоичным числом (000-111)!"
        try:
            if len(V_binary) != 3 or not all(c in '01' for c in V_binary):
                raise ValueError(error_msg)
            V = int(V_binary, 2)
            if V < 0 or V > 7:
                raise ValueError(error_msg)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return

        changed = False
        print(f"\nВыполняем арифметическую операцию для V={V_binary} ({V}):")

        for k in range(16):
            word = self.read_word(k)
            Vj = (word >> 13) & 0x7  # Биты 15-13 (поле V)
            if Vj == V:
                Aj = (word >> 9) & 0xF  # Биты 12-9 (поле A)
                Bj = (word >> 5) & 0xF  # Биты 8-5 (поле B)
                sum_val = Aj + Bj
                new_word = (word & 0xFFE0) | (sum_val & 0x1F)  # Обновляем только S (биты 4-0)
                self.write_word(k, new_word)

                print(f"* Слово {k:2d}:")
                print(
                    f"  V={Vj} ({bin(Vj)[2:].zfill(3)}), A={Aj}, B={Bj}, S={sum_val & 0x1F} (A+B={Aj}+{Bj}={sum_val})")
                print(f"  Было: {bin(word)[2:].zfill(16)} ({word})")
                print(f"  Стало: {bin(new_word)[2:].zfill(16)} ({new_word})")
                changed = True

        if not changed:
            print(f"Не найдено слов с V={V_binary} ({V})")

    def display_matrix(self):
        """Вывод матрицы на экран"""
        for row in self.matrix:
            print(' '.join(map(str, row)))

    def display_word(self, k):
        """Вывод слова в бинарном и десятичном формате"""
        word = self.read_word(k)
        print(f"Слово {k:2d}: {bin(word)[2:].zfill(16)} ({word})")

    def display_word_fields(self, k):
        """Вывод слова с разбиением на поля и полным десятичным значением"""
        word = self.read_word(k)
        V = (word >> 13) & 0x7  # Битты 15-13
        A = (word >> 9) & 0xF  # Битты 12-9
        B = (word >> 5) & 0xF  # Битты 8-5
        S = word & 0x1F  # Битты 4-0

        # Полное слово в десятичном формате (уже содержится в word)
        decimal_value = word

        print(f"Слово {k:2d}: V={V} ({bin(V)[2:].zfill(3)}) | "
              f"A={A} ({bin(A)[2:].zfill(4)}) | "
              f"B={B} ({bin(B)[2:].zfill(4)}) | "
              f"S={S} ({bin(S)[2:].zfill(5)}) | "
              f"Dec: {decimal_value}")


def main():
    parser = argparse.ArgumentParser(description='Ассоциативный процессор')
    parser.add_argument('--test', action='store_true', help='Тестовый режим с детерминированными данными')
    args = parser.parse_args()

    print("\nИнициализация ассоциативного процессора...")
    ap = AssociativeProcessor(test_mode=args.test)

    print("\nМатрица 16x16:")
    ap.display_matrix()

    print("\nЗначения всех слов:")
    for k in range(16):
        ap.display_word_fields(k)

    print("\nЛогические операции над столбцами 0 и 1:")
    col0 = ap.read_bit_column(0)
    col1 = ap.read_bit_column(1)
    print(f"F2 (x1 AND NOT x2): {ap.f2(col0, col1)}")
    print(f"F7 (x1 OR x2):      {ap.f7(col0, col1)}")
    print(f"F8 (NOT (x1 OR x2)): {ap.f8(col0, col1)}")
    print(f"F13 (NOT x1 OR x2): {ap.f13(col0, col1)}")

    print("\nПоиск слов в интервале:")
    while True:
        try:
            A = int(input("  Нижняя граница (A, 0-65535): "))
            B = int(input("  Верхняя граница (B, 0-65535): "))
            if 0 <= A <= B <= 65535:
                break
            print("Ошибка: A и B должны быть в диапазоне 0-65535, и A ≤ B!")
        except ValueError:
            print("Ошибка: введите целые числа!")

    results = ap.search_in_interval(A, B)
    print(f"\nСлова в интервале [{A}, {B}]:")
    if not results:
        print("Не найдено.")
    else:
        for k, val in results:
            ap.display_word_fields(k)

    print("\nАрифметическая операция (сложение A+B для слов с заданным V):")
    while True:
        V_binary = input("Введите значение V (3 бита, двоичное 000-111): ").strip()
        if len(V_binary) == 3 and all(c in '01' for c in V_binary):
            break
        print("Ошибка: введите ровно 3 бита (0 или 1), например, 010!")

    ap.arithmetic_operation(V_binary)

    print("\nФинальное состояние всех слов:")
    for k in range(16):
        ap.display_word_fields(k)


if __name__ == "__main__":
    main()