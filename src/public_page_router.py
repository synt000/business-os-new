from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.business_profile import BusinessProfile


router = APIRouter(
    prefix="",
    tags=["Public Web Page"]
)


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
