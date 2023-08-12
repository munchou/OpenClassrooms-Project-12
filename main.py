import os.path
from controllers.first_connection import FirstLaunch
import sentry_sdk


sentry_sdk.init(
    dsn="https://c0eb8866f5695f4f48d3856d010b9129@o4505691007680512.ingest.sentry.io/4505691010367488",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)


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
    if auth_menu == "exit":
        exit()


if __name__ == "__main__":
    main()
