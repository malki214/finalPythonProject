
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from alerts_functions import *
from graphs_functions import *
from models import file
from fastapi.staticfiles import StaticFiles

app = FastAPI()

if not os.path.exists("images"):
    os.mkdir("images")

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

    html_content = "<html><head><title>Code Analysis Graphs</title><style>body {background-color: #f0f4f8;font-family: Arial, sans-serif;text-align: center;padding: 30px;}h1 {color: #333;margin-bottom: 40px;}.image-container {display: flex;justify-content: center; flex-wrap: wrap; gap: 20px;}.image-container img {max-width: 400px;width: 100%;height: auto;border: 2px solid #ccc; border-radius: 10px;background: white;padding: 10px;box-shadow: 2px 2px 12px rgba(0,0,0,0.15);}</style></head><body><h1>Code Analysis Graphs</h1><div class='image-container'>"
    images = os.listdir("./images")
    for image in images:
        if image != "output.html":
            image_path = f"/images/{image}"
            html_content += f'<img src="{image_path}" alt=f"{image}"><br>'
    html_content += "</div></body></html>"

    html_file_path = "./images/output.html"
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    return "You can see the graphs at this link: http://localhost:8000/output"
    # return "http://localhost:8000/output"

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
