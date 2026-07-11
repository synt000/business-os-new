from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.hero-section{

    animation:fadeUp .6s ease;

}


.hero-btn{

    cursor:pointer;

    transition:.3s;

}


.hero-btn:active{

    transform:scale(.95);

}


.metric-mini{

    transition:.3s;

}


.metric-mini:active{

    transform:translateY(-4px);

}


@keyframes fadeUp{

    from{

        opacity:0;

        transform:translateY(20px);

    }

    to{

        opacity:1;

        transform:translateY(0);

    }

}



/* =====================
   STATISTICS READY
===================== */


.stats-section{

    margin-top:25px;

}


.section-title{

    font-size:18px;

    font-weight:800;

    margin-bottom:15px;

}



"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""</section>


<!-- HERO BANNER END -->""",
"""</section>


<!-- HERO BANNER END -->


<!-- STATISTICS SECTION START -->


<section class="stats-section">


<h2 class="section-title">

Live Statistics

</h2>


<div id="stats-container">


<!-- Statistics Cards Coming Part 7 -->


</div>


</section>


<!-- STATISTICS SECTION END -->"""
)


file.write_text(html)

print("Part 6 Completed")
