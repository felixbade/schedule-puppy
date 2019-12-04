import time

from ics import Calendar
from ics.timeline import Timeline
import arrow
import requests

from schedule_puppy.telegram import send_message, get_updates, pin_chat_message, unpin_chat_message
from schedule_puppy.event_message_formatting import format_events_to_message
from schedule_puppy.config import tz, pin_schedule
from secret import calendar_url, tg_chat

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
        if pin_schedule:
            response = unpin_chat_message(tg_chat)
            if response['ok']:
                print('Unpinned previous message.')
            else:
                print('Failed to unpin the previous message.')

    else:
        message = format_events_to_message(events, tomorrow_begin)
        response = send_message(tg_chat, message)
        if response['ok']:
            print('Successfully sent schedule to the group', tg_chat)
            message_id = response['result']['message_id']
            if pin_schedule:
                response = pin_chat_message(tg_chat, message_id, True)
                if response['ok']:
                    print('Pinned the schedule.')
                else:
                    print('Failed to pin the schedule.')
        else:
            print('Failed to send message to the group.')
            print(repr(response))

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
