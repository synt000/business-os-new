from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()

html = html.replace(
""".top-bar{

    height:70px;

    padding:15px 20px;

    display:flex;

    justify-content:space-between;

    align-items:center;

    background:

    linear-gradient(
    135deg,
    rgba(255,255,255,0.08),
    rgba(255,255,255,0.02)
    );


    backdrop-filter:blur(20px);

    border-bottom:

    1px solid rgba(255,255,255,0.08);

}
""",
""".top-bar{

    height:78px;

    padding:15px 20px;

    display:flex;

    justify-content:space-between;

    align-items:center;

    background:
    linear-gradient(
    135deg,
    rgba(0,229,255,0.12),
    rgba(255,255,255,0.03)
    );

    backdrop-filter:blur(25px);

    border-bottom:
    1px solid rgba(255,255,255,0.12);

}


.brand-area{

    display:flex;

    flex-direction:column;

}


.brand-name{

    font-size:20px;

    font-weight:800;

}


.status{

    font-size:11px;

    color:#00ff99;

}


.status::before{

    content:"";

    display:inline-block;

    width:7px;

    height:7px;

    background:#00ff99;

    border-radius:50%;

    margin-right:5px;

}


.top-actions{

    display:flex;

    align-items:center;

    gap:10px;

}


.notification{

    width:38px;

    height:38px;

    border-radius:14px;

    display:flex;

    align-items:center;

    justify-content:center;

    background:rgba(255,255,255,0.08);

}


.vip{

    font-size:10px;

    padding:5px 8px;

    border-radius:20px;

    background:linear-gradient(135deg,#ffd700,#ff8c00);

    color:#111;

    font-weight:800;

}
"""
)


html = html.replace(
"""<div class="logo">

Business<span>OS</span>

</div>


<div class="profile-btn">

R

</div>
""",
"""<div class="brand-area">

<div class="brand-name">

Business<span>OS</span>

</div>

<div class="status">

Online

</div>

</div>


<div class="top-actions">

<div class="vip">

VIP

</div>


<div class="notification">

🔔

</div>


<div class="profile-btn">

R

</div>

</div>
"""
)

file.write_text(html)

print("Part 2 Top Bar Updated")
