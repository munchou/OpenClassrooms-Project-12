from controllers.utils import Utils
from controllers.authentication_users import UserAuthentication
from controllers.crud_user import CrudUser

from views.views_crud_user import CrudUserView
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
