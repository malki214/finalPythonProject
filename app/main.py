
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from alerts_functions import *
from graphs_functions import *
from models import file
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get('/')
async def check_if_alive():
    return 'site is alive 🙌'

app.mount("/images", StaticFiles(directory="images"), name="images")


@app.post('/analyze')
async def graphs(file: file.File):
    if not os.path.exists(file.path):
        raise HTTPException(status_code=401, detail="The path does not exist.")

    clear_objects()
    open_directory(file.path)

    histogram_functions_lengths()
    number_problems_for_each_problem_type()
    number_problem_per_file()

    html_content = "<html><body><h1>graphs</h1>"
    images = os.listdir("./images")
    for image in images:
        if image != "output.html":
            # השתמש בנתיב סטטי לתמונה
            image_path = f"/images/{image}"
            html_content += f'<img src="{image_path}" alt="Image"><br>'
    html_content += "</body></html>"

    html_file_path = "./images/output.html"
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    # return {"link": "/output"}
    return "http://localhost:8000/output"

@app.get("/output", response_class=HTMLResponse)
async def get_html():
    with open("./images/output.html", "r") as html_file:
        return HTMLResponse(content=html_file.read())

@app.post('/alerts')
async def alerts(file: file.File):
    if not os.path.exists(file.path):
        raise HTTPException(status_code=400, detail="The path does not exist.")
    clear_objects()
    open_directory(file.path)
    mat_alerts = []
    mat_alerts.append(check_over_20_lines())
    mat_alerts.append(check_file_over_200_lines())
    mat_alerts.append(find_unused_variables())
    mat_alerts.append(find_functions_without_docstrings())

    arr_alerts = [alert for arr_alert in mat_alerts for alert in arr_alert]

    return ''.join(arr_alerts)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=8000)
    if not os.path.exists("images"):
        os.mkdir("images")