import pytest
from fastapi.testclient import TestClient
from app.main import app, events


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_events():
    events.clear()

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

def test_get_events_returns_recorded_death():
    event = {
        "event": "player_died",
        "level": "SampleScene",
        "x": 18.4,
        "y": 2.1
    }

    client.post("/events", json=event)

    response = client.get("/events")

    assert response.status_code == 200

    events = response.json()

    assert len(events) > 0
    assert events[-1]["event"] == "player_died"
    assert events[-1]["level"] == "SampleScene"

def test_get_deaths_filters_by_level():
    client.post("/events", json={
        "event": "player_died",
        "level": "SampleScene",
        "x": 18.4,
        "y": 2.1
    })

    client.post("/events", json={
        "event": "player_died",
        "level": "OtherLevel",
        "x": 30.0,
        "y": 4.0
    })

    response = client.get("/deaths?level=SampleScene")

    assert response.status_code == 200

    deaths = response.json()

    assert len(deaths) > 0
    assert all(death["event"] == "player_died" for death in deaths)
    assert all(death["level"] == "SampleScene" for death in deaths)