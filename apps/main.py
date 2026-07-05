from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="apps/templates"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("apps/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/start")
async def start_os(os_name: str = Form(...)):
    return {"message": f"Welcome to {os_name}, တောဘုရင်ရဲ့ နယ်မြေက မင်းကို ကြိုဆိုပါတယ်!"}
