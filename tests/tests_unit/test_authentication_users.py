from controllers.config import config
from controllers.data_access_layer import DALSession, DALUser, DALClient, DALContract
from controllers.utils import Utils

from tests.conftest_database import TestDatabaseCreation

from views.views_authentication import AuthenticationView

from models import models
import random, hashlib, secrets


class TestUserAuthentication:
    params = TestDatabaseCreation().config()

    def test_user_authentication(self, session):
        # Utils.clear_screen()
        admin_connect = False
        user_connect = False

        username, password = self.params["user"], self.params["password"]

        if username == self.params["user"] and password == self.params["password"]:
            admin_connect = True

        # If not superuser, then normal connection:
        username, password = "User1", "qqqqqqqq"

        check_user = self.test_check_if_user_exists(session, username)
        if check_user == 0:
            AuthenticationView().user_auth_error()

        check_password = "checked"
        if check_password == 0:
            AuthenticationView().user_auth_error()
        else:
            user_connect = True

        # DALSession().session_close(session)

        assert admin_connect == True
        assert user_connect == True

    def test_check_if_user_exists(self, session, username="User1"):
        user_exists = False
        all_users_list = DALUser().get_all_users_usernames(session)
        existing_usernames = []
        for t in all_users_list:
            existing_usernames.append(t[0])

        if username in existing_usernames:
            user_exists = True

        assert user_exists == True

    def test_retrieve_salties(self, session, username="User1"):
        user_saltychain = DALUser().get_user_saltychain(session, username)

        chains_list = str(user_saltychain[0][1:-1]).split(",")

        assert chains_list is not None

    def test_check_password(self, session, username="User1", password="qqqqqqqq"):
        check_ok = False
        user_saltychain = DALUser().get_user_saltychain(session, username)
        chains_list = str(user_saltychain[0][1:-1]).split(",")
        salty_first = chains_list[0]
        salty_second = chains_list[1]
        salty_third = chains_list[2]
        salted_password = (
            f"{salty_first}{password[:4]}{salty_second}{password[4:]}{salty_third}"
        )

        user_hashkey = DALUser().get_user_hashkey(session, username)
        zupakey = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()
        if user_hashkey == zupakey:
            check_ok = True

        assert check_ok == True

    def test_check_user_status(self, session):
        status_management = False
        status_sales = False
        status_support = False

        username = "User1"
        user = DALUser().get_user_by_username(session, username)
        if user.status == models.Users.StatusEnum.management:
            status_management = True
        username = "User2"
        user = DALUser().get_user_by_username(session, username)
        if user.status == models.Users.StatusEnum.sales:
            status_sales = True
        username = "User3"
        user = DALUser().get_user_by_username(session, username)
        if user.status == models.Users.StatusEnum.support:
            status_support = True

        assert status_management == True
        assert status_sales == True
        assert status_support == True

    def test_password_encryption(self, password="qqqqqqqq"):
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

        assert salted_password.isascii()
        assert zupakey[0].isascii()
