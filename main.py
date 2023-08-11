import os.path
from controllers.first_connection import FirstLaunch

path = "database.ini"
check_file = os.path.isfile(path)
if not check_file:
    FirstLaunch().create_ini()


def main():
    from controllers.authentication_users import UserAuthentication
    from controllers.menu_management import MenuManagement
    from controllers.menu_sales import MenuSales
    from controllers.menu_support import MenuSupport
    from controllers.menu_admin import MenuAdmin

    auth_menu, username = UserAuthentication().user_authentication()
    if auth_menu == "zupayuzaaa":
        MenuAdmin().menu_admin(username)
    if auth_menu == 1:
        MenuManagement().menu_management(username)
    if auth_menu == 2:
        MenuSales().menu_sales(username)
    if auth_menu == 3:
        MenuSupport().menu_support(username)


if __name__ == "__main__":
    main()
