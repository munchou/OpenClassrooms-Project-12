from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudUserMessagesView, CrudGeneralMessagesView
from controllers.check_object_exists import CheckObjectExists

from models import models


class CrudUser:
    def user_create(self, session):
        while True:
            username_input = CrudInputsView().username_input()
            if CheckObjectExists().check_username_exists(session, username_input):
                CrudGeneralMessagesView().already_exists()
                continue

            password, saltychain = CrudInputsView().password_encryption()

            full_name_input = CrudInputsView().fullname_input()

            email_input = CrudInputsView().email_input()
            if CheckObjectExists().check_email_exists(session, email_input):
                CrudGeneralMessagesView().already_exists()
                continue

            phone_number_input = CrudInputsView().phonenumber_input()

            status_input = CrudInputsView().status_input()

            CrudUserMessagesView().user_confirmation(
                username_input,
                full_name_input,
                email_input,
                phone_number_input,
                status_input,
            )

            confirm_input = CrudInputsView().confirm_creation()
            if confirm_input:
                break
            continue

        # Processing the creation
        user = models.Users(
            username=username_input,
            password=password,
            full_name=full_name_input,
            email=email_input,
            phone_number=phone_number_input,
            status=status_input,
            saltychain=saltychain,
        )

        session.add(user)
        session.commit()
        CrudUserMessagesView().creation_successful(user)

        # print(f"saltychain: {saltychain}")

    def user_update(self, session):
        while True:
            user_id_input = CrudInputsView().update_user_id_input()
            user_update = CheckObjectExists().check_userID_exists_update_delete(
                session, user_id_input
            )
            if user_update in session.query(models.Users):
                confirm_choice = CrudInputsView().confirm_update_choice(user_update)
                if confirm_choice == "y":
                    break
                break
            continue

        field, value, chain = self.user_update_fieldandvalue(user_update.username)
        if field == "1":
            user_update.username = value
        if field == "2":
            user_update.full_name = value
        if field == "3":
            user_update.email = value
        if field == "4":
            user_update.phone_number = value
        if field == "5":
            user_update.status = value
        if field == "123":
            user_update.password = value
            user_update.saltychain = chain

        session.commit()

        CrudUserMessagesView().update_successful()

    def user_update_fieldandvalue(self, username):
        field_to_update = CrudInputsView().what_to_update()

        if field_to_update == "1":
            value_to_update = CrudInputsView().username_input()
        if field_to_update == "2":
            value_to_update = CrudInputsView().fullname_input()
        if field_to_update == "3":
            value_to_update = CrudInputsView().email_input()
        if field_to_update == "4":
            value_to_update = CrudInputsView().phonenumber_input()
        if field_to_update == "5":
            value_to_update = CrudInputsView().status_input()
        if field_to_update == "password":
            value_to_update, chain = CrudInputsView().password_encryption()
            return field_to_update, value_to_update, chain

        return field_to_update, value_to_update, None

    def user_delete(self, session):
        while True:
            user_id_input = CrudInputsView().remove_user_id_input()
            user = CheckObjectExists().check_userID_exists_update_delete(
                session, user_id_input
            )
            if user:
                break
            continue
        user = session.query(models.Users).filter_by(id=user_id_input).first()
        confirm_deletion = CrudInputsView().remove_user_confirm_deletion(user)
        if confirm_deletion == "y":
            session.delete(user)
            session.commit()
            CrudUserMessagesView().remove_user_sucess(user)
