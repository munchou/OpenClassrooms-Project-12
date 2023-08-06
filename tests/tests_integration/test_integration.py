from sqlalchemy import exc
from models import models
from datetime import datetime

from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import (
    CrudUserMessagesView,
    CrudClientMessagesView,
    CrudContractMessagesView,
    CrudEventMessagesView,
    CrudGeneralMessagesView,
)

from controllers.utils import Utils
from controllers.data_access_layer import (
    DALSession,
    DALUser,
    DALClient,
    DALContract,
    DALEvent,
)
from controllers.check_object_exists import CheckObjectExists

import secrets, random, hashlib


class TestIntegrationUser:
    def password_encryption(self):
        password = "qqqqqqqq"
        numbers = [4, 5, 6, 7, 8]
        salty_first = secrets.token_hex(random.choice(numbers))
        salty_second = secrets.token_hex(random.choice(numbers))
        salty_third = secrets.token_hex(random.choice(numbers))
        salty_chain = []
        salty_chain.extend((salty_first, salty_second, salty_third))
        salted_password = (
            f"{salty_first}{password[:4]}{salty_second}{password[4:]}{salty_third}"
        )

        zupakey = [hashlib.sha256(salted_password.encode("utf-8")).hexdigest()]
        return zupakey, salty_chain

    def test_user_create(self, session):
        password, saltychain = self.password_encryption()
        test_user = models.Users(
            username="TestUser",
            password=password,
            full_name="Test User",
            email="test_user@testouille.com",
            phone_number="145645007",
            status="management",
            saltychain=saltychain,
        )

        try:
            test_user_exists = (
                session.query(models.Users).filter_by(username="TestUser").first()
            )
            if not test_user_exists:
                session.add(test_user)
                session.commit()
        except Exception:
            pass

        test_user = session.query(models.Users).filter_by(username="TestUser").first()
        assert test_user.username == "TestUser"
        assert test_user.full_name == "Test User"
        assert test_user.email == "test_user@testouille.com"
        assert test_user.phone_number == "145645007"
        assert test_user.status == models.Users.StatusEnum.management

    def test_check_password_input(self, session, username="User1"):
        password = "qqqqqqqq"
        check_password = Utils().check_password(session, username, password)

        assert check_password == "hash ok"

    def test_check_password_input_fail(self, session, username="User1"):
        password = "qqqdqqqq"
        check_password = Utils().check_password(session, username, password)

        assert check_password == 0

    def test_user_update(self, session, username="TestUser"):
        self.test_check_password_input(session, username)
        while True:
            user_id_input = DALUser().get_user_by_username(session, username).id
            user_update = CheckObjectExists().check_userID_exists_update_delete(
                session, user_id_input
            )
            if user_update in DALUser().get_all_users(session):
                confirm_choice = "y"
                if confirm_choice == "y":
                    break
                continue
            continue

        field, value = "1", "TestUser_updated"
        if field == "1":
            user_update.username = value
        field, value = "2", "Test User Updated"
        if field == "2":
            user_update.full_name = value
        field, value = "3", "test_user_updated@testouille.com"
        if field == "3":
            user_update.email = value
        field, value = "4", "145645007_updated"
        if field == "4":
            user_update.phone_number = value
        field, value = "5", "support"
        if field == "5":
            user_update.status = value
        field, (value, chain) = "password", self.password_encryption()
        if field == "password":
            user_update.password = value
            user_update.saltychain = chain

        DALSession().session_commit(session)

        assert (
            user_update
            == session.query(models.Users).filter_by(id=user_id_input).first()
        )
        assert user_update.username == "TestUser_updated"
        assert user_update.full_name == "Test User Updated"
        assert user_update.email == "test_user_updated@testouille.com"
        assert user_update.phone_number == "145645007_updated"
        assert user_update.status == models.Users.StatusEnum.support

    def test_user_delete(self, session, username="TestUser_updated"):
        user_exists_before_deletion = False
        self.test_check_password_input(session, username)
        user_id_input = DALUser().get_user_by_username(session, username).id
        user = CheckObjectExists().check_userID_exists_update_delete(
            session, user_id_input
        )
        if user:
            user_exists_before_deletion = True
        user = DALUser().get_user_by_id(session, user_id_input)
        confirm_deletion = "y"
        if confirm_deletion == "y":
            DALSession().session_delete_and_commit(session, user)

        assert user_exists_before_deletion == True
        assert DALUser().get_user_by_username(session, username) == None


