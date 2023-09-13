from md_parser import get_markdown_document, render_html, render_ast, render_mpm
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    doc = get_markdown_document('../example/test.md')
    html = render_mpm(doc)
    return html