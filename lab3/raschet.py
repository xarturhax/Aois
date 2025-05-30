from copy import deepcopy

def calculation_method(function, is_dnf=False):
    implicants = deepcopy(function)
    changed = True
    while changed:
        changed = False
        new_implicants = []
        used = set()
        for i in range(len(implicants)):
            for j in range(i + 1, len(implicants)):
                diff = set(implicants[i]).symmetric_difference(set(implicants[j]))
                if len(diff) == 2:
                    # Проверяем, что различающиеся переменные — это одна и та же с разными знаками
                    var1, var2 = diff
                    if var1 == '!' + var2 or var2 == '!' + var1:
                        new_implicant = list(set(implicants[i]) & set(implicants[j]))
                        new_implicant.sort(key=lambda x: x[-1])
                        if new_implicant not in new_implicants:
                            new_implicants.append(new_implicant)
                            used.add(i)
                            used.add(j)
                            changed = True
        # Добавляем несклеенные импликанты
        for i in range(len(implicants)):
            if i not in used and implicants[i] not in new_implicants:
                new_implicants.append(implicants[i])
        implicants = new_implicants
    return implicants

def set_variables(implicant, is_dnf):
    variables = {}
    for variable in implicant:
        if variable.startswith('!'):
            variables[variable[1:]] = not is_dnf
        else:
            variables[variable] = is_dnf
    return variables

def substitute_variables(implicants, variables):
    result = []
    for implicant in implicants:
        new_implicant = []
        for variable in implicant:
            if variable in variables:
                new_implicant.append(variables[variable])
            elif variable.startswith('!') and variable[1:] in variables:
                new_implicant.append(not variables[variable[1:]])
            else:
                new_implicant.append(variable)
        result.append(new_implicant)
    return result