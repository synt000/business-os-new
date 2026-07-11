from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.bottom-nav{

    position:fixed;

    left:50%;

    bottom:15px;

    transform:translateX(-50%);


    width:calc(100% - 30px);

    max-width:450px;


    height:70px;


    border-radius:28px;


    display:flex;

    align-items:center;

    justify-content:space-around;


    background:

    rgba(15,20,35,.85);


    backdrop-filter:blur(25px);


    border:

    1px solid rgba(255,255,255,.12);


    z-index:40;


}



.nav-item{

    flex:1;

    text-align:center;

    color:#9caec3;

    font-size:11px;

    position:relative;

}



.nav-icon{

    font-size:22px;

    display:block;

    margin-bottom:4px;

}



.nav-item.active{

    color:#00e5ff;

}



.nav-item.active::before{

    content:"";

    position:absolute;

    top:-12px;

    left:50%;

    transform:translateX(-50%);


    width:35px;

    height:4px;


    border-radius:10px;


    background:#00e5ff;

}



"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""<!-- FLOATING ACTION BUTTON END -->""",
"""<!-- FLOATING ACTION BUTTON END -->


<!-- BOTTOM NAVIGATION START -->


<nav class="bottom-nav">


<div class="nav-item active">

<span class="nav-icon">

🏠

</span>

Home

</div>


<div class="nav-item">

<span class="nav-icon">

🛒

</span>

Orders

</div>


<div class="nav-item">

<span class="nav-icon">

📦

</span>

Products

</div>


<div class="nav-item">

<span class="nav-icon">

📈

</span>

Analytics

</div>


<div class="nav-item">

<span class="nav-icon">

👤

</span>

Profile

</div>


</nav>


<!-- BOTTOM NAVIGATION END -->"""
)


file.write_text(html)

print("Part 17 Bottom Navigation Added")
