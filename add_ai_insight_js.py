from pathlib import Path

p = Path("src/templates/dashboard.html")
text = p.read_text(encoding="utf-8")

if "loadAIInsights" in text:
    print("✅ AI Insight JS already exists")
    raise SystemExit

js = r"""

<script>

async function loadAIInsights(){

try{

const res = await fetch(
"/ai/insights",
{
headers:{
"Authorization":
"Bearer "+localStorage.getItem("access_token")
}
}
);

const data = await res.json();

const box = document.getElementById(
"aiInsightList"
);

if(!box) return;


box.innerHTML = "";


data.forEach(item=>{

let icon="ℹ️";

if(item.level==="WARNING"){
icon="⚠️";
}

box.innerHTML += `
<div style="margin:12px 0;padding:10px;border-radius:8px;background:#111827;color:white;">
<b>${icon} ${item.title}</b>
<br>
${item.message}
</div>
`;

});


}
catch(e){

console.log(
"AI Insight Error",
e
);

}

}


loadAIInsights();

</script>

"""

text = text.replace(
"</body>",
js + "\n</body>",
1
)

p.write_text(text, encoding="utf-8")

print("✅ AI Insight JS Added")
