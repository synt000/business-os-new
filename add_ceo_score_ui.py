from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text(encoding="utf-8")

if "CEO Health Score" in text:
    print("Already Added")
    exit()

insert = """

<div class="card">

<h3>🧠 CEO Health Score</h3>

<div id="ceoScore">
Loading CEO Score...
</div>

</div>


<script>

async function loadCEOScore(){

try{

const res = await fetch(
"/ai/ceo-score",
{
headers:{
"Authorization":
"Bearer "+localStorage.getItem("access_token")
}
}
);

const data = await res.json();


let color =
data.level=="EXCELLENT"
? "#22c55e"
: "#f59e0b";


let html = `

<h4>
Score:
<b>${data.score}/100</b>
</h4>


<div style="
background:#222;
height:14px;
border-radius:10px;
">

<div style="
width:${data.score}%;
background:${color};
height:14px;
border-radius:10px;
">
</div>

</div>


<br>

<b>Status:</b>
${data.level}


<br><br>

<b>Risks:</b>

<ul>
${
data.risks.map(
r=>`<li>${r}</li>`
).join("")
}
</ul>

`;

document.getElementById(
"ceoScore"
).innerHTML = html;


}

catch(e){

console.log(
"CEO Score Error",
e
);

}

}


loadCEOScore();

</script>

"""


text = text.replace(
"</body>",
insert + "\n</body>"
)

p.write_text(
text,
encoding="utf-8"
)

print("CEO Score UI Added")

