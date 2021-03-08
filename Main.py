import subprocess
import sys
from collections import defaultdict
import re


def check_file(file_path):
    result = subprocess.run(['flake8',  file_path], stdout=subprocess.PIPE)
    result_string = result.stdout.decode('utf-8')
    parse_result(result_string, file_path)


def parse_result(result_string, file_path):
    result_list = list(result_string.split('\n'))
    result_list = list(map(lambda elem: elem[len(file_path) + 1:], result_list))
    result_list.pop()
    for i in range(len(result_list)):
        result_list[i] = str(i + 1) + ' ' + result_list[i] + '\n'
    group_errors(result_list)


def group_errors(result_list):
    result_groups = defaultdict(list)
    for i in range(len(result_list)):
        start = result_list[i].find(':')
        error_code_start = result_list[i].find(':', start + 1) + 2
        error_code_end = result_list[i].find(' ', error_code_start + 2)
        error_code = result_list[i][error_code_start:error_code_end + 1]
        error_group = get_error_group(error_code)
        result_groups[error_group].append(result_list[i])
    for key, value in result_groups.items():
        print(str(key) + ':')
        for index, elem in enumerate(value):
            print(str(index + 1) + ') ' + elem, end='')
        print()


def get_error_group(error_code):
    error_codes = [[['B', [1, 8]], 'flake8-bugbear'], [['C', [400, 411]], 'flake8-comprehensions'],
                   [['C', [812, 819]], 'flake8-commas'], [['C', [901, 901]], 'mccabe'],
                   [['D', [100, 417]], 'flake8-docstrings'], [['E', [1, 902]], 'py-codestyle'],
                   [['W', [1, 606]], 'py-codestyle'], [['E', [800, 800]], 'flake8-eradicate'],
                   [['F', [400, 901]], 'flake8'], [['I', [1, 5]], 'flake8-isort'],
                   [['N', [400, 400]], 'flake8-broken-line'], [['P', [101, 302]], 'flake8-string-format'],
                   [['N', [800, 820]], 'pep8-naming'], [['Q', [0, 0]], 'flake8-quotes'],
                   [['S', [100, 710]], 'flake8-bandit'], [['T', [100, 100]], 'flake8-debugger'],
                   [["RST", [201, 499]], 'flake8-rst-docstrings'], [["DAR", [1, 501]], 'darglint'],
                   [['WPS', [0, 99]], 'wemake-python-styleguide System'],
                   [['WPS', [100, 199]], 'wemake-python-styleguide Naming'],
                   [['WPS', [200, 299]], 'wemake-python-styleguide Complexity'],
                   [['WPS', [300, 399]], 'wemake-python-styleguide Consistency'],
                   [['WPS', [400, 499]], 'wemake-python-styleguide Best practices'],
                   [['WPS', [500, 599]], 'wemake-python-styleguide Refactoring'],
                   [['WPS', [600, 699]], 'wemake-python-styleguide OOP']]
    error_code_number = int(error_code[re.search(r"\d", error_code).start():])
    error_code_name = error_code[:re.search(r"\d", error_code).start()]
    for key, value in error_codes:
        if error_code_name == key[0] and key[1][0] <= error_code_number <= key[1][1]:
            return value


if __name__ == '__main__':
    check_file(sys.argv[1])
