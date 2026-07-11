from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


insert_css = """

/* =====================
   HERO READY CONTAINER
===================== */


.hero-section{

    margin-top:20px;

    padding:22px;

    border-radius:28px;

    background:

    linear-gradient(
    135deg,
    rgba(0,229,255,0.18),
    rgba(0,102,255,0.18)
    );

    border:

    1px solid rgba(255,255,255,0.12);

    overflow:hidden;

    position:relative;

}


.hero-section::before{

    content:"";

    position:absolute;

    width:160px;

    height:160px;

    right:-50px;

    top:-50px;

    background:

    radial-gradient(
    circle,
    rgba(0,229,255,.5),
    transparent 70%
    );

}


.hero-title{

    font-size:24px;

    font-weight:800;

    position:relative;

}


.hero-subtitle{

    margin-top:8px;

    font-size:13px;

    color:#b8c7d9;

    position:relative;

}

"""


html = html.replace(
"</style>",
insert_css + "\n\n</style>"
)


html = html.replace(
"""<!-- NEXT PARTS WILL COME HERE -->


</main>""",
"""<!-- HERO BANNER START -->


<section class="hero-section">


<h1 class="hero-title">

Welcome Back 👋

</h1>


<p class="hero-subtitle">

Manage your business smarter with Business OS

</p>


</section>


<!-- HERO BANNER END -->


</main>"""
)


file.write_text(html)

print("Part 3 Completed")
