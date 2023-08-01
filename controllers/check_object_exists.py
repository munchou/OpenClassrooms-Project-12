from views.views_crud_messages import CrudGeneralMessagesView

from models import models


class CheckObjectExists:
    def check_userID_exists_update_delete(self, session, user_id):
        try:
            user = session.query(models.Users).filter_by(id=user_id).first()
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if user in session.query(models.Users):
            return user
        else:
            CrudGeneralMessagesView().user_not_exist()
            return False

    def check_username_exists(self, session, input_to_check):
        try:
            item = (
                session.query(models.Users).filter_by(username=input_to_check).first()
            )
        except Exception:
            pass

        if item in session.query(models.Users):
            return item
        else:
            return False

    def check_email_user_exists(self, session, input_to_check):
        try:
            item = (
                session.query(models.Users.email)
                .filter_by(email=input_to_check)
                .first()
            )
        except Exception:
            pass

        if item in session.query(models.Users.email).all():
            return item
        else:
            print("")
            return False

    def check_email_client_exists(self, session, input_to_check):
        try:
            item = (
                session.query(models.Client.email)
                .filter_by(email=input_to_check)
                .first()
            )
        except Exception:
            pass

        if item in session.query(models.Client.email).all():
            return item
        else:
            return False

    def check_clientID_exists(self, session, input_to_check):
        try:
            client = session.query(models.Client).filter_by(id=input_to_check).first()
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if client in session.query(models.Client):
            return client
        else:
            return False

    def check_salesmanID_exists(self, session, input_to_check):
        try:
            item = session.query(models.Users).filter_by(id=input_to_check).first()
        except Exception:
            pass

        if item in session.query(models.Users).all():
            if item.status == models.Users.StatusEnum.sales:
                return item
        else:
            return False

    def check_contractID_exists(self, session, input_to_check):
        try:
            contract = (
                session.query(models.Contract).filter_by(id=input_to_check).first()
            )
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if contract in session.query(models.Contract):
            return contract
        else:
            return False

    def check_eventID_exists(self, session, input_to_check):
        try:
            event = session.query(models.Event).filter_by(id=input_to_check).first()
        except Exception:
            CrudGeneralMessagesView().wrong_input()

        if event in session.query(models.Event):
            return event
        else:
            return False

    def check_supportID_exists(self, session, input_to_check):
        try:
            item = session.query(models.Users).filter_by(id=input_to_check).first()
        except Exception:
            pass

        if item in session.query(models.Users).all():
            if item.status == models.Users.StatusEnum.support:
                return item
        else:
            return False
