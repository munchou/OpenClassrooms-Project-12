from controllers.data_access_layer import (
    DALUser,
    DALClient,
    DALContract,
    DALEvent,
)

from views.views_crud_messages import CrudGeneralMessagesView

from models import models


class CheckObjectExists:
    def check_userID_exists_update_delete(self, session, user_id):
        try:
            user = DALUser().get_user_by_id(session, user_id)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if user in DALUser().get_all_users(session):
            return user
        else:
            CrudGeneralMessagesView().user_not_exist()
            return False

    def check_username_exists(self, session, input_to_check):
        try:
            item = DALUser().get_user_by_username(session, input_to_check)
        except Exception:
            pass

        if item in DALUser().get_all_users(session):
            return item
        else:
            return False

    def check_email_user_exists(self, session, input_to_check):
        try:
            item = DALUser().get_user_email(session, input_to_check)
        except Exception:
            pass

        if item in DALUser().get_all_users_emails(session):
            return item
        else:
            print("")
            return False

    def check_email_client_exists(self, session, input_to_check):
        try:
            item = DALClient().get_email_of_client(session, input_to_check)
        except Exception:
            pass

        if item in DALClient().get_all_clients_emails(session):
            return item
        else:
            return False

    def check_clientID_exists(self, session, input_to_check):
        try:
            client = DALClient().get_client_by_id(session, input_to_check)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if client in DALClient().get_all_clients(session):
            return client
        else:
            return False

    def check_salesmanID_exists(self, session, input_to_check):
        try:
            item = DALUser().get_user_by_id(session, input_to_check)
        except Exception:
            pass

        if item in DALUser().get_all_users(session):
            if item.status == models.Users.StatusEnum.sales:
                return item
        else:
            return False

    def check_contractID_exists(self, session, input_to_check):
        try:
            contract = DALContract().get_contract_by_id(session, input_to_check)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if contract in DALContract().get_all_contracts(session):
            return contract
        else:
            return False

    def check_eventID_exists(self, session, input_to_check):
        try:
            event = DALEvent().get_event_by_id(session, input_to_check)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if event in DALEvent().get_all_events(session):
            return event
        else:
            return False

    def check_supportID_exists(self, session, input_to_check):
        try:
            item = DALUser().get_user_by_id(session, input_to_check)
        except Exception:
            pass

        if item in DALUser().get_all_users(session):
            if item.status == models.Users.StatusEnum.support:
                return item
        else:
            return False
