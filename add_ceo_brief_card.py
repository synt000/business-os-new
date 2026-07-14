from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text(encoding="utf-8")

card = """

<div class="card">

<h3>🤖 CEO Daily Brief</h3>

<div id="ceoBrief">
Loading AI Report...
</div>

</div>

<script>

async function loadCEOBrief(){

try{

const res = await fetch(
"/ai/ceo-brief",
{
headers:{
"Authorization":
"Bearer "+localStorage.getItem("access_token")
}
}
);

const data = await res.json();


let html = "";

html += `
<b>📈 Performance</b><br>
Revenue: ${data.performance.revenue}<br>
Profit: ${data.performance.profit}<br>
Margin: ${data.performance.margin}%<br><br>
`;


data.insights.forEach(i=>{

html += `
<div>
<b>${i.title}</b><br>
${i.message}
</div>
<br>
`;

});


document.getElementById("ceoBrief").innerHTML = html;


}

catch(e){

console.log(
"CEO Brief Error",
e
);

}

}


loadCEOBrief();

</script>

"""


if "CEO Daily Brief" not in text:

    text += card

    p.write_text(
        text,
        encoding="utf-8"
    )

    print("✅ CEO Brief Card Added")

else:
    print("Already Added")
