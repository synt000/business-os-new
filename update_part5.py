from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.hero-metrics{

    margin-top:22px;

    display:flex;

    gap:10px;

}


.metric-mini{

    flex:1;

    padding:12px;

    border-radius:18px;

    background:

    rgba(255,255,255,0.08);

    border:

    1px solid rgba(255,255,255,.1);

    backdrop-filter:blur(15px);

}


.metric-mini h3{

    font-size:18px;

    font-weight:800;

}


.metric-mini p{

    margin-top:4px;

    font-size:11px;

    color:#b8c7d9;

}


.float-card{

    position:absolute;

    right:18px;

    bottom:18px;

    width:80px;

    height:80px;

    border-radius:25px;

    background:

    rgba(255,255,255,.12);

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:35px;

    backdrop-filter:blur(20px);

}

"""


html = html.replace(
"</style>",
css + "\n</style>"
)


old = """
<div class="hero-btn">

⚡ Open Workspace

</div>


</div>


</section>"""


new = """
<div class="hero-btn">

⚡ Open Workspace

</div>


<div class="hero-metrics">


<div class="metric-mini">

<h3>12.5K</h3>

<p>Sales</p>

</div>


<div class="metric-mini">

<h3>348</h3>

<p>Orders</p>

</div>


<div class="metric-mini">

<h3>+24%</h3>

<p>Growth</p>

</div>


</div>


</div>


<div class="float-card">

📊

</div>


</section>"""


html = html.replace(old,new)


file.write_text(html)

print("Part 5 Hero Metrics Added")
