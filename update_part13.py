from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.activity-item{

    display:flex;

    align-items:center;

    gap:12px;

    padding:14px;

    border-radius:22px;


    background:

    linear-gradient(
    145deg,
    rgba(255,255,255,.08),
    rgba(255,255,255,.03)
    );


    border:

    1px solid rgba(255,255,255,.10);

}


.activity-icon{

    width:42px;

    height:42px;

    border-radius:15px;


    display:flex;

    align-items:center;

    justify-content:center;


    background:

    rgba(255,255,255,.12);

    font-size:20px;

}


.activity-info{

    flex:1;

}


.activity-title{

    font-size:13px;

    font-weight:700;

}


.activity-time{

    margin-top:4px;

    font-size:11px;

    color:#9caec3;

}


"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<!-- Activity Items Coming Part 13 -->""",
"""<div class="activity-item">


<div class="activity-icon">

🛒

</div>


<div class="activity-info">


<div class="activity-title">

New Order Created

</div>


<div class="activity-time">

2 minutes ago

</div>


</div>


</div>



<div class="activity-item">


<div class="activity-icon">

💰

</div>


<div class="activity-info">


<div class="activity-title">

Payment Received

</div>


<div class="activity-time">

15 minutes ago

</div>


</div>


</div>



<div class="activity-item">


<div class="activity-icon">

📦

</div>


<div class="activity-info">


<div class="activity-title">

Product Added

</div>


<div class="activity-time">

1 hour ago

</div>


</div>


</div>"""
)


file.write_text(html)

print("Part 13 Activity Timeline Added")
