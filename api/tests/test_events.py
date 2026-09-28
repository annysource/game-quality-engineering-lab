from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class MockDocument:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data


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


@patch("app.main.db")
def test_reject_event_without_position(mock_db):
    event = {
        "event": "player_died",
        "level": "SampleScene"
    }

    response = client.post("/events", json=event)

    assert response.status_code == 422

    mock_db.collection.assert_not_called()


@patch("app.main.db")
def test_get_events(mock_db):
    mock_db.collection.return_value.stream.return_value = [
        MockDocument({
            "event": "player_died",
            "level": "SampleScene",
            "x": 18.4,
            "y": 2.1
        })
    ]

    response = client.get("/events")

    assert response.status_code == 200
    assert response.json() == [
        {
            "event": "player_died",
            "level": "SampleScene",
            "x": 18.4,
            "y": 2.1
        }
    ]

    mock_db.collection.assert_called_once_with("events")


@patch("app.main.db")
def test_get_deaths_filters_by_level(mock_db):
    mock_query = mock_db.collection.return_value.where.return_value
    mock_query.where.return_value.stream.return_value = [
        MockDocument({
            "event": "player_died",
            "level": "SampleScene",
            "x": 18.4,
            "y": 2.1
        })
    ]

    response = client.get("/deaths?level=SampleScene")

    assert response.status_code == 200

    deaths = response.json()

    assert len(deaths) == 1
    assert deaths[0]["event"] == "player_died"
    assert deaths[0]["level"] == "SampleScene"