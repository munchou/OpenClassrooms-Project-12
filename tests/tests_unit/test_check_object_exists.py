from controllers.data_access_layer import (
    DALUser,
    DALClient,
    DALContract,
    DALEvent,
)

from views.views_crud_messages import CrudGeneralMessagesView

from models import models


class TestCheckObjectExists:
    def test_check_userID_exists_update_delete(self, session):
        user_get = session.query(models.Users).filter_by(username="User3").first()
        user_id = user_get.id
        user_exists = False
        try:
            user = DALUser().get_user_by_id(session, user_id)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if user in DALUser().get_all_users(session):
            user_exists = True
        else:
            CrudGeneralMessagesView().user_not_exist()
            user_exists = False

        assert user_get == user
        assert user_exists == True

    def test_check_username_exists(self, session, input_to_check="User3"):
        item_exists = False
        try:
            item = DALUser().get_user_by_username(session, input_to_check)
        except Exception:
            pass

        if item in DALUser().get_all_users(session):
            item_exists = True
        else:
            item_exists = False

        assert item_exists == True

    def test_check_email_user_exists(
        self, session, input_to_check="user3@testouille.com"
    ):
        email_exists = False
        try:
            item = DALUser().get_user_email(session, input_to_check)
        except Exception:
            pass

        if item in DALUser().get_all_users_emails(session):
            email_exists = True
        else:
            email_exists = False

        assert email_exists == True

    def test_check_email_client_exists(
        self, session, input_to_check="client_one_up@testouille.com"
    ):
        email_exists = False
        try:
            item = DALClient().get_email_of_client(session, input_to_check)
        except Exception:
            pass

        if item in DALClient().get_all_clients_emails(session):
            email_exists = True
        else:
            email_exists = False

        assert email_exists == True

    def test_check_clientID_exists(self, session):
        client_exists = False
        client_get = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        try:
            client = DALClient().get_client_by_id(session, client_get.id)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if client in DALClient().get_all_clients(session):
            client_exists = True
        else:
            client_exists = False

        assert client_exists == True

    def test_check_salesmanID_exists(self, session, input_to_check="User2"):
        salesmanid_exists = False
        salesman = (
            session.query(models.Users).filter_by(username=input_to_check).first()
        )
        input_to_check
        try:
            item = DALUser().get_user_by_id(session, salesman.id)
        except Exception:
            pass

        if item in DALUser().get_all_users(session):
            if item.status == models.Users.StatusEnum.sales:
                salesmanid_exists = True
        else:
            salesmanid_exists = False

        assert salesmanid_exists == True

    def test_check_contractID_exists(self, session):
        contract_exists = False
        client_get = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract_get = (
            session.query(models.Contract).filter_by(client=client_get.id).first()
        )
        input_to_check = contract_get.id
        try:
            contract = DALContract().get_contract_by_id(session, input_to_check)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if contract in DALContract().get_all_contracts(session):
            contract_exists = True
        else:
            contract_exists = False

        assert contract_exists == True

    def test_check_eventID_exists(self, session):
        event_exists = False
        client_get = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract_get = (
            session.query(models.Contract).filter_by(client=client_get.id).first()
        )
        event_get = (
            session.query(models.Event).filter_by(contract_id=contract_get.id).first()
        )
        input_to_check = event_get.id
        try:
            event = DALEvent().get_event_by_id(session, input_to_check)
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if event in DALEvent().get_all_events(session):
            event_exists = True
        else:
            event_exists = False

        assert event_exists == True

    def test_check_supportID_exists(self, session, input_to_check="User3"):
        supportid_exists = False
        user_get = (
            session.query(models.Users).filter_by(username=input_to_check).first()
        )
        try:
            item = DALUser().get_user_by_id(session, user_get.id)
        except Exception:
            pass
        # print(f"\n user_get: {user_get.status}\n")
        # print(f"\n item: {item.status}\n")
        if item in DALUser().get_all_users(session):
            if item.status == "StatusEnum.support":
                supportid_exists = True
        else:
            supportid_exists = False

        assert supportid_exists == False
