from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.activity-header-action{

    font-size:12px;

    color:#00e5ff;

    padding:8px 14px;

    border-radius:16px;

    background:

    rgba(0,229,255,.10);

    border:

    1px solid rgba(0,229,255,.20);

}


.activity-item[data-id]{

    transition:.3s;

}


.activity-item[data-id]:active{

    transform:scale(.98);

}



.empty-state{

    display:none;

    text-align:center;

    padding:20px;

    color:#9caec3;

    font-size:13px;

}



"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<h2 class="section-title">

Recent Activity

</h2>""",
"""<h2 class="section-title">

Recent Activity

</h2>


<div class="activity-header-action">

View All

</div>"""
)


html = html.replace(
"""<div class="activity-item">""",
"""<div class="activity-item" data-id="activity-001">""",
1
)


html = html.replace(
"""<div class="activity-item" data-type="warning">""",
"""<div class="activity-item" data-id="activity-003" data-type="warning">"""
)


html = html.replace(
"""<div class="activity-item">""",
"""<div class="activity-item" data-id="activity-002">""",
1
)


html = html.replace(
"""</div>


</section>


<!-- RECENT ACTIVITY END -->""",
"""</div>


<div class="empty-state">

No recent activity

</div>


</section>


<!-- RECENT ACTIVITY END -->"""
)


file.write_text(html)

print("Part 15 Recent Activity Final Completed")
