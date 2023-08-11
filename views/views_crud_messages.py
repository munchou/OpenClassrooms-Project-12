from models import models


from controllers.data_access_layer import (
    DALUser,
    DALClient,
    DALContract,
    DALEvent,
)


class CrudUserMessagesView:
    def __init__(self):
        pass

    @staticmethod
    def creation_title():
        print("CREATION OF A USER:")

    def user_confirmation(self, username, fullname, email, phone, status):
        print("\nPlease confirm the new user's details:")
        print(f"\tUsername: {username}")
        print(f"\tFull name: {fullname}")
        print(f"\temail: {email}")
        print(f"\tPhone number: {phone}")
        print(f"\tTeam: {status}")

    @staticmethod
    def creation_successful(user):
        print(f"User {user.username} was successfully created.")

    @staticmethod
    def update_successful():
        print("The user was updated successfully.")

    def remove_user_sucess(self, user):
        print(f"{user.username} (ID: {user.id}) was successfully deleted.")


class CrudClientMessagesView:
    def __init__(self):
        pass

    @staticmethod
    def creation_title():
        print("CREATION OF A CLIENT:")

    def client_confirmation(self, fullname, email, phone, company, lastcontacted):
        print("\nPlease confirm the new client's details:")
        print(f"\tFull name: {fullname}")
        print(f"\temail: {email}")
        print(f"\tPhone number: {phone}")
        print(f"\tCompany name: {company}")
        print(f"\tLast contacted: {lastcontacted}")

    @staticmethod
    def creation_successful(client):
        print(f"Client {client.full_name} was successfully created.")

    @staticmethod
    def not_salesmans_in_charge():
        print(
            "You are not in charge of that client, please try again with another one."
        )
        # while True:
        #     print("\n\tERROR: The contract your referred to has NOT been signed yet.")
        #     press_enter = input("\tPress ENTER to go back to the authentication menu. ")
        #     if press_enter.strip() == "":
        #         break
        #     continue

    @staticmethod
    def update_successful():
        print("The client was updated successfully.")

    def client_display_all(self, session, clients):
        for client in clients:
            print(f"Client ID: {client.id} | {client.full_name}")
            print(f"\temail: {client.email}")
            print(f"\tPhone number: {client.phone_number}")
            print(f"\tName of the company: {client.company_name}")
            print(f"\tDate of creation: {client.created_on}")
            print(f"\tLast contacted: {client.last_contacted}")
            salesman_in_charge = DALUser().get_user_by_id(
                session, client.salesman_in_charge
            )
            print(
                f"\tSalesman in charge: {salesman_in_charge.full_name} (ID: {salesman_in_charge.id})\n"
            )


class CrudContractMessagesView:
    def __init__(self):
        pass

    @staticmethod
    def creation_title():
        print("CREATION OF A CONTRACT:")

    @staticmethod
    def contractID_not_exist():
        print("\n\tERROR: That ID does not match any contracts. Please try again.")

    @staticmethod
    def clientID_not_exist():
        print("\n\tERROR: That ID does not match any clients. Please try again.")

    @staticmethod
    def salesmanID_not_exist():
        print("\n\tERROR: That ID does not match any salesman. Please try again.")

    @staticmethod
    def salesmanID_bad_id():
        print(
            "\n\tERROR: You must enter the ID of the salesman in charge of the client. Please try again."
        )

    def contract_confirmation(
        self, client_id, salesman, total_amount, amount_due, signed
    ):
        print("\nPlease confirm the new contract's details:")
        print(f"\tClient's ID: {client_id}")
        print(f"\tSalesman in charge of the contract: {salesman}")
        print(f"\tContract's total amount: {total_amount}")
        print(f"\tDue amount: {amount_due}")
        if signed:
            print("\tThe contract has been signed.")
        elif not signed:
            print("\tThe contract has NOT been signed.")

    @staticmethod
    def creation_successful():
        print("The contract was successfully created.")

    def contract_display_all(self, session, contracts):
        for contract in contracts:
            client = DALClient().get_client_by_id(session, contract.client)
            print(f"\tContract ID: {contract.id} | {client.full_name}")
            salesman_in_charge = DALUser().get_user_by_id(
                session, contract.linked_salesman
            )
            print(
                f"\tSalesman in charge: {salesman_in_charge.full_name} (ID: {salesman_in_charge.id})"
            )
            print(f"\tContract amount: {contract.total_amount}")
            print(f"\tRemaining to pay: {contract.amount_due}")
            print(f"\tDate of creation: {contract.created_on}")
            if not contract.signed:
                contract_signed = "The contract has NOT been signed yet."
            if contract.signed:
                contract_signed = "The contract has been signed."
            print(f"\t{contract_signed}\n")

    def contract_display_not_signed(self, session, contracts):
        print("\tCONTRACTS THAT HAVEN'T BEEN SIGNED YET:\n")
        for contract in contracts:
            if not contract.signed:
                client = DALClient().get_client_by_id(session, contract.client)
                print(f"Contract ID: {contract.id} | {client.full_name}")
                salesman_in_charge = DALUser().get_user_by_id(
                    session, contract.linked_salesman
                )
                print(
                    f"\tSalesman in charge: {salesman_in_charge.full_name} (ID: {salesman_in_charge.id})"
                )
                print(f"\tContract amount: {contract.total_amount}")
                print(f"\tRemaining to pay: {contract.amount_due}")
                print(f"\tDate of creation: {contract.created_on}\n")

    def contract_display_not_paid(self, session, contracts):
        print("\tCONTRACTS THAT HAVEN'T BEEN FULLY PAID YET:\n")
        for contract in contracts:
            if contract.amount_due > 0:
                client = DALClient().get_client_by_id(session, contract.client)
                print(f"Contract ID: {contract.id} | {client.full_name}")
                salesman_in_charge = DALUser().get_user_by_id(
                    session, contract.linked_salesman
                )
                print(
                    f"\tSalesman in charge: {salesman_in_charge.full_name} (ID: {salesman_in_charge.id})"
                )
                print(f"\tContract amount: {contract.total_amount}")
                print(f"\tRemaining to pay: {contract.amount_due}")
                print(f"\tDate of creation: {contract.created_on}")
                if not contract.signed:
                    contract_signed = "The contract has NOT been signed yet."
                if contract.signed:
                    contract_signed = "The contract has been signed."
                print(f"\t{contract_signed}\n")

    @staticmethod
    def update_successful():
        print("The contract was updated successfully.")


