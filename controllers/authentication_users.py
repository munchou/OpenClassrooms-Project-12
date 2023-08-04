from controllers.config import config
from controllers.data_access_layer import DALSession, DALUser, DALClient, DALContract
from controllers.utils import Utils

from views.views_authentication import AuthenticationView

from models import models
import random, hashlib, secrets


class UserAuthentication:
    params = config()

    # def server_connection(self):
    #     # params = config()

    #     try:
    #         engine = create_engine(
    #             f"postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.params['database']}"
    #         )
    #         # engine.connect()
    #         return engine
    #     except Exception:
    #         AuthenticationView().authentication_error()

    def user_authentication(self):
        Utils.clear_screen()
        while True:
            username, password = AuthenticationView().input_user(
                self.params["database"]
            )

            if username == self.params["user"] and password == self.params["password"]:
                return "zupayuzaaa", username

            # If not superuser, then normal connection:
            session = Utils().session_init()

            check_user = self.check_if_user_exists(session, username)
            if check_user == 0:
                AuthenticationView().user_auth_error()
                continue

            check_password = self.check_password(session, username, password)
            if check_password == 0:
                AuthenticationView().user_auth_error()
                continue

            DALSession().session_close(session)
            return self.check_user_status(session, username), username

    def check_if_user_exists(self, session, username):
        all_users_list = DALUser().get_all_users_usernames(session)
        existing_usernames = []
        for t in all_users_list:
            existing_usernames.append(t[0])

        if username not in existing_usernames:
            return 0

    def retrieve_salties(self, session, username):
        user_saltychain = DALUser().get_user_saltychain(session, username)

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

        user_hashkey = DALUser().get_user_hashkey(session, username)
        # print(f"user_hashkey: {user_hashkey}")
        zupakey = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()
        # print(f"zupakey: {zupakey}")

        if user_hashkey == zupakey:
            return "hash ok"
        else:
            return 0

    def check_user_status(self, session, username):
        user = DALUser().get_user_by_username(session, username)

        if user.status == models.Users.StatusEnum.management:
            AuthenticationView().user_team_management(username)
            return 1
        if user.status == models.Users.StatusEnum.sales:
            print(f"{username} is in the Sales Team")
            return 2
        if user.status == models.Users.StatusEnum.support:
            print(f"{username} is in the Support Team")
            return 3
        else:
            return 0

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
