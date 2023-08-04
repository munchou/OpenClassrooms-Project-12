import pytest

import os
import hashlib
import enum

from sqlalchemy import (
    Column,
    Enum,
    Integer,
    Float,
    String,
    Text,
    Boolean,
    DateTime,
    CheckConstraint,
    ForeignKey,
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from controllers.data_access_layer import DALSession, DALUser
from controllers.config import config

from views.views_crud_inputs import CrudInputsView
from views.views_authentication import AuthenticationView

from models import models

Base = declarative_base()


@pytest.fixture(scope="session")
def server_connection():
    # params = config()
    # engine = create_engine(
    #             f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
    #         )
    engine = create_engine(
        "postgresql://test_db_user:test_db_password@test_db_host:test_db_port]/test_db_database"
    )
    return engine


@pytest.fixture(scope="session")
def session_init():
    engine = server_connection()
    Session = sessionmaker(bind=engine)
    return Session()


@pytest.fixture(scope="session")
def setup_database(connection):
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()

    seed_database()

    yield

    models.Base.metadata.drop_all()


def seed_database():
    users = [
        {
            "id": 1,
            "name": "John Doe",
        },
        # ...
    ]

    for user in users:
        db_user = User(**user)
        db_session.add(db_user)
    db_session.commit()


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
