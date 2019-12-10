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

def get_timeline():
    calendar = Calendar(requests.get(calendar_url).text)
    return Timeline(calendar)

def filter_events_happening_between(timeline, range_begin, range_end):
    events = []
    for event in timeline:
        happens_in_range = ((event.begin < range_end) and (event.end > range_begin))
        if happens_in_range:
            events.append(event)
    return events

def filter_events_starting_between(timeline, range_begin, range_end):
    events = []
    for event in timeline:
        starts_in_range = ((event.begin >= range_begin) and (event.begin < range_end))
        if starts_in_range:
            events.append(event)
    return events



# Scheduler

def send_schedule_for_day_in(days):
    now = arrow.now(tz)
    tomorrow_begin = now.replace(hour=0, minute=0, second=0, microsecond=0).shift(days=days)
    tomorrow_end = tomorrow_begin.shift(days=1)

    timeline = get_timeline()
    events = filter_events_happening_between(timeline, tomorrow_begin, tomorrow_end)
    events_starting_tomorrow = filter_events_starting_between(timeline, tomorrow_begin, tomorrow_end)

    if not events_starting_tomorrow:
        print('No events starting tomorrow, skipping messge')
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
