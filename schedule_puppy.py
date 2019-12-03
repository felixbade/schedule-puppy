import time

from ics import Calendar
from ics.timeline import Timeline
import arrow
import requests

from telegram import send_message, get_updates
from event_message_formatting import format_events_to_message
from secret import calendar_url, tg_chat
from config import tz

# iCalendar

def get_events_between(tomorrow_begin, tomorrow_end):
    calendar = Calendar(requests.get(calendar_url).text)
    events = []
    for event in Timeline(calendar):
        starts_tomorrow = ((event.begin >= tomorrow_begin) and (event.begin < tomorrow_end))
        #ends_tomorrow = ((event.end > tomorrow_begin) and (event.end <= tomorrow_end))
        if starts_tomorrow:
            events.append(event)
    return events



# Scheduler

def send_schedule_for_day_in(days):
    now = arrow.now(tz)
    tomorrow_begin = now.replace(hour=0, minute=0, second=0, microsecond=0).shift(days=days)
    tomorrow_end = tomorrow_begin.shift(days=1)

    events = get_events_between(tomorrow_begin, tomorrow_end)

    if not events:
        print('No events for tomorrow, skipping messge')
    else:
        message = format_events_to_message(events, tomorrow_begin)
        send_message(tg_chat, message)
        print('Sent schedule to the group', tg_chat)

def send_schedule_for_tomorrow():
    send_schedule_for_day_in(1)

def get_time_until_next_daily():
    now = arrow.now(tz)
    posting = now.replace(hour=18, minute=0, second=1, microsecond=500000)
    if now > posting:
        posting = posting.shift(days=1)
    return (posting - now).total_seconds()


while True:
    t = get_time_until_next_daily()
    print('Sleeping for', t)
    time.sleep(t)
    send_schedule_for_tomorrow()
