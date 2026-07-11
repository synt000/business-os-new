from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.quick-section{

    animation:fadeUp .7s ease;

}


.action-card{

    overflow:hidden;

}


.action-card::before{

    content:"";

    position:absolute;

    inset:0;

    background:

    linear-gradient(
    135deg,
    rgba(0,229,255,.12),
    transparent
    );

    opacity:0;

    transition:.3s;

}


.action-card:hover::before{

    opacity:1;

}



.activity-section{

    margin-top:30px;

}


.activity-list{

    display:flex;

    flex-direction:column;

    gap:12px;

}



"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<!-- QUICK ACTIONS END -->""",
"""<!-- QUICK ACTIONS END -->


<!-- RECENT ACTIVITY START -->


<section class="activity-section">


<div class="section-header">

<h2 class="section-title">

Recent Activity

</h2>


</div>



<div class="activity-list">


<!-- Activity Items Coming Part 13 -->


</div>


</section>


<!-- RECENT ACTIVITY END -->"""
)


file.write_text(html)

print("Part 12 Completed")
