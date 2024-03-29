from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="",
    tags=["Pages"],
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def start_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
