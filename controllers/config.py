from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create parser
    parser = ConfigParser()

    # read config file
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} was not found in the {filename}")

    return db


def create_ini(
    config_host_input,
    config_port_input,
    config_database_input,
    config_user_input,
    config_password_input,
    filename="database.ini",
):
    parser = ConfigParser()
    parser.add_section("postgresql")
    parser.set("postgresql", "host", config_host_input)
    parser.set("postgresql", "port", config_port_input)
    parser.set("postgresql", "database", config_database_input)
    parser.set("postgresql", "user", config_user_input)
    parser.set("postgresql", "password", config_password_input)

    with open(filename, "w") as configfile:
        parser.write(configfile)


def ini_update_database(new_database, filename="database.ini"):
    parser = ConfigParser()
    parser.read(filename)
    parser.set("postgresql", "database", new_database)

    with open(filename, "w") as configfile:
        parser.write(configfile)
