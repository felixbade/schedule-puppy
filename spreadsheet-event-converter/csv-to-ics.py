from sys import argv
import csv
import pytz
from datetime import date, time, datetime

from convert import create_calendar, save_calendar, create_event2

calendar = create_calendar()

def to_time(txt):
    a = txt.split(':')
    hour = int(a[0])
    minute = int(a[1])
    return time(hour, minute, 0)

def to_date(txt):
    a = txt.split('/')
    day = int(a[0])
    month = int(a[1])
    year = int(a[2])
    return date(year, month, day)

with open(argv[1], newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    rows = list(reader)
    header_row = rows[0]
    rows_with_titles = []
    for row in rows[1:]:
        if all(cell == '' for cell in row):
            continue
        row_with_titles = {}
        for title, cell in zip(rows[0], row):
            row_with_titles.update({title: cell})
        rows_with_titles.append(row_with_titles)

    for row in rows_with_titles:
        day = int(row['Day'])
        month = int(row['Month'])
        year = int(row['Year'])
        event_date = date(year, month, day)
        start_time = to_time(row['Start time'])
        end_time = to_time(row['End time'])

        name = row['Event name']
        location = row['Location'] or None
        description = row['Additional info'] or None

        event = create_event2(name, event_date, start_time, end_time, location, description)
        #print(event)

        calendar.add_component(event)


#event.add('dtstart', datetime(2020, 1, 19, 9, 15, 0, tzinfo=pytz.timezone('Europe/Helsinki')))
# time(18, 0, 0, tzinfo=pytz.timezone('Europe/Helsinki'))

save_calendar(calendar, 'export.ics')
print('Saved conversion to export.ics.')
