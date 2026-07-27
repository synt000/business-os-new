from pathlib import Path

p = Path("src/telegram_bot/callbacks/registry.py")
s = p.read_text()

old = """    elif data == "customer":
        await customer_callback(update, context)
"""

new = """    elif data == "customer":
        await customer_callback(update, context)

    elif data == "customer_list":
        await customer_list_callback(update, context)

    elif data == "customer_add":
        await customer_add_callback(update, context)

    elif data == "customer_analysis":
        await customer_analysis_callback(update, context)
"""

if "customer_list_callback(update, context)" not in s:
    s = s.replace(old, new)


old2 = """    elif data == "supplier":
        await supplier_callback(update, context)
"""

new2 = """    elif data == "supplier":
        await supplier_callback(update, context)

    elif data == "supplier_list":
        await supplier_list_callback(update, context)

    elif data == "supplier_add":
        await supplier_add_callback(update, context)

    elif data == "supplier_analysis":
        await supplier_analysis_callback(update, context)
"""

if "supplier_list_callback(update, context)" not in s:
    s = s.replace(old2, new2)

p.write_text(s)
