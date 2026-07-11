from pathlib import Path

path = Path("dashboard.html")
html = path.read_text(encoding="utf-8")

script = r"""

<script>

document.addEventListener("DOMContentLoaded", () => {

    // Bottom Navigation
    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach(item => {

        item.addEventListener("click", () => {

            navItems.forEach(n => n.classList.remove("active"));

            item.classList.add("active");

        });

    });

    // Floating Action Button
    const fab = document.querySelector(".fab");

    if(fab){

        fab.addEventListener("click", () => {

            alert("Quick Add");

        });

    }

    // Quick Actions
    document.querySelectorAll(".action-card").forEach(card => {

        card.addEventListener("click", () => {

            const title = card.querySelector(".action-name");

            if(title){

                alert(title.textContent);

            }

        });

    });

    // Demo Live Statistics
    const revenue = document.querySelector('[data-api="revenue"]');

    if(revenue){

        let value = 24800;

        setInterval(() => {

            value += Math.floor(Math.random()*20);

            revenue.textContent = "$" + (value/1000).toFixed(1) + "K";

        },3000);

    }

});

</script>

"""

html = html.replace("</body>", script + "\n</body>")

path.write_text(html, encoding="utf-8")

print("Part 18 Completed")
