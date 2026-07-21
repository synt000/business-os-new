from pathlib import Path

p = Path("src/templates/dashboard.html")

text = p.read_text()

# remove CEO JS block
start = text.find("// CEO FINANCE INSIGHT")

if start != -1:
    # next script section end ရှာ
    end = text.find("</script>", start)

    if end != -1:
        text = text[:start] + text[end:]
        print("REMOVED CEO JS BLOCK")
    else:
        print("END SCRIPT NOT FOUND")
else:
    print("CEO BLOCK NOT FOUND")

p.write_text(text)
