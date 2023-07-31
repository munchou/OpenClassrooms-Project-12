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

    def check_email_exists(self, session, input_to_check):
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
            return False
