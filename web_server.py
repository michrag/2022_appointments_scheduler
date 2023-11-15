#!/usr/bin/env python3


from abc import ABC, abstractmethod
from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import jsonpickle


##############################################################################
# Data Model Classes
##############################################################################

class Appointment(ABC):  # Python's way of defining an Abstract Base Class (ABC)
    """Abstract Base Class defining Appointment interface"""

    @abstractmethod
    def update_date(self, date):
        """Update the date of an existing appointment"""
        pass

    @abstractmethod
    def get_date(self):
        """Retrieve the date of an existing appointment"""
        pass

    @abstractmethod
    def _to_json(self):
        """Serialize the appointment to JSON (in human readable form)"""
        pass


class Reminder(Appointment, object):  # it implements Appointment (and inherits from object)
    def __init__(self, reminder_id, date):
        self.reminder_id = reminder_id
        self.date = date

    def _to_json(self):  # implements abstract method of Appointment
        return {"reminder_id": self.reminder_id, "date": self.date}

    def update_date(self, date):  # implements abstract method of Appointment
        self.date = date

    def get_date(self):  # implements abstract method of Appointment
        return self.date


class Attendee(object):  # it inherits from object
    def __init__(self, name):
        self.name = name

    def _to_json(self):
        return {"name": self.name}


class Meeting(Appointment, object):  # it implements Appointment (and inherits from object)
    def __init__(self, meeting_id, date, attendees_names):
        self.meeting_id = meeting_id
        self.date = date
        self.attendees = {}  # creates an empty dictionary of attendees
        self.update_attendees(attendees_names)

    def _to_json(self):  # implements abstract method of Appointment
        return {"meeting_id": self.meeting_id, "date": self.date, "attendees": self.attendees}

    def update_date(self, date):  # implements abstract method of Appointment
        self.date = date

    def get_date(self):  # implements abstract method of Appointment
        return self.date

    def update_attendees(self, attendees_names):
        """Update (overwriting it) the list of attendees to the meeting"""
        self.attendees.clear()
        for attendee_name in attendees_names:
            attendee = Attendee(attendee_name)
            self.attendees[attendee_name] = attendee


class CustomEncoder(json.JSONEncoder):
    """Custom JSON encoder that will call '_to_json' methods of each object"""
    def default(self, obj):
        try:
            return obj._to_json()
        except AttributeError:
            return super().default(obj)


##############################################################################
# Business Logic Classes (Schedulers and Viewers)
##############################################################################

class AppointmentsScheduler(Resource):  # it inherits from Resource, base class of the chosen framework (Flask-RESTful)
    def __init__(self, parser, appointments):
        self.parser = parser
        self.appointments = appointments

    def get_appointment(self, appointment_id):
        for saved_appointment_id in self.appointments:
            if saved_appointment_id == appointment_id:
                return self.appointments[appointment_id]
        else:
            return None

    def get(self, appointment_id):
        if self.get_appointment(appointment_id) is None:
            return f'Appointment {appointment_id} does not exist', 404

        serialized_appointment = json.dumps(self.appointments[appointment_id], cls=CustomEncoder)
        return serialized_appointment, 200

    def get_date(self):
        args = self.parser.parse_args()
        date = args['date']
        return date

    def delete(self, appointment_id):
        if self.get_appointment(appointment_id) is None:
            return f'Appointment {appointment_id} does not exist', 404

        del self.appointments[appointment_id]
        return 200

    def post(self, appointment_id):
        return "Not implemented, use put instead", 501


class RemindersScheduler(AppointmentsScheduler):  # it inherits from AppointmentsScheduler
    def __init__(self, parser, reminders):
        super().__init__(parser, reminders)

    def put(self, appointment_id):
        date = self.get_date()
        if not date:
            return "Date is required", 400  # 400 = bad request

        if self.get_appointment(appointment_id) is None:
            return self.create_reminder(appointment_id, date)
        else:
            return self.update_reminder(appointment_id, date)

    def create_reminder(self, reminder_id, date):
        reminder = Reminder(reminder_id, date)
        self.appointments[reminder_id] = reminder

        serialized_reminder = json.dumps(self.appointments[reminder_id], cls=CustomEncoder)
        return serialized_reminder, 201  # 201 = created

    def update_reminder(self, reminder_id, date):
        self.appointments[reminder_id].update_date(date)

        serialized_reminder = json.dumps(self.appointments[reminder_id], cls=CustomEncoder)
        return serialized_reminder, 200  # 200 = OK


class MeetingsScheduler(AppointmentsScheduler):  # it inherits from AppointmentsScheduler
    def __init__(self, parser, meetings):
        super().__init__(parser, meetings)

    def put(self, appointment_id):
        if self.get_appointment(appointment_id) is None:
            return self.create_meeting(appointment_id)
        else:
            return self.update_meeting(appointment_id)

    def create_meeting(self, meeting_id):
        date = self.get_date()
        attendees_names = self.get_attendees_names()

        if not date or not attendees_names:
            return "Date and at least 1 attendee are required", 400  # 400 = bad request

        meeting = Meeting(meeting_id, date, attendees_names)
        self.appointments[meeting_id] = meeting

        serialized_meeting = json.dumps(self.appointments[meeting_id], cls=CustomEncoder)
        return serialized_meeting, 201  # 201 = created

    def update_meeting(self, meeting_id):
        date = self.get_date()
        attendees_names = self.get_attendees_names()

        if not date and not attendees_names:
            return "Date or at least 1 attendee are required", 400  # 400 = bad request

        if date:
            self.update_meeting_date(meeting_id)

        if attendees_names:
            self.update_meeting_attendees(meeting_id)

        serialized_meeting = json.dumps(self.appointments[meeting_id], cls=CustomEncoder)
        return serialized_meeting, 200  # 200 = OK

    def update_meeting_date(self, meeting_id):
        date = self.get_date()
        self.appointments[meeting_id].update_date(date)

    def update_meeting_attendees(self, meeting_id):
        attendees_names = self.get_attendees_names()
        self.appointments[meeting_id].update_attendees(attendees_names)

    def get_attendees_names(self):
        args = self.parser.parse_args()
        attendees_names = args['names']
        return attendees_names


class AppointmentsViewer(Resource):  # it inherits from Resource, base class of the chosen framework (Flask-RESTful)
    def post(self, date):
        return "Not implemented", 501

    def put(self, date):
        return "Not implemented", 501

    def delete(self, date):
        return "Not implemented", 501


class AppointmentsOnDateViewer(AppointmentsViewer):  # it inherits from AppointmentsViewer
    def __init__(self, reminders, meetings):
        self.reminders = reminders
        self.meetings = meetings

    def get(self, date):
        appointments_list = list(self.reminders.values()) + list(self.meetings.values())

        appointments_on_date_list = []

        for appointment in appointments_list:
            if appointment.get_date() == date:
                appointments_on_date_list.append(appointment)

        if appointments_on_date_list:
            serialized_appointments = json.dumps(appointments_on_date_list, cls=CustomEncoder)
            return serialized_appointments, 200
        else:
            return f'No appointments on {date}', 404


class MeetingsOnDateForAttendeeViewer(AppointmentsViewer):  # it inherits from AppointmentsViewer
    def __init__(self, meetings):
        self.meetings = meetings

    def get(self, date, attendee_name):
        appointments_for_attendee_on_date_list = []

        for meeting in self.meetings.values():
            if meeting.get_date() == date:
                if attendee_name in meeting.attendees:
                    appointments_for_attendee_on_date_list.append(meeting)

        if appointments_for_attendee_on_date_list:
            serialized_appointments = json.dumps(appointments_for_attendee_on_date_list, cls=CustomEncoder)
            return serialized_appointments, 200
        else:
            return f'No meetings for {attendee_name} on {date}', 404


def main():
    reminders_db_file_path = "db/reminders.json"
    reminders = load_db_from_file(reminders_db_file_path)

    meetings_db_file_path = "db/meetings.json"
    meetings = load_db_from_file(meetings_db_file_path)

    app = Flask(__name__)
    api = Api(app)

    # JSON parser of data from received request
    parser = reqparse.RequestParser()
    parser.add_argument('date')
    parser.add_argument('names', action='append')  # action='append' : accept multiple values for a key as a list

    # binding Resources to URLs
    api.add_resource(RemindersScheduler, '/reminders/<string:appointment_id>',
                     resource_class_kwargs={'parser': parser, 'reminders': reminders})
    api.add_resource(MeetingsScheduler, '/meetings/<string:appointment_id>',
                     resource_class_kwargs={'parser': parser, 'meetings': meetings})
    api.add_resource(AppointmentsOnDateViewer, '/date/<string:date>',
                     resource_class_kwargs={'reminders': reminders, 'meetings': meetings})
    api.add_resource(MeetingsOnDateForAttendeeViewer, '/date/<string:date>/attendee/<string:attendee_name>',
                     resource_class_kwargs={'meetings': meetings})

    # run the server
    app.run(debug=True, use_reloader=False)

    # on exit...
    save_db_to_file(reminders_db_file_path, reminders)
    save_db_to_file(meetings_db_file_path, meetings)


def load_db_from_file(db_file_path):
    db = {}
    try:
        with open(db_file_path, 'r') as db_file:  # load from DB file
            try:
                db = jsonpickle.decode(json.load(db_file))
            except ValueError as e:
                print(e)
    except IOError:  # DB file does not exist
        with open(db_file_path, 'w'):  # creates empty DB file
            pass

    return db


def save_db_to_file(db_file_path, db):
    with open(db_file_path, 'w') as db_file:  # save to DB file
        json.dump(jsonpickle.encode(db), db_file)


if __name__ == '__main__':
    main()
