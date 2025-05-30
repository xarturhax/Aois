from typing import *
from priority import *
import re

def check_input(formula: str) -> bool:
    valid_characters = set("abcdefghijklmnopqrstuvwxyz|!&()>~")
    formula = formula.replace(" ", "")  # Remove spaces for validation
    if not formula:
        return False
    # Check for valid characters
    if not all(c in valid_characters for c in formula):
        return False
    # Check for at least one variable
    variables = set(re.findall(r"[a-z]", formula))
    return len(variables) >= 1

def create_sknf(table: Dict[int, list], variables: list) -> str:
    sknf = ''
    for i in range(len(table)):
        if table[i][LAST] == 0:
            sknf += '('
            for j in range(len(table[i]) - 1):
                if table[i][j] == 0:
                    sknf += f'{variables[j]}|'
                else:
                    sknf += f'!{variables[j]}|'
            sknf = sknf[:LAST]
            sknf += ')&'
    if sknf and sknf[LAST] == '&':
        sknf = sknf[:LAST]
    return sknf

def create_sdnf(table: dict[int, list], variables: list) -> str:
    sdnf = ''
    for i in range(len(table)):
        if table[i][LAST] == 1:
            sdnf += '('
            for j in range(len(table[i]) - 1):
                if table[i][j] == 0:
                    sdnf += f'!{variables[j]}&'
                else:
                    sdnf += f'{variables[j]}&'
            sdnf = sdnf[:LAST]
            sdnf += ')|'
    if sdnf and sdnf[LAST] == '|':
        sdnf = sdnf[:LAST]
    return sdnf

def gluing(SNF):
    nf = []
    if len(SNF) == 1:
        return SNF
    for i in range(len(SNF)):
        for j in range(i + 1, len(SNF)):
            summand1 = set(SNF[i])
            summand2 = set(SNF[j])
            implicant = list(summand1 & summand2)
            implicant.sort(key=lambda x: x[-1])
            if len(implicant) == len(SNF[i]) - 1:  # Ensure one variable difference
                nf.append(implicant)
    return nf

def print_dnf(dnf):
    dnf_output = ""
    for i in dnf:
        dnf_output += f"({'&'.join(i)})|"
    print(f"ДНФ: {dnf_output[:-1] if dnf_output else ''}")

def print_knf(knf):
    knf_output = ""
    for i in knf:
        knf_output += f"({'|'.join(i)})&"
    print(f"КНФ: {knf_output[:-1] if knf_output else ''}")

def print_mdnf(mdnf):
    mdnf_output = ""
    for i in mdnf:
        mdnf_output += f"({'&'.join(i)})|"
    print(f"Минимизированная ДНФ: {mdnf_output[:-1] if mdnf_output else ''}")

def print_mknf(mknf):
    mknf_output = ""
    for i in mknf:
        mknf_output += f"({'|'.join(i)})&"
    print(f"Минимизированная КНФ: {mknf_output[:-1] if mknf_output else ''}")