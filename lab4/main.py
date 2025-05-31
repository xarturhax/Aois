from summator import *
from converter import *


def main():
    input_variables = ['A', 'B', 'Cin']

    table, field_names = truth_table(input_variables)
    print(table)
    sdnf_sum = create_sdnf(table, input_variables, key='sum')
    sdnf_c_out = create_sdnf(table, input_variables, key='cout')
    print(f'Совершенная дизъюнктивная нормальная форма (СДНФ) для суммы:\n'
          f'{format_str(sdnf_sum)}')
    merged_sdnf = merging(sdnf_sum)
    merged_sdnf_str = format_str(merged_sdnf)
    print(f'Минимизация СДНФ для суммы:\n'
          f'{merged_sdnf_str}\n\n')

    print(f'Совершенная дизъюнктивная нормальная форма (СДНФ) для переноса:\n'
          f'{format_str(sdnf_c_out)}')
    merged_sdnf = merging(sdnf_c_out)
    merged_sdnf_str = format_str(merged_sdnf)
    print(f'Минимизация СДНФ для переноса:\n'
          f'{merged_sdnf_str}\n\n')

    field_names = ["x1", "x2", "x3", "x4"]
    table = d8421_table()
    print(table)
    sdnf_expressions = create_sdnf_expressions(table, field_names)
    for i, expr in enumerate(sdnf_expressions):
        print(f"СДНФ для бита {i}: {format_str(expr)}")
        merged_bits = format_str(merging(expr))
        print(f'Минимизация: {merged_bits}\n')


if __name__ == '__main__':
    main()