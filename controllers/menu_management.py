from controllers.utils import Utils
from controllers.crud_user import CrudUser
from controllers.crud_client import CrudClient
from controllers.crud_contract import CrudContract
from controllers.crud_event import CrudEvent

from views.views_menu_management import MenuManagementView


class MenuManagement:
    session = Utils().session_init()

    def menu_management(self, username):
        """Management Team Menu: controller where the menu
        is displayed, the input checked and the user redirected
        according to the input."""
        Utils().clear_screen()
        input_choice = MenuManagementView().menu_management(username)

        if input_choice == "1":
            CrudUser().user_create(self.session, username)

        if input_choice == "2":
            CrudUser().user_update(self.session, username)

        if input_choice == "3":
            CrudUser().user_delete(self.session, username)

        if input_choice == "4":
            CrudContract().contract_create(self.session, username)

        if input_choice == "5":
            CrudContract().contract_update(self.session, username)

        if input_choice == "6":
            CrudEvent().event_display_no_support(self.session, username)

        if input_choice == "7":
            CrudEvent().event_update_add_support(self.session, username)

        if input_choice == "8":
            CrudClient().client_display_all(self.session, username)

        if input_choice == "9":
            CrudContract().contract_display_all(self.session, username)

        if input_choice == "10":
            CrudEvent().event_display_all(self.session, username)

        if input_choice == "disconnect":
            Utils().disconnect_and_back_to_authentication(self.session)
