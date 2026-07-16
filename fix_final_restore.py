import os

main_path = "src/main.py"
if os.path.exists(main_path):
    with open(main_path, "r") as f:
        lines = f.readlines()
    
    # ImportError ဖြစ်စေသော စာသားများပါဝင်သည့် Line များကို ဖယ်ထုတ်ပြီး မူရင်းအတိုင်း သန့်စင်သည်
    clean_lines = [l for l in lines if "Dynamic Hot-Fix" not in l and "Category.tenant" not in l and "configure_mappers" not in l and "from src.models.saas_core import Category" not in l]
    
    with open(main_path, "w") as f:
        f.writelines(clean_lines)
    print("[✓] src/main.py has been perfectly restored to original clean state.")
