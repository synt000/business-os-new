from pathlib import Path

p = Path("src/dashboard/router.py")

text = p.read_text()

insert = '''

@router.get("/accounting/ui", response_class=HTMLResponse)
async def accounting_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="accounting.html"
    )


@router.get("/invoice/ui", response_class=HTMLResponse)
async def invoice_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="invoice.html"
    )


@router.get("/payment/ui", response_class=HTMLResponse)
async def payment_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="payment.html"
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="settings.html"
    )

'''

marker='@router.get("/api/public/home-summary")'

text=text.replace(marker, insert+marker)

p.write_text(text)

print("DONE")
