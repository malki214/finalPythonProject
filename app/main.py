
import uvicorn
from fastapi import FastAPI
from alerts_functions import *
from graphs_functions import *
from PIL import Image
from models import file

app = FastAPI()
mal = 0
abc = "sdf"
@app.get('/')
async def check_if_alive():
    return 'site is alive 🙌'

@app.post('/analyze')
async def graphs(file: file.File):
    open_file(file)
    img = Image.open(histogram_functions_lengths(file.path))
    img.show()
    img = Image.open(number_problems_for_each_problem_type(file.path))
    img.show()
    img = Image.open(number_problem_per_file(file))
    img.show()
    return f'{file.path}\images'

@app.post('/alerts')
async def alerts(file: file.File):
    open_file(file)
    arr_alerts = []
    arr_alerts.append(check_over_20_lines())
    arr_alerts.append(check_file_over_200_lines())
    arr_alerts.append(find_unused_variables())
    arr_alerts.append(find_functions_without_docstrings())
    return arr_alerts

def a():
    """
    this a example func
    :return:
    """
    print("hello")

def b():
    print("hello")
    print("hello")

def c():
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")

def d():
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")
    print("hello")


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000)