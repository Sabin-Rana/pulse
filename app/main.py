from fastapi import FastAPI
from app.check import check_url

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/check")
def check(url: str):
    return check_url(url)

@app.get("/checkall")
def check_all():
    sites = ["https://www.google.com", "https://www.facebook.com", "https://broken.sabinrana.xyz"]
    results = []
    for url in sites:
        results.append(check_url(url))
    return results