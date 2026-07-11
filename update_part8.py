from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.live-dot{

    width:8px;

    height:8px;

    background:#00ff99;

    border-radius:50%;

    display:inline-block;

    margin-right:6px;

    animation:pulse 1.5s infinite;

}


.live-status{

    font-size:11px;

    color:#00ff99;

    margin-bottom:15px;

}



.chart-box{

    margin-top:15px;

    height:45px;

    display:flex;

    align-items:flex-end;

    gap:5px;

}


.bar{

    flex:1;

    height:20%;

    border-radius:8px;

    background:

    linear-gradient(
    top,
    #00e5ff,
    #0066ff
    );

}


.bar:nth-child(2){

    height:45%;

}


.bar:nth-child(3){

    height:70%;

}


.bar:nth-child(4){

    height:55%;

}


.bar:nth-child(5){

    height:90%;

}



@keyframes pulse{

    50%{

        opacity:.3;

    }

}


"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<div class="stat-number">

$24.8K

</div>""",
"""<div class="live-status">

<span class="live-dot"></span>

Live

</div>


<div class="stat-number">

$24.8K

</div>


<div class="chart-box">

<div class="bar"></div>

<div class="bar"></div>

<div class="bar"></div>

<div class="bar"></div>

<div class="bar"></div>

</div>"""
)


file.write_text(html)

print("Part 8 Statistics Advanced Completed")
