from md_parser import get_markdown_document, render_html, render_ast, render_mpm
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory="../static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    doc = get_markdown_document('../example/test.md')
    html = render_mpm(doc)
    return html