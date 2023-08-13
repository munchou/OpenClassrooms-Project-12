from controllers.config import config, ini_update_database

from sqlalchemy_utils import create_database

from views.views_start import StartProgramView
from views.views_create_load_db import LoadCreateDBView
from views.views_authentication import AuthenticationView

from models import models

import sqlalchemy

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, exc


class DatabaseCreation:
    def session_init(self):
        params = config()
        try:
            engine = create_engine(
                f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
            )
            return engine
        except Exception:
            AuthenticationView().authentication_error()

        Session = sessionmaker(bind=engine)
        return Session()

    def special_authentication(self):
        while True:
            host_input = AuthenticationView().input_config_host()
            port_input = AuthenticationView().input_config_port()
            database_input = AuthenticationView().input_config_database()
            user_input = AuthenticationView().input_config_user()
            password_input = AuthenticationView().input_config_password()

            try:
                engine = create_engine(
                    f"postgresql://{user_input}:{password_input}@{host_input}:{port_input}/{database_input}"
                )
                engine.connect()
                break
            except Exception:
                AuthenticationView().authentication_error()
                continue

        self.create_load_database()

    def create_load_database(self):
        """Connects to the default PostgreSQL or another database
        in order to either load or create a database."""
        params = config()
        current_database = params["database"]

        try:
            engine = create_engine(
                f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{'postgres'}"
            )
            conn = engine.connect()
            conn.execute(sqlalchemy.text("COMMIT"))

        except Exception:
            LoadCreateDBView().create_db_error()

        while True:
            if current_database == "postgres":
                StartProgramView().currentdb_is_postgres()

            database_to_create = LoadCreateDBView().load_or_create_database_name(
                current_database
            )

            if database_to_create.strip() == "" or database_to_create == "postgres":
                LoadCreateDBView().wrong_input()
                continue
            else:
                break

        try:
            db_url = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{database_to_create}"
            create_database(db_url)

            LoadCreateDBView().database_created(database_to_create)
            ini_update_database(database_to_create)
            LoadCreateDBView().config_file_updated()

        except exc.ProgrammingError:
            ini_update_database(database_to_create)
            LoadCreateDBView().database_already_exists()

        engine = create_engine(
            f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{database_to_create}"
        )
        LoadCreateDBView().connected_to_database(database_to_create)

        self.check_tables_exist(engine)

        conn.close()

    def check_tables_exist(self, engine):
        """Create the needed tables if they are not in the database."""
        # conn = engine.connect()

        insp = sqlalchemy.inspect(engine)
        if (
            insp.has_table("users", schema="public")
            and insp.has_table("client", schema="public")
            and insp.has_table("contract", schema="public")
            and insp.has_table("event", schema="public")
        ):
            print("ALL REQUIRED TABLES ARE PRESENT, SKIPPING THEIR CREATION PROCESS.")

        else:
            print("REQUIRED TABLES NOT FOUND, CREATING THEM.")
            self.tables_creation(engine)

    def tables_creation(self, engine):
        Base = models.Base
        Base.metadata.create_all(bind=engine)

    def tables_delete(self, username):
        from controllers.menu_admin import MenuAdmin

        params = config()
        current_database = params["database"]

        confirm_delete = StartProgramView().tables_delete_confirm(current_database)

        if confirm_delete == "delete":
            try:
                engine = create_engine(
                    f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{current_database}"
                )
                conn = engine.connect()
                conn.execute(sqlalchemy.text("COMMIT"))

            except Exception:
                LoadCreateDBView().create_db_error()

            Base = models.Base
            Base.metadata.drop_all(engine)
            print("Tables successfully deleted")

        MenuAdmin().menu_admin(username)
