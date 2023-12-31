from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudContractMessagesView, CrudClientMessagesView

from controllers.utils import Utils
from controllers.data_access_layer import DALSession, DALUser, DALClient, DALContract
from controllers.check_object_exists import CheckObjectExists

from models import models
import sentry_sdk


class CrudContract:
    def contract_create(self, session, username):
        """Create a contract after filling the required fields.
        If needed, each input will be checked to ensure that
        the entered information is valid and can be processed."""
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        CrudContractMessagesView().creation_title()

        while True:
            client_id_input = CrudInputsView().contract_clientid_input(session)
            client = DALClient().get_client_by_id(session, client_id_input)
            salesman_input = client.salesman_in_charge
            # CrudInputsView().contract_salesmanid_input(
            #     session, client_id_input
            # )
            total_amount_input = CrudInputsView().contract_total_amount_input()
            amount_due_input = CrudInputsView().contract_due_amount_input()
            signed_input = CrudInputsView().contract_signed()

            CrudContractMessagesView().contract_confirmation(
                client_id_input,
                salesman_input,
                total_amount_input,
                amount_due_input,
                signed_input,
            )

            confirm_input = CrudInputsView().confirm_creation()
            if confirm_input:
                break
            continue

        # Processing the creation
        contract = models.Contract(
            client=client_id_input,
            linked_salesman=salesman_input,
            total_amount=total_amount_input,
            amount_due=amount_due_input,
            signed=signed_input,
        )

        DALSession().session_add_and_commit(session, contract)
        CrudContractMessagesView().creation_successful()
        if signed_input is True:
            sentry_sdk.capture_message(
                f"A contract has been signed (ID: {contract.id})"
            )
        Utils().back_to_menu(session, username)

    def contract_update(self, session, username):
        """Update a contract's selected field."""
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        current_user = DALUser().get_user_by_username(session, username)
        # print(f"current_user status: {current_user.status}")
        while True:
            already_signed = False
            contract_id_input = CrudInputsView().update_contract_id(session)
            contract_update = CheckObjectExists().check_contractID_exists(
                session, contract_id_input
            )
            if contract_update in DALContract().get_all_contracts(session):
                if contract_update.signed:
                    already_signed = True
                client = DALClient().get_client_by_id(session, contract_update.client)
                if current_user.status != models.Users.StatusEnum.management:
                    if client.salesman_in_charge != current_user.id:
                        CrudClientMessagesView().not_salesmans_in_charge()
                        continue
                confirm_choice = CrudInputsView().confirm_contract_update_choice(
                    session, contract_update
                )
                if confirm_choice == "y":
                    break
                continue
            continue

        field, value = self.contract_update_fieldandvalue(session, contract_update)
        if field == "1":
            contract_update.total_amount = value
        if field == "2":
            contract_update.amount_due = value
        if field == "3" and value != None:
            contract_update.signed = value
            if already_signed is False and value is True:
                sentry_sdk.capture_message(
                    f"A contract has been signed (ID: {contract_update.id})"
                )
        if field == "4":
            contract_update.linked_salesman = value

        DALSession().session_commit(session)
        CrudContractMessagesView().update_successful()
        Utils().back_to_menu(session, username)

    def contract_update_fieldandvalue(self, session, contract):
        field_to_update = CrudInputsView().what_to_update_contract(contract)

        if field_to_update == "1":
            value_to_update = CrudInputsView().contract_total_amount_input()
        if field_to_update == "2":
            value_to_update = CrudInputsView().contract_due_amount_input()
        if field_to_update == "3":
            value_to_update = CrudInputsView().contract_signed()
        # if field_to_update == "4":
        #     value_to_update = CrudInputsView().contract_linked_salesman(
        #         session, contract
        #     )

        return field_to_update, value_to_update

    def contract_display_all(self, session, username):
        """Display all the contracts in the database."""
        Utils().clear_screen()
        contracts = DALContract().get_all_contracts(session)
        CrudContractMessagesView().contract_display_all(session, contracts)
        Utils().back_to_menu(session, username)

    def contract_display_not_signed(self, session, username):
        """Display the contracts that have not been signed."""
        Utils().clear_screen()
        contracts = DALContract().get_all_contracts(session)
        CrudContractMessagesView().contract_display_not_signed(session, contracts)
        Utils().back_to_menu(session, username)

    def contract_display_not_paid(self, session, username):
        """Display the contracts that have not been fully paid."""
        Utils().clear_screen()
        contracts = DALContract().get_all_contracts(session)
        CrudContractMessagesView().contract_display_not_paid(session, contracts)
        Utils().back_to_menu(session, username)
