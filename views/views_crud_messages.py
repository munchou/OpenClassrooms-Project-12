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
    def creation_successful(client):
        print(f"Client {client.full_name} was successfully created.")


class CrudContractMessagesView:
    def __init__(self):
        pass


class CrudEventMessagesView:
    def __init__(self):
        pass


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
