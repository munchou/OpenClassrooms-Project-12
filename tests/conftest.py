import pytest
import os
import os.path

import secrets, random, hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.conftest_database import TestDatabaseCreation

from tests.conftest_views import StartProgramView

from models import models


class IniFile:
    def check_if_exists(self):
        path = "tests/test_database.ini"
        check_file = os.path.isfile(path)
        if not check_file:
            self.create_ini()

    def create_ini(self):
        """Create the INI (= configuration) file based on
        the user input in the main folder of the program.
        Then goes to the load/creation of the DB."""

        StartProgramView().first_prompt()
        config_file = False
        while not config_file:
            config_host_input = StartProgramView().input_config_host()
            config_port_input = StartProgramView().input_config_port()
            while True:
                config_database_input = StartProgramView().input_config_database()
                if config_database_input == "postgres":
                    break
                if config_database_input.strip() == "":
                    StartProgramView().wrong_input()
                    continue
                else:
                    break
            config_user_input = StartProgramView().input_config_user()
            config_password_input = StartProgramView().input_config_password()

            StartProgramView().confirm_config_details(
                config_host_input,
                config_port_input,
                config_database_input,
                config_user_input,
                config_password_input,
            )

            while True:
                confirm_input = StartProgramView().confirm_input()
                if confirm_input == "y":
                    config_file = True
                    break
                elif confirm_input != "n":
                    continue
                break
            continue

        TestDatabaseCreation().create_ini(
            config_host_input,
            config_port_input,
            config_database_input,
            config_user_input,
            config_password_input,
        )

        TestDatabaseCreation().create_load_database()


@pytest.fixture(scope="session", autouse=True)
def connection():
    params = TestDatabaseCreation().config()
    engine = create_engine(
        f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
    )
    return engine


@pytest.fixture(scope="session", autouse=True)
def session(connection):
    models.Base.metadata.create_all(connection)
    Session = sessionmaker(bind=connection)
    add_users(Session())
    yield Session()
    Session().close()
    models.Base.metadata.drop_all(connection)


def password_encryption():
    password = "qqqqqqqq"
    """Password salting and hashing. Good luck to hackers..."""
    numbers = [4, 5, 6, 7, 8]
    salty_first = secrets.token_hex(random.choice(numbers))
    salty_second = secrets.token_hex(random.choice(numbers))
    salty_third = secrets.token_hex(random.choice(numbers))
    salty_chain = []
    salty_chain.extend((salty_first, salty_second, salty_third))
    salted_password = (
        f"{salty_first}{password[:4]}{salty_second}{password[4:]}{salty_third}"
    )

    zupakey = [hashlib.sha256(salted_password.encode("utf-8")).hexdigest()]
    return zupakey, salty_chain


def add_users(session):
    password, saltychain = password_encryption()
    test_user_one = models.Users(
        username="User1",
        password=password,
        full_name="User One",
        email="user1@testouille.com",
        phone_number="+819065504495",
        status="management",
        saltychain=saltychain,
    )

    password, saltychain = password_encryption()
    test_user_two = models.Users(
        username="User2",
        password=password,
        full_name="User Two",
        email="user2@testouille.com",
        phone_number="911",
        status="sales",
        saltychain=saltychain,
    )

    password, saltychain = password_encryption()
    test_user_three = models.Users(
        username="User3",
        password=password,
        full_name="User Three",
        email="user3@testouille.com",
        phone_number="+33780041253",
        status="support",
        saltychain=saltychain,
    )

    try:
        user_one_exists = (
            session.query(models.Users).filter_by(username="User1").first()
        )
        if not user_one_exists:
            session.add(test_user_one)
            session.commit()
    except Exception:
        pass

    try:
        user_two_exists = (
            session.query(models.Users).filter_by(username="User2").first()
        )
        if not user_two_exists:
            session.add(test_user_two)
            session.commit()
    except Exception:
        pass

    try:
        user_three_exists = (
            session.query(models.Users).filter_by(username="User3").first()
        )
        if not user_three_exists:
            session.add(test_user_three)
            session.commit()
    except Exception:
        pass
