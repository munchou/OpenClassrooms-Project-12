from configparser import ConfigParser

from sqlalchemy_utils import create_database

from views.views_create_load_db import LoadCreateDBView

import sqlalchemy

from sqlalchemy import create_engine, exc


class TestDatabaseCreation:
    def config(self, filename="tests/test_database.ini", section="postgresql"):
        parser = ConfigParser()
        parser.read(filename)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} was not found in the {filename}")

        return db

    def create_ini(
        self,
        config_host_input,
        config_port_input,
        config_database_input,
        config_user_input,
        config_password_input,
        filename="tests/test_database.ini",
    ):
        parser = ConfigParser()
        parser.add_section("postgresql")
        parser.set("postgresql", "host", config_host_input)
        parser.set("postgresql", "port", config_port_input)
        parser.set("postgresql", "database", config_database_input)
        parser.set("postgresql", "user", config_user_input)
        parser.set("postgresql", "password", config_password_input)

        with open(filename, "w") as configfile:
            parser.write(configfile)

    def ini_update_database(self, new_database, filename="tests/test_database.ini"):
        parser = ConfigParser()
        parser.read(filename)
        parser.set("postgresql", "database", new_database)

        with open(filename, "w") as configfile:
            parser.write(configfile)

    def create_load_database(self):
        """Connects to the default PostgreSQL or another database
        in order to create the test database."""
        params = self.config()

        try:
            engine = create_engine(
                f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{'postgres'}"
            )
            conn = engine.connect()
            conn.execute(sqlalchemy.text("COMMIT"))

        except Exception:
            LoadCreateDBView().create_db_error()

        try:
            database_to_create = "test_database"
            db_url = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{database_to_create}"
            create_database(db_url)

            LoadCreateDBView().database_created(database_to_create)
            self.ini_update_database(database_to_create)
            LoadCreateDBView().config_file_updated()

        except exc.ProgrammingError:
            self.ini_update_database(database_to_create)
            LoadCreateDBView().database_already_exists()

        engine = create_engine(
            f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{database_to_create}"
        )
        LoadCreateDBView().connected_to_database(database_to_create)

        conn.close()
