from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudClientMessagesView, CrudEventMessagesView

from controllers.utils import Utils
from controllers.data_access_layer import (
    DALSession,
    DALUser,
    DALContract,
    DALEvent,
)
from controllers.check_object_exists import CheckObjectExists

from models import models


class CrudEvent:
    def event_create(self, session, username):
        """Create an event after filling the required fields.
        If needed, each input will be checked to ensure that
        the entered information is valid and can be processed."""
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        CrudEventMessagesView().creation_title()

        salesman = DALUser().get_user_by_username(session, username)
        while True:
            contract_id_input = CrudInputsView().update_contract_id(session)
            contract = DALContract().get_contract_by_id(session, contract_id_input)
            if not contract.signed:
                CrudEventMessagesView().contract_not_signed()
                Utils().back_to_menu(session, username)

                from main import main

                main()

            if contract.linked_salesman != salesman.id:
                CrudClientMessagesView().not_salesmans_in_charge()
                continue
            client_name_input = CrudInputsView().event_client_name(
                session, contract_id_input
            )
            client_contact_input = CrudInputsView().event_client_contact_input()
            start_date_input = CrudInputsView().event_startdate()
            end_date_input = CrudInputsView().event_enddate(start_date_input)
            support_contact_input = CrudInputsView().event_supportid_input(session)
            location_input = CrudInputsView().event_location_input()
            attendees_input = CrudInputsView().event_attendees_input()
            notes_input = CrudInputsView().event_notes_input()

            CrudEventMessagesView().event_confirmation(
                contract_id_input,
                client_name_input,
                client_contact_input,
                start_date_input,
                end_date_input,
                support_contact_input,
                location_input,
                attendees_input,
                notes_input,
            )

            confirm_input = CrudInputsView().confirm_creation()
            if confirm_input:
                break
            continue

        # Processing the creation
        event = models.Event(
            contract_id=contract_id_input,
            client_name=client_name_input,
            client_contact=client_contact_input,
            start_date=start_date_input,
            end_date=end_date_input,
            support_contact=support_contact_input,
            location=location_input,
            attendees=attendees_input,
            notes=notes_input,
        )

        DALSession().session_add_and_commit(session, event)
        CrudEventMessagesView().creation_successful()
        Utils().back_to_menu(session, username)

    def event_update_add_support(self, session, username):
        """Update an event to assign/modify support."""
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        while True:
            event_id_input = CrudInputsView().update_event_id(session)
            event_update = CheckObjectExists().check_eventID_exists(
                session, event_id_input
            )
            if event_update in DALEvent().get_all_events(session):
                confirm_choice = CrudInputsView().confirm_event_update_choice(
                    session, event_update
                )
                if confirm_choice == "y":
                    break
                continue
            continue

        support_contact_input = CrudInputsView().event_supportid_input(session)

        event_update.support_contact = support_contact_input

        DALSession().session_commit(session)
        CrudEventMessagesView().support_update_successful()
        Utils().back_to_menu(session, username)

    def event_update(self, session, username):
        """Update an event's selected field."""
        Utils().user_status_request_pwd(session, username)
        Utils().clear_screen()
        current_support = DALUser().get_user_by_username(session, username)
        while True:
            event_id_input = CrudInputsView().update_event_id(session)
            event_update = CheckObjectExists().check_eventID_exists(
                session, event_id_input
            )
            if event_update in DALEvent().get_all_events(session):
                if event_update.support_contact != current_support.id:
                    CrudEventMessagesView().not_support_in_charge()
                    continue
                confirm_choice = CrudInputsView().confirm_event_update_choice(
                    session, event_update
                )
                if confirm_choice == "y":
                    break
                continue
            continue

        field, value = self.event_update_fieldandvalue(event_id_input, session)
        if field == "1":
            event_update.client_contact = value
        if field == "2":
            event_update.start_date = value
        if field == "3":
            event_update.end_date = value
        if field == "4":
            event_update.support_contact = value
        if field == "5":
            event_update.location = value
        if field == "6":
            event_update.attendees = value
        if field == "7":
            event_update.notes = value

        DALSession().session_commit(session)
        CrudEventMessagesView().update_successful()
        Utils().back_to_menu(session, username)

    def event_update_fieldandvalue(self, event_id, session):
        field_to_update = CrudInputsView().what_to_update_event()

        if field_to_update == "1":
            value_to_update = CrudInputsView().event_client_contact_input()
        if field_to_update == "2":
            value_to_update = CrudInputsView().event_startdate()
        if field_to_update == "3":
            value_to_update = CrudInputsView().event_enddate_update(event_id, session)
        if field_to_update == "4":
            value_to_update = CrudInputsView().event_supportid_input(session)
        if field_to_update == "5":
            value_to_update = CrudInputsView().event_location_input()
        if field_to_update == "6":
            value_to_update = CrudInputsView().event_attendees_input()
        if field_to_update == "7":
            value_to_update = CrudInputsView().event_notes_input()

        return field_to_update, value_to_update

    def event_display_no_support(self, session, username):
        """Display the events without assigned support."""
        Utils().clear_screen()
        events = DALEvent().get_all_events(session)
        CrudEventMessagesView().event_display_no_support(events)
        Utils().back_to_menu(session, username)

    def event_display_for_supportincharge(self, session, username):
        """Display the events the logged in support member
        is in charge of."""
        Utils().clear_screen()
        user = DALUser().get_user_by_username(session, username)
        events = DALEvent().get_events_by_supportid(session, user)
        CrudEventMessagesView().event_display_for_supportincharge(session, events)
        Utils().back_to_menu(session, username)

    def event_display_all(self, session, username):
        """Display all the events in the database."""
        Utils().clear_screen()
        events = DALEvent().get_all_events(session)
        CrudEventMessagesView().event_display_all(session, events)
        Utils().back_to_menu(session, username)
