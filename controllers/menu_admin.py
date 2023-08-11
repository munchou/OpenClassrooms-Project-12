from controllers.utils import Utils
from controllers.crud_user import CrudUser
from controllers.crud_client import CrudClient
from controllers.crud_contract import CrudContract
from controllers.crud_event import CrudEvent


from views.views_authentication import AuthenticationView


class MenuAdmin:
    session = Utils().session_init()

    def menu_admin(self, username):
        admin_menu_choice = AuthenticationView().admin_menu()

        if admin_menu_choice == "db_update":
            from controllers.database_load_creation import DatabaseCreation

            DatabaseCreation().create_load_database()

        if admin_menu_choice == "db_removetables":
            from controllers.database_load_creation import DatabaseCreation

            DatabaseCreation().tables_delete(username)

        if admin_menu_choice == "1":
            CrudUser().user_create(self.session, username)

        if admin_menu_choice == "2":
            CrudUser().user_update(self.session, username)

        if admin_menu_choice == "3":
            CrudUser().user_delete(self.session, username)

        if admin_menu_choice == "4":
            CrudClient().client_create(self.session, username)

        # if admin_menu_choice == "5":
        #     CrudClient().client_update(self.session, username)

        if admin_menu_choice == "6":
            CrudClient().client_display_all(self.session, username)

        if admin_menu_choice == "7":
            CrudContract().contract_create(self.session, username)

        # if admin_menu_choice == "8":
        #     CrudContract().contract_update(self.session, username)

        if admin_menu_choice == "9":
            CrudContract().contract_display_all(self.session, username)

        if admin_menu_choice == "10":
            CrudContract().contract_display_not_signed(self.session, username)

        if admin_menu_choice == "11":
            CrudContract().contract_display_not_paid(self.session, username)

        if admin_menu_choice == "12":
            CrudEvent().event_create(self.session, username)

        if admin_menu_choice == "13":
            CrudEvent().event_display_no_support(self.session, username)

        if admin_menu_choice == "14":
            CrudEvent().event_update_add_support(self.session, username)

        if admin_menu_choice == "15":
            CrudEvent().event_update(self.session, username)

        if admin_menu_choice == "16":
            CrudEvent().event_display_for_supportincharge(self.session, username)

        if admin_menu_choice == "17":
            CrudEvent().event_display_all(self.session, username)

        if admin_menu_choice == "disconnect":
            Utils().disconnect_and_back_to_authentication(self.session)
