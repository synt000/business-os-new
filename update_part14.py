from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.activity-list{

    position:relative;

}


.activity-list::before{

    content:"";

    position:absolute;

    left:34px;

    top:20px;

    bottom:20px;

    width:1px;

    background:

    rgba(255,255,255,.15);

}


.activity-item{

    position:relative;

    z-index:1;

}



.activity-status{

    display:inline-flex;

    align-items:center;

    gap:5px;

    margin-top:6px;

    padding:4px 9px;

    border-radius:12px;

    font-size:10px;

    background:

    rgba(0,255,153,.12);

    color:#00ff99;

}



.status-dot{

    width:6px;

    height:6px;

    border-radius:50%;

    background:#00ff99;

}



.activity-item[data-type="warning"] .activity-status{

    color:#ffd700;

    background:

    rgba(255,215,0,.12);

}


.activity-item[data-type="warning"] .status-dot{

    background:#ffd700;

}



"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<div class="activity-time">

2 minutes ago

</div>""",
"""<div class="activity-time">

2 minutes ago

</div>


<div class="activity-status">

<span class="status-dot"></span>

Completed

</div>"""
)


html = html.replace(
"""<div class="activity-item">


<div class="activity-icon">

📦

</div>""",
"""<div class="activity-item" data-type="warning">


<div class="activity-icon">

📦

</div>"""
)


html = html.replace(
"""<div class="activity-time">

1 hour ago

</div>""",
"""<div class="activity-time">

1 hour ago

</div>


<div class="activity-status">

<span class="status-dot"></span>

Updated

</div>"""
)


file.write_text(html)

print("Part 14 Activity Advanced Completed")
