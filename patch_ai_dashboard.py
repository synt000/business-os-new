from pathlib import Path

path = Path("src/templates/dashboard.html")

text = path.read_text(encoding="utf-8")


ai_html = """

<div class="ai-panel">

<div class="ai-title">
🤖 AI Business Advisor
</div>

<div id="aiRecommendations">
Loading AI recommendations...
</div>

</div>

"""


marker = """
<div class="menu">
"""


if "aiRecommendations" not in text:

    text = text.replace(
        marker,
        ai_html + marker
    )


js_code = """

async function loadAIRecommendations(){

try{

const res = await fetch(
"/ai/recommendations",
{
headers:{
"Authorization":
"Bearer " + localStorage.getItem("access_token")
}
}
);


const data = await res.json();


const box =
document.getElementById(
"aiRecommendations"
);


box.innerHTML = "";


data.forEach(item=>{


let cls =
item.priority.toLowerCase();


box.innerHTML += `

<div class="ai-item ai-${cls}">

<b>${item.title}</b>

<br>

${item.action}

</div>

`;

});


}
catch(error){

console.log(
"AI Error:",
error
);

}

}

"""


if "loadAIRecommendations" not in text:

    text = text.replace(
        "loadDashboard();",
        "loadDashboard();\nloadAIRecommendations();"
    )

    text = text.replace(
        "</script>",
        js_code + "\n</script>"
    )


css = """

<style>

.ai-panel{
margin-top:20px;
background:#111827;
padding:20px;
border-radius:16px;
color:white;
}

.ai-title{
font-size:20px;
font-weight:bold;
margin-bottom:15px;
}

.ai-item{
background:#1f2937;
padding:12px;
margin-bottom:10px;
border-radius:10px;
}

.ai-high{
border-left:5px solid red;
}

.ai-medium{
border-left:5px solid orange;
}

.ai-info{
border-left:5px solid blue;
}

</style>

"""


if "AI Business Advisor" in text and "<style>" not in text:

    text = css + text


path.write_text(
    text,
    encoding="utf-8"
)

print("AI Dashboard Panel Patched Successfully")
