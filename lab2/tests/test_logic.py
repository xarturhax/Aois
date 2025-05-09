import sys
import os
import pytest
from unittest.mock import patch, MagicMock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from formula_utils import *
from logic_table import *
from main import display_results, run

@pytest.fixture
def formulas():
    return {
        "formula1": "(a&b)~(!c)",
        "formula2": "d|(c&(!a))",
        "formula3": "(e~d)&(b->a)"
    }

def test_reversed_polish_notation(formulas):
    result1 = to_postfix(formulas["formula1"])
    result2 = to_postfix(formulas["formula2"])
    result3 = to_postfix(formulas["formula3"])
    assert result1 == "ab&c!~"
    assert result2 == "dca!&|"
    assert result3 == "ed~ba>&"

def test_true_table(formulas):
    table1, variables1 = generate_truth_table(formulas["formula1"], False)
    table2, variables2 = generate_truth_table(formulas["formula2"], False)

    result1 = [0, 1, 0, 1, 0, 1, 1, 0]
    result2 = [0, 1, 1, 1, 0, 1, 0, 1]

    for i in range(len(result1)):
        assert result1[0] == table1[0][len(variables1)]

    for j in range(len(result2)):
        assert result2[0] == table2[0][len(variables2)]

def test_sdnf(formulas):
    table1, variables1 = generate_truth_table(formulas["formula1"], False)
    table2, variables2 = generate_truth_table(formulas["formula2"], False)

    result1 = build_dnf(table1, variables1)
    result2 = build_dnf(table2, variables2)
    assert result1 == "((!a)&(!b)&(c))|((!a)&(b)&(c))|((a)&(!b)&(c))|((a)&(b)&(!c))"
    assert result2 == "((!a)&(!c)&(d))|((!a)&(c)&(!d))|((!a)&(c)&(d))|((a)&(!c)&(d))|((a)&(c)&(d))"

def test_sknf(formulas):
    table1, variables1 = generate_truth_table(formulas["formula1"], False)
    table2, variables2 = generate_truth_table(formulas["formula2"], False)

    result1 = build_cnf(table1, variables1)
    result2 = build_cnf(table2, variables2)
    assert result1 == "((a)|(b)|(c))&((a)|(!b)|(c))&((!a)|(b)|(c))&((!a)|(!b)|(!c))"
    assert result2 == "((a)|(c)|(d))&((!a)|(c)|(d))&((!a)|(!c)|(d))"

def test_num_sknf(formulas):
    table1, variables1 = generate_truth_table(formulas["formula1"], False)
    table2, variables2 = generate_truth_table(formulas["formula2"], False)

    result_bin_sknf1 = binary_cnf(table1, variables1)
    result_dec_sknf1 = decimal_cnf(table1, variables1)
    assert result_bin_sknf1 == "&(000,010,100,111)"
    assert result_dec_sknf1 == "&(0,2,4,7)"

    result_bin_sknf2 = binary_cnf(table2, variables2)
    result_dec_sknf2 = decimal_cnf(table2, variables2)
    assert result_bin_sknf2 == "&(000,100,110)"
    assert result_dec_sknf2 == "&(0,4,6)"

def test_num_sdnf(formulas):
    table1, variables1 = generate_truth_table(formulas["formula1"], False)
    table2, variables2 = generate_truth_table(formulas["formula2"], False)

    result_bin_sdnf1 = binary_dnf(table1, variables1)
    result_dec_sdnf1 = decimal_dnf(table1, variables1)
    assert result_bin_sdnf1 == "|(001,011,101,110)"
    assert result_dec_sdnf1 == "|(1,3,5,6)"

    result_bin_sdnf2 = binary_dnf(table2, variables2)
    result_dec_sdnf2 = decimal_dnf(table2, variables2)
    assert result_bin_sdnf2 == "|(001,010,011,101,111)"
    assert result_dec_sdnf2 == "|(1,2,3,5,7)"

def test_index_form(formulas):
    table1, variables1 = generate_truth_table(formulas["formula1"], False)
    table2, variables2 = generate_truth_table(formulas["formula2"], False)

    result_bin1 = binary_index(table1)
    result_bin2 = binary_index(table2)
    assert result_bin1 == "01010110"
    assert result_bin2 == "01110101"

    result_dec1 = to_decimal(binary_index(table1))
    result_dec2 = to_decimal(binary_index(table2))
    assert result_dec1 == "86"
    assert result_dec2 == "117"

