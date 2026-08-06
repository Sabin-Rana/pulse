from fastapi import FastAPI
from app.check import check_url

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/check")
def check(url: str):
    return check_url(url)