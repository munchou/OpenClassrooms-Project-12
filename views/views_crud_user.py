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
            checked_input = self.check_input_characters(username_input)
            if checked_input != "input_passed":
                print(
                    "\nERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
                continue

            return username_input

    def username_input_update(self):
        while True:
            username_input = input("\tusername: ")
            checked_input = self.check_input_characters(username_input)
            if checked_input != "input_passed":
                print(
                    "\nERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
                continue

            return username_input

    def password_input(self):
        while True:
            pwd = getpass("\tPassword (at least 8 characters): ")

            checked_input = self.check_input_characters(pwd)
            if checked_input != "input_passed":
                continue

            if len(pwd) < 8:
                print(
                    f"\n\tERROR: Your password contains {len(pwd)} characters. Please try again"
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
        return input("\tFull name: ")

    def email_input(self, username):
        while True:
            email_input = input("\temail (optional, press ENTER if no email): ")
            if email_input == "":
                return f"{username}_no_email"
            if self.check_input_characters(email_input) != "input_passed":
                print(
                    "\nERROR in the input, please enter only valid characters, NO SPACE ALLOWED.\n"
                )
                continue

            return email_input

    def phonenumber_input(self):
        return input("\tTelephone number: ")

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
                return "supportu"
            else:
                print("Input error, please try again.")
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
        input("Please enter the ID of the user you wish to update: ")
        # if user_id.isdigit():
        #     return user_id

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


# user_confirm = False
# while not user_confirm:
#     username_input = input("Username: ")
#     password_input = getpass("Password: ")
#     full_name_input = input("Full name: ")
#     email_input = input("email (optional): ")
#     phone_number_input = input("Phone number: ")
#     status_input = input("Team (1, 2 or 3): ")

#     print("\nPlease confirm the new user's details:")
#     print(f"Username: {username_input}")
#     print(f"Password: {password_input}")
#     print(f"Full name: {full_name_input}")
#     print(f"email: {email_input}")
#     print(f"Phone number: {phone_number_input}")
#     print(f"Team: {status_input}")

#     while True:
#         confirm_input = input("\nConfirm? (y/n)").casefold()
#         if confirm_input == "y":
#             user_confirm = True
#             break
#         elif confirm_input != "n":
#             continue
#         break
#     continue


# # Let's try adding a user
# print("User creation")
# user = Users(
#     username=username_input,
#     password=password_input,
#     full_name=full_name_input,
#     email=email_input,
#     phone_number=phone_number_input,
#     status=status_input,
# )
# session.add(user)
# session.commit()
# print(f"User {user.username} was successfully created.")
