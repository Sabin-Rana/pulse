from fastapi import FastAPI
from app.check import check_url
from datetime import datetime
import json
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/check")
def check(url: str):
    return check_url(url)

def run_checks():
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

@app.get("/checkall")
def check_all():
    return run_checks()

@app.get("/history", response_class=HTMLResponse)
def history():
    try:
        with open("app/history.txt") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        lines = []    
    html = "<style>body { font-family: Arial, sans-serif; padding: 20px; } table { border-collapse: collapse; } td { border: 1px solid #ccc; padding: 8px; } th { border: 1px solid #ccc; padding: 8px; background: #f0f0f0; }</style>"
    html = html + "<h1>Pulse History</h1>"
    html = html + "<table>"
    html = html + "<tr><th>URL</th><th>OK</th><th>Status</th><th>Time</th></tr>"
    
    for line in lines:
        result = json.loads(line)
        if result["ok"] == True:
            color = "#d4f7d4"
        else:
            color = "#f7d4d4"
        html = html + "<tr style='background:" + color + "'>"
        html = html + "<td>" + str(result["url"]) + "</td>"
        html = html + "<td>" + str(result["ok"]) + "</td>"
        html = html + "<td>" + str(result["status_code"]) + "</td>"
        html = html + "<td>" + str(result["time"]) + "</td>"
        html = html + "</tr>"
    
    html = html + "</table>"
    return html

scheduler = BackgroundScheduler()
scheduler.add_job(run_checks, "interval", seconds=60)
scheduler.start()