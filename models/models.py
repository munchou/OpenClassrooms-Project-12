from datetime import datetime

import enum

from sqlalchemy import (
    Column,
    Enum,
    Integer,
    Float,
    String,
    Text,
    Boolean,
    DateTime,
    CheckConstraint,
    ForeignKey,
)

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

"""class Collaborator(Base):

    class RoleEnum(enum.Enum):
        administrator = 1
        seller = 2
        support = 3

        def __json__(self):
            return self.value

    __tablename__ = 'collaborators'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(length=50))
    lastname = Column(String(length=50))
    email = Column(String(length=50), unique=True)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String(length=60)) # The hashed password will always be 60 characters
    token = Column(String)
    token_expiration = Column(DateTime)
    customers = relationship("Customer", back_populates="collaborator", cascade="all, delete")
    events = relationship("Event", back_populates="collaborator", cascade="all, delete")

    def __init__(self, firstname, lastname, email, role, password):
        self.set_firstname(firstname)
        self.set_lastname(lastname)
        self.set_email(email)
        self.set_role(role)
        self.set_password(password)"""


class Users(Base):
    class StatusEnum(enum.Enum):
        management = 1
        sales = 2
        support = 3

    __tablename__ = "users"
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone_number = Column(String(20), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    saltychain = Column(String(200), unique=True, nullable=False)

    def __repr__(self):
        return f"User {self.id}: {self.full_name}, nick: {self.username}, pwd: {self.password}, {self.email}, tel: {self.phone_number}, status:{self.status}"


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer(), primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone_number = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    last_contacted = Column(DateTime(), default=datetime.now)
    salesman_in_charge = Column(Integer(), ForeignKey("users.id"), nullable=True)


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
