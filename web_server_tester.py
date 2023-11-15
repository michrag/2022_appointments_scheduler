#!/usr/bin/env python3


from requests import put, get, delete, post


def main():
    test_reminders()

    test_dates()

    test_meetings()

    test_dates()

    test_attendees()


def test_reminders():
    print("post reminder 1 (not implemented)")
    r = post('http://localhost:5000/reminders/reminder1', json={})
    print_request(r)

    print("get reminder 1")
    r = get('http://localhost:5000/reminders/reminder1')
    print_request(r)

    print("delete reminder 1")
    r = delete('http://localhost:5000/reminders/reminder1')
    print_request(r)

    print("put reminder 1")
    r = put('http://localhost:5000/reminders/reminder1', json={'date': '2022-04-04'})
    print_request(r)

    print("put (update) reminder 1 without date (fail)")
    r = put('http://localhost:5000/reminders/reminder1', json={})
    print_request(r)

    print("get reminder 1")
    r = get('http://localhost:5000/reminders/reminder1')
    print_request(r)

    print("put reminder 2")
    r = put('http://localhost:5000/reminders/reminder2', json={'date': '2022-04-05'})
    print_request(r)

    print("get reminder 2")
    r = get('http://localhost:5000/reminders/reminder2')
    print_request(r)

    print("put reminder 3 without date (fail)")
    r = put('http://localhost:5000/reminders/reminder3', json={})
    print_request(r)

    print("get reminder 3 (fail)")
    r = get('http://localhost:5000/reminders/reminder3')
    print_request(r)

    print("put reminder 4")
    r = put('http://localhost:5000/reminders/reminder4', json={'date': '2022-04-06'})
    print_request(r)

    print("delete reminder 4")
    r = delete('http://localhost:5000/reminders/reminder4')
    print_request(r)


def test_meetings():
    print("post meeting 1 (not implemented)")
    r = post('http://localhost:5000/meetings/meeting1', json={})
    print_request(r)

    print("put meeting 1")
    data = {'date': '2022-04-04', 'names': ['Alice', 'Bob', 'Carol', 'Charles', 'Charlie']}
    r = put('http://localhost:5000/meetings/meeting1', json=data)
    print_request(r)

    print("get meeting 1")
    r = get('http://localhost:5000/meetings/meeting1')
    print_request(r)

    print("put (update) meeting 1 without date nor attendees (fail)")
    r = put('http://localhost:5000/meetings/meeting1', json={})
    print_request(r)

    print("put (update) meeting 1 attendees")
    data = {'names': ['Alice', 'Bob', 'Charles']}
    r = put('http://localhost:5000/meetings/meeting1', json=data)
    print_request(r)

    print("get meeting 1")
    r = get('http://localhost:5000/meetings/meeting1')
    print_request(r)

    print("put meeting 2")
    data = {'date': '2022-04-04', 'names': ['Alice', 'Chuck', 'Chad', 'Craig']}
    r = put('http://localhost:5000/meetings/meeting2', json=data)
    print_request(r)

    print("get meeting 2")
    r = get('http://localhost:5000/meetings/meeting2')
    print_request(r)

    print("put (update) meeting 2 date")
    data = {'date': '2022-04-11'}
    r = put('http://localhost:5000/meetings/meeting2', json=data)
    print_request(r)

    print("get meeting 2")
    r = get('http://localhost:5000/meetings/meeting2')
    print_request(r)

    print("put meeting 3")
    data = {'date': '2022-04-04', 'names': ['Craig', 'Dan', 'Dave', 'David', 'Erin']}
    r = put('http://localhost:5000/meetings/meeting3', json=data)
    print_request(r)

    print("get meeting 3")
    r = get('http://localhost:5000/meetings/meeting3')
    print_request(r)

    print("put (update) meeting 3 date and attendees")
    data = {'date': '2022-04-11', 'names': ['Eve', 'Faythe', 'Frank']}
    r = put('http://localhost:5000/meetings/meeting3', json=data)
    print_request(r)

    print("get meeting 3")
    r = get('http://localhost:5000/meetings/meeting3')
    print_request(r)

    print("put meeting 4 without date (fail)")
    data = {'names': ['Grace', 'Heidi', 'Ivan', 'Judy']}
    r = put('http://localhost:5000/meetings/meeting4', json=data)
    print_request(r)

    print("put meeting 4 without attendees (fail)")
    data = {'date': '2022-04-07'}
    r = put('http://localhost:5000/meetings/meeting4', json=data)
    print_request(r)

    print("get meeting 4 (fail)")
    r = get('http://localhost:5000/meetings/meeting4')
    print_request(r)

    print("put meeting 4")
    data = {'date': '2022-04-07', 'names': ['Grace', 'Heidi', 'Ivan', 'Judy']}
    r = put('http://localhost:5000/meetings/meeting4', json=data)
    print_request(r)

    print("get meeting 4")
    r = get('http://localhost:5000/meetings/meeting4')
    print_request(r)

    print("delete meeting 4")
    r = delete('http://localhost:5000/meetings/meeting4')
    print_request(r)

    print("get meeting 4 (fail)")
    r = get('http://localhost:5000/meetings/meeting4')
    print_request(r)

    print("put meeting 5")
    data = {'date': '2022-04-07', 'names': ['Ivan', 'Mallory', 'Mike', 'Oscar']}
    r = put('http://localhost:5000/meetings/meeting5', json=data)
    print_request(r)


def test_dates():
    print("get appointments on date 2022-04-04")
    r = get('http://localhost:5000/date/2022-04-04')
    print_request(r)

    print("get appointments on date 2022-04-05")
    r = get('http://localhost:5000/date/2022-04-05')
    print_request(r)

    print("get appointments on date 2022-04-06 (none)")
    r = get('http://localhost:5000/date/2022-04-06')
    print_request(r)

    print("get appointments on date 2022-04-07")
    r = get('http://localhost:5000/date/2022-04-07')
    print_request(r)

    print("get appointments on date 2022-04-08 (none)")
    r = get('http://localhost:5000/date/2022-04-08')
    print_request(r)

    print("get appointments on date 2022-04-11")
    r = get('http://localhost:5000/date/2022-04-11')
    print_request(r)


def test_attendees():
    print("get meetings for Alice on date 2022-04-04")
    r = get('http://localhost:5000/date/2022-04-04/attendee/Alice')
    print_request(r)

    print("get meetings for Charles on date 2022-04-04")
    r = get('http://localhost:5000/date/2022-04-04/attendee/Charles')
    print_request(r)

    print("get meetings for Grace on date 2022-04-05")
    r = get('http://localhost:5000/date/2022-04-05/attendee/Grace')
    print_request(r)

    print("get meetings for Ivan on date 2022-04-07")
    r = get('http://localhost:5000/date/2022-04-07/attendee/Ivan')
    print_request(r)

    print("get meetings for Chuck on date 2022-04-11")
    r = get('http://localhost:5000/date/2022-04-11/attendee/Chuck')
    print_request(r)


def print_request(r):
    print(r)
    print(r.content)
    print()


if __name__ == '__main__':
    main()
