from controllers.utils import Utils
from controllers.authentication_users import UserAuthentication
from controllers.crud_user import CrudUser
from controllers.crud_client import CrudClient
from controllers.crud_contract import CrudContract

from views.views_menu_management import MenuManagementView

from models import models


class MenuManagement:
    session = Utils().session_init()

    def menu_management(self, username):
        """Check if the INI (= configuration) file exists.
        If not, create the INI file based on the user input
        in the main folder of the program. Then goes to the
        load/creation of the DB.
        If the INI file already exists, skip its creation
        and directly goes to the next step."""
        management_choice = MenuManagementView().menu_management(username)

        if management_choice == "1":
            CrudUser().user_create(self.session)

        if management_choice == "2":
            CrudUser().user_update(self.session)

        if management_choice == "3":
            CrudUser().user_delete(self.session)

        if management_choice == "4":
            CrudClient().client_create(self.session, username)
        #     CrudContract().contract_create(self.session)

        if management_choice == "5":
            CrudClient().client_update(self.session)
        #     CrudContract().contract_update(self.session)

        if management_choice == "6":
            CrudContract().contract_create(self.session)
        #     CrdSupport().display_events_without_support(self.session)

        if management_choice == "7":
            CrudClient().client_update(self.session)
        #     CrudSupport().assign_support_to_event(self.session)

        if management_choice == "8":
            self.session.close()
            from main import main  # To avoid the idiotic circular import error...

            main()
