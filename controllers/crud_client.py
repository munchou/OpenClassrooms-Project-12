from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudUserMessagesView

from models import models


class CrudClient:
    def client_create(self, session, connected_user):
        CrudInputsView().creation_title()
        current_user = (
            session.query(models.Users).filter_by(username=connected_user).first()
        )

        while True:
            full_name_input = CrudInputsView().fullname_input()
            email_input = CrudInputsView().email_input()
            phone_number_input = CrudInputsView().phonenumber_input()
            company_name_input = CrudInputsView().company_name_input()
            last_contacted_input = CrudInputsView().last_contacted_input()
            salesman_in_charge_autofill = current_user.id

            CrudUserMessagesView().user_confirmation(
                full_name_input,
                email_input,
                phone_number_input,
                company_name_input,
                last_contacted_input,
            )

            confirm_input = CrudInputsView().confirm_creation()
            if confirm_input:
                break
            continue

        # Processing the creation
        client = models.Client(
            full_name=full_name_input,
            email=email_input,
            phone_number=phone_number_input,
            company_name=company_name_input,
            last_contacted=last_contacted_input,
            salesman_in_charge=salesman_in_charge_autofill,
        )

        session.add(client)
        session.commit()
        CrudUserMessagesView().creation_successful(client)

        # print(f"saltychain: {saltychain}")

    def client_update(self, session):
        while True:
            client_id_input = CrudInputsView().update_client_id_input()
            try:
                client_update = (
                    session.query(models.Client).filter_by(id=client_id_input).first()
                )

            except Exception:
                print("ERROR in the input, please try again")
                continue

            confirm_choice = CrudInputsView().confirm_update_choice(client_update)
            if confirm_choice == "y":
                break
            continue

        field, value, chain = self.user_update_fieldandvalue(client_update.username)
        if field == "1":
            client_update.username = value
        if field == "2":
            client_update.full_name = value
        if field == "3":
            client_update.email = value
        if field == "4":
            client_update.phone_number = value
        if field == "5":
            client_update.status = value
        if field == "123":
            client_update.password = value
            client_update.saltychain = chain

        session.commit()

        CrudUserMessagesView().update_successful()

    def user_update_fieldandvalue(self, username):
        while True:
            # fields = ["username", "full_name", "email", "phone_number", "status"]
            field_to_update = input(
                "What to update (1.username, 2.full_name, 3.email, 4.phone_number, 5.status, 123.password): "
            )

            if field_to_update not in ["1", "2", "3", "4", "5", "123"]:
                print("\n\tERROR: Wrong input, please try again")
                continue
            break

        if field_to_update == "1":
            value_to_update = CrudInputsView().username_input()
        if field_to_update == "2":
            value_to_update = CrudInputsView().fullname_input()
        if field_to_update == "3":
            value_to_update = CrudInputsView().email_input(username)
        if field_to_update == "4":
            value_to_update = CrudInputsView().phonenumber_input()
        if field_to_update == "5":
            value_to_update = CrudInputsView().status_input()
        if field_to_update == "123":
            value_to_update, chain = CrudInputsView().password_encryption()
            return field_to_update, value_to_update, chain

        return field_to_update, value_to_update, None

    def user_delete(self, session):
        user_id_input = CrudInputsView().remove_user_id_input()
        user = session.query(models.Users).filter_by(id=user_id_input).first()
        confirm_deletion = CrudInputsView().remove_user_confirm_deletion(user)
        if confirm_deletion == "y":
            session.delete(user)
            session.commit()
            CrudUserMessagesView().remove_user_sucess(user)
