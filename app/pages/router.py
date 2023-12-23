from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get('/main')
def get_main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "title": "Result"})

