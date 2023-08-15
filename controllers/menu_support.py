from controllers.utils import Utils
from controllers.crud_client import CrudClient
from controllers.crud_contract import CrudContract
from controllers.crud_event import CrudEvent

from views.views_menu_support import MenuSupportView


class MenuSupport:
    session = Utils().session_init()

    def menu_support(self, username):
        """Support Team Menu: controller where the menu
        is displayed, the input checked and the user redirected
        according to the input."""
        Utils().clear_screen()
        input_choice = MenuSupportView().menu_support(username)

        if input_choice == "1":
            CrudEvent().event_update(self.session, username)

        if input_choice == "2":
            CrudEvent().event_display_for_supportincharge(self.session, username)

        if input_choice == "3":
            CrudClient().client_display_all(self.session, username)

        if input_choice == "4":
            CrudContract().contract_display_all(self.session, username)

        if input_choice == "5":
            CrudEvent().event_display_all(self.session, username)

        if input_choice == "disconnect":
            Utils().disconnect_and_back_to_authentication(self.session)
