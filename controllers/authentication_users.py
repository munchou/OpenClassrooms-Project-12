from controllers.config import config
from controllers.data_access_layer import DALSession, DALUser
from controllers.utils import Utils

from views.views_authentication import AuthenticationView

from models import models
import random, hashlib, secrets


class UserAuthentication:
    params = config()

    def user_authentication(self):
        """User authentication. The function checks the inputs,
        if the user exists and returns the status and the username."""
        Utils().clear_screen()
        while True:
            username, password = AuthenticationView().input_user(
                self.params["database"]
            )

            if username == self.params["user"] and password == self.params["password"]:
                return "zupayuzaaa", username

            # To  exit the program
            if username == "exit":
                return username, ""

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
        """Check if the user exists among the users present
        in the database."""
        all_users_list = DALUser().get_all_users_usernames(session)
        existing_usernames = []
        for t in all_users_list:
            existing_usernames.append(t[0])

        if username not in existing_usernames:
            return 0

    def retrieve_salties(self, session, username):
        """Get the user's salty chain chunks from the database."""
        user_saltychain = DALUser().get_user_saltychain(session, username)

        chains_list = str(user_saltychain[0][1:-1]).split(",")

        return chains_list

    def check_password(self, session, username, password):
        """Check the password entered while trying to log in.
        If it matches: proceed. If it doesn't: error and the user
        must type in their IDs again."""
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
        """Check the user's status and return a value
        used to display the menu accordingly."""
        user = DALUser().get_user_by_username(session, username)

        if user.status == models.Users.StatusEnum.management:
            return 1
        if user.status == models.Users.StatusEnum.sales:
            return 2
        if user.status == models.Users.StatusEnum.support:
            return 3
        if user.status == models.Users.StatusEnum.deactivated:
            return 4
        else:
            return 0

    def password_encryption(self, password):
        """Password salting and hashing."""
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
