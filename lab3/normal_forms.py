from typing import List, Dict, Set, Tuple
from itertools import combinations

class NormalFormGenerator:
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = sorted(list(set([var for row in truth_table for var in row.keys() if var != 'result'])))
        self.rows = len(truth_table)
        self.cols = len(self.variables)

    def _get_row_values(self, row_idx: int) -> list:
        row = self.truth_table[row_idx]
        return [row[var] for var in self.variables]

    def _get_row_result(self, row_idx: int) -> int:
        return self.truth_table[row_idx]['result']

    def _format_term(self, values: list, is_dnf: bool) -> str:
        terms = []
        for i, val in enumerate(values):
            if is_dnf:
                if val == 1:
                    terms.append(self.variables[i])
                else:
                    terms.append(f"!{self.variables[i]}")
            else:
                if val == 0:
                    terms.append(self.variables[i])
                else:
                    terms.append(f"!{self.variables[i]}")
        return "&".join(terms) if is_dnf else "|".join(terms)

    def generate_dnf(self) -> str:
        terms = []
        for i in range(self.rows):
            if self._get_row_result(i) == 1:
                terms.append(self._format_term(self._get_row_values(i), True))
        return "(" + ")|(".join(terms) + ")" if terms else ""

    def generate_cnf(self) -> str:
        terms = []
        for i in range(self.rows):
            if self._get_row_result(i) == 0:
                terms.append(self._format_term(self._get_row_values(i), False))
        return "(" + ")&(".join(terms) + ")" if terms else ""

    def generate_sdnf(self) -> str:
        terms = []
        for row in self.truth_table:
            if row['result'] == 1:
                term = []
                for var in self.variables:
                    if row[var] == 0:
                        term.append(f"!{var}")
                    else:
                        term.append(var)
                terms.append("&".join(term))
        return "|".join(f"({term})" for term in terms)

    def generate_sknf(self) -> str:
        terms = []
        for row in self.truth_table:
            if row['result'] == 0:
                term = []
                for var in self.variables:
                    if row[var] == 1:
                        term.append(f"!{var}")
                    else:
                        term.append(var)
                terms.append("|".join(term))
        return "&".join(f"({term})" for term in terms)

    def format_result(self, terms, is_dnf=True):
        if not terms:
            return ""
        
        # Фильтруем пустые термы и пропускаем переменные со значением -1
        formatted_terms = []
        for term in terms:
            if not term:
                continue
            var_terms = []
            for var, val in term.items():
                if val == -1:
                    continue
                if is_dnf:
                    var_terms.append(f"{'!' if not val else ''}{var}")
                else:
                    var_terms.append(f"{'!' if val else ''}{var}")
            if var_terms:
                if is_dnf:
                    formatted_terms.append("&".join(var_terms))
                else:
                    formatted_terms.append("|".join(var_terms))
        
        if not formatted_terms:
            return ""
        
        # Объединяем термы
        if is_dnf:
            return "|".join(f"({term})" for term in formatted_terms)
        else:
            return "&".join(f"({term})" for term in formatted_terms)

