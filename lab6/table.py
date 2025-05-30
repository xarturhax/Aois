class SportHashTable:
    def __init__(self, size=20):
        self.size = size
        self.table = [{'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None} for _ in range(size)]
        self.alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                         'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

    def v_function(self, key):
        if len(key) < 2:
            raise ValueError("Ключ должен содержать не менее двух символов")
        char_one, char_two = key[0].upper(), key[1].upper()
        if char_one not in self.alphabet or char_two not in self.alphabet:
            raise ValueError("Ключ должен начинаться с двух русских букв")
        index_one = self.alphabet.index(char_one)
        index_two = self.alphabet.index(char_two)
        return index_one * 33 + index_two

    def hash_function(self, v_value):
        return v_value % self.size

    def next_slot(self, current):
        return (current + 1) % self.size

    def insert(self, key, data):
        v_value = self.v_function(key)
        hash_value = self.hash_function(v_value)
        original_hash = hash_value
        prev_slot = None

        while True:
            if self.table[hash_value]['U'] == 0 or self.table[hash_value]['D'] == 1:
                self.table[hash_value] = {
                    'ID': key,
                    'C': 1 if prev_slot is not None else 0,
                    'U': 1,
                    'T': 1,
                    'L': 0,
                    'D': 0,
                    'Po': prev_slot if prev_slot is not None else None,
                    'Pi': data
                }
                if prev_slot is not None:
                    self.table[prev_slot]['T'] = 0
                    self.table[prev_slot]['Po'] = hash_value
                return True
            elif self.table[hash_value]['ID'] == key and self.table[hash_value]['D'] == 0:
                return False
            else:
                prev_slot = hash_value
                hash_value = self.next_slot(hash_value)
                if hash_value == original_hash:
                    self.rehash()
                    return self.insert(key, data)

    def rehash(self):
        old_table = [entry for entry in self.table if entry['U'] == 1 and entry['D'] == 0]
        self.size *= 2
        self.table = [{'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None} for _ in range(self.size)]
        for entry in old_table:
            self.insert(entry['ID'], entry['Pi'])

    def search(self, key):
        v_value = self.v_function(key)
        hash_value = self.hash_function(v_value)
        original_hash = hash_value
        while self.table[hash_value]['U'] == 1:
            if self.table[hash_value]['ID'] == key and self.table[hash_value]['D'] == 0:
                return self.table[hash_value]['Pi']
            hash_value = self.next_slot(hash_value)
            if hash_value == original_hash:
                break
        return None

    def update(self, key, data):
        v_value = self.v_function(key)
        hash_value = self.hash_function(v_value)
        original_hash = hash_value
        while self.table[hash_value]['U'] == 1:
            if self.table[hash_value]['ID'] == key and self.table[hash_value]['D'] == 0:
                self.table[hash_value]['Pi'] = data
                return True
            hash_value = self.next_slot(hash_value)
            if hash_value == original_hash:
                break
        return False

    def delete(self, key):
        v_value = self.v_function(key)
        hash_value = self.hash_function(v_value)
        original_hash = hash_value
        prev_slot = None

        while self.table[hash_value]['U'] == 1:
            if self.table[hash_value]['ID'] == key and self.table[hash_value]['D'] == 0:
                next_slot = self.table[hash_value]['Po']

                # Случай 1: Одиночная строка (нет коллизий)
                if self.table[hash_value]['C'] == 0 and self.table[hash_value]['T'] == 1:
                    self.table[hash_value] = {'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None}
                    return True

                # Случай 2: Последняя в цепочке
                elif self.table[hash_value]['T'] == 1:
                    if prev_slot is not None:
                        self.table[prev_slot]['T'] = 1
                        self.table[prev_slot]['Po'] = None
                    self.table[hash_value] = {'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None}
                    return True

                # Случай 3: Первая в цепочке
                elif self.table[hash_value]['C'] == 0 and next_slot is not None:
                    self.table[hash_value] = self.table[next_slot]
                    self.table[next_slot] = {'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None}
                    self.table[hash_value]['C'] = 0
                    if prev_slot is not None:
                        self.table[prev_slot]['Po'] = hash_value
                    return True

                # Случай 4: Промежуточная в цепочке
                else:
                    if next_slot is not None:
                        # Проверяем, является ли следующая ячейка терминальной
                        if self.table[next_slot]['T'] == 1:
                            # Если следующая ячейка терминальная, очищаем обе ячейки
                            if prev_slot is not None:
                                self.table[prev_slot]['T'] = 1
                                self.table[prev_slot]['Po'] = None
                            self.table[hash_value] = {'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None}
                            self.table[next_slot] = {'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None}
                        else:
                            # Переносим следующую ячейку
                            self.table[hash_value] = self.table[next_slot]
                            self.table[next_slot] = {'ID': None, 'C': 0, 'U': 0, 'T': 0, 'L': 0, 'D': 0, 'Po': None, 'Pi': None}
                            self.table[hash_value]['C'] = 1 if prev_slot is not None else 0
                            if prev_slot is not None:
                                self.table[prev_slot]['Po'] = hash_value
                                self.table[prev_slot]['T'] = 0
                    return True

            prev_slot = hash_value
            hash_value = self.next_slot(hash_value)
            if hash_value == original_hash:
                break
        return False

    def get_fill_factor(self):
        occupied = sum(1 for entry in self.table if entry['U'] == 1 and entry['D'] == 0)
        return occupied / self.size

    def __getitem__(self, key):
        return self.search(key)

    def __setitem__(self, key, data):
        return self.insert(key, data)