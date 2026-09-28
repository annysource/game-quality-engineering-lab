from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_player_died_event():
    event = {
        "event": "player_died",
        "level": "SampleScene",
        "x": 18.4,
        "y": 2.1
    }

    response = client.post("/events", json=event)

    assert response.status_code == 201
    assert response.json()["event"] == "player_died"
    assert response.json()["level"] == "SampleScene"
    assert response.json()["x"] == 18.4
    assert response.json()["y"] == 2.1

def test_reject_event_without_position():
    event = {
        "event": "player_died",
        "level": "SampleScene"
    }

    response = client.post("/events", json=event)

    assert response.status_code == 422