from models import models

from sqlalchemy import exc


class DALSession:
    def session_commit(self, session):
        session.commit()

    def session_add_and_commit(self, session, object):
        session.add(object)
        self.session_commit(session)

    def session_delete_and_commit(self, session, object):
        """Instead of deleting it, the user is actually deactivated
        by modifying its status. This prevents the program from
        crashing because of associated Foreign Keys. The user could
        then be reactivated if needed."""
        object.status = "deactivated"
        self.session_commit(session)
        # try:
        #     session.delete(object)
        #     try:
        #         self.session_commit(session)
        #     except Exception:
        #         pass
        # except Exception:
        #     pass
        #     print(
        #         "That user is linked to other entities (clients/contracts/events) and cannot be removed."
        #     )

    def session_close(self, session):
        session.close()


class DALUser:
    def get_current_user(self, session, connected_user):
        return session.query(models.Users).filter_by(username=connected_user).first()

    def get_user_by_id(self, session, user_id):
        return session.query(models.Users).filter_by(id=user_id).first()

    def get_user_by_username(self, session, user):
        return session.query(models.Users).filter_by(username=user).first()

    def get_all_users(self, session):
        return session.query(models.Users)

    def get_all_users_usernames(self, session):
        return session.query(models.Users.username).all()

    def get_user_email(self, session, email_input):
        return session.query(models.Users.email).filter_by(email=email_input).first()

    def get_all_users_emails(self, session):
        return session.query(models.Users.email).all()

    def get_user_saltychain(self, session, username):
        return (
            session.query(models.Users.saltychain)
            .filter(models.Users.username == username)
            .first()
        )

    def get_user_hashkey(self, session, username):
        user_hashkey = (
            session.query(models.Users.password)
            .filter(models.Users.username == username)
            .first()
        )
        return user_hashkey[0][1:-1]


class DALClient:
    def get_client_by_id(self, session, client_id):
        return session.query(models.Client).filter_by(id=client_id).first()

    def get_client_of_contract(self, session, contract):
        return session.query(models.Client).filter_by(id=contract.client).first()

    def get_all_clients(self, session):
        return session.query(models.Client)

    def get_email_of_client(self, session, email_input):
        return session.query(models.Client.email).filter_by(email=email_input).first()

    def get_all_clients_emails(self, session):
        return session.query(models.Client.email).all()


class DALContract:
    def get_all_contracts(self, session):
        return session.query(models.Contract)

    def get_contract_by_id(self, session, contract_id):
        return session.query(models.Contract).filter_by(id=contract_id).first()

    def get_contracts_from_a_client(self, session, client_id):
        return session.query(models.Contract).filter_by(client=client_id).all()

    def get_contractid_of_event(self, session, event):
        return session.query(models.Contract).filter_by(id=event.contract_id).first()


class DALEvent:
    def get_event_by_id(self, session, event_id):
        return session.query(models.Event).filter_by(id=event_id).first()

    def get_events_by_supportid(self, session, user):
        return session.query(models.Event).filter_by(support_contact=user.id).all()

    def get_all_events(self, session):
        return session.query(models.Event)
