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
    return event