from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

app: FastAPI = FastAPI()


@app.get("/")
async def index():
    with open(file='index.html',
              mode='r',
              encoding='utf-8') as html_file:
        html_content = html_file.read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
