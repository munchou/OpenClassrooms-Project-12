import os
import hashlib

from controllers.data_access_layer import DALSession, DALUser
from controllers.config import config

from views.views_crud_inputs import CrudInputsView
from views.views_authentication import AuthenticationView
from views.views_crud_messages import CrudGeneralMessagesView

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Utils:
    params = config()

    def server_connection(self):
        try:
            engine = create_engine(
                f"postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.params['database']}"
            )
            return engine
        except Exception:
            AuthenticationView().authentication_error()

    def session_init(self):
        engine = self.server_connection()
        Session = sessionmaker(bind=engine)
        return Session()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def retrieve_salties(self, session, username):
        user_saltychain = DALUser().get_user_saltychain(session, username)
        chains_list = str(user_saltychain[0][1:-1]).split(",")

        return chains_list

    def user_status_request_pwd(self, session, username):
        from controllers.authentication_users import UserAuthentication

        try:
            user_status = UserAuthentication().check_user_status(session, username)
            if user_status:
                self.clear_screen
                self.check_password_input(session, username)
        except AttributeError:
            pass

    def check_password(self, session, username, password):
        chains_list = self.retrieve_salties(session, username)
        salty_first = chains_list[0]
        salty_second = chains_list[1]
        salty_third = chains_list[2]

        salted_password = (
            f"{salty_first}{password[:4]}{salty_second}{password[4:]}{salty_third}"
        )

        user_hashkey = DALUser().get_user_hashkey(session, username)
        zupakey = hashlib.sha256(salted_password.encode("utf-8")).hexdigest()

        if user_hashkey == zupakey:
            return "hash ok"
        else:
            return 0

    def check_password_input(self, session, username):
        Utils().clear_screen()
        password = CrudInputsView().crud_password_check_input()
        check_password = self.check_password(session, username, password)
        if check_password == 0:
            self.wrong_password_so_disconnect(session)

    def wrong_password_so_disconnect(self, session):
        DALSession().session_close(session)
        AuthenticationView().crud_password_check_wrong()
        from main import main

        main()

    def disconnect_and_back_to_authentication(self, session):
        DALSession().session_close(session)
        from main import main

        main()

    def back_to_menu(self, session, username):
        CrudGeneralMessagesView().press_enter_to_menu()
        from controllers.authentication_users import UserAuthentication

        try:
            user_status = UserAuthentication().check_user_status(session, username)
            if user_status == 1:
                from controllers.menu_management import MenuManagement

                MenuManagement().menu_management(username)
            if user_status == 2:
                from controllers.menu_sales import MenuSales

                MenuSales().menu_sales(username)
            if user_status == 3:
                from controllers.menu_support import MenuSupport

                MenuSupport().menu_support(username)
        except AttributeError:
            pass
        from controllers.menu_admin import MenuAdmin

        MenuAdmin().menu_admin(username)
