from controllers.utils import Utils
from controllers.crud_client import CrudClient
from controllers.crud_contract import CrudContract
from controllers.crud_event import CrudEvent

from views.views_menu_sales import MenuSalesView


class MenuSales:
    session = Utils().session_init()

    def menu_sales(self, username):
        """Check if the INI (= configuration) file exists.
        If not, create the INI file based on the user input
        in the main folder of the program. Then goes to the
        load/creation of the DB.
        If the INI file already exists, skip its creation
        and directly goes to the next step."""
        Utils().clear_screen()
        input_choice = MenuSalesView().menu_sales(username)

        if input_choice == "1":
            CrudClient().client_create(self.session, username)

        if input_choice == "2":
            CrudClient().client_update(self.session, username)

        if input_choice == "3":
            CrudContract().contract_update(self.session, username)

        if input_choice == "4":
            CrudContract().contract_display_not_signed(self.session, username)

        if input_choice == "5":
            CrudContract().contract_display_not_paid(self.session, username)

        if input_choice == "6":
            CrudEvent().event_create(self.session, username)

        if input_choice == "7":
            CrudClient().client_display_all(self.session, username)

        if input_choice == "8":
            CrudContract().contract_display_all(self.session, username)

        if input_choice == "9":
            CrudEvent().event_display_all(self.session, username)

        if input_choice == "disconnect":
            Utils().disconnect_and_back_to_authentication(self.session)
