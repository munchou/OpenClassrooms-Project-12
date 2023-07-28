from controllers.config import config, ini_update_database

from sqlalchemy_utils import create_database, database_exists

from views.views_start import StartProgramView
from views.views_create_load_db import LoadCreateDBView
from views.views_authentication import AuthenticationView
from views.views_user_creation import UserCreationView

from models import models
import random, sqlalchemy, hashlib, string, secrets
from getpass import getpass

from sqlalchemy import create_engine, exc, select

from sqlalchemy.orm import sessionmaker


class UserAuthentication:
    params = config()

    def server_connection(self):
        # params = config()

        try:
            engine = create_engine(
                f"postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.params['database']}"
            )
            # engine = create_engine(
            #     f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
            # )
            # engine.connect()
            return engine
        except Exception:
            AuthenticationView().authentication_error()

    def user_authentication(self):
        while True:
            username, password = AuthenticationView().input_user(
                self.params["database"]
            )

            if username == self.params["user"] and password == self.params["password"]:
                return "zupayuzaaa", None, None

            # If not superuser, then normal connection:
            engine = self.server_connection()
            Session = sessionmaker(bind=engine)
            session = Session()

            check_user = self.check_if_user_exists(session, username)
            if check_user == 0:
                AuthenticationView().user_auth_error()
                continue

            check_password = self.check_password(session, username, password)
            if check_password == 0:
                continue

            return self.check_user_status(session, username), engine, username

    def check_if_user_exists(self, session, username):
        all_users_list = session.query(models.Users.username).all()
        existing_usernames = []
        for t in all_users_list:
            # print(f"user in DB: '{t[0]}'")
            existing_usernames.append(t[0])
        print(existing_usernames)

        if username not in existing_usernames:
            return 0

        # print(f"Current user '{username}' is in the DB.")

    def retrieve_salties(self, session, username):
        user_saltychain = (
            session.query(models.Users.saltychain)
            .filter(models.Users.username == username)
            .first()
        )

        chains_list = str(user_saltychain[0][1:-1]).split(",")

        return chains_list

    def check_password(self, session, username, password):
        chains_list = self.retrieve_salties(session, username)
        salty_first = chains_list[0]
        salty_second = chains_list[1]
        salty_third = chains_list[2]

        salted_password = (
            f"{salty_first}{password[:4]}{salty_second}{password[4:]}{salty_third}"
        )
        # print(f"SALTED PASSWORD: {salted_password}")

        user_hashkey = (
            session.query(models.Users.password)
            .filter(models.Users.username == username)
            .first()
        )
        user_hashkey = user_hashkey[0][1:-1]
        # print(f"user_hashkey: {user_hashkey}")
        zupakey = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()
        # print(f"zupakey: {zupakey}")

        if user_hashkey == zupakey:
            return "hash ok"
        else:
            return 0

    def check_user_status(self, session, username):
        user_status = (
            session.query(models.Users.status)
            .filter(models.Users.username == username)
            .first()
        )

        if user_status[0] == 1:
            AuthenticationView().user_team_management(username)
            return 1
        if user_status[0] == 2:
            print(f"{username} is in the Sales Team")
            return 2
        if user_status[0] == 3:
            print(f"{username} is in the Support Team")
            return 3
        else:
            return 0

    def create_user_test(self, session):
        user_confirm = False
        while not user_confirm:
            username_input = UserCreationView().username_input()
            password_input = UserCreationView().password_input()
            password_hashed, saltychain = UserCreationView().password_encryption()
            # self.password_encryption(password_input)
            full_name_input = UserCreationView().fullname_input()
            email_input = UserCreationView().email_input(username_input)
            phone_number_input = UserCreationView().phonenumber_input()
            status_input = UserCreationView().status_input()

            print("\nPlease confirm the new user's details:")
            print(f"\tUsername: {username_input}")
            print(f"\tPassword: {password_input}")
            print(f"\tFull name: {full_name_input}")
            print(f"\temail: {email_input}")
            print(f"\tPhone number: {phone_number_input}")
            print(f"\tTeam: {status_input}")

            while True:
                confirm_input = input("\nConfirm? (y/n)").casefold()
                if confirm_input == "y":
                    user_confirm = True
                    break
                elif confirm_input != "n":
                    continue
                break
            continue

        # Let's try adding a user
        print("User creation")
        user = models.Users(
            username=username_input,
            password=password_hashed,
            full_name=full_name_input,
            email=email_input,
            phone_number=phone_number_input,
            status=status_input,
            saltychain=saltychain,
        )

        # user = models.Users(
        #     username="testoune2",
        #     password="zurzulute",
        #     full_name="Test Oune",
        #     email="",
        #     phone_number="080-3654-4454",
        #     status=3,
        # )

        session.add(user)
        session.commit()
        print(f"User {user.username} was successfully created.")
        print(f"saltychain: {saltychain}")

    def password_encryption(self, password):
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

        # hash the passwords
        zupakey = [hashlib.sha256(salted_password.encode("utf-8")).hexdigest()]
        # return f"{password}{zupakey}"
        return zupakey, salty_chain