class Minimizer:
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = sorted(list(set([var for row in truth_table for var in row.keys() if var != 'result'])))
        self.merging_steps = []
        self.prime_implicants = []
        self.essential_prime_implicants = []
        self.coverage_matrix = []
        self.terms = []
        self.merged_terms = []
        self.final_terms = []

    def format_term(self, term, is_dnf=True):
        if isinstance(term, int):
            return str(term)
        if not term:
            return ""
        if is_dnf:
            return "&".join(f"{'!' if not v else ''}{var}" for var, v in term.items())
        else:
            return "|".join(f"{'!' if v else ''}{var}" for var, v in term.items())

    def calculate_implicants(self, is_dnf=True):
        self.terms = []
        self.merged_terms = []
        self.final_terms = []
        self.merging_steps = []
        
        # Начальные импликанты
        for row in self.truth_table:
            if (is_dnf and row['result'] == 1) or (not is_dnf and row['result'] == 0):
                term = {var: row[var] for var in self.variables}
                self.terms.append(term)
                self.merging_steps.append(f"Начальный импликант: {self.format_term(term, is_dnf)}")

        # Склеивание
        while self.terms:
            new_terms = []
            used = set()
            
            for i, term1 in enumerate(self.terms):
                for j, term2 in enumerate(self.terms[i+1:], i+1):
                    if j in used:
                        continue
                    
                    # Проверяем возможность склеивания
                    diff_count = 0
                    diff_var = None
                    for var in self.variables:
                        if term1[var] != term2[var]:
                            diff_count += 1
                            diff_var = var
                    
                    if diff_count == 1:
                        # Склеиваем термы
                        new_term = term1.copy()
                        new_term[diff_var] = -1  # Помечаем как "не важно"
                        new_terms.append(new_term)
                        used.add(i)
                        used.add(j)
                        self.merging_steps.append(
                            f"Склеивание: {self.format_term(term1, is_dnf)} + {self.format_term(term2, is_dnf)} = {self.format_term(new_term, is_dnf)}"
                        )
            
            # Добавляем неиспользованные термы
            for i, term in enumerate(self.terms):
                if i not in used:
                    self.merged_terms.append(term)
                    self.merging_steps.append(f"Простой импликант: {self.format_term(term, is_dnf)}")
            
            self.terms = new_terms
            if new_terms:
                self.merging_steps.append("---")
        
        # Формируем финальные термы
        self.final_terms = self.merged_terms + self.terms
        
        # Проверяем покрытие
        covered = set()
        for term in self.final_terms:
            for row in self.truth_table:
                if (is_dnf and row['result'] == 1) or (not is_dnf and row['result'] == 0):
                    covers = True
                    for var in self.variables:
                        if term[var] != -1 and term[var] != row[var]:
                            covers = False
                            break
                    if covers:
                        key = tuple(row[var] for var in self.variables)
                        covered.add(key)
        
        # Проверяем, все ли термы покрыты
        all_terms = set()
        for row in self.truth_table:
            if (is_dnf and row['result'] == 1) or (not is_dnf and row['result'] == 0):
                key = tuple(row[var] for var in self.variables)
                all_terms.add(key)
        
        if covered != all_terms:
            # Добавляем недостающие термы
            for row in self.truth_table:
                if (is_dnf and row['result'] == 1) or (not is_dnf and row['result'] == 0):
                    key = tuple(row[var] for var in self.variables)
                    if key not in covered:
                        term = {var: row[var] for var in self.variables}
                        self.final_terms.append(term)
                        covered.add(key)
        
        return self.final_terms

    def print_coverage_matrix(self, is_dnf=True):
        if not self.final_terms:
            return

        # Заголовок
        header = "            |"
        for row in self.truth_table:
            if (is_dnf and row['result'] == 1) or (not is_dnf and row['result'] == 0):
                term = {var: row[var] for var in self.variables}
                header += f" {self.format_term(term, is_dnf):<10} |"
        print(header)

        # Строки матрицы
        for term in self.final_terms:
            row_str = f" {self.format_term(term, is_dnf):<10} |"
            for row in self.truth_table:
                if (is_dnf and row['result'] == 1) or (not is_dnf and row['result'] == 0):
                    # Проверяем покрытие
                    covers = True
                    for var in self.variables:
                        if term[var] != -1 and term[var] != row[var]:
                            covers = False
                            break
                    row_str += f" {'x' if covers else ' ':^10} |"
            print(row_str)

    def calculation_method(self, cnf=False):
        is_dnf = not cnf
        min_terms = self.calculate_implicants(is_dnf)
        print("\nЭтапы склеивания:")
        for step in self.merging_steps:
            print(step)
        return self.format_result(min_terms, is_dnf)

    def calculation_tabular_method(self, cnf=False):
        is_dnf = not cnf
        min_terms = self.calculate_implicants(is_dnf)
        print("\nТаблица покрытия:")
        self.print_coverage_matrix(is_dnf)
        return self.format_result(min_terms, is_dnf)

    def table_method(self, cnf=False):
        is_dnf = not cnf
        min_terms = self.calculate_implicants(is_dnf)
        print("\nКарта Карно:")
        self.print_karnaugh_map(is_dnf)
        return self.format_result(min_terms, is_dnf)

    def print_karnaugh_map(self, is_dnf=True):
        # Создаем карту Карно
        k_map = {}
        for row in self.truth_table:
            key = tuple(row[var] for var in self.variables)
            k_map[key] = row['result']

        # Выводим карту только для ДНФ
        if is_dnf:
            print("+------+--------+--------+--------+--------+")
            print("|        | (0,0)  | (0,1)  | (1,1)  | (1,0)  |")
            print("+------+--------+--------+--------+--------+")
            
            for i in range(2):
                row = f"|  ({i},)  |"
                for j in range(2):
                    for k in range(2):
                        val = k_map.get((i, j, k), 0)
                        row += f"   {val}    |"
                print(row)
                print("+------+--------+--------+--------+--------+")

        # Выводим минимальные термы только для ДНФ
        if is_dnf:
            min_terms = self.calculate_implicants(is_dnf)
            print(f"Минимизированная ДНФ: {self.format_result(min_terms, True)}")

    def print_steps(self):
        for step in self.merging_steps:
            print(step)

    def format_result(self, terms, is_dnf=True):
        if not terms:
            return ""
        
        # Фильтруем пустые термы и пропускаем переменные со значением -1
        formatted_terms = []
        for term in terms:
            if not term:
                continue
            var_terms = []
            for var, val in term.items():
                if val == -1:
                    continue
                if is_dnf:
                    var_terms.append(f"{'!' if not val else ''}{var}")
                else:
                    var_terms.append(f"{'!' if val else ''}{var}")
            if var_terms:
                if is_dnf:
                    formatted_terms.append("&".join(var_terms))
                else:
                    formatted_terms.append("|".join(var_terms))
        
        if not formatted_terms:
            return ""
        
        # Объединяем термы
        if is_dnf:
            return "|".join(f"({term})" for term in formatted_terms)
        else:
            return "&".join(f"({term})" for term in formatted_terms) 