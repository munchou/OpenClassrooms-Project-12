import os.path
from controllers.first_connection import FirstLaunch


def main():
    path = "database.ini"
    check_file = os.path.isfile(path)
    if not check_file:
        FirstLaunch().check_ini_exists()
    connect()


from controllers.database_load_creation import DatabaseCreation
from controllers.authentication_users import UserAuthentication
from controllers.menu_management import MenuManagement


def connect():
    # path = "database.ini"
    # check_file = os.path.isfile(path)
    # if not check_file:
    #     FirstLaunch().check_ini_exists()
    FirstLaunch().check_ini_exists()

    auth_menu, username = UserAuthentication().user_authentication()
    if auth_menu == "zupayuzaaa":
        DatabaseCreation().admin_menu(username)
    if auth_menu == 1:
        MenuManagement().menu_management(username)
    if auth_menu == 2:
        print("Sales Team MENU")
    if auth_menu == 3:
        print("Support Team MENU")


if __name__ == "__main__":
    main()
