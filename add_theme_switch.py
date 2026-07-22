from pathlib import Path

p = Path("src/static/js/dashboard.js")

s = p.read_text()

js = r'''

// =====================================
// BUSINESS OS THEME SWITCH
// =====================================

document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        const btn =
            document.getElementById("themeToggle");

        const saved =
            localStorage.getItem(
                "businessos_theme"
            );

        if(saved === "light"){
            document.body.classList.add(
                "light-theme"
            );
        }

        if(btn){

            btn.innerText =
                document.body.classList.contains(
                    "light-theme"
                )
                ? "☀️ Light"
                : "🌙 Dark";


            btn.onclick = ()=>{

                document.body.classList.toggle(
                    "light-theme"
                );


                const mode =
                    document.body.classList.contains(
                        "light-theme"
                    )
                    ? "light"
                    : "dark";


                localStorage.setItem(
                    "businessos_theme",
                    mode
                );


                btn.innerText =
                    mode === "light"
                    ? "☀️ Light"
                    : "🌙 Dark";

            };

        }

    }
);

'''

if "BUSINESS OS THEME SWITCH" not in s:
    s += js
    p.write_text(s)
    print("theme switch added")
else:
    print("already exists")