class CrudEventMessagesView:
    def __init__(self):
        pass

    @staticmethod
    def creation_title():
        print("CREATION OF AN EVENT:")

    @staticmethod
    def contract_not_signed():
        while True:
            print("\n\tERROR: The contract your referred to has NOT been signed yet.")
            press_enter = input("\tPress ENTER to go back to the authentication menu. ")
            if press_enter.strip() == "":
                break
            continue

    def event_confirmation(
        self,
        contract_id,
        client_name,
        client_contact,
        start_date,
        end_date,
        support_contact,
        location,
        attendees,
        notes,
    ):
        print("\nPlease confirm the new event's details:")
        print(f"\tContract's ID: {contract_id}")
        print(f"\tClient: {client_name}")
        print(f"\tClient's contact information: {client_contact}")
        print(f"\tStarts on: {start_date}")
        print(f"\tEnds: {end_date}")
        print(f"\tSupport member's ID: {support_contact}")
        print(f"\tLocation: {location}")
        print(f"\tNumber of attendees: {attendees}")
        print(f"\tNotes: {notes}")

    @staticmethod
    def supportID_not_exist():
        print("\n\tERROR: That ID does not match any support member. Please try again.")

    @staticmethod
    def creation_successful():
        print(f"The event was successfully created.")

    @staticmethod
    def support_update_successful():
        print("The event's assigned support member was updated successfully.")

    @staticmethod
    def update_successful():
        print("The event was updated successfully.")

    @staticmethod
    def eventID_not_exist():
        print("\n\tERROR: That ID does not match any events. Please try again.")

    def event_display_all(self, session, events):
        print("Events without an assigned Support member:")
        for event in events:
            print(f"\tEvent ID: {event.id}")
            print(f"\tRelated to contract ID: {event.contract_id}")
            print(f"\tClient: {event.client_name}")
            print(f"\tClient's contact information: {event.client_contact}")
            print(f"\tStart date: {event.start_date}")
            print(f"\tEnd date: {event.end_date}")
            support_in_charge = DALUser().get_user_by_id(session, event.support_contact)
            print(
                f"\tSupport member in charge: {support_in_charge.full_name} (ID: {support_in_charge.id})"
            )
            print(f"\tLocation: {event.location}")
            print(f"\tAttendees: {event.attendees}")
            print(f"\tNotes: {event.notes}\n")

    def event_display_no_support(self, events):
        print("Events without an assigned Support member:")
        for event in events:
            if event.support_contact is None:
                print(f"\tEvent ID: {event.id}")
                print(f"\tRelated to contract ID: {event.contract_id}")
                print(f"\tClient: {event.client_name}")
                print(f"\tClient's contact information: {event.client_contact}")
                print(f"\tStart date: {event.start_date}")
                print(f"\tEnd date: {event.end_date}")
                print(f"\tLocation: {event.location}")
                print(f"\tAttendees: {event.attendees}")
                print(f"\tNotes: {event.notes}\n")

    def event_display_for_supportincharge(self, session, events):
        if len(events) == 0:
            return print("You do not have any assigned events.")

        print("Events your are assigned to:")
        for event in events:
            print(f"\tEvent ID: {event.id}")
            print(f"\tRelated to contract ID: {event.contract_id}")
            print(f"\tClient: {event.client_name}")
            print(f"\tClient's contact information: {event.client_contact}")
            print(f"\tStart date: {event.start_date}")
            print(f"\tEnd date: {event.end_date}")
            support_in_charge = DALUser().get_user_by_id(session, event.support_contact)
            print(
                f"\tSupport member in charge: {support_in_charge.full_name} (ID: {support_in_charge.id})"
            )
            print(f"\tLocation: {event.location}")
            print(f"\tAttendees: {event.attendees}")
            print(f"\tNotes: {event.notes}\n")


class CrudGeneralMessagesView:
    def __init__(self):
        pass

    @staticmethod
    def wrong_input():
        print("\n\tERROR: Wrong input, please try again.\n")

    @staticmethod
    def user_not_exist():
        print("That user does not exist.")

    def already_exists(self):
        print(f"Already used, please type in something else.\n")

    def confirm_update_choice(self, user_update):
        while True:
            print(f"\nYou are about to update '{user_update.username}'.")
            confirm_input = input("Please confirm (y/n):\n").casefold()
            if confirm_input == "y":
                return "y"
            elif confirm_input != "n":
                continue
            return False

    @staticmethod
    def press_enter_to_menu():
        while True:
            press_enter = input("\tPress ENTER to go back to your menu. ")
            if press_enter.strip() == "":
                break
            continue
