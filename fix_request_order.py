from pathlib import Path

p = Path("src/auth/router.py")
text = p.read_text()

text = text.replace(
'''async def authenticate_via_oauth2_form_flow(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request,
    db: Session = Depends(get_db)
):''',
'''async def authenticate_via_oauth2_form_flow(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):'''
)

text = text.replace(
'''async def authenticate_via_pure_json_payload(
    payload: JSONLoginInboundPayload,
    request: Request,
    db: Session = Depends(get_db)
):''',
'''async def authenticate_via_pure_json_payload(
    request: Request,
    payload: JSONLoginInboundPayload,
    db: Session = Depends(get_db)
):'''
)

p.write_text(text)

print("REQUEST PARAMETER ORDER FIXED")
