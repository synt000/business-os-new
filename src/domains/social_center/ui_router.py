from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["Social Center UI"]
)


templates = Jinja2Templates(
    directory="src/templates"
)


@router.get(
    "/social-center",
    response_class=HTMLResponse
)
def social_center_page(
    request: Request
):

    return templates.TemplateResponse(
        "social_center.html",
        {
            "request": request
        }
    )
