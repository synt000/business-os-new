from pathlib import Path

file = Path("dashboard.html")

html = file.read_text()


css = """

.fab{

    position:fixed;

    right:22px;

    bottom:90px;

    width:62px;

    height:62px;


    border-radius:50%;


    display:flex;

    align-items:center;

    justify-content:center;


    font-size:28px;


    background:

    linear-gradient(
    135deg,
    #00e5ff,
    #0066ff
    );


    box-shadow:

    0 10px 35px rgba(0,229,255,.35);


    cursor:pointer;


    z-index:50;


    transition:.3s;

}



.fab:active{

    transform:scale(.88) rotate(10deg);

}



.fab-ring{

    position:absolute;

    width:100%;

    height:100%;

    border-radius:50%;

    border:2px solid rgba(255,255,255,.35);

    animation:ring 2s infinite;

}



@keyframes ring{

    0%{

        transform:scale(1);

        opacity:1;

    }


    100%{

        transform:scale(1.5);

        opacity:0;

    }

}



"""


html = html.replace(
"</style>",
css + "\n</style>"
)


html = html.replace(
"""</div>


</body>


</html>""",
"""</div>


<!-- FLOATING ACTION BUTTON START -->


<div class="fab">


<div class="fab-ring"></div>


➕

</div>


<!-- FLOATING ACTION BUTTON END -->


</body>


</html>"""
)


file.write_text(html)

print("Part 16 FAB Added")
