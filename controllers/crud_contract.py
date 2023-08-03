from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudContractMessagesView

from controllers.data_access_layer import DALSession, DALUser, DALClient, DALContract
from controllers.check_object_exists import CheckObjectExists

from models import models


class CrudContract:
    def contract_create(self, session):
        CrudContractMessagesView().creation_title()

        while True:
            client_id_input = CrudInputsView().contract_clientid_input(session)
            salesman_input = CrudInputsView().contract_salesmanid_input(session)
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

    def contract_update(self, session):
        while True:
            contract_id_input = CrudInputsView().update_contract_id(session)
            contract_update = CheckObjectExists().check_contractID_exists(
                session, contract_id_input
            )
            if contract_update in DALContract().get_all_contracts(session):
                confirm_choice = CrudInputsView().confirm_contract_update_choice(
                    session, contract_update
                )
                if confirm_choice == "y":
                    break
                continue
            continue

        field, value = self.contract_update_fieldandvalue()
        if field == "1":
            contract_update.total_amount = value
        if field == "2":
            contract_update.amount_due = value
        if field == "3":
            contract_update.signed = value

        DALSession().session_commit(session)
        CrudContractMessagesView().update_successful()

    def contract_update_fieldandvalue(self):
        field_to_update = CrudInputsView().what_to_update_contract()

        if field_to_update == "1":
            value_to_update = CrudInputsView().contract_total_amount_input()
        if field_to_update == "2":
            value_to_update = CrudInputsView().contract_due_amount_input()
        if field_to_update == "3":
            value_to_update = CrudInputsView().contract_signed()

        return field_to_update, value_to_update

    def contract_display_all(self, session):
        contracts = DALContract().get_all_contracts(session)
        CrudContractMessagesView().contract_display_all(session, contracts)

    def contract_display_not_signed(self, session):
        contracts = DALContract().get_all_contracts(session)
        for contract in contracts:
            if not contract.signed:
                CrudContractMessagesView().contract_display_not_signed(
                    session, contracts
                )

    def contract_display_not_paid(self, session):
        contracts = DALContract().get_all_contracts(session)
        CrudContractMessagesView().contract_display_not_paid(session, contracts)
