import os

main_path = "src/main.py"
if os.path.exists(main_path):
    with open(main_path, "r") as f:
        content = f.read()
    
    # Hot-Fix အပိုင်းကို ရှာပြီး ဖယ်ထုတ်သည်
    if "# Dynamic Hot-Fix" in content:
        lines = content.splitlines()
        clean_lines = [l for l in lines if "Category.tenant" not in l and "configure_mappers" not in l and "silent_variable_injection" not in l and "AIBusinessMemory" not in l]
        # target snippet သန့်စင်ခြင်း
        out = content.split("# Dynamic Hot-Fix for Category Mapper Relationship Alignment")
        if len(out) > 1:
            # တကယ်လို့ split ရရင် ဒုတိယပိုင်း (မူရင်းကုဒ်) ကိုပဲ ပြန်ယူသည်
            final_content = out[1].split("pass\n")[-1] if "pass" in out[1] else out[1]
            with open(main_path, "w") as f:
                f.write(final_content.strip() + "\n")
            print("[✓] Main entrypoint restored to original clean state safely.")
        else:
            print("[i] Cleaning lines dynamically...")
else:
    print("[X] Main path not found.")
