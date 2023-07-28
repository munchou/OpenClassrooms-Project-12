from config import config, update_database, create_ini
from views.views_start import StartProgramView

from getpass import getpass

from datetime import datetime

import sqlalchemy
from sqlalchemy import (
    create_engine,
    exc,
    Column,
    Integer,
    Float,
    String,
    Text,
    Boolean,
    DateTime,
    CheckConstraint,
    ForeignKey,
    select,
    update,
)

from sqlalchemy.orm import sessionmaker, declarative_base


while True:
    StartProgramView().print_current_database(params["database"])
    connect_or_exit_input = input(
        "1. YES\n2. CHOOSE ANOTHER DATABASE\n3. EXIT\nChoice: "
    )
    if connect_or_exit_input == "1":
        break
    elif connect_or_exit_input == "2":
        connect_to_db_input = input("Name of the database (must be existing): ")
        update_database(connect_to_db_input)
        params["database"] = connect_to_db_input
        continue
    elif connect_or_exit_input == "3":
        exit()
    else:
        continue

# Create a database

try:
    engine = create_engine(
        f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{'postgres'}"
    )
    conn = engine.connect()
    conn.execute(sqlalchemy.text("COMMIT"))
except Exception:
    print("One or several errors in the provided connection's paramaters.")
    print("Exiting the program.")
    exit()


while True:
    database_to_create = input(
        "Please enter the name of the database you wish to create (NO SPACE ALLOWED!): "
    )
    if database_to_create.strip() == "" or database_to_create == "postgres":
        print("Wrong input, please try again.")
        continue
    else:
        break


try:
    conn.execute(sqlalchemy.text(f"CREATE DATABASE {database_to_create}"))
    print(
        f"* * * * * * * * * *\nDatabase '{database_to_create}' successfully created.\n"
    )
    update_database(database_to_create)
    print("Config file updated successfully.\n")

except exc.ProgrammingError:
    print("Database already exists, skipping that step\n")
    # pass
conn.close()


engine = create_engine(
    f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{database_to_create}"
)
print("Connecting to the postgreSQL database...")

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    phone_number = Column(String(20), nullable=False)
    # status = Column(
    #     String(20),
    #     nullable=False,
    status = Column(
        Integer(),
        CheckConstraint("status >= 0 AND status <= 3"),
        nullable=False,
    )

    def __repr__(self):
        return f"User {self.id}: {self.full_name}, nick: {self.username}, pwd: {self.password}, {self.email}, tel: {self.phone_number}, status:{self.status}"


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer(), primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    phone_number = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    last_contacted = Column(DateTime(), default=datetime.now)
    salesman_in_charge = Column(
        Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )


class Contract(Base):
    __tablename__ = "contract"
    id = Column(Integer(), primary_key=True)
    client = Column(Integer(), ForeignKey("client.id"), nullable=False)
    linked_salesman = Column(Integer(), ForeignKey("users.id"), nullable=True)
    total_amount = Column(Float(), default=0.0)
    amount_due = Column(Float(), default=0.0)
    created_on = Column(DateTime(), default=datetime.now)
    signed = Column(Boolean, default=False)


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer(), primary_key=True)
    contract_id = Column(Integer(), ForeignKey("contract.id"), nullable=False)
    client_name = Column(String(100), nullable=False)
    client_contact = Column(String(100), nullable=False)
    start_date = Column(DateTime(), nullable=True)
    end_date = Column(DateTime(), nullable=True)
    support_contact = Column(Integer(), ForeignKey("users.id"), nullable=True)
    location = Column(String(100), nullable=False)
    attendees = Column(Integer(), nullable=True)
    notes = Column(Text(), nullable=True)


Base.metadata.create_all(bind=engine)
print("Tables successfully created")

# Base.metadata.drop_all(engine)
# print("Tables successfully deleted")

Session = sessionmaker(bind=engine)
session = Session()

# connection = engine.connect()
# test = connection.execute(sqlalchemy.text("SELECT username from users;"))
test = session.query(Users.username).all()
existing_usernames = []
for t in test:
    print(t[0])
    existing_usernames.append(t[0])
print(existing_usernames)


user_confirm = False
while not user_confirm:
    username_input = input("Username: ")
    password_input = getpass("Password: ")
    full_name_input = input("Full name: ")
    email_input = input("email (optional): ")
    phone_number_input = input("Phone number: ")
    status_input = input("Team (1, 2 or 3): ")

    print("\nPlease confirm the new user's details:")
    print(f"Username: {username_input}")
    print(f"Password: {password_input}")
    print(f"Full name: {full_name_input}")
    print(f"email: {email_input}")
    print(f"Phone number: {phone_number_input}")
    print(f"Team: {status_input}")

    while True:
        confirm_input = input("\nConfirm? (y/n)").casefold()
        if confirm_input == "y":
            user_confirm = True
            break
        elif confirm_input != "n":
            continue
        break
    continue


# Let's try adding a user
print("User creation")
user = Users(
    username=username_input,
    password=password_input,
    full_name=full_name_input,
    email=email_input,
    phone_number=phone_number_input,
    status=status_input,
)
session.add(user)
session.commit()
print(f"User {user.username} was successfully created.")


""" USER UPDATE """
# user_update = session.query(Users).filter_by(id=1).first()
# user_update.email = "zupajohn@labidouille.com"
# session.commit()
