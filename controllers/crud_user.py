from views.views_crud_user import CrudUserView

from models import models


class CrudUser:
    def user_create(self, session):
        CrudUserView().creation_title()
        user_confirm = False
        while not user_confirm:
            username_input = CrudUserView().username_input()
            password, saltychain = CrudUserView().password_encryption()
            full_name_input = CrudUserView().fullname_input()
            email_input = CrudUserView().email_input(username_input)
            phone_number_input = CrudUserView().phonenumber_input()
            status_input = CrudUserView().status_input()

            CrudUserView().user_confirmation(
                username_input,
                full_name_input,
                email_input,
                phone_number_input,
                status_input,
            )

            confirm_input = CrudUserView().confirm_creation()
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
        CrudUserView().creation_successful(user)

        # print(f"saltychain: {saltychain}")

    def user_update(self, session):
        while True:
            user_id_input = CrudUserView().update_user_id_input()
            try:
                user_update = (
                    session.query(models.Users).filter_by(id=user_id_input).first()
                )

            except Exception:
                print("ERROR in the input, please try again")
                continue

            confirm_choice = CrudUserView().confirm_update_choice(user_update)
            if confirm_choice == "y":
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

        CrudUserView().update_successful()

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
            value_to_update = CrudUserView().username_input_update()
        if field_to_update == "2":
            value_to_update = CrudUserView().fullname_input()
        if field_to_update == "3":
            value_to_update = CrudUserView().email_input(username)
        if field_to_update == "4":
            value_to_update = CrudUserView().phonenumber_input()
        if field_to_update == "5":
            value_to_update = CrudUserView().status_input()
        if field_to_update == "123":
            value_to_update, chain = CrudUserView().password_encryption()
            return field_to_update, value_to_update, chain

        return field_to_update, value_to_update, None

    def user_delete(self, session):
        user_id_input = CrudUserView().remove_user_id_input()
        user = session.query(models.Users).filter_by(id=user_id_input).first()
        confirm_deletion = CrudUserView().remove_user_confirm_deletion(user)
        if confirm_deletion == "y":
            session.delete(user)
            session.commit()
            CrudUserView().remove_user_sucess(user)