@patch('builtins.print')
@patch('main.generate_truth_table')
@patch('main.validate_formula')
def test_display_results(mock_validate_formula, mock_generate_truth_table, mock_print, formulas):
    # Setup mock data
    formula = formulas["formula1"]
    truth_data = {i: [0, 0, 0, 0] for i in range(8)}  # Simplified truth table
    var_list = ['a', 'b', 'c']
    mock_validate_formula.return_value = True
    mock_generate_truth_table.return_value = (truth_data, var_list)

    # Mock other functions from formula_utils
    with patch('main.build_cnf', return_value="((a)|(b)|(c))&...") as mock_build_cnf, \
         patch('main.build_dnf', return_value="((!a)&(!b)&(c))|...") as mock_build_dnf, \
         patch('main.binary_cnf', return_value="&(000,010,100,111)") as mock_binary_cnf, \
         patch('main.decimal_cnf', return_value="&(0,2,4,7)") as mock_decimal_cnf, \
         patch('main.binary_dnf', return_value="|(001,011,101,110)") as mock_binary_dnf, \
         patch('main.decimal_dnf', return_value="|(1,3,5,6)") as mock_decimal_dnf, \
         patch('main.binary_index', return_value="01010110") as mock_binary_index, \
         patch('main.to_decimal', return_value="86") as mock_to_decimal:

        # Test valid formula
        display_results(formula)

        # Check that print was called with expected outputs
        expected_calls = [
            "==================================================\nCNF (SKNF): ((a)|(b)|(c))&...",
            "==================================================\nDNF (SDNF): ((!a)&(!b)&(c))|...",
            "==================================================\nCNF Binary: &(000,010,100,111)",
            "==================================================\nCNF Decimal: &(0,2,4,7)",
            "==================================================\nDNF Binary: |(001,011,101,110)",
            "==================================================\nDNF Decimal: |(1,3,5,6)",
            "==================================================\nIndex Binary: 01010110",
            "==================================================\nIndex Decimal: 86"
        ]
        for call, expected in zip(mock_print.call_args_list, expected_calls):
            assert call.args[0] == expected

    # Test invalid formula
    mock_validate_formula.return_value = False
    with pytest.raises(ValueError, match="Invalid formula entered!"):
        display_results(formula)

    # Test empty CNF/DNF results
    mock_validate_formula.return_value = True
    with patch('main.build_cnf', return_value="") as mock_build_cnf, \
         patch('main.build_dnf', return_value="") as mock_build_dnf, \
         patch('main.binary_cnf', return_value="&(000)") as mock_binary_cnf, \
         patch('main.decimal_cnf', return_value="&(0)") as mock_decimal_cnf, \
         patch('main.binary_dnf', return_value="|(001)") as mock_binary_dnf, \
         patch('main.decimal_dnf', return_value="|(1)") as mock_decimal_dnf, \
         patch('main.binary_index', return_value="00000000") as mock_binary_index, \
         patch('main.to_decimal', return_value="0") as mock_to_decimal:

        display_results(formula)
        expected_empty_calls = [
            "==================================================\nCNF (SKNF): ",
            "==================================================\nDNF (SDNF): ",
            "==================================================\nCNF Binary: &(000)",
            "==================================================\nCNF Decimal: &(0)",
            "==================================================\nDNF Binary: |(001)",
            "==================================================\nDNF Decimal: |(1)",
            "==================================================\nIndex Binary: 00000000",
            "==================================================\nIndex Decimal: 0"
        ]
        for call, expected in zip(mock_print.call_args_list[-8:], expected_empty_calls):
            assert call.args[0] == expected

@patch('builtins.input', return_value='(a&b)~(!c)')
@patch('main.display_results')
def test_run(mock_display_results, mock_input):
    # Test run with valid input
    run()
    mock_display_results.assert_called_once_with('(a&b)~(!c)')

    # Test run with another input
    mock_input.return_value = 'd|(c&(!a))'
    run()
    mock_display_results.assert_called_with('d|(c&(!a))')