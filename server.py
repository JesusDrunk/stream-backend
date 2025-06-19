
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()
users = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class TwitchUrl(BaseModel):
    url: str

@app.get("/api/streamer/{user_id}")
def get_streamer(user_id: str):
    user = users.setdefault(user_id, {"role": "streamer", "balance": 0, "twitch": ""})
    return {"balance": user["balance"], "twitch": user["twitch"]}

@app.post("/api/streamer/{user_id}/topup")
def topup(user_id: str):
    user = users.setdefault(user_id, {"role": "streamer", "balance": 0, "twitch": ""})
    user["balance"] += 10
    return {"balance": user["balance"]}

@app.post("/api/streamer/{user_id}/twitch")
def set_twitch(user_id: str, body: TwitchUrl):
    user = users.setdefault(user_id, {"role": "streamer", "balance": 0, "twitch": ""})
    user["twitch"] = body.url
    return {"status": "ok"}

@app.get("/api/viewer/{user_id}")
def get_viewer(user_id: str):
    user = users.setdefault(user_id, {"role": "viewer", "coins": 0})
    return {"coins": user["coins"]}

@app.post("/api/viewer/{user_id}/watch")
def watch(user_id: str):
    user = users.setdefault(user_id, {"role": "viewer", "coins": 0})
    user["coins"] += 1
    return {"coins": user["coins"]}

@app.get("/api/viewer/random-stream")
def random_stream():
    streamers = [v for v in users.values() if v["role"] == "streamer" and v.get("twitch")]
    if not streamers:
        return {"url": ""}
    return {"url": random.choice(streamers)["twitch"]}
