from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@patch("app.main.db")
def test_create_player_died_event(mock_db):
    event = {
        "event": "player_died",
        "level": "SampleScene",
        "x": 18.4,
        "y": 2.1
    }

    response = client.post("/events", json=event)

    assert response.status_code == 201
    assert response.json() == event

    mock_db.collection.assert_called_once_with("events")
    mock_db.collection.return_value.add.assert_called_once_with(event)

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