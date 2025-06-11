
import ast
import os

source_codes = {}
trees = {}
count_warn_per_file = {}

def open_directory(path):
    files = os.listdir(path)
    for fname in files:
        new_path = os.path.join(path, fname)
        if os.path.isfile(new_path) and fname.endswith('.py'):
            open_file(path,fname)
        elif os.path.isdir(new_path) and not fname.startswith('.'):
            open_directory(new_path)

def open_file(path, file_name):
    with open(f"{path}/{file_name}", 'r', encoding='utf-8') as openfile:
        source_codes[file_name] = openfile.read()
        trees[file_name] = ast.parse(source_codes[file_name])


# def get_functions_lengths():
#     lengths = {}
#     for file_name,tree in trees.items():
#         for node in ast.walk(tree):
#             if isinstance(node, ast.FunctionDef):
#                 # אורך הפונקציה הוא מספר השורות בגוף הפונקציה
#                 length = len(node.body)
#                 lengths[f'{file_name}: {node.name}'] = length
#
#     return lengths

def get_functions_lengths():
    lengths = {}
    for file_name, source_code in source_codes.items():
        tree = trees[file_name]
        lines = source_code.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start = node.lineno
                end = node.end_lineno
                func_lines = lines[start:end]

                #אם יש תיעוד, סופר את השורות שלו
                docstring_line_count = 0
                if (node.body and
                    isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                    docstring_line_count = (
                        node.body[0].end_lineno - node.body[0].lineno + 1
                    )
                code_lines = func_lines[docstring_line_count:]  # מדלגים על docstring
                #סינון שורות ריקות והערות
                real_code_lines = [
                    line for line in code_lines
                    if line.strip() and not line.strip().startswith("#") and not line.strip().startswith('"""') and not line.strip().startswith("'''")
                ]
                lengths[f'{file_name}: {node.name}'] = len(real_code_lines)
    return lengths


def check_over_20_lines():
    lengths = get_functions_lengths()
    arr_warnings = []
    for function_name, length in lengths.items():
        if length > 20:
            arr_warnings.append(f"Warning: The length of function '{function_name}' is {length}!! greater than 20!\n")
            file_name = function_name.split(':')[0]
            count_warn_per_file[file_name] = count_warn_per_file[file_name] + 1 if file_name in count_warn_per_file.keys() else 1

    arr_warnings.sort()
    return arr_warnings

def check_file_over_200_lines():
    arr_warnings = []
    for name,source_code in source_codes.items():
        line_count = source_code.count('\n') + 1
        if line_count > 200:
            count_warn_per_file[name] = count_warn_per_file[name] + 1 if  name in count_warn_per_file.keys() else 1
            arr_warnings.append(f"Warning: The length of file {name} is {line_count} - greater than 200!\n")
    arr_warnings.sort()
    return arr_warnings

def find_unused_variables():

    assigned_variables = set()
    used_variables = set()
    for file_name,tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_variables.add(f'{file_name}: {target.id}')
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_variables.add(f'{file_name}: {node.id}')

    # משתנים שהוקצו אך לא בשימוש
    unused_variables = assigned_variables - used_variables

    # התרעה עבור כל משתנה לא בשימוש
    arr_warnings = []
    for var in unused_variables:
        arr_warnings.append(f"Warning: Variable '{var}' is assigned but not used.\n")
        file_name = var.split(':')[0]
        count_warn_per_file[file_name] = count_warn_per_file[file_name] + 1 if file_name in count_warn_per_file.keys() else 1
    arr_warnings.sort()
    return arr_warnings


def find_functions_without_docstrings():
    warnings_functions_without_docstrings = []
    for file_name, tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if ast.get_docstring(node) is None:
                    warnings_functions_without_docstrings.append(f"Warning: Function '{file_name}: {node.name}' has no documentation.\n")
                    count_warn_per_file[file_name] = count_warn_per_file[file_name] + 1 if file_name in count_warn_per_file.keys() else 1

    warnings_functions_without_docstrings.sort()
    return warnings_functions_without_docstrings

def get_count_warn_per_file():
    return count_warn_per_file

def clear_objects():
    clear_count_warn_per_file()
    source_codes.clear()
    trees.clear()

def clear_count_warn_per_file():
    count_warn_per_file.clear()

if __name__ == '__main__':
    # f = file.File(path=r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app",
    #               name="main.py")
    # print(f)
    # open_file(f)
    # print(source_code)

    open_directory(r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app")
    # print(source_codes)
    # for key,value in source_codes.items():
    #     print(key + ":")
    #     print(value)
    # print(check_over_20_lines())
    # print(check_file_over_200_lines())
    # print(find_unused_variables())
    print(find_functions_without_docstrings())
    # for key,value in count_warn_per_file.items():
    #     print(key + ":")
    #     print(value)
    # length = get_functions_lengths()
    # print(length)

