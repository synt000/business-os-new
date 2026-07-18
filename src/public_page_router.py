from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.business_profile import BusinessProfile


BLOCKED_PUBLIC_PATHS = {
    "favicon.ico",
    "dashboard",
    "login",
    "logout",
    "api",
    "docs",
    "openapi.json"
}

router = APIRouter(
    prefix="",
    tags=["Public Web Page"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
async def read_landing_page(
    request: Request,
    db: Session = Depends(get_db)
):

    businesses = (
        db.query(BusinessProfile)
        .filter(
            BusinessProfile.is_public == True
        )
        .order_by(
            BusinessProfile.id
        )
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={
            "businesses": businesses
        }
    )


@router.get("/landing-page", response_class=HTMLResponse)
async def read_test_landing_page(request: Request):
    return templates.TemplateResponse(request=request, name="landing.html")



@router.get("/register", response_class=HTMLResponse)
async def read_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})




@router.get("/openapi.json", include_in_schema=False)
async def openapi_guard():
    raise HTTPException(
        status_code=404,
        detail="NOT_PUBLIC_PAGE"
    )


@router.get("/docs", include_in_schema=False)
async def docs_guard():
    raise HTTPException(
        status_code=404,
        detail="NOT_PUBLIC_PAGE"
    )


@router.get("/{business_slug}", response_class=HTMLResponse)
async def public_business_page(
    business_slug: str,
    db: Session = Depends(get_db)
):

    if business_slug in BLOCKED_PUBLIC_PATHS:
        raise HTTPException(
            status_code=404,
            detail="PUBLIC_PAGE_NOT_FOUND"
        )

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
<html lang="my">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{profile.business_name}</title>

<style>

* {{
box-sizing:border-box;
}}

body {{
margin:0;
font-family:Inter,Arial,sans-serif;
background:#f8fafc;
color:#0f172a;
}}


.cover {{
height:260px;
background:
linear-gradient(
rgba(0,0,0,.35),
rgba(0,0,0,.55)
),
url('{profile.cover_url or ""}')
center/cover;
}}


.header {{
background:{color};
color:white;
padding:35px 20px 80px;
text-align:center;
font-size:34px;
font-weight:800;
}}


.container {{
max-width:900px;
margin:-60px auto 40px;
padding:20px;
}}


.card {{
background:white;
border-radius:30px;
padding:30px;
box-shadow:
0 20px 50px rgba(15,23,42,.12);
text-align:center;
}}


.logo {{
width:120px;
height:120px;
border-radius:50%;
object-fit:cover;
border:6px solid white;
margin-top:-90px;
background:white;
}}


h1,h2,h3 {{
margin-top:15px;
}}


.description {{
font-size:18px;
color:#475569;
line-height:1.8;
}}


.owner {{
margin:25px 0;
font-size:18px;
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
padding:14px 22px;
border-radius:999px;
text-decoration:none;
font-weight:700;
}}


.order {{
display:block;
margin-top:30px;
background:#16a34a;
color:white;
padding:18px;
border-radius:999px;
font-size:20px;
font-weight:800;
text-decoration:none;
}}


.feature-grid {{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:20px;
margin-top:25px;
}}


.feature {{
background:#f1f5f9;
padding:25px;
border-radius:25px;
font-weight:700;
}}


footer {{
text-align:center;
padding:30px;
color:#64748b;
}}

</style>

</head>


<body>


<div class="cover"></div>


<div class="header">

{profile.business_name}

</div>



<div class="container">


<div class="card">


<img class="logo"
src="{profile.logo_url or 'https://via.placeholder.com/120'}">


<h2>
{profile.welcome_message or "Welcome"}
</h2>


<p class="description">
{profile.description or ""}
</p>



<div class="owner">

👤 Owner:
<b>{profile.owner_name or "Business Owner"}</b>

</div>



<div class="contact">

{contact_buttons}

</div>



<a class="order" href="#">

🛒 Order Now

</a>



<div class="feature-grid">


<div class="feature">
📦 Products
</div>


<div class="feature">
🧾 Invoice
</div>


<div class="feature">
💰 Finance
</div>


<div class="feature">
👥 Customers
</div>


</div>


</div>


</div>



<footer>

Powered by 🚀 Business OS Myanmar

</footer>


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


@router.get("/api/public/home-activity")
async def public_home_activity(
    db: Session = Depends(get_db)
):

    from src.models.saas_core import AccountLedger, Order

    activities = []

    payments = (
        db.query(AccountLedger)
        .order_by(AccountLedger.created_at.desc())
        .limit(5)
        .all()
    )

    for item in payments:

        activities.append({
            "title": item.account_head,
            "detail": str(item.amount) + " MMK",
            "type": item.entry_type
        })


    orders = (
        db.query(Order)
        .order_by(Order.created_at.desc())
        .limit(3)
        .all()
    )

    for order in orders:

        activities.append({
            "title": "Order Created",
            "detail": order.order_number,
            "type": "ORDER"
        })


    return activities[:5]



@router.get("/api/public/home-health")
async def public_home_health(
    db: Session = Depends(get_db)
):

    from sqlalchemy import text
    from src.models.saas_core import Tenant


    health = {
        "database": "Healthy",
        "accounting": "Balanced",
        "subscription": "Active",
        "security": "Protected"
    }


    try:
        db.execute(text("SELECT 1"))
        health["database"] = "Healthy"

    except Exception:
        health["database"] = "Error"


    tenant = db.query(Tenant).first()

    if tenant:

        if tenant.is_billing_active:
            health["subscription"] = "Active"
        else:
            health["subscription"] = "Inactive"


    return health

