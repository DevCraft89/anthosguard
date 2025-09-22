from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from google.cloud import pubsub_v1
import json, os, time

PROJECT_ID = os.environ["PROJECT_ID"]
TOPIC_ID = os.environ.get("TOPIC_ID", "account-created")

app = FastAPI()
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


class AccountCreate(BaseModel):
    user_id: str
    email: EmailStr
    country: str


@app.get("/healthz")
def health():
    return {"ok": True, "topic": TOPIC_ID}


@app.post("/accounts")
def create_account(body: AccountCreate):
    event = {
        "event_type": "account_created",
        "version": "1.0",
        "timestamp": int(time.time()),
        "payload": body.dict(),
    }
    try:
        publisher.publish(topic_path, data=json.dumps(event).encode("utf-8")).result(10)
        return {"status": "ok", "event": event}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))