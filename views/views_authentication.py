from getpass import getpass


class AuthenticationView:
    def __init__(self):
        pass

    def input_config_host(self):
        print("\nADMIN AUTHENTICATION")
        print("*" * 20)
        config_host_input = input("\tHost (default: localhost): ")
        if config_host_input == "":
            return "localhost"
        else:
            return config_host_input

    def input_config_port(self):
        config_port_input = input("\tPort (default: 5432): ")
        if config_port_input == "":
            return "5432"
        else:
            return config_port_input

    def input_config_database(self):
        config_database_input = input("\tDatabase's name (default: postgres): ")
        for character in config_database_input:
            if character == " ":
                return " "
        if config_database_input == "":
            return "postgres"
        else:
            return config_database_input

    def input_config_user(self):
        config_user_input = input("\tUser (default: postgres): ")
        if config_user_input == "":
            return "postgres"
        else:
            return config_user_input

    def input_config_password(self):
        return getpass("\tPASSWORD (the one used when PostgreSQL was installed): ")

    @staticmethod
    def authentication_error():
        print("\nError while trying to connect, please try again.\n")
        # print("Press any key to exit the program.")
        # _ = getch()
        # exit()

    def input_user(self, current_database):
        full_title = f"* AUTHENTICATION to database '{current_database}' *"
        auth_len = len(full_title)
        if auth_len % 2 == 0:
            auth_len = int(auth_len / 2)
        else:
            auth_len = int(auth_len / 2) + 1
        print("* " * auth_len)
        print(full_title)
        print("* " * auth_len)

        print("(type 'exit' as the username to exit the program)\n")
        username_input = input("\tusername: ")
        if username_input == "exit":
            return username_input, ""
        password_input = getpass("\tpassword: ")
        return username_input, password_input

    def admin_menu(self):
        from controllers.utils import Utils

        Utils().clear_screen()
        while True:
            print("Hello, God. What will it be today?")
            print("\tdb_update. Create/Update a database")
            print("\tdb_removetables. Remove all the database's table")
            print("\n\t1. Create a user (management team)")
            print("\t2. Update a user (management team)")
            print("\t3. Deactivate a user (management team)")
            print("\t4. Create a client (sales team)")
            print("\t5. Update a client (salesman in charge of the client)")
            print("\t6. Display all clients (all the teams)")
            print("\t7. Create a contract (management team)")
            print(
                "\t8. (unavailable for admin) Update a contract (management + salesman in charge of the client)"
            )
            print("\t9. Display all the contracts (all the teams)")
            print("\t10. Display contracts that haven't been signed yet (sales team)")
            print("\t11. Display contracts that haven't been fully paid (sales team)")
            print("\t12. Create an event (salesman in charge of the client)")
            print("\t13. Display events without support staff (management team)")
            print("\t14. Update an event to add support staff (management team)")
            print("\t15. Update an event (support member in charge of it)")
            print("\t16. Display events the support member is in charge of (support)")
            print("\t17. Display all the events (all the teams)")
            print("\n\tdisconnect. DISCONNECT and go back to authentication")

            menu_choice = input("Your choice: ")
            if menu_choice in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "db_update",
                "db_removetables",
                "disconnect",
            ]:
                return menu_choice
            else:
                print("\n\tERROR: Please enter an existing menu.\n")
                continue

    @staticmethod
    def user_auth_error():
        print(
            "\n\tERROR: Either the user does not exist or the password is wrong. Please try again.\n"
        )

    # def user_team_management(self, username):
    #     print(f"{username} is in the Management Team")

    # def user_team_sales(self, username):
    #     print(f"{username} is in the Sales Team")

    # def user_team_support(self, username):
    #     print(f"{username} is in the Support Team")

    def crud_password_check_wrong(self):
        print("Wrong password, you are going to be disconnected.")
        while True:
            enter_input = input("Press ENTER to continue. ")
            if enter_input == "":
                break
            continue
