from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.action-card{

    position:relative;

    cursor:pointer;

}


.action-card[data-role="admin"]::after{

    content:"PRO";

    position:absolute;

    top:8px;

    right:8px;

    font-size:8px;

    padding:3px 6px;

    border-radius:10px;

    background:

    linear-gradient(
    135deg,
    #ffd700,
    #ff9800
    );

    color:#111;

    font-weight:800;

}


.action-badge{

    position:absolute;

    top:-5px;

    right:-5px;

    min-width:18px;

    height:18px;

    padding:0 5px;

    border-radius:20px;

    background:#ff3b5c;

    font-size:10px;

    display:flex;

    align-items:center;

    justify-content:center;

}


.action-icon{

    transition:.3s;

}


.action-card:active .action-icon{

    transform:rotate(8deg) scale(1.1);

}


"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<div class="action-card">


<div class="action-icon">

🛒

</div>""",
"""<div class="action-card" data-role="admin">


<div class="action-icon">

🛒

</div>"""
)


html = html.replace(
"""<div class="action-icon">

📊

</div>


<div class="action-name">

Reports

</div>""",
"""<div class="action-icon">

📊

</div>


<div class="action-badge">

3

</div>


<div class="action-name">

Reports

</div>"""
)


file.write_text(html)

print("Part 11 Quick Actions Advanced Completed")
