from pathlib import Path

p = Path("src/domains/dashboard/router.py")

text = p.read_text()

insert = '''

@router.get("", response_class=HTMLResponse)
def owner_dashboard_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "owner_dashboard.html",
        {
            "request": request,
            "user": current_user
        }
    )

'''

marker = '@router.get(\n    "/menus"'

if insert not in text:
    text = text.replace(marker, insert + marker)

p.write_text(text)

print("Owner page route added")
