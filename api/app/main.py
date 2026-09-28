from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(title="Game Telemetry API")


class GameplayEvent(BaseModel):
    event: str
    level: str
    x: float
    y: float


events: list[GameplayEvent] = []


@app.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: GameplayEvent):
    events.append(event)
    return event

@app.get("/events")
def get_events():
    return events

@app.get("/deaths")
def get_deaths(level: str):
    return [
        event
        for event in events
        if event.event == "player_died" and event.level == level
    ]