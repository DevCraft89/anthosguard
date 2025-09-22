from fastapi import FastAPI
from google.cloud import pubsub_v1
from collections import deque
from fastapi.responses import HTMLResponse
import json, os, threading, time

PROJECT_ID = os.environ["PROJECT_ID"]
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", "fraud-detector")

app = FastAPI()
subscriber = pubsub_v1.SubscriberClient()
sub_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

# state
last_seen = {}
_history = deque(maxlen=50)
_counters = {"LOW": 0, "MED": 0, "HIGH": 0}


def score(payload):
    uid = payload.get("user_id", "")
    if uid.isdigit():
        val = int(uid) % 100
    else:
        val = sum(ord(c) for c in uid) % 100
    level = "LOW" if val < 30 else "MED" if val < 60 else "HIGH"
    return {"score": val, "level": level}


def cb(message):
    event = json.loads(message.data.decode("utf-8"))
    result = score(event["payload"])
    print(f"[fraud-detector] {event['payload'].get('user_id')} -> {result}")

    _history.append({
        "user_id": event["payload"].get("user_id"),
        "email": event["payload"].get("email"),
        "country": event["payload"].get("country"),
        "result": result
    })
    _counters[result["level"]] = _counters.get(result["level"], 0) + 1
    last_seen.update({"event": event, "result": result, "ready": True})
    message.ack()


def run_sub():
    future = subscriber.subscribe(sub_path, cb)
    try:
        future.result()
    except Exception as e:
        print(f"Subscription error: {e}")


threading.Thread(target=run_sub, daemon=True).start()


@app.get("/healthz")
def health():
    return {"ok": True, "ready": last_seen.get("ready", False)}


@app.get("/status")
def status():
    return {
        "ok": True,
        "ready": last_seen.get("ready", False),
        "totals": _counters,
        "recent": list(_history),
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    rows = "".join(
        f"<tr><td>{i+1}</td><td>{e.get('user_id','')}</td><td>{e.get('email','')}</td>"
        f"<td>{e.get('country','')}</td><td>{e['result']['level']}</td><td>{e['result']['score']}</td></tr>"
        for i, e in enumerate(reversed(_history))
    )
    html = f"""
    <html><head><title>Fraud Detector Dashboard</title></head>
    <body>
    <h1>Recent Events</h1>
    <table border="1">
      <thead><tr><th>#</th><th>User ID</th><th>Email</th><th>Country</th><th>Level</th><th>Score</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p>Totals: {_counters}</p>
    </body></html>
    """
    return HTMLResponse(content=html, status_code=200)