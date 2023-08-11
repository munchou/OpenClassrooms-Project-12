from models import models


class TestDALUser:
    def test_get_current_user(self, session):
        user = session.query(models.Users).filter_by(username="User3").first()
        assert user.username == "User3"

    def test_get_user_by_id(self, session):
        user = session.query(models.Users).filter_by(username="User3").first()
        user_id = user.id
        assert str(user_id).isdigit() == True

    def test_get_user_by_username(self, session):
        user = session.query(models.Users).filter_by(username="User3").first()
        assert user.username == "User3"

    def test_get_all_users(self, session):
        len = 0
        users = session.query(models.Users)
        for user in users:
            len += 1
        assert len == 4

    def test_get_all_users_usernames(self, session):
        users_list = []
        users = session.query(models.Users.username).all()
        for user in users:
            users_list.append(user[0])
        assert len(users_list) == 4
        assert "User1" in users_list
        assert "User2" in users_list
        assert "User3" in users_list

    def test_get_user_email(self, session):
        email_input = "user2@testouille.com"
        user = session.query(models.Users.email).filter_by(email=email_input).first()
        assert user.email == "user2@testouille.com"

    def test_get_all_users_emails(self, session):
        users_email = session.query(models.Users.email).all()
        len = 0
        for email in users_email:
            len += 1
        assert len == 4

    def test_get_user_saltychain(self, session):
        chains = (
            session.query(models.Users.saltychain)
            .filter(models.Users.username == "User2")
            .first()
        )
        assert type(chains[0][1:-1]) == str


class TestDALClient:
    # print(f"\n\nCHAINS: {chains}\n\n")

    def test_get_client_by_id(self, session):
        client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        client_id = client.id
        client_by_id = session.query(models.Client).filter_by(id=client.id).first()
        assert client == client_by_id
        assert str(client_id).isdigit() == True

        # session.rollback()

    def test_get_client_of_contract(self, session):
        client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = session.query(models.Contract).filter_by(client=client.id).first()
        contract_client = (
            session.query(models.Client).filter_by(id=contract.client).first()
        )
        assert contract_client == client

    def test_get_all_clients(self, session):
        clients = session.query(models.Client)
        len = 0
        for client in clients:
            len += 1
        assert len == 1

    def test_get_email_of_client(self, session):
        client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        email = (
            session.query(models.Client.email)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        assert email[0] == client.email

    def test_get_all_clients_emails(self, session):
        emails = session.query(models.Client.email).all()
        len = 0
        for email in emails:
            len += 1
        assert len == 1


class TestDALContract:
    def test_get_all_contracts(self, session):
        contracts = session.query(models.Contract)
        len = 0
        for contract in contracts:
            len += 1
        assert len == 1

    def test_get_contract_by_id(self, session):
        client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = session.query(models.Contract).filter_by(client=client.id).first()
        contractbyid = session.query(models.Contract).filter_by(id=contract.id).first()
        assert contract.id == contractbyid.id

    def test_get_contractid_of_event(self, session):
        client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = session.query(models.Contract).filter_by(client=client.id).first()
        event = session.query(models.Event).filter_by(contract_id=contract.id).first()
        contractid_of_event = (
            session.query(models.Contract).filter_by(id=event.contract_id).first()
        )
        assert contract == contractid_of_event


class TestDALEvent:
    def test_get_event_by_id(self, session):
        client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = session.query(models.Contract).filter_by(client=client.id).first()
        event_get = (
            session.query(models.Event).filter_by(contract_id=contract.id).first()
        )
        event = session.query(models.Event).filter_by(id=event_get.id).first()
        assert event == event_get

    def test_get_events_by_supportid(self, session):
        user = session.query(models.Users).filter_by(username="User3").first()
        len = 0
        events_by_supportid = (
            session.query(models.Event).filter_by(support_contact=user.id).all()
        )
        for item in events_by_supportid:
            len += 1
        assert len == 1

    def test_get_all_events(self, session):
        len = 0
        events = session.query(models.Event)
        for event in events:
            len += 1
        assert len == 1
