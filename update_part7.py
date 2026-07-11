from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.stats-grid{

    display:grid;

    grid-template-columns:repeat(2,1fr);

    gap:14px;

}


.stat-card{

    padding:18px;

    border-radius:24px;

    background:

    linear-gradient(
    145deg,
    rgba(255,255,255,.10),
    rgba(255,255,255,.03)
    );


    border:

    1px solid rgba(255,255,255,.12);


    backdrop-filter:blur(20px);


    transition:.3s;

}


.stat-card:active{

    transform:scale(.96);

}


.stat-icon{

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


.stat-number{

    margin-top:15px;

    font-size:24px;

    font-weight:800;

}


.stat-label{

    margin-top:5px;

    font-size:12px;

    color:#b8c7d9;

}


.stat-growth{

    margin-top:10px;

    font-size:12px;

    color:#00ff99;

}


"""


html = html.replace(
"</style>",
css + "\n</style>"
)


old = """
<div id="stats-container">


<!-- Statistics Cards Coming Part 7 -->


</div>
"""


new = """
<div id="stats-container">


<div class="stats-grid">


<div class="stat-card">


<div class="stat-icon">

💰

</div>


<div class="stat-number">

$24.8K

</div>


<div class="stat-label">

Revenue

</div>


<div class="stat-growth">

↑ 18.5% Growth

</div>


</div>



<div class="stat-card">


<div class="stat-icon">

📦

</div>


<div class="stat-number">

1,248

</div>


<div class="stat-label">

Orders

</div>


<div class="stat-growth">

↑ 12% Today

</div>


</div>



<div class="stat-card">


<div class="stat-icon">

👥

</div>


<div class="stat-number">

856

</div>


<div class="stat-label">

Customers

</div>


<div class="stat-growth">

↑ 8.4% New

</div>


</div>



<div class="stat-card">


<div class="stat-icon">

🏬

</div>


<div class="stat-number">

342

</div>


<div class="stat-label">

Products

</div>


<div class="stat-growth">

Stock Ready

</div>


</div>


</div>


</div>
"""


html = html.replace(old,new)


file.write_text(html)

print("Part 7 Statistics Cards Added")
