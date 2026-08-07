from pathlib import Path
import subprocess

p = Path("src/product/router.py")

current = p.read_text()

head = subprocess.check_output(
    ["git", "show", "HEAD:src/product/router.py"],
    text=True
)

start = '@router.get("/orders/{order_id}/invoice")'
end = '@router.put("/orders/{order_id}/payment")'

head_block = head[
    head.index(start):
    head.index(end)
]

if start in current:
    a = current.index(start)
    b = current.index(end)
    current = current[:a] + current[b:]

current = current.replace(
    end,
    head_block + "\n\n" + end,
    1
)

p.write_text(current)

print("RESTORED INVOICE ENDPOINT FROM HEAD")
