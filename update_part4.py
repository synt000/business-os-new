from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.hero-content{

    position:relative;

    z-index:2;

}


.hero-tag{

    display:inline-block;

    padding:6px 12px;

    border-radius:20px;

    background:rgba(255,255,255,.12);

    font-size:11px;

    margin-bottom:15px;

}


.hero-title span{

    color:#00e5ff;

}


.hero-desc{

    margin-top:12px;

    line-height:1.5;

    font-size:14px;

    color:#c5d2e3;

}


.hero-btn{

    margin-top:20px;

    display:inline-flex;

    align-items:center;

    gap:8px;

    padding:12px 20px;

    border-radius:18px;

    background:

    linear-gradient(
    135deg,
    #00e5ff,
    #0066ff
    );

    color:white;

    font-weight:700;

    font-size:14px;

}

"""


html = html.replace(
"</style>",
css + "\n</style>"
)


old = """<section class="hero-section">


<h1 class="hero-title">

Welcome Back 👋

</h1>


<p class="hero-subtitle">

Manage your business smarter with Business OS

</p>


</section>"""


new = """<section class="hero-section">


<div class="hero-content">


<div class="hero-tag">

🚀 Premium Dashboard

</div>


<h1 class="hero-title">

Grow Your <span>Business</span> Faster

</h1>


<p class="hero-desc">

Track sales, manage inventory and control your entire business from one smart platform.

</p>


<div class="hero-btn">

⚡ Open Workspace

</div>


</div>


</section>"""


html = html.replace(old,new)


file.write_text(html)

print("Part 4 Hero Design Completed")
