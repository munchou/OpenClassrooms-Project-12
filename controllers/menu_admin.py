from controllers.data_access_layer import DALSession
from controllers.utils import Utils
from controllers.crud_user import CrudUser
from controllers.crud_client import CrudClient
from controllers.crud_contract import CrudContract
from controllers.crud_event import CrudEvent


class MenuAdmin:
    session = Utils().session_init()

    def menu_admin(self, username):
        Utils.clear_screen()
        print("Hello, God. What will it be today?")
        print("\t1. Create a user (management team)")  # OK
        print("\t2. Update a user (management team)")  # OK
        print("\t3. Delete a user (management team)")  # OK
        print("\t4. Create a client (sales team)")  # OK
        print("\t5. Update a client (salesman in charge of the client)")  # OK
        print("\t6. Display all clients (all the teams)")  # OK
        print("\t7. Create a contract (management team)")  # OK
        print(
            "\t8. Update a contract (management + salesman in charge of the client)"
        )  # OK
        print("\t9. Display all the contracts (all the teams)")  # OK
        print("\t10. Display contracts that haven't been signed yet (sales team)")  # OK
        print("\t11. Display contracts that haven't been fully paid (sales team)")  # OK
        print("\t12. Create an event (salesman in charge of the client)")  # OK
        print("\t13. Display events without support staff (management team)")  # OK
        print("\t14. Update an event to add support staff (management team)")  # OK
        print("\t15. Update an event (support member in charge of it)")  # OK
        print("\t16. Display events the support member is in charge of (support)")  # OK
        print("\t17. Display all the events (all the teams)")  # OK
        print("\n\tquit. DISCONNECT and go back to authentication")  # OK

        management_choice = input("Choice: ")

        if management_choice == "1":
            CrudUser().user_create(self.session)

        if management_choice == "2":
            CrudUser().user_update(self.session)

        if management_choice == "3":
            CrudUser().user_delete(self.session)

        if management_choice == "4":
            CrudClient().client_create(self.session, username)

        if management_choice == "5":
            CrudClient().client_update(self.session)

        if management_choice == "6":
            CrudClient().client_display_all(self.session)

        if management_choice == "7":
            CrudContract().contract_create(self.session)

        if management_choice == "8":
            CrudContract().contract_update(self.session)

        if management_choice == "9":
            CrudContract().contract_display_all(self.session)

        if management_choice == "10":
            CrudContract().contract_display_not_signed(self.session)

        if management_choice == "11":
            CrudContract().contract_display_not_paid(self.session)

        if management_choice == "12":
            CrudEvent().event_create(self.session)

        if management_choice == "13":
            CrudEvent().event_display_no_support(self.session)

        if management_choice == "14":
            CrudEvent().event_update_add_support(self.session)

        if management_choice == "15":
            CrudEvent().event_update(self.session)

        if management_choice == "16":
            CrudEvent().event_display_for_supportincharge(self.session, username)

        if management_choice == "17":
            CrudEvent().event_display_all(self.session)

        if management_choice == "quit":
            DALSession().session_close(self.session)
            from main import main  # To avoid the idiotic circular import error...

            main()
