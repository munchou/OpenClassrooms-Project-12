from getpass import getpass
import secrets, random, hashlib


class CrudUserView:
    def __init__(self):
        pass

    @staticmethod
    def creation_title():
        print("CREATION OF A USER:")

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

    def username_input(self):
        while True:
            username_input = input("\tusername: ")
            if len(username_input) > 50:
                print(
                    "\n\tERROR: The username cannot contain than 50 characters. Please try again.\n"
                )
                continue
            checked_input = self.check_input_characters(username_input)
            if checked_input != "input_passed":
                print(
                    "\n\tERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
                continue

            return username_input

    def username_input_update(self):
        while True:
            username_input = input("\tusername: ")
            if len(username_input) > 50:
                print(
                    "\n\tERROR: The username cannot contain than 50 characters. Please try again.\n"
                )
                continue
            checked_input = self.check_input_characters(username_input)
            if checked_input != "input_passed":
                print(
                    "\n\tERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
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
            return fullname_input

    def email_input(self, username):
        while True:
            email_input = input("\temail (optional, press ENTER if no email): ")
            if len(email_input) > 100:
                print(
                    "\n\tERROR: the enail cannot contain more than 100 characters. Please try again.\n"
                )
                continue
            if email_input == "":
                return f"{username}_no_email"
            if self.check_input_characters(email_input) != "input_passed":
                print(
                    "\n\tERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
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

    def user_confirmation(self, username, fullname, email, phone, status):
        print("\nPlease confirm the new user's details:")
        print(f"\tUsername: {username}")
        print(f"\tFull name: {fullname}")
        print(f"\temail: {email}")
        print(f"\tPhone number: {phone}")
        print(f"\tTeam: {status}")

    def confirm_creation(self):
        while True:
            confirm_input = input("\nConfirm? (y/n)\n").casefold()
            if confirm_input == "y":
                return True
            elif confirm_input != "n":
                continue
            return False

    @staticmethod
    def creation_successful(user):
        print(f"User {user.username} was successfully created.")

    def update_user_id_input(self):
        user_id = input("Please enter the ID of the user you wish to update: ")
        # if user_id.isdigit():
        return user_id

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
    def update_successful():
        print("The user was updated successfully.")

    def remove_user_id_input(self):
        while True:
            user_id = input("Please enter the ID of the user you wish to remove: ")
            if user_id.isdigit():
                return user_id
            print("Bad input, try again")
            continue

    def remove_user_confirm_deletion(self, user):
        while True:
            confirm_deletion = input(
                f"Do you confirm the deletion of {user.username} (ID: {user.id}) (y/n)? "
            ).casefold()
            if confirm_deletion == "y":
                return "y"
            elif confirm_deletion == "n":
                return "n"
            print("Input error, please try again.")
            continue

    def remove_user_sucess(self, user):
        print(f"{user.username} (ID: {user.id}) was successfully deleted.")
