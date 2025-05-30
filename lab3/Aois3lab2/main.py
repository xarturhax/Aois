from tablica import *
from raschet_tablich import *
from karno import *
from snf import *

def main():
    formula = input("Введите формулу: ")

    if not check_input(formula):
        raise Exception('Некорректный ввод!')

    table, variables = true_table(formula)
    print("_" * 60)

    SDNF = create_sdnf(table, variables)
    SDNF = SDNF.replace('-', '!')
    print("СДНФ: " + SDNF)
    SKNF = create_sknf(table, variables)
    SKNF = SKNF.replace('-', '!')
    print("СКНФ: " + SKNF)
    SDNF = [i.split("&") for i in SDNF[1:-1].split(")|(")] if SDNF else []
    SKNF = [i.split("|") for i in SKNF[1:-1].split(")&(")] if SKNF else []

    dnf = gluing(SDNF)
    knf = gluing(SKNF)

    print("\nРасчетно-табличный метод:")
    mdnf_tabular = calculation_tabular_method(dnf, SDNF, "sdnf")
    print_mdnf(mdnf_tabular)
    mknf_tabular = calculation_tabular_method(knf, SKNF, "sknf")
    print_mknf(mknf_tabular)

    print("\nРасчетный метод:")
    print("Результат склеивания:")
    print_dnf(dnf)
    print_knf(knf)
    mdnf = calculation_method(SDNF, is_dnf=True)
    mknf = calculation_method(SKNF, is_dnf=False)
    print_mdnf(mdnf)
    print_mknf(mknf)

    print("\nТабличный метод:")
    table_res = []
    for i in table.values():
        LAST = len(i) - 1
        table_res.append(int(i[LAST]))

    table_method(table_res, mdnf, mknf, len(variables))

if __name__ == '__main__':
    main()