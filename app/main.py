from fastapi import FastAPI
from app.check import check_url
from datetime import datetime

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/check")
def check(url: str):
    return check_url(url)

@app.get("/checkall")
def check_all():
    with open("app/sites.txt") as f:
        sites = f.read().splitlines()
    results = []
    for url in sites:
        result = check_url(url)
        now = datetime.now()
        with open("app/history.txt", "a") as f:
            f.write(now.strftime("%Y-%m-%d %H:%M:%S") + " " + str(result) + "\n")
        results.append(result)
    return results