from controllers.config import create_ini

from controllers.database_load_creation import DatabaseCreation

from views.views_start import StartProgramView

import os.path


class FirstLaunch:
    def check_ini_exists(self):
        """Check if the INI (= configuration) file exists.
        If not, create the INI file based on the user input
        in the main folder of the program. Then goes to the
        load/creation of the DB.
        If the INI file already exists, skip its creation
        and directly goes to the next step."""
        # path = "database.ini"
        # check_file = os.path.isfile(path)

        # if not check_file:
        StartProgramView().first_prompt()
        config_file = False
        while not config_file:
            config_host_input = StartProgramView().input_config_host()
            config_port_input = StartProgramView().input_config_port()
            while True:
                config_database_input = StartProgramView().input_config_database()
                if config_database_input == "postgres":
                    break
                if config_database_input.strip() == "":
                    StartProgramView().wrong_input()
                    continue
                else:
                    break
            config_user_input = StartProgramView().input_config_user()
            config_password_input = StartProgramView().input_config_password()

            StartProgramView().confirm_config_details(
                config_host_input,
                config_port_input,
                config_database_input,
                config_user_input,
                config_password_input,
            )

            while True:
                confirm_input = StartProgramView().confirm_input()
                if confirm_input == "y":
                    config_file = True
                    break
                elif confirm_input != "n":
                    continue
                break
            continue

        create_ini(
            config_host_input,
            config_port_input,
            config_database_input,
            config_user_input,
            config_password_input,
        )

        DatabaseCreation().create_load_database()
