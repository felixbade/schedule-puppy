from icalendar import Calendar, Event
import pytz
from datetime import date, time, datetime

def create_calendar():
    cal = Calendar()
    cal.add('prodid', '-//Schedule Puppy//Schedule Puppy Event Converter//')
    cal.add('version', '2.0')
    return cal

def save_calendar(cal, filename='example.ics'):
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())


def create_event(name, start, end, location=None, description=None):
    event = Event()

    event.add('summary', name)
    event.add('dtstart', start)
    event.add('dtend', end)
    event.add('dtstamp', datetime.utcnow()) # Required by RFC 2445

    if location is not None:
        event.add('location', location)

    if description is not None:
        event.add('description', description)

    return event

def create_event2(name, day, start_time, end_time, location=None, description=None):
    start = datetime.combine(day, start_time)
    end = datetime.combine(day, end_time)
    return create_event(name, start, end, location, description)



#cal.add_component(event)
