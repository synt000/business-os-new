from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.quick-section{

    margin-top:28px;

}


.action-grid{

    display:grid;

    grid-template-columns:repeat(4,1fr);

    gap:12px;

}


.action-card{

    padding:14px 8px;

    border-radius:20px;

    text-align:center;

    background:

    linear-gradient(
    145deg,
    rgba(255,255,255,.10),
    rgba(255,255,255,.03)
    );


    border:

    1px solid rgba(255,255,255,.12);

    backdrop-filter:blur(15px);

    transition:.3s;

}


.action-card:active{

    transform:scale(.92);

}


.action-icon{

    width:42px;

    height:42px;

    margin:auto;

    border-radius:15px;

    display:flex;

    align-items:center;

    justify-content:center;

    background:

    rgba(255,255,255,.12);

    font-size:20px;

}


.action-name{

    margin-top:8px;

    font-size:11px;

    color:#d8e5f5;

}


"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<!-- STATISTICS SECTION END -->""",
"""<!-- STATISTICS SECTION END -->


<!-- QUICK ACTIONS START -->


<section class="quick-section">


<div class="section-header">

<h2 class="section-title">

Quick Actions

</h2>


</div>



<div class="action-grid">


<div class="action-card">


<div class="action-icon">

➕

</div>


<div class="action-name">

Product

</div>


</div>



<div class="action-card">


<div class="action-icon">

🛒

</div>


<div class="action-name">

Order

</div>


</div>



<div class="action-card">


<div class="action-icon">

📦

</div>


<div class="action-name">

Stock

</div>


</div>



<div class="action-card">


<div class="action-icon">

📊

</div>


<div class="action-name">

Reports

</div>


</div>


</div>


</section>


<!-- QUICK ACTIONS END -->"""
)


file.write_text(html)

print("Part 10 Quick Actions Added")
