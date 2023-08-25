from datetime import datetime
from getpass import getpass
import secrets, random, hashlib

from models import models

from controllers.data_access_layer import (
    DALClient,
    DALContract,
    DALEvent,
)
from controllers.check_object_exists import CheckObjectExists

from views.views_crud_messages import (
    CrudContractMessagesView,
    CrudEventMessagesView,
    CrudGeneralMessagesView,
)


class CrudInputsView:
    def __init__(self):
        pass

    # @staticmethod
    # def creation_title():
    #     print("CREATION OF A CLIENT:")

    def check_input_characters(self, input_to_check):
        input_is_ascii = True
        if input_to_check.isascii():
            for chara in input_to_check:
                if chara == " ":
                    input_is_ascii = False

            if input_is_ascii:
                return "input_passed"

        # forbidden_characters = " %&@+^"
        # for character in input_to_check:
        #     if character in forbidden_characters:
        #         print(f"\n\tERROR: '{character}' not allowed, please type again.")
        #         return character

    def check_if_input_empty(self, input_to_check):
        if input_to_check == "" or input_to_check.strip() == "":
            print("\n\tThis field is required, please type in something.\n")
            return True
        return False

    def username_input(self, session):
        while True:
            username_input = input("\tusername: ")
            if len(username_input) > 50:
                print(
                    "\n\tERROR: The username cannot contain more than 50 characters. Please try again.\n"
                )
                continue
            if self.check_if_input_empty(username_input):
                continue
            checked_input = self.check_input_characters(username_input)
            if checked_input != "input_passed":
                print(
                    "\n\tERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
                continue

            if CheckObjectExists().check_username_exists(session, username_input):
                CrudGeneralMessagesView().already_exists()
                continue
            return username_input

    def password_input(self):
        while True:
            pwd = getpass("\tPassword (at least 8 characters): ")

            checked_input = self.check_input_characters(pwd)
            if checked_input != "input_passed":
                continue

            if len(pwd) < 8 or len(pwd) > 100:
                print(
                    f"\n\tERROR: Your password contains {len(pwd)} characters. Please try again.\n"
                )
                continue

            pwd_repeat = getpass("\tRepeat the password: ")
            if pwd == pwd_repeat:
                return pwd

            print("The passwords did not match, please try again.")
            continue

    def password_encryption(self):
        password = self.password_input()
        """Password salting and hashing. Good luck to hackers..."""
        numbers = [4, 5, 6, 7, 8]
        salty_first = secrets.token_hex(random.choice(numbers))
        salty_second = secrets.token_hex(random.choice(numbers))
        salty_third = secrets.token_hex(random.choice(numbers))
        salty_chain = []
        salty_chain.extend((salty_first, salty_second, salty_third))
        salted_password = (
            f"{salty_first}{password[:4]}{salty_second}{password[4:]}{salty_third}"
        )

        # hash the passwords
        zupakey = [hashlib.sha256(salted_password.encode("utf-8")).hexdigest()]
        # return f"{password}{zupakey}"
        return zupakey, salty_chain

    def fullname_input(self):
        while True:
            fullname_input = input("\tFull name: ")
            if len(fullname_input) > 100:
                print(
                    "\n\tERROR: the user's full name cannot contain more than 100 characters. Please try again.\n"
                )
                continue
            if self.check_if_input_empty(fullname_input):
                continue
            return fullname_input

    def email_input(self, session):
        while True:
            email_input = input("\temail (optional, press ENTER if no email): ")
            if len(email_input) > 100:
                print(
                    "\n\tERROR: the email cannot contain more than 100 characters. Please try again.\n"
                )
                continue
            if email_input == "":
                return f"no_email@{secrets.token_hex(8)}"
            if self.check_input_characters(email_input) != "input_passed":
                print(
                    "\n\tERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
                continue

            if CheckObjectExists().check_email_user_exists(session, email_input):
                CrudGeneralMessagesView().already_exists()
                continue
            return email_input

    def phonenumber_input(self):
        while True:
            phone_input = input("\tTelephone number: ")
            if len(phone_input) > 20:
                print(
                    "\n\tERROR: the phone number cannot contain more than 20 characters. Please try again.\n"
                )
                continue
            if self.check_if_input_empty(phone_input):
                continue
            return phone_input

    def status_input(self):
        while True:
            print("\nWhich team will the user be part of?")
            print("\t1. Management Team")
            print("\t2. Sales Team")
            print("\t3. Support Team")
            status_input = input("CHOICE: ")
            if status_input == "1":
                return "management"
            elif status_input == "2":
                return "sales"
            elif status_input == "3":
                return "support"
            else:
                print("\n\tInput error, please try again.\n")
                continue

    def company_name_input(self):
        while True:
            company_name_input = input("\tName of the Company: ")
            if len(company_name_input) > 100:
                print(
                    "\n\tERROR: the company's name cannot contain more than 100 characters. Please try again.\n"
                )
            if company_name_input.strip() == "":
                print(
                    "\n\tERROR: the company's name cannot be left empty. Please try again.\n"
                )
                continue
            return company_name_input

    def last_contacted_input(self):
        while True:
            print(
                f"\n\tCurrent date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            current_date = input("\tUse the current date? (y/n)? ").casefold()
            if current_date == "y":
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if current_date == "n":
                while True:
                    year = input("\tYear: ")
                    month = input("\tMonth: ")
                    day = input("\tDay: ")
                    time_hours = input("\tHours: ")
                    time_minutes = input("\tMinutes: ")
                    custom_date = f"{year}-{month}-{day} {time_hours}:{time_minutes}"

                    try:
                        custom_date = datetime.strptime(custom_date, "%Y-%m-%d %H:%M")
                    except ValueError:
                        print(f"Error in the date {custom_date}, please try again.")
                        continue

                    custom_date = str(custom_date)

                    print(f"now : {datetime.now()} /// custom_date: {custom_date}")
                    if str(datetime.now()) < custom_date:
                        print("You can't be from the future, can you? Try again...")
                        continue

                    print("Is that date correct?")
                    check_time = input(f"\t{custom_date} (y/n): ").casefold()
                    if check_time == "y":
                        return custom_date
                    if check_time == "n":
                        continue
                    else:
                        print("\n\tERROR in the input, please try again.\n")
                        continue
            else:
                print("\n\tERROR in the input, please try again.\n")
                continue

    def confirm_creation(self):
        while True:
            confirm_input = input("\nConfirm? (y/n)\n").casefold()
            if confirm_input == "y":
                return True
            elif confirm_input != "n":
                continue
            return False

    def client_update_salesmanid_input(self, session, client_id):
        """Change the salesman in charge of the client.
        When done so, update all the related contracts so that
        the salesman linked to them is the new salesman in
        charge of the client."""
        client = DALClient().get_client_by_id(session, client_id)
        client_contracts = DALContract().get_contracts_from_a_client(session, client_id)

        print(f"Current Salesman ID in charge: {client.salesman_in_charge}")
        while True:
            salesman_id = input("\tID of the new Salesman in charge of that contract: ")
            if salesman_id.isdigit():
                if not CheckObjectExists().check_salesmanID_exists(
                    session, salesman_id
                ):
                    CrudContractMessagesView().salesmanID_not_exist()
                    continue
                # if salesman_id != str(client.salesman_in_charge):
                #     CrudContractMessagesView().salesmanID_bad_id()
                #     continue
                for contract in client_contracts:
                    contract.linked_salesman = salesman_id
                    session.commit()
                return salesman_id
            print("\n\tERROR: Only digits are allowed.")

    def update_user_id_input(self):
        while True:
            user_id = input("Please enter the ID of the user you wish to update: ")
            if user_id.isdigit():
                return user_id
            print("\n\tERROR: Only digits are allowed.")

    def what_to_update_user(self):
        while True:
            print("What would you like to update?")
            print("\t1: username")
            print("\t2: User's name")
            print("\t3: email")
            print("\t4: Phone number")
            print("\t5: Status")
            print("\tpassword: password")
            field_to_update = input("Choice: ")
            if field_to_update not in ["1", "2", "3", "4", "5", "password"]:
                CrudGeneralMessagesView().wrong_input()
                continue
            return field_to_update

    def confirm_user_update_choice(self, user_update):
        while True:
            print(f"\nYou are about to update '{user_update.username}'.")
            confirm_input = input("Please confirm (y/n):\n").casefold()
            if confirm_input == "y":
                return "y"
            elif confirm_input != "n":
                continue
            return False

    def remove_user_id_input(self):
        while True:
            user_id = input("Please enter the ID of the user you wish to deactivate: ")
            if user_id.isdigit():
                return user_id
            print("Bad input, try again")
            continue

    def remove_user_confirm_deletion(self, user):
        while True:
            confirm_deletion = input(
                f"Do you confirm the deactivation of {user.username} (ID: {user.id}) (y/n)? "
            ).casefold()
            if confirm_deletion == "y":
                return "y"
            elif confirm_deletion == "n":
                return "n"
            print("Input error, please try again.")
            continue

    def confirm_client_update_choice(self, client_update):
        while True:
            print(f"\nYou are about to update the client '{client_update.full_name}'.")
            confirm_input = input("Please confirm (y/n):\n").casefold()
            if confirm_input == "y":
                return "y"
            elif confirm_input != "n":
                continue
            return False

    def what_to_update_client(self):
        while True:
            print("What would you like to update?")
            print("\t1: Client's name")
            print("\t2: email")
            print("\t3: Phone number")
            print("\t4: Company's name")
            print("\t5: Last contact date")
            print("\tsalesman: Salesman in charge")
            field_to_update = input("Choice: ")
            if field_to_update not in ["1", "2", "3", "4", "5", "salesman"]:
                CrudGeneralMessagesView().wrong_input()
                continue
            return field_to_update

    def update_contract_id(self, session):
        while True:
            contract_id = input("\tContract's ID: ")
            if contract_id.isdigit():
                if not CheckObjectExists().check_contractID_exists(
                    session, contract_id
                ):
                    CrudContractMessagesView().contractID_not_exist()
                    continue
                return contract_id
            print("\n\tERROR: Only digits are allowed.")

    def contract_clientid_input(self, session):
        while True:
            client_id = input("\tClient's ID: ")
            if client_id.isdigit():
                if not CheckObjectExists().check_clientID_exists(session, client_id):
                    CrudContractMessagesView().clientID_not_exist()
                    continue
                return client_id
            print("\n\tERROR: Only digits are allowed.")

    # def contract_salesmanid_input(self, session, client_id):
    #     current_client = DALClient().get_client_by_id(session, client_id).first()
    #     while True:
    #         salesman_id = input("\tID of the Salesman in charge of that contract: ")
    #         if salesman_id.isdigit():
    #             if not CheckObjectExists().check_salesmanID_exists(
    #                 session, salesman_id
    #             ):
    #                 CrudContractMessagesView().salesmanID_not_exist()
    #                 continue
    #             return salesman_id
    #         print("\n\tERROR: Only digits are allowed.")

    def contract_total_amount_input(self):
        while True:
            amount_input = input("\tContract's total price: ")
            try:
                float(amount_input)
                return amount_input
            except ValueError:
                print("\n\tERROR: Please enter a number.")

    def contract_due_amount_input(self):
        while True:
            amount_input = input("\tContract's due amount: ")
            try:
                float(amount_input)
                return amount_input
            except ValueError:
                print("\n\tERROR: Please enter a number.")

    def contract_signed(self):
        while True:
            signed_input = input("\tThe contract has been signed (y/n): ").casefold()
            if signed_input == "y":
                return True
            if signed_input == "n":
                return False
            else:
                CrudGeneralMessagesView().wrong_input()
                continue

    def contract_linked_salesman(self, session, contract):
        client = DALClient().get_client_by_id(session, contract.client)
        print(f"client.salesman_in_charge: {client.salesman_in_charge}")
        while True:
            salesman_id = input("\tID of the Salesman in charge of that contract: ")
            if salesman_id.isdigit():
                if not CheckObjectExists().check_salesmanID_exists(
                    session, salesman_id
                ):
                    CrudContractMessagesView().salesmanID_not_exist()
                    continue
                if salesman_id != str(client.salesman_in_charge):
                    CrudContractMessagesView().salesmanID_bad_id()
                    continue
                return salesman_id
            print("\n\tERROR: Only digits are allowed.")

    def confirm_contract_update_choice(self, session, contract_update):
        contract_client = DALClient().get_client_of_contract(session, contract_update)
        while True:
            print(
                f"\nYou are about to update [{contract_client.full_name}]'s contract."
            )
            confirm_input = input("Please confirm (y/n):\n").casefold()
            if confirm_input == "y":
                return "y"
            elif confirm_input != "n":
                continue
            return False

    def what_to_update_contract(self, contract):
        while True:
            print("What would you like to update?")
            print("\t1: Contract's total price")
            print("\t2: Contract's due amount")
            if not contract.signed:
                print("\t3: Contract's signature")
                field_to_update = input("Choice: ")
                if field_to_update not in ["1", "2", "3"]:
                    CrudGeneralMessagesView().wrong_input()
                    continue
            else:
                print("\tThe contract has already been signed")
                field_to_update = input("Choice: ")
                if field_to_update not in ["1", "2"]:
                    CrudGeneralMessagesView().wrong_input()
                    continue
            return field_to_update

    def event_client_name(self, session, contract_id):
        contract = DALContract().get_contract_by_id(session, contract_id)
        client = DALClient().get_client_of_contract(session, contract)
        return client.full_name

    def event_client_contact_input(self):
        while True:
            contact_input = input(
                "\tClient's contact info (name, phone number, etc.): "
            )
            if len(contact_input) > 100:
                print(
                    f"\n\tERROR: Your text contains {len(contact_input)} characters (max 100). Please try again.\n"
                )
                continue
            return contact_input

    def event_startdate(self):
        while True:
            print("\tStart date of the event (press ENTER to skip that step)")
            year = input("\tYear: ")
            if year.strip() == "":
                return None
            month = input("\tMonth: ")
            day = input("\tDay: ")
            time_hours = input("\tHours: ")
            time_minutes = input("\tMinutes: ")
            custom_date = f"{year}-{month}-{day} {time_hours}:{time_minutes}"

            try:
                custom_date = datetime.strptime(custom_date, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"Error in the date {custom_date}, please try again.")
                continue

            custom_date = str(custom_date)

            if custom_date < str(datetime.now()):
                print("The start date cannot be prior to the current date.")
                continue

            print("Is that date correct?")
            check_time = input(f"\t{custom_date} (y/n): ").casefold()
            if check_time == "y":
                return custom_date
            if check_time == "n":
                continue
            else:
                print("\n\tERROR in the input, please try again.\n")
                continue

    def event_enddate(self, startdate):
        while True:
            print("\tEnd date of the event (press ENTER to skip that step)")
            year = input("\tYear: ")
            if year.strip() == "":
                return None
            month = input("\tMonth: ")
            day = input("\tDay: ")
            time_hours = input("\tHours: ")
            time_minutes = input("\tMinutes: ")
            custom_date = f"{year}-{month}-{day} {time_hours}:{time_minutes}"

            try:
                custom_date = datetime.strptime(custom_date, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"Error in the date {custom_date}, please try again.")
                continue

            startdate = str(startdate)
            custom_date = str(custom_date)

            if custom_date < startdate:
                print("The end date cannot be prior to the start date.")
                continue

            print("Is that date correct?")
            check_time = input(f"\t{custom_date} (y/n): ").casefold()
            if check_time == "y":
                return custom_date
            if check_time == "n":
                continue
            else:
                print("\n\tERROR in the input, please try again.\n")
                continue

    def event_supportid_input(self, session):
        while True:
            support_id = input(
                "\tID of the Support member in charge of that contract (0 if undecided): "
            )
            if support_id == "0":
                return None
            if support_id.isdigit():
                if not CheckObjectExists().check_supportID_exists(session, support_id):
                    CrudEventMessagesView().supportID_not_exist()
                    continue
                return support_id
            print("\n\tERROR: Only digits are allowed.")

    def event_location_input(self):
        while True:
            location_input = input("\tLocation: ")
            if len(location_input) > 100:
                print(
                    f"\n\tERROR: The location contains {len(location_input)} characters (max 100). Please try again.\n"
                )
                continue
            return location_input

    def event_attendees_input(self):
        while True:
            attendees_input = input("\tHow many attendees? ")
            if attendees_input.isdigit():
                return attendees_input
            else:
                print("\n\tERROR: Only digits are allowed.")
                continue

    def event_notes_input(self):
        return input("\tAdditional notes: ")

    def update_event_id(self, session):
        while True:
            event_id = input("\tEvent's ID: ")
            if event_id.isdigit():
                if not CheckObjectExists().check_eventID_exists(session, event_id):
                    CrudEventMessagesView().eventID_not_exist()
                    continue
                return event_id
            print("\n\tERROR: Only digits are allowed.")

    def confirm_event_update_choice(self, session, event_update):
        event_contract = DALContract().get_contractid_of_event(session, event_update)
        contract_client = DALClient().get_client_of_contract(session, event_contract)
        while True:
            print(
                f"\nYou are about to update the event for [{contract_client.full_name}]'s contract (ID: {event_contract.id})."
            )
            confirm_input = input("Please confirm (y/n):\n").casefold()
            if confirm_input == "y":
                return "y"
            elif confirm_input != "n":
                continue
            return False

    def what_to_update_event(self):
        while True:
            print("What would you like to update?")
            print("\t1: Client's contact info")
            print("\t2: Start date")
            print("\t3: End date")
            print("\t4: Assigned Support member")
            print("\t5: Location")
            print("\t6: Number of attendees")
            print("\t7: Notes")
            field_to_update = input("Choice: ")
            if field_to_update not in ["1", "2", "3", "4", "5", "6", "7"]:
                CrudGeneralMessagesView().wrong_input()
                continue
            return field_to_update

    def event_enddate_update(self, event_id, session):
        event = DALEvent().get_event_by_id(session, event_id)
        startdate = event.start_date
        while True:
            print(f"\tEvent's start date: {startdate}.")
            print("\tEnd date of the event (press ENTER to skip that step)")
            year = input("\tYear: ")
            if year.strip() == "":
                return None
            month = input("\tMonth: ")
            day = input("\tDay: ")
            time_hours = input("\tHours: ")
            time_minutes = input("\tMinutes: ")
            custom_date = f"{year}-{month}-{day} {time_hours}:{time_minutes}"

            try:
                custom_date = datetime.strptime(custom_date, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"Error in the date {custom_date}, please try again.")
                continue

            startdate = str(startdate)
            custom_date = str(custom_date)

            if custom_date < startdate:
                print("The end date cannot be prior to the start date.")
                continue

            print("Is that date correct?")
            check_time = input(f"\t{custom_date} (y/n): ").casefold()
            if check_time == "y":
                return custom_date
            if check_time == "n":
                continue
            else:
                print("\n\tERROR in the input, please try again.\n")
                continue

    def crud_password_check_input(self):
        return getpass("Please confirm your password in order to proceed: ")
