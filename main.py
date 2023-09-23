from lib.md_parser import markdown2html
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory="./static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    html = markdown2html('./example/test.md')
    return html