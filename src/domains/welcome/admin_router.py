from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from sqlalchemy.orm import Session

from src.core.database import get_db
from .service import WelcomeService
from .schemas import WelcomeUpdate


router = APIRouter(
    prefix="/admin",
    tags=["Welcome CMS Admin"]
)


templates = Jinja2Templates(
    directory="src/templates"
)


@router.get(
    "/welcome",
    response_class=HTMLResponse
)
def welcome_editor(
    request: Request,
    db: Session = Depends(get_db)
):

    welcome = WelcomeService.get_welcome(
        db,
        "mm"
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/welcome_editor.html",
        context={
            "welcome": welcome
        }
    )


@router.post("/welcome/update")
def update_welcome(
    payload: WelcomeUpdate,
    db: Session = Depends(get_db)
):

    try:
        payload.features_json = json.loads(
            payload.features_json
            if isinstance(payload.features_json,str)
            else json.dumps(payload.features_json)
        )
    except:
        payload.features_json = []

    try:
        payload.sections_json = json.loads(
            payload.sections_json
            if isinstance(payload.sections_json,str)
            else json.dumps(payload.sections_json)
        )
    except:
        payload.sections_json = []

    WelcomeService.update_welcome(
        db,
        payload
    )

    return RedirectResponse(
        "/admin/welcome",
        status_code=303
    )
