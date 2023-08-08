from controllers.check_object_exists import CheckObjectExists
from controllers.data_access_layer import (
    DALClient,
    DALContract,
    DALEvent,
)

from views.views_crud_messages import (
    CrudContractMessagesView,
    CrudEventMessagesView,
    CrudGeneralMessagesView,
)

from models import models


class TestCrudInputsView:
    def test_check_input_characters(self, input_to_check="This#is_a_v@alid_text!"):
        input_is_ascii = True
        if input_to_check.isascii():
            for chara in input_to_check:
                if chara == " ":
                    input_is_ascii = False

        input_to_checkbis = "This text has spaces oh noooo!"
        input_is_asciibis = True
        if input_to_checkbis.isascii():
            for chara in input_to_checkbis:
                if chara == " ":
                    input_is_asciibis = False

        assert input_is_ascii == True
        assert input_is_asciibis == False

    def test_check_if_input_empty(self, input_to_check="    "):
        if input_to_check == "" or input_to_check.strip() == "":
            print("\n\tThis field is required, please type in something.\n")
            returnee = True
        else:
            returnee = False
        assert returnee == True

    def test_check_if_input_empty_false(
        self, input_to_check="This is not an empty field"
    ):
        if input_to_check == "" or input_to_check.strip() == "":
            print("\n\tThis field is required, please type in something.\n")
            returnee = True
        else:
            returnee = False

        assert returnee == False

    def test_username_input(self, session):
        empty_input = False
        user_exists = False

        username_input = "dgdg45yhrft"

        if len(username_input) > 50:
            print(
                "\n\tERROR: The username cannot contain than 50 characters. Please try again.\n"
            )

        if CheckObjectExists().check_username_exists(session, username_input):
            user_exists = True

        assert empty_input == False
        assert user_exists == False

    def test_password_input(self):
        pwd = "qqqqqqqq"
        pwd_repeat = "qqqqqqqq"

        assert pwd == pwd_repeat

    def test_password_input_fail(self):
        pwd = "qqqqqqqq"
        pwd_repeat = "qqqqgqqq"

        assert pwd != pwd_repeat

    def test_fullname_input(self):
        fullname_input = "Full name"

        assert fullname_input == "Full name"

    def test_email_input(self, session):
        email_exists = False
        email_input = "hellowello@email.com"
        email_input_empty = ""
        email_input_exists = "user1@testouille.com"

        if email_input_empty == "":
            email_empty = "no_email@secret98743token"

        if CheckObjectExists().check_email_user_exists(session, email_input_exists):
            email_exists = True

        assert email_input == "hellowello@email.com"
        assert email_empty == "no_email@secret98743token"
        assert email_exists == True

    def test_phonenumber_input(self):
        too_long = False
        phone_input = "+33245689745"
        phone_input_long = "+012345714571654615460065484685"
        if len(phone_input_long) > 20:
            too_long = True

        assert phone_input == "+33245689745"
        assert too_long == True

    def test_status_input(self):
        error = False
        status_input = "1"
        if status_input == "1":
            management = 1
        status_input = "2"
        if status_input == "2":
            sales = 2
        status_input = "3"
        if status_input == "3":
            support = 3
        status_input = "osijhf90843"
        if status_input not in ["1", "2", "3"]:
            error = True

        assert management == 1
        assert sales == 2
        assert support == 3
        assert error == True

    def test_company_name_input(self):
        bad_input = False
        company_name_input = "Name of the Company"
        if len(company_name_input) > 100 or company_name_input.strip() == "":
            bad_input = True
        assert bad_input == False

    def test_last_contacted_input(self):
        current_date = "2023-08-07 10:30"
        custom_date_ok = "2023-08-08 10:30"
        custom_date_wrong = "2023-08-06 10:30"

        date_ok = False
        date_not_ok = False

        if current_date < custom_date_ok:
            date_ok = True

        if current_date > custom_date_wrong:
            date_not_ok = True

        assert current_date == "2023-08-07 10:30"
        assert date_ok == True
        assert date_not_ok == True

    def test_confirm_creation(self):
        confirm_ok = False
        confirm_input = "y"
        if confirm_input == "y":
            confirm_ok = True

        assert confirm_ok == True

    def test_update_user_id_input(self, session):
        user_id_digit = False
        user_id = "10"
        if user_id.isdigit():
            user_id_digit = True

        assert user_id_digit == True

    def test_what_to_update_user(self):
        test_list = ["234", "hello", "0"]
        wrong_input = False
        for item in test_list:
            if item not in ["1", "2", "3", "4", "5", "password"]:
                wrong_input = True

        assert wrong_input == True

    def test_confirm_user_update_choice(self, user_update="User2"):
        while True:
            print(f"\nYou are about to update '{user_update}'.")
            confirmed = False
            confirm_input = "y"
            if confirm_input == "y":
                confirmed = True
                break
            elif confirm_input != "n":
                continue

        assert confirmed == True

    def test_remove_user_id_input(self):
        id_digit = False
        id_not_digit = False
        user_id = "12"
        user_id_bis = "d5"
        if user_id.isdigit():
            id_digit = True
        if not user_id_bis.isdigit():
            id_not_digit = True

        assert id_digit == True
        assert id_not_digit == True

    def test_remove_user_confirm_deletion(self):
        delete_user = False
        dont_delete_user = False
        confirm_deletion = "y"
        if confirm_deletion == "y":
            delete_user = True
        confirm_deletion = "n"
        if confirm_deletion == "n":
            dont_delete_user = True

        assert delete_user == True
        assert dont_delete_user == True

    def test_confirm_client_update_choice(self):
        while True:
            confirmed = False
            confirm_input = "y"
            if confirm_input == "y":
                confirmed = True
                break
            elif confirm_input != "n":
                continue

        assert confirmed == True

    def test_what_to_update_client(self):
        test_list = ["234", "hello", "0"]
        test_input_ok = "4"
        wrong_input = False
        good_input = False
        for item in test_list:
            if item not in ["1", "2", "3", "4", "5"]:
                wrong_input = True
        if test_input_ok in ["1", "2", "3", "4", "5"]:
            good_input = True

        assert wrong_input == True
        assert good_input == True

    def test_update_contract_id(self, session):
        current_client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = (
            session.query(models.Contract).filter_by(client=current_client.id).first()
        )
        contract_exists = False
        contract_id = contract.id
        if str(contract_id).isdigit():
            if not CheckObjectExists().check_contractID_exists(session, contract_id):
                CrudContractMessagesView().contractID_not_exist()
            else:
                contract_exists = True

        assert contract_exists == True

    def test_contract_clientid_input(self, session):
        client_exists = False
        current_client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        client_id = current_client.id
        if str(client_id).isdigit():
            if not CheckObjectExists().check_clientID_exists(session, client_id):
                CrudContractMessagesView().clientID_not_exist()
            else:
                client_exists = True

        assert client_exists == True

    def test_contract_salesmanid_input(self, session):
        salesman_exists = False
        # salesman_not_exists = False
        salesman_ok = session.query(models.Users).filter_by(username="User2").first()

        salesman_id_ok = salesman_ok.id
        salesman_not_ok_id = 45214
        if str(salesman_not_ok_id).isdigit():
            if not CheckObjectExists().check_salesmanID_exists(
                session, salesman_not_ok_id
            ):
                salesman_not_exists = True
        if str(salesman_id_ok).isdigit():
            if CheckObjectExists().check_salesmanID_exists(session, salesman_id_ok):
                salesman_exists = True

        assert salesman_exists == True
        assert salesman_not_exists == True

        session.rollback()

    def test_contract_total_amount_input(self):
        input_ok = False
        amount_input = 50000.0
        try:
            float(amount_input)
            input_ok = True
        except ValueError:
            print("\n\tERROR: Please enter a number.")
        assert input_ok == True

    def test_contract_due_amount_input(self):
        input_ok = False
        amount_input = 10000.0
        try:
            float(amount_input)
            input_ok = True
        except ValueError:
            print("\n\tERROR: Please enter a number.")
        assert input_ok == True

    def test_contract_signed(self):
        signed_ok = False
        signed_not_ok = False
        signed_input = "y"
        if signed_input == "y":
            signed_ok = True
        signed_input = "n"
        if signed_input == "n":
            signed_not_ok = True
        assert signed_ok == True
        assert signed_not_ok == True

    def test_confirm_contract_update_choice(self, session):
        current_client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = (
            session.query(models.Contract).filter_by(client=current_client.id).first()
        )
        contract_update = contract.client
        contract_client = (
            session.query(models.Client).filter_by(id=contract_update).first()
        )

        assert current_client == contract_client
        assert contract_client.full_name == "Client One Updated"

    def test_what_to_update_contract(self):
        test_list = ["234", "hello", "0"]
        test_input_ok = "2"
        wrong_input = False
        good_input = False
        for item in test_list:
            if item not in ["1", "2", "3"]:
                wrong_input = True
        if test_input_ok in ["1", "2", "3"]:
            good_input = True

        assert wrong_input == True
        assert good_input == True

    def test_event_client_name(self, session):
        current_client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = (
            session.query(models.Contract).filter_by(client=current_client.id).first()
        )
        contract_id = contract.id
        contract_check = DALContract().get_contract_by_id(session, contract_id)
        client = DALClient().get_client_of_contract(session, contract)

        assert current_client == client
        assert contract == contract_check

    def test_event_client_contact_input(self):
        input_len_ok = False
        contact_input = "Client's contact info (name, phone number, etc.)"
        if len(contact_input) < 100:
            input_len_ok = True
        assert input_len_ok == True

    def test_event_startdate(self):
        current_date = "2023-08-07 10:30"
        custom_date_ok = "2023-08-08 10:30"
        custom_date_wrong = "2023-08-06 10:30"

        date_ok = False
        date_not_ok = False

        if current_date < custom_date_ok:
            date_ok = True

        if current_date > custom_date_wrong:
            date_not_ok = True

        assert current_date == "2023-08-07 10:30"
        assert date_ok == True
        assert date_not_ok == True

    def test_event_enddate(self):
        current_date = "2023-08-07 10:30"
        custom_date_ok = "2023-08-08 10:30"
        custom_date_wrong = "2023-08-06 10:30"

        date_ok = False
        date_not_ok = False

        if current_date < custom_date_ok:
            date_ok = True

        if current_date > custom_date_wrong:
            date_not_ok = True

        assert current_date == "2023-08-07 10:30"
        assert date_ok == True
        assert date_not_ok == True

    def test_event_supportid_input(self, session):
        support_contact = (
            session.query(models.Users).filter_by(username="User3").first()
        )
        support_id = support_contact.id
        id_not_zero = False
        supportID_exists = False
        if support_id != "0":
            id_not_zero = True
        if str(support_id).isdigit():
            if CheckObjectExists().check_supportID_exists(session, support_id):
                print("CHECK and EXISTS")
                supportID_exists = True

        assert id_not_zero == True
        assert supportID_exists == True

    def test_event_location_input(self):
        location_input = (
            "Location there, 30 miles away from New York City, just turn left."
        )
        assert len(location_input) < 100

    def test_event_attendees_input(self):
        attendees_input = "25"
        attendees_input_wrong = "ten"

        assert attendees_input.isdigit()
        assert not attendees_input_wrong.isdigit()

    def test_event_notes_input(self):
        notes_input = "Additional notes: kldjgflkdfjglk sdlfksdlfkl iwefjewjf"
        notes_input_integer = 654650

        assert isinstance(notes_input, str)
        assert not isinstance(notes_input_integer, str)

    def test_update_event_id(self, session):
        event_exists = False
        client = (
            session.query(models.Client)
            .filter_by(email="client_one_up@testouille.com")
            .first()
        )
        contract = session.query(models.Contract).filter_by(client=client.id).first()
        event = session.query(models.Event).filter_by(contract_id=contract.id).first()
        event_id = event.id
        if str(event_id).isdigit():
            if CheckObjectExists().check_eventID_exists(session, event_id):
                event_exists = True
        assert event_exists == True
        session.rollback()

    def test_what_to_update_event(self):
        test_list = ["234", "hello", "0"]
        test_input_ok = "6"
        wrong_input = False
        good_input = False
        for item in test_list:
            if item not in ["1", "2", "3", "4", "5", "6", "7"]:
                wrong_input = True
        if test_input_ok in ["1", "2", "3", "4", "5", "6", "7"]:
            good_input = True

        assert wrong_input == True
        assert good_input == True

    def test_event_enddate_update(self):
        current_date = "2023-08-07 10:30"
        custom_date_ok = "2023-08-08 10:30"
        custom_date_wrong = "2023-08-06 10:30"

        date_ok = False
        date_not_ok = False

        if current_date < custom_date_ok:
            date_ok = True

        if current_date > custom_date_wrong:
            date_not_ok = True

        assert current_date == "2023-08-07 10:30"
        assert date_ok == True
        assert date_not_ok == True
