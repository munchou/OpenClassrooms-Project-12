from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudClientMessagesView

from controllers.utils import Utils
from controllers.data_access_layer import DALSession, DALUser, DALClient
from controllers.check_object_exists import CheckObjectExists

from models import models


class CrudClient:
    def client_create(self, session, connected_user):
        Utils().user_status_request_pwd(session, connected_user)
        Utils().clear_screen()
        CrudClientMessagesView().creation_title()
        current_user = DALUser().get_current_user(session, connected_user)

        while True:
            full_name_input = CrudInputsView().fullname_input()
            email_input = CrudInputsView().email_input(session)
            phone_number_input = CrudInputsView().phonenumber_input()
            company_name_input = CrudInputsView().company_name_input()
            last_contacted_input = CrudInputsView().last_contacted_input()
            salesman_in_charge_autofill = current_user.id

            CrudClientMessagesView().client_confirmation(
                full_name_input,
                email_input,
                phone_number_input,
                company_name_input,
                last_contacted_input,
            )

            confirm_input = CrudInputsView().confirm_creation()
            if confirm_input:
                break
            continue

        # Processing the creation
        client = models.Client(
            full_name=full_name_input,
            email=email_input,
            phone_number=phone_number_input,
            company_name=company_name_input,
            last_contacted=last_contacted_input,
            salesman_in_charge=salesman_in_charge_autofill,
        )

        DALSession().session_add_and_commit(session, client)
        CrudClientMessagesView().creation_successful(client)
        Utils().back_to_menu(session, connected_user)

    def client_update(self, session, username):
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        is_salesman = False
        salesman = DALUser().get_user_by_username(session, username)
        if salesman != None:
            is_salesman = True

        while True:
            client_id_input = CrudInputsView().contract_clientid_input(session)
            client_update = CheckObjectExists().check_clientID_exists(
                session, client_id_input
            )
            if client_update in DALClient().get_all_clients(session):
                if is_salesman == True:
                    if client_update.salesman_in_charge != salesman.id:
                        CrudClientMessagesView().not_salesmans_in_charge()
                        continue
                confirm_choice = CrudInputsView().confirm_client_update_choice(
                    client_update
                )
                if confirm_choice == "y":
                    break
                continue
            continue

        field, value = self.client_update_fieldandvalue(session, client_id_input)
        if field == "1":
            client_update.full_name = value
        if field == "2":
            client_update.email = value
        if field == "3":
            client_update.phone_number = value
        if field == "4":
            client_update.company_name = value
        if field == "5":
            client_update.last_contacted = value
        if field == "salesman":
            client_update.salesman_in_charge = value

        DALSession().session_commit(session)

        CrudClientMessagesView().update_successful()
        Utils().back_to_menu(session, username)

    def client_update_fieldandvalue(self, session, client_id):
        field_to_update = CrudInputsView().what_to_update_client()

        if field_to_update == "1":
            value_to_update = CrudInputsView().fullname_input()
        if field_to_update == "2":
            value_to_update = CrudInputsView().email_input(session)
        if field_to_update == "3":
            value_to_update = CrudInputsView().phonenumber_input()
        if field_to_update == "4":
            value_to_update = CrudInputsView().company_name_input()
        if field_to_update == "5":
            value_to_update = CrudInputsView().last_contacted_input()
        if field_to_update == "salesman":
            value_to_update = CrudInputsView().client_update_salesmanid_input(
                session, client_id
            )

        return field_to_update, value_to_update

    def client_display_all(self, session, username):
        Utils().clear_screen()
        clients = DALClient().get_all_clients(session)
        CrudClientMessagesView().client_display_all(session, clients)
        Utils().back_to_menu(session, username)
