from ics import Calendar
from ics.timeline import Timeline
import arrow
from datetime import timedelta
import requests

from secret import calendar_url

calendar = Calendar(requests.get(calendar_url).text)
events_on = Timeline(calendar).on(arrow.now().shift(days=5))


def arrow_to_local_str(time):
    return time.to('EEST').strftime('%H:%M')

def event_time_to_tg(event):
    event_time = arrow_to_local_str(event.begin)
    if event.duration > timedelta(minutes=15):
        event_time += '–' + arrow_to_local_str(event.end)
    return event_time

def event_to_tg(event):
    text = event_time_to_tg(event)
    if event.location:
        text += '\n'
        text += '📍 '
        text += event.location
    text += '\n'
    text += '👉 '
    text += event.name
    return text

for event in events_on:
    print(event_to_tg(event))
    print()
