import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Enterprise Dashboard"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="workspace.html"
    )


@router.get("/products", response_class=HTMLResponse)
async def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html"
    )


@router.get("/orders", response_class=HTMLResponse)
async def orders(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="orders.html"
    )


@router.get("/inventory", response_class=HTMLResponse)
async def inventory(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="inventory.html"
    )
