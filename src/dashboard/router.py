import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Enterprise Dashboard Core"])

# Resolve target templates folder dynamically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/dashboard", response_class=HTMLResponse)
async def render_secure_workspace_dashboard(request: Request):
    """Renders the guarded multi-tenant corporate hub environment safely."""
    return templates.TemplateResponse(request=request, name="workspace.html")
