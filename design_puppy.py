from ics import Calendar
from ics.timeline import Timeline
import arrow
from datetime import timedelta
import requests

from secret import calendar_url

calendar = Calendar(requests.get(calendar_url).text)


def arrow_to_local_str(time):
    return time.to('EEST').strftime('%H:%M')

def event_time_to_tg(event):
    event_time = arrow_to_local_str(event.begin)
    if event.duration > timedelta(minutes=15):
        event_time += '–' + arrow_to_local_str(event.end)
    return event_time

events_on = Timeline(calendar).on(arrow.now().shift(days=5))
for event in events_on:
    print('name:', event.name)
    print('location:', event.location)
    print('time:', event_time_to_tg(event))
    print()
