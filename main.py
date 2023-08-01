import os.path
from controllers.first_connection import FirstLaunch


# from datetime import datetime

# custom_date = "2023-7-30 15:40:58"
# custom_date = str(datetime.strptime(custom_date, "%Y-%m-%d %H:%M:%S"))
# current_date = datetime.now()
# print(f"current_date: {current_date} /// custom_date: {custom_date}")

# if str(current_date) < custom_date:
#     print("You can't be from the future, can you?")
# else:
#     print("Date OK")

path = "database.ini"
check_file = os.path.isfile(path)
if not check_file:
    FirstLaunch().check_ini_exists()


def main():
    from controllers.database_load_creation import DatabaseCreation
    from controllers.authentication_users import UserAuthentication
    from controllers.menu_management import MenuManagement
    from controllers.menu_admin import MenuAdmin

    auth_menu, username = UserAuthentication().user_authentication()
    if auth_menu == "zupayuzaaa":
        DatabaseCreation().admin_menu(username)
    if auth_menu == 1:
        MenuAdmin().menu_admin(username)
        # MenuManagement().menu_management(username)
    if auth_menu == 2:
        print("Sales Team MENU")
        MenuAdmin().menu_admin(username)
    if auth_menu == 3:
        print("Support Team MENU")


if __name__ == "__main__":
    main()
