from pathlib import Path

p = Path("src/static/js/dashboard.js")

s = p.read_text()

js = """


// BUSINESS OS THEME SWITCH

document.addEventListener("DOMContentLoaded",()=>{

const btn=document.getElementById("themeToggle");

if(localStorage.getItem("businessos_theme")==="light"){
    document.body.classList.add("light-theme");
}

if(btn){

btn.onclick=()=>{

document.body.classList.toggle("light-theme");

localStorage.setItem(
"businessos_theme",
document.body.classList.contains("light-theme")
?"light"
:"dark"
);

btn.innerText =
document.body.classList.contains("light-theme")
?"🌙 Dark"
:"☀️ Light";

};

}

});

"""

if "BUSINESS OS THEME SWITCH" not in s:
    s += js
    p.write_text(s)
    print("theme js added")
else:
    print("already exists")
