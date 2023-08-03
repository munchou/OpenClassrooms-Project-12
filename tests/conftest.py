import pytest
from datetime import datetime, timedelta


@pytest.fixture(scope="function", autouse=True)
def clubs(monkeypatch):
    mock_clubs = [
        {"name": "Club 101", "email": "club101@gmail.com", "points": "13"},
        {"name": "Club 102", "email": "club102@gmail.com", "points": "4"},
        {"name": "Club 103", "email": "club103@gmail.com", "points": "30"},
    ]
    monkeypatch.setattr("server.clubs", mock_clubs)


@pytest.fixture(scope="function", autouse=True)
def competitions(monkeypatch):
    future_date = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    past_date = (datetime.now() + timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S")

    mock_competitions = [
        {"name": "Competition 101", "date": future_date, "numberOfPlaces": "132"},
        {"name": "Competition 102", "date": past_date, "numberOfPlaces": "10"},
    ]
    monkeypatch.setattr("server.competitions", mock_competitions)


@pytest.fixture(scope="function", autouse=True)
def booked_seats(monkeypatch):
    mock_booked_seats = [
        {
            "club": "Club 101",
            "competition": "Competition 101",
            "booked_seats": 0,
        },
    ]
    monkeypatch.setattr("server.all_booked_seats", mock_booked_seats)
