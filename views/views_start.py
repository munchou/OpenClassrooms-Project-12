from getpass import getpass


class StartProgramView:
    def __init__(self):
        pass

    @staticmethod
    def first_prompt():
        print("Configuration file not found. Let's create one.")
        print("IMPORTANT: Leave empty for default value (simply press ENTER)")
        print(
            "Unless specified, it is strongly advised to use the default settings. You only must enter your password.\n"
        )

    def input_config_host(self):
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
        while True:
            pwd = getpass("\tPASSWORD (the one used when PostgreSQL was installed): ")
            pwd_repeat = getpass("\tRepeat the password: ")
            if pwd == pwd_repeat:
                return pwd
            print("The passwords did not match, please try again.")
            continue

    def confirm_config_details(
        self,
        config_host_input,
        config_port_input,
        config_database_input,
        config_user_input,
        config_password_input,
    ):
        print("\nPlease confirm the configuration details:")
        print(f"Host: {config_host_input}")
        print(f"Port: {config_port_input}")
        print(f"Database's name: {config_database_input}")
        print(f"User: {config_user_input}")
        print(f"Password: {'*'*(len(config_password_input))}")

    def confirm_input(self):
        choice = input("\nConfirm? (y/n) ").casefold()
        if choice == "y":
            return "y"
        elif choice != "n":
            print("Y or N")
            return None
        else:
            print("\nPlease fill in the configuration details: ")
            return "n"

    @staticmethod
    def currentdb_is_postgres():
        print(
            "Because the current database is 'postgres', you must choose another one or create a new database."
        )

    def current_db_display(self, database):
        print(f"\nCurrent database: '{database}'.")

    def print_connect_to_database(self, database):
        print(f"\nCurrent database: '{database}'. Connect to it?")

    def create_database_or_exit(self):
        create_or_exit = input(
            "\t1. Create a new database or load a different one\n\t8. Exit\n\tChoice: "
        )
        if create_or_exit == "1":
            return "1"
        elif create_or_exit == "8":
            return "8"
        else:
            print("ERROR: Wrong input\n")

    @staticmethod
    def wrong_input():
        print("\nWrong input, please try again.\n")

    def tables_delete_confirm(self, current_databse):
        while True:
            confirm_input = input(
                f"Delete the tables from database {current_databse} (y/n)? "
            ).casefold()

            if confirm_input == "y":
                return "delete"
            elif confirm_input == "n":
                return "no"
            else:
                self.wrong_input()
                continue
