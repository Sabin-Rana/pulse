from fastapi import FastAPI
from app.check import check_url
from datetime import datetime
import json

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
        result["time"] = now.strftime("%Y-%m-%d %H:%M:%S")
        with open("app/history.txt", "a") as f:
            f.write(json.dumps(result) + "\n") 
        results.append(result)
    return results

@app.get("/history")
def history():
    with open("app/history.txt") as f:
        lines = f.read().splitlines()
    results = []
    for line in lines:
        result = json.loads(line)
        results.append(result)
    return results