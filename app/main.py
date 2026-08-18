from fastapi import FastAPI
from app.check import check_url
from datetime import datetime
import json
from fastapi.responses import HTMLResponse

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

@app.get("/history", response_class=HTMLResponse)
def history():
    with open("app/history.txt") as f:
        lines = f.read().splitlines()
    
    html = "<h1>Pulse History</h1>"
    html = html + "<table border='1'>"
    html = html + "<tr><td>URL</td><td>OK</td><td>Status</td><td>Time</td></tr>"
    
    for line in lines:
        result = json.loads(line)
        html = html + "<tr>"
        html = html + "<td>" + str(result["url"]) + "</td>"
        html = html + "<td>" + str(result["ok"]) + "</td>"
        html = html + "<td>" + str(result["status_code"]) + "</td>"
        html = html + "<td>" + str(result["time"]) + "</td>"
        html = html + "</tr>"
    
    html = html + "</table>"
    return html