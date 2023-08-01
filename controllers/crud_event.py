from views.views_crud_inputs import CrudInputsView
from views.views_crud_messages import CrudContractMessagesView, CrudEventMessagesView
from controllers.check_object_exists import CheckObjectExists

from models import models


class CrudEvent:
    def event_create(self, session):
        CrudEventMessagesView().creation_title()

        while True:
            contract_id_input = CrudInputsView().update_contract_id(session)
            contract = (
                session.query(models.Contract).filter_by(id=contract_id_input).first()
            )
            if not contract.signed:
                CrudEventMessagesView().contract_not_signed()
                session.close()
                from main import main

                main()

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

        session.add(event)
        session.commit()
        CrudEventMessagesView().creation_successful()

    def event_update_add_support(self, session):
        while True:
            event_id_input = CrudInputsView().update_event_id(session)
            event_update = CheckObjectExists().check_eventID_exists(
                session, event_id_input
            )
            if event_update in session.query(models.Event):
                confirm_choice = CrudInputsView().confirm_event_update_choice(
                    session, event_update
                )
                if confirm_choice == "y":
                    break
                continue
            continue

        support_contact_input = CrudInputsView().event_supportid_input(session)

        event_update.support_contact = support_contact_input

        session.commit()
        CrudEventMessagesView().support_update_successful()

    def event_update(self, session):
        while True:
            event_id_input = CrudInputsView().update_event_id(session)
            event_update = CheckObjectExists().check_eventID_exists(
                session, event_id_input
            )
            if event_update in session.query(models.Event):
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

        session.commit()

        CrudEventMessagesView().update_successful()

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

    def contract_display_all(self, session):
        contracts = session.query(models.Contract)
        CrudContractMessagesView().contract_display_all(session, contracts)

    def contract_display_not_signed(self, session):
        contracts = session.query(models.Contract)
        for contract in contracts:
            if not contract.signed:
                CrudContractMessagesView().contract_display_not_signed(
                    session, contracts
                )

    def contract_display_not_paid(self, session):
        contracts = session.query(models.Contract)
        CrudContractMessagesView().contract_display_not_paid(session, contracts)

    def event_display_no_support(self, session):
        events = session.query(models.Event)
        CrudEventMessagesView().event_display_no_support(events)

    def event_display_for_supportincharge(self, session, user):
        user = session.query(models.Users).filter_by(username=user).first()
        events = session.query(models.Event).filter_by(support_contact=user.id).all()
        CrudEventMessagesView().event_display_for_supportincharge(session, events)

    def event_display_all(self, session):
        events = session.query(models.Event)
        CrudEventMessagesView().event_display_all(session, events)
