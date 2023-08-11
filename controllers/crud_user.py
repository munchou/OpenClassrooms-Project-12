from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudUserMessagesView

from controllers.utils import Utils
from controllers.data_access_layer import DALSession, DALUser
from controllers.check_object_exists import CheckObjectExists

from models import models

import sqlalchemy


class CrudUser:
    # def back_to_menu(self, session, username):
    #     from controllers.authentication_users import UserAuthentication

    #     try:
    #         user_status = UserAuthentication().check_user_status(session, username)
    #         if user_status == 1:
    #             from controllers.menu_management import MenuManagement

    #             MenuManagement().menu_management(username)
    #         if user_status == 2:
    #             from controllers.menu_sales import MenuSales

    #             MenuSales().menu_sales(username)
    #         if user_status == 3:
    #             from controllers.menu_support import MenuSupport

    #             MenuSupport().menu_support(username)
    #     except AttributeError:
    #         pass
    #     from controllers.menu_admin import MenuAdmin

    #     MenuAdmin().menu_admin(username)

    def user_create(self, session, username):
        """Create a user after filling the necessary fields.
        If needed, each input will check that the entered
        information is valid and can be processed."""
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        CrudUserMessagesView().creation_title()
        while True:
            username_input = CrudInputsView().username_input(session)
            password, saltychain = CrudInputsView().password_encryption()
            full_name_input = CrudInputsView().fullname_input()
            email_input = CrudInputsView().email_input(session)
            phone_number_input = CrudInputsView().phonenumber_input()
            status_input = CrudInputsView().status_input()

            CrudUserMessagesView().user_confirmation(
                username_input,
                full_name_input,
                email_input,
                phone_number_input,
                status_input,
            )

            confirm_input = CrudInputsView().confirm_creation()
            if confirm_input:
                break
            continue

        user = models.Users(
            username=username_input,
            password=password,
            full_name=full_name_input,
            email=email_input,
            phone_number=phone_number_input,
            status=status_input,
            saltychain=saltychain,
        )

        DALSession().session_add_and_commit(session, user)
        CrudUserMessagesView().creation_successful(user)
        # self.back_to_menu(session, username)
        Utils().back_to_menu(session, username)

    def user_update(self, session, username):
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        while True:
            user_id_input = CrudInputsView().update_user_id_input()
            user_update = CheckObjectExists().check_userID_exists_update_delete(
                session, user_id_input
            )
            if user_update in DALUser().get_all_users(session):
                confirm_choice = CrudInputsView().confirm_user_update_choice(
                    user_update
                )
                if confirm_choice == "y":
                    break
                continue
            continue

        field, value, chain = self.user_update_fieldandvalue(session)
        if field == "1":
            user_update.username = value
        if field == "2":
            user_update.full_name = value
        if field == "3":
            user_update.email = value
        if field == "4":
            user_update.phone_number = value
        if field == "5":
            user_update.status = value
        if field == "password":
            user_update.password = value
            user_update.saltychain = chain

        DALSession().session_commit(session)
        CrudUserMessagesView().update_successful()
        # self.back_to_menu(username)
        Utils().back_to_menu(session, username)

    def user_update_fieldandvalue(self, session):
        field_to_update = CrudInputsView().what_to_update_user()

        if field_to_update == "1":
            value_to_update = CrudInputsView().username_input(session)
        if field_to_update == "2":
            value_to_update = CrudInputsView().fullname_input()
        if field_to_update == "3":
            value_to_update = CrudInputsView().email_input(session)
        if field_to_update == "4":
            value_to_update = CrudInputsView().phonenumber_input()
        if field_to_update == "5":
            value_to_update = CrudInputsView().status_input()
        if field_to_update == "password":
            value_to_update, chain = CrudInputsView().password_encryption()
            return field_to_update, value_to_update, chain

        return field_to_update, value_to_update, None

    def user_delete(self, session, username):
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        while True:
            user_id_input = CrudInputsView().remove_user_id_input()
            user = CheckObjectExists().check_userID_exists_update_delete(
                session, user_id_input
            )
            if user:
                break
            continue
        user = DALUser().get_user_by_id(session, user_id_input)
        confirm_deletion = CrudInputsView().remove_user_confirm_deletion(user)
        if confirm_deletion == "y":
            DALSession().session_delete_and_commit(session, user)
            CrudUserMessagesView().remove_user_sucess(user)
        # self.back_to_menu(username)
        Utils().back_to_menu(session, username)
