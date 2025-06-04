
import ast
from models import file


source_code = ""
tree = ""

def open_file(file: file.File):
    with open(f"{file.path}/{file.name}", 'r', encoding='utf-8') as openfile:
        global source_code
        source_code = openfile.read()
        global tree
        tree = ast.parse(source_code)


def get_functions_lengths():
    lengths = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # אורך הפונקציה הוא מספר השורות בגוף הפונקציה
            length = len(node.body)
            lengths[node.name] = length

    return lengths


def check_over_20_lines():
    lengths = get_functions_lengths()
    arr_warnings = []
    for function_name, length in lengths.items():
        if length > 20:
            arr_warnings.append(f"warning: The length of function '{function_name}' is {length}!! greater than 20!")
    return arr_warnings

def check_file_over_200_lines():
    line_count = source_code.count('\n') + 1
    if line_count > 200:
        return f"The file length is {line_count} - greater than 200!"

def find_unused_variables():

    assigned_variables = set()
    used_variables = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_variables.add(target.id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_variables.add(node.id)

    # משתנים שהוקצו אך לא בשימוש
    unused_variables = assigned_variables - used_variables

    # התרעה עבור כל משתנה לא בשימוש
    arr_warnings = []
    for var in unused_variables:
        arr_warnings.append(f"Warning: Variable '{var}' is assigned but not used.")

    return arr_warnings


def find_functions_without_docstrings():
    warnings_functions_without_docstrings = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                warnings_functions_without_docstrings.append(f"Warning: Function '{node.name}' has no documentation.")

    return warnings_functions_without_docstrings

if __name__ == '__main__':
    f = file.File(path=r"C:\Users\user1\Desktop\תכנות\יד - שנה ב\פייתון\פייתון מתקדם\finalPythonProject\app",
                  name="main.py")
    # print(f)
    open_file(f)
    # print(source_code)
    print(check_over_20_lines())
    print(check_file_over_200_lines())
    print(find_unused_variables())
    print(find_functions_without_docstrings())