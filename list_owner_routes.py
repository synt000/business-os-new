from src.main import app

for r in app.routes:
    print(
        getattr(r,"path",None),
        getattr(r,"methods",None)
    )
