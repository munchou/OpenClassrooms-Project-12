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
        print("*")
        print(f"* AUTHENTICATION to database '{current_database}'")
        print("*\n")

        username_input = input("\tusername: ")
        password_input = getpass("\tpassword: ")
        return username_input, password_input

    def admin_menu(self, username):
        while True:
            print(f"WECOME, {username}")
            print("* " * 16)
            print("\t1. Create a user")
            print("\t2. Update a user")
            print("\t3. Delete a user")
            print("\t4. Create/Update a database")
            print("\t5. Remove all the database's table")

            menu_choice = input("Your choice: ")
            if menu_choice in ["1", "2", "3", "4", "5"]:
                return menu_choice
            else:
                print("\n\tERROR: Please enter an existing menu.\n")
                continue

    @staticmethod
    def user_auth_error():
        print(
            "\n\tERROR: Either the user does not exist or the password is wrong. Please try again.\n"
        )

    def user_team_management(self, username):
        print(f"{username} is in the Management Team")

    def user_team_sales(self, username):
        print(f"{username} is in the Sales Team")

    def user_team_support(self, username):
        print(f"{username} is in the Support Team")

    def crud_password_check_wrong(self):
        print("Wrong password, you are going to be disconnected.")
        while True:
            enter_input = input("Press ENTER to continue. ")
            if enter_input == "":
                break
            continue
