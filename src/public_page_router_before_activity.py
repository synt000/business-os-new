from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.business_profile import BusinessProfile


router = APIRouter(
    prefix="",
    tags=["Public Web Page"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
async def read_landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@router.get("/landing-page", response_class=HTMLResponse)
async def read_test_landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})



@router.get("/register", response_class=HTMLResponse)
async def read_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})




@router.get("/{business_slug}", response_class=HTMLResponse)
async def public_business_page(
    business_slug: str,
    db: Session = Depends(get_db)
):

    profile = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.business_slug == business_slug,
            BusinessProfile.is_public == True
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="PUBLIC_PAGE_NOT_FOUND"
        )


    color = profile.theme_color or "#6F4E37"


    def btn(icon, text, url):
        if url:
            return f"""
            <a class="contact-btn" href="{url}">
                {icon} {text}
            </a>
            """
        return ""


    phone = profile.owner_phone or profile.phone


    contact_buttons = ""

    contact_buttons += btn(
        "📞",
        "Call Owner",
        f"tel:{phone}"
        if phone else None
    )


    contact_buttons += btn(
        "💬",
        "Viber",
        f"viber://chat?number={profile.viber_number}"
        if profile.viber_number else None
    )


    contact_buttons += btn(
        "✈️",
        "Telegram",
        f"https://t.me/{profile.telegram_username}"
        if profile.telegram_username else None
    )


    contact_buttons += btn(
        "📘",
        "Facebook",
        f"https://facebook.com/{profile.facebook_username}"
        if profile.facebook_username else None
    )


    contact_buttons += btn(
        "🌐",
        "Website",
        profile.website_url
    )


    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">


<title>{profile.business_name}</title>


<style>

body {{
margin:0;
font-family:Arial;
background:#f3f4f6;
}}


.cover {{
height:180px;
background:
url('{profile.cover_url or ""}')
center/cover;
}}


.header {{

background:{color};
color:white;

padding:30px;

text-align:center;

font-size:30px;

font-weight:bold;

}}



.logo {{

width:90px;

height:90px;

border-radius:50%;

object-fit:cover;

margin-top:-45px;

border:5px solid white;

}}



.card {{

background:white;

margin:20px;

padding:25px;

border-radius:25px;

text-align:center;

box-shadow:0 5px 20px #ddd;

}}



.owner {{

font-size:20px;

margin:20px;

}}



.contact {{

display:flex;

flex-wrap:wrap;

justify-content:center;

gap:12px;

}}



.contact-btn {{

background:{color};

color:white;

padding:14px 20px;

border-radius:30px;

text-decoration:none;

font-weight:bold;

}}



.order {{

display:block;

margin-top:25px;

background:#16a34a;

color:white;

padding:16px;

border-radius:30px;

text-decoration:none;

font-size:18px;

}}

</style>


</head>



<body>


<div class="cover"></div>


<div class="header">

{profile.business_name}

</div>



<div class="card">


<img class="logo"
src="{profile.logo_url or 'https://via.placeholder.com/100'}">



<h2>
{profile.welcome_message or ""}
</h2>


<p>
{profile.description or ""}
</p>



<div class="owner">

👤 Owner:
<b>{profile.owner_name or "Business Owner"}</b>

</div>



<div class="contact">

{contact_buttons}

</div>



<a class="order">

🛒 Order Now

</a>



</div>


</body>

</html>

"""


    return HTMLResponse(html)


@router.get("/api/public/home-revenue-chart")
async def public_home_revenue_chart(
    db: Session = Depends(get_db)
):

    from sqlalchemy import func
    from src.models.saas_core import AccountLedger

    rows = (
        db.query(
            func.date(AccountLedger.created_at),
            func.sum(AccountLedger.amount)
        )
        .filter(
            AccountLedger.entry_type == "CREDIT"
        )
        .group_by(
            func.date(AccountLedger.created_at)
        )
        .order_by(
            func.date(AccountLedger.created_at)
        )
        .all()
    )

    return {
        "labels": [
            str(r[0])
            for r in rows
        ],
        "values": [
            r[1]
            for r in rows
        ]
    }


@router.get("/api/public/home-dashboard")
async def public_home_dashboard(
    db: Session = Depends(get_db)
):

    from sqlalchemy import func
    from src.models.saas_core import (
        Tenant,
        Order,
        AccountLedger
    )
    from src.domains.product.models import Product


    tenant = (
        db.query(Tenant)
        .first()
    )

    if not tenant:
        return {
            "revenue":0,
            "orders":0,
            "products":0,
            "subscription":"NONE"
        }


    revenue = (
        db.query(func.sum(AccountLedger.amount))
        .filter(
            AccountLedger.tenant_id == tenant.id,
            AccountLedger.entry_type == "CREDIT"
        )
        .scalar()
        or 0
    )


    orders = (
        db.query(Order)
        .filter(
            Order.tenant_id == tenant.id
        )
        .count()
    )


    products = (
        db.query(Product)
        .filter(
            Product.tenant_id == tenant.id
        )
        .count()
    )


    return {
        "revenue": revenue,
        "orders": orders,
        "products": products,
        "subscription": tenant.subscription_tier.value
    }
