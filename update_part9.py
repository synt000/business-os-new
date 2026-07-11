from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.section-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:15px;

}


.view-btn{

    font-size:12px;

    padding:8px 14px;

    border-radius:16px;

    background:

    rgba(255,255,255,.08);

    color:#00e5ff;

    border:

    1px solid rgba(255,255,255,.12);

}


.stat-card[data-loading="true"]{

    opacity:.5;

}


.api-value{

    transition:.4s;

}


"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<h2 class="section-title">

Live Statistics

</h2>""",
"""<div class="section-header">

<h2 class="section-title">

Live Statistics

</h2>


<div class="view-btn">

View Report

</div>


</div>"""
)


html = html.replace(
"""<div class="stat-number">

$24.8K

</div>""",
"""<div class="stat-number api-value" data-api="revenue">

$24.8K

</div>"""
)


html = html.replace(
"""<div class="stat-number">

1,248

</div>""",
"""<div class="stat-number api-value" data-api="orders">

1,248

</div>"""
)


html = html.replace(
"""<div class="stat-number">

856

</div>""",
"""<div class="stat-number api-value" data-api="customers">

856

</div>"""
)


html = html.replace(
"""<div class="stat-number">

342

</div>""",
"""<div class="stat-number api-value" data-api="products">

342

</div>"""
)


file.write_text(html)

print("Part 9 Statistics Final Completed")
