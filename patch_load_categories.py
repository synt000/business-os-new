from pathlib import Path

p = Path("src/templates/products.html")
text = p.read_text()

marker = "const token = localStorage.getItem(\"access_token\");"

if marker in text and "async function loadCategories()" not in text:
    inject = marker + '''

            async function loadCategories() {
                const select = document.getElementById("category_id");

                try {
                    const response = await fetch("/api/v4/business/categories", {
                        headers: {
                            "Authorization": `Bearer ${token}`
                        }
                    });

                    const data = await response.json();

                    select.innerHTML = "";

                    (data.categories || []).forEach(cat => {
                        const option = document.createElement("option");
                        option.value = cat.id;
                        option.textContent = cat.name;
                        select.appendChild(option);
                    });

                } catch (err) {
                    select.innerHTML =
                        "<option value=''>Unable to load categories</option>";
                    console.error(err);
                }
            }

            loadCategories();
'''
    text = text.replace(marker, inject)

p.write_text(text)

print("CATEGORY AUTO LOAD ADDED")