class TestIntegrationClient:
    def test_client_create(self, session, connected_user="User2"):
        TestIntegrationUser().test_check_password_input(session, connected_user)
        current_user = DALUser().get_user_by_username(session, connected_user)

        full_name_input = "Client One"
        email_input = "client_one@testouille.com"
        phone_number_input = "+33380541298"
        company_name_input = "Dry Water"
        last_contacted_input = "2023-08-06 18:20"
        salesman_in_charge_autofill = current_user.id

        client = models.Client(
            full_name=full_name_input,
            email=email_input,
            phone_number=phone_number_input,
            company_name=company_name_input,
            last_contacted=last_contacted_input,
            salesman_in_charge=salesman_in_charge_autofill,
        )

        DALSession().session_add_and_commit(session, client)

        client_one = (
            session.query(models.Client)
            .filter_by(email="client_one@testouille.com")
            .first()
        )

        assert current_user.username == "User2"
        assert client_one.full_name == "Client One"
        assert client_one.email == "client_one@testouille.com"
        assert client_one.phone_number == "+33380541298"
        assert client_one.company_name == "Dry Water"
        assert client_one.last_contacted == datetime.strptime(
            "2023-08-06 18:20", "%Y-%m-%d %H:%M"
        )
        assert client_one.salesman_in_charge == current_user.id

    def test_client_update(self, session):
        client_one = (
            session.query(models.Client)
            .filter_by(email="client_one@testouille.com")
            .first()
        )
        client_id_input = client_one.id
        client_update = CheckObjectExists().check_clientID_exists(
            session, client_id_input
        )

        field, value = "1", "Client One Updated"
        if field == "1":
            client_update.full_name = value
        field, value = "2", "client_one_up@testouille.com"
        if field == "2":
            client_update.email = value
        field, value = "3", "0380541298"
        if field == "3":
            client_update.phone_number = value
        field, value = "4", "Dry Water Updated"
        if field == "4":
            client_update.company_name = value
        field, value = "5", "2023-08-06 23:20"
        if field == "5":
            client_update.last_contacted = value

        DALSession().session_commit(session)

        assert (
            client_update
            == session.query(models.Client).filter_by(id=client_id_input).first()
        )
        assert client_update.full_name == "Client One Updated"
        assert client_update.email == "client_one_up@testouille.com"
        assert client_update.phone_number == "0380541298"
        assert client_update.company_name == "Dry Water Updated"
        assert client_update.last_contacted == datetime.strptime(
            "2023-08-06 23:20", "%Y-%m-%d %H:%M"
        )

    def test_client_display_all(self, session):
        clients = DALClient().get_all_clients(session)
        len = 0
        for client in clients:
            len += 1

        assert len == 1

    class TestIntegrationContract:
        def test_contract_create(self, session):
            current_client = (
                session.query(models.Client)
                .filter_by(email="client_one_up@testouille.com")
                .first()
            )
            client_id_input = current_client.id
            salesman_input = current_client.salesman_in_charge
            total_amount_input = 50000.0
            amount_due_input = 22000.0
            signed_input = False

            contract = models.Contract(
                client=client_id_input,
                linked_salesman=salesman_input,
                total_amount=total_amount_input,
                amount_due=amount_due_input,
                signed=signed_input,
            )

            DALSession().session_add_and_commit(session, contract)

            new_contract = (
                session.query(models.Contract)
                .filter_by(client=current_client.id)
                .first()
            )
            assert new_contract.client == current_client.id
            assert new_contract.linked_salesman == current_client.salesman_in_charge
            assert new_contract.total_amount == 50000.0
            assert new_contract.amount_due == 22000.0
            assert new_contract.signed == False

        def test_contract_update(self, session):
            current_client = (
                session.query(models.Client)
                .filter_by(email="client_one_up@testouille.com")
                .first()
            )
            contract = (
                session.query(models.Contract)
                .filter_by(client=current_client.id)
                .first()
            )
            contract_id_input = contract.id
            contract_update = CheckObjectExists().check_contractID_exists(
                session, contract_id_input
            )
            if contract_update in DALContract().get_all_contracts(session):
                confirm_choice = "y"

            field, value = "1", 75000.0
            if field == "1":
                contract_update.total_amount = value
            field, value = "2", 30000.0
            if field == "2":
                contract_update.amount_due = value
            field, value = "3", True
            if field == "3":
                contract_update.signed = value

            DALSession().session_commit(session)

            assert (
                contract_update
                == session.query(models.Contract)
                .filter_by(id=contract_id_input)
                .first()
            )
            assert confirm_choice == "y"
            assert contract_update.total_amount == 75000.0
            assert contract_update.amount_due == 30000.0
            assert contract_update.signed == True

    def test_contract_display_all(self, session):
        contracts = DALContract().get_all_contracts(session)
        len = 0
        for contract in contracts:
            len += 1
        assert len == 1

    def test_contract_display_not_signed(self, session):
        contracts = DALContract().get_all_contracts(session)
        not_signed = False
        for contract in contracts:
            if not contract.signed:
                not_signed = True

        assert not_signed == False

    def test_contract_display_not_paid(self, session):
        contracts = DALContract().get_all_contracts(session)
        not_paid = False
        for contract in contracts:
            if contract.amount_due > 0:
                not_paid = True

        assert not_paid

    class TestIntegrationEvent:
        def test_event_create(self, session):
            current_client = (
                session.query(models.Client)
                .filter_by(email="client_one_up@testouille.com")
                .first()
            )
            contract = (
                session.query(models.Contract)
                .filter_by(client=current_client.id)
                .first()
            )
            contract_id_input = contract.id
            contract_signed = False
            contract = DALContract().get_contract_by_id(session, contract_id_input)
            if contract.signed:
                contract_signed = True

            client_name_input = current_client.full_name
            client_contact_input = "Client, tel: 911"
            start_date_input = "2023-08-07 12:00"
            end_date_input = None
            support_contact_input = None
            location_input = "Rue de la Marmotte, 42000 Papiédalu"
            attendees_input = 0
            notes_input = "Notes go here."

            event = models.Event(
                contract_id=contract_id_input,
                client_name=client_name_input,
                client_contact=client_contact_input,
                start_date=start_date_input,
                end_date=end_date_input,
                support_contact=support_contact_input,
                location=location_input,
                attendees=attendees_input,
                notes=notes_input,
            )

            DALSession().session_add_and_commit(session, event)

            event = (
                session.query(models.Event)
                .filter_by(client_name=client_name_input)
                .first()
            )
            assert contract_signed == True
            assert event.client_name == current_client.full_name
            assert event.client_contact == "Client, tel: 911"
            assert event.start_date == datetime.strptime(
                "2023-08-07 12:00", "%Y-%m-%d %H:%M"
            )
            assert event.end_date == None
            assert event.support_contact == None
            assert event.location == "Rue de la Marmotte, 42000 Papiédalu"
            assert event.attendees == 0
            assert event.notes == "Notes go here."

    def test_event_update_add_support(self, session):
        current_client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        event = (
            session.query(models.Event)
            .filter_by(client_name=current_client.full_name)
            .first()
        )
        event_id_input = event.id
        event_update = CheckObjectExists().check_eventID_exists(session, event_id_input)
        event_exists = False
        if event_update in DALEvent().get_all_events(session):
            event_exists = True

        support_contact_input = (
            session.query(models.Users).filter_by(username="User3").first()
        )

        event_update.support_contact = support_contact_input.id

        DALSession().session_commit(session)

        assert event_exists == True
        assert event.support_contact == support_contact_input.id

    def test_event_update(self, session):
        current_client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        event = (
            session.query(models.Event)
            .filter_by(client_name=current_client.full_name)
            .first()
        )
        event_id_input = event.id
        event_update = CheckObjectExists().check_eventID_exists(session, event_id_input)
        event_exists = False
        if event_update in DALEvent().get_all_events(session):
            event_exists = True

        field, value = "1", "New Client, newcl@moumoute.ru"
        if field == "1":
            event_update.client_contact = value
        # field, value = "2", "2023-08-07 12:00"
        # if field == "2":
        #     event_update.start_date = value
        field, value = "3", "2023-08-07 14:00"
        if field == "3":
            event_update.end_date = value
        # field, value = "4", None
        # if field == "4":
        #     event_update.support_contact = value
        field, value = "5", "Rue, et bon courage pour trouver"
        if field == "5":
            event_update.location = value
        field, value = "6", 14
        if field == "6":
            event_update.attendees = value
        field, value = "7", "14 guests have been added."
        if field == "7":
            event_update.notes = value

        DALSession().session_commit(session)

        support_contact = (
            session.query(models.Users).filter_by(username="User3").first()
        )

        assert event_exists == True
        assert event.client_contact == "New Client, newcl@moumoute.ru"
        assert event.start_date == datetime.strptime(
            "2023-08-07 12:00", "%Y-%m-%d %H:%M"
        )
        assert event.end_date == datetime.strptime("2023-08-07 14:00", "%Y-%m-%d %H:%M")
        assert event.support_contact == support_contact.id
        assert event.location == "Rue, et bon courage pour trouver"
        assert event.attendees == 14
        assert event.notes == "14 guests have been added."

    def test_event_display_no_support(self, session):
        events = DALEvent().get_all_events(session)
        len = 0
        for event in events:
            if event.support_contact is None:
                len += 1

        assert len == 0

    def test_event_display_for_supportincharge(self, session, user="User3"):
        user = DALUser().get_user_by_username(session, user)
        events = DALEvent().get_events_by_supportid(session, user)
        assert len(events) == 1

    def test_event_display_all(self, session):
        events = DALEvent().get_all_events(session)
        len = 0
        for event in events:
            len += 1

        assert len == 1
