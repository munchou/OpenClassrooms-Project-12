import os
from getpass import getpass


class LoadCreateDBView:
    def __init__(self):
        pass

    @staticmethod
    def wrong_input():
        print("\nWrong input, please try again.\n")

    @staticmethod
    def create_db_error():
        print(
            "There are one or several errors in the provided connection's parameters."
        )
        print(
            "Deleting the configuration file. Please restart the program and create a new config file."
        )
        os.remove("database.ini")
        while True:
            if getpass("Press ENTER to quit: ") == "":
                exit()

    @staticmethod
    def config_file_updated():
        print("Config file updated successfully.\n")

    def load_or_create_database_name(self, current_database):
        print("*" * 16)
        print(f"Current database: {current_database}")
        print("*" * 16)

        while True:
            print("- Please enter the name of the database you wish to load or create.")
            print(
                f"- Leave blank and simply press ENTER to use the current database ('{current_database}')."
            )
            print("- Regarding CREATION:")
            print(
                "\tOnly alphabet characters (letters aA, bB, cC...), digits (0, 1, 2...), and [@ _ $ #]."
            )
            print("\tNO SPACES ALLOWED!")
            print("\tMaximum length: 20 characters\n")

            # allowed_characters = "abcdefghijklmnopqrstuvwxyz0123456789"
            allowed_characters = "@_$#"
            database_input = input("\tdatabase: ")
            if len(database_input) > 20:
                print(
                    "\n\tERROR: The name of the database contains more than 20 characters. Please try again.\n"
                )
                continue
            elif database_input == "":
                return current_database

            else:
                input_is_ok = True
                for character in database_input:
                    # if character.isalpha() or character.isdigit():
                    if (
                        character.isalpha()
                        or character.isdigit()
                        or character in allowed_characters
                    ):  # in allowed_characters:
                        # print(f"Chara {character} OK")
                        continue
                    else:
                        print(
                            "\n* * FORBIDDEN CHARACTER IN YOUR INPUT. PLEASE TYPE AGAIN.\n"
                        )
                        input_is_ok = False
                        break
                if input_is_ok:
                    return database_input
                continue
            # else:
            #     return database_input

    def database_created(self, database):
        print(f"* * * * * * * * * *\nDatabase '{database}' successfully created.\n")

    @staticmethod
    def database_already_exists():
        print("\nThe database already exists, connecting to it.\n")

    def connected_to_database(self, database):
        print(f"Connected to '{database}'.\n")
