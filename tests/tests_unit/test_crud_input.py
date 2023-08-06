from sqlalchemy import exc
from models import models
from datetime import datetime

from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudUserMessagesView

from controllers.utils import Utils
from controllers.data_access_layer import DALSession, DALUser
from controllers.check_object_exists import CheckObjectExists

import secrets, random, hashlib


class TestCrudInputs:
    def test_check_input_characters(self, input_to_check="This#is_a_v@alid_text!"):
        input_is_ascii = True
        if input_to_check.isascii():
            for chara in input_to_check:
                if chara == " ":
                    input_is_ascii = False

        input_to_checkbis = "This text has spaces oh noooo!"
        input_is_asciibis = True
        if input_to_checkbis.isascii():
            for chara in input_to_checkbis:
                if chara == " ":
                    input_is_asciibis = False

        assert input_is_ascii == True
        assert input_is_asciibis == False

    def test_check_if_input_empty(self, input_to_check="    "):
        if input_to_check == "" or input_to_check.strip() == "":
            print("\n\tThis field is required, please type in something.\n")
            returnee = True
        else:
            returnee = False
        assert returnee == True

    def test_check_if_input_empty_false(
        self, input_to_check="This is not an empty field"
    ):
        if input_to_check == "" or input_to_check.strip() == "":
            print("\n\tThis field is required, please type in something.\n")
            returnee = True
        else:
            returnee = False

        assert returnee == False

    def test_username_input(self, session):
        empty_input = False
        user_exists = False

        username_input = "dgdg45yhrft"

        if len(username_input) > 50:
            print(
                "\n\tERROR: The username cannot contain than 50 characters. Please try again.\n"
            )

        if CheckObjectExists().check_username_exists(session, username_input):
            user_exists = True

        assert empty_input == False
        assert user_exists == False

    def test_password_input(self):
        pwd = "qqqqqqqq"
        pwd_repeat = "qqqqqqqq"

        assert pwd == pwd_repeat

    def test_password_input_fail(self):
        pwd = "qqqqqqqq"
        pwd_repeat = "qqqqgqqq"

        assert pwd != pwd_repeat

    def test_fullname_input(self):
        fullname_input = "Full name"

        assert fullname_input == "Full name"

    def test_email_input(self, session):
        email_exists = False
        email_input = "hellowello@email.com"
        email_input_empty = ""
        email_input_exists = "user1@testouille.com"

        if email_input_empty == "":
            email_empty = "no_email@secret98743token"

        if CheckObjectExists().check_email_user_exists(session, email_input_exists):
            email_exists = True

        assert email_input == "hellowello@email.com"
        assert email_empty == "no_email@secret98743token"
        assert email_exists == True

        session.rollback()

    def test_phonenumber_input(self):
        too_long = False
        phone_input = "+33245689745"
        phone_input_long = "+012345714571654615460065484685"
        if len(phone_input_long) > 20:
            too_long = True

        assert phone_input == "+33245689745"
        assert too_long == True

    def test_status_input(self):
        error = False
        status_input = "1"
        if status_input == "1":
            management = 1
        status_input = "2"
        if status_input == "2":
            sales = 2
        status_input = "3"
        if status_input == "3":
            support = 3
        status_input = "osijhf90843"
        if status_input not in ["1", "2", "3"]:
            error = True

        assert management == 1
        assert sales == 2
        assert support == 3
        assert error == True

    def test_company_name_input(self):
        bad_input = False
        company_name_input = "Name of the Company"
        if len(company_name_input) > 100 or company_name_input.strip() == "":
            bad_input = True
        assert bad_input == False
