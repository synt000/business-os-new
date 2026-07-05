from fastapi import FastAPI

app = FastAPI(title="Business OS")

@app.get("/")
async def root():
    return {"message": "Hello Business OS! 🚀"}
