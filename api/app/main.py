from app.firebase import db
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(title="Game Telemetry API")


class GameplayEvent(BaseModel):
    event: str
    level: str
    x: float
    y: float




@app.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: GameplayEvent):
    db.collection("events").add(event.model_dump())

    return event

@app.get("/events")
def get_events():
    docs = db.collection("events").stream()

    events = []

    for doc in docs:
        events.append(doc.to_dict())

    return events

@app.get("/deaths")
def get_deaths(level: str):
    docs = (
        db.collection("events")
        .where("event", "==", "player_died")
        .where("level", "==", level)
        .stream()
    )

    return [doc.to_dict() for doc in docs]