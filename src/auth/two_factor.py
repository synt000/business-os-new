import pyotp
import qrcode
import io
import base64
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import get_current_user
from src.models.saas_core import User


router = APIRouter(
    prefix="/api/v4/auth/2fa",
    tags=["Two Factor Security"]
)


def generate_backup_codes():

    return [
        secrets.token_hex(4).upper()
        for _ in range(10)
    ]


@router.post("/setup")
def setup_two_factor(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    secret = pyotp.random_base32()

    current_user.two_factor_secret = secret

    otp_uri = pyotp.TOTP(secret).provisioning_uri(
        name=current_user.email,
        issuer_name="Business OS"
    )

    img = qrcode.make(otp_uri)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()


    db.commit()


    return {
        "status": "2FA_SETUP_READY",
        "secret": secret,
        "qr_code": f"data:image/png;base64,{qr_base64}"
    }



@router.post("/verify")
def verify_two_factor(
    otp: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.two_factor_secret:

        raise HTTPException(
            status_code=400,
            detail="2FA_NOT_INITIALIZED"
        )


    verified = pyotp.TOTP(
        current_user.two_factor_secret
    ).verify(otp)


    if not verified:

        raise HTTPException(
            status_code=401,
            detail="INVALID_2FA_CODE"
        )


    current_user.two_factor_enabled = True

    current_user.backup_codes = ",".join(
        generate_backup_codes()
    )


    db.commit()


    return {
        "status": "2FA_ENABLED",
        "message": "Two Factor Authentication Activated"
    }



@router.post("/disable")
def disable_two_factor(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    current_user.two_factor_enabled = False
    current_user.two_factor_secret = None
    current_user.backup_codes = None

    db.commit()


    return {
        "status": "2FA_DISABLED"
    }
