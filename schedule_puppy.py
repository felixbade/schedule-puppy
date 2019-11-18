import time

from ics import Calendar
from ics.timeline import Timeline
import arrow
from datetime import timedelta
import requests

from secret import calendar_url, tg_token, tg_chat

tz = 'Europe/Helsinki' # Should be the same as the calendar time zone

# iCalendar

def get_events_tomorrow():
    calendar = Calendar(requests.get(calendar_url).text)
    now = arrow.now(tz)
    tomorrow_begin = now.replace(hour=0, minute=0, second=0, microsecond=0).shift(days=1)
    tomorrow_end = tomorrow_begin.shift(days=1)
    events = []
    for event in Timeline(calendar):
        starts_tomorrow = ((event.begin >= tomorrow_begin) and (event.begin < tomorrow_end))
        #ends_tomorrow = ((event.end > tomorrow_begin) and (event.end <= tomorrow_end))
        if starts_tomorrow:
            events.append(event)
    return events

def arrow_to_local_str(time):
    return time.to(tz).strftime('%H:%M')

def event_time_to_tg(event):
    event_time = arrow_to_local_str(event.begin)
    if event.duration > timedelta(minutes=15):
        event_time += '–' + arrow_to_local_str(event.end)
    return event_time

def event_to_tg(event):
    rows = []
    if not event.all_day:
        rows.append(event_time_to_tg(event))

    if event.location:
        rows.append('📍 ' + event.location)

    rows.append('👉 ' + event.name)
    return '\n'.join(rows)



# Telegram
def getUpdates(offset):
    url = 'https://api.telegram.org/bot%s/getUpdates?offset=%d' % (tg_token, offset)
    response = requests.get(url).json()
    return response['result']

def sendMessage(chat_id, text):
    url = 'https://api.telegram.org/bot%s/sendMessage' % tg_token
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url, data)

def sendMessageToGroup(text):
    sendMessage(tg_chat, text)



# Scheduler

def sendScheduleForTomorrow():
    events = get_events_tomorrow()
    if not events:
        print('No events for tomorrow, skipping messge')
    else:
        text = 'Schedule for tomorrow 😊'
        for event in events:
            text += '\n\n'
            text += event_to_tg(event)
        sendMessageToGroup(text)
        print('Sent schedule to the group', tg_chat)

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
    sendScheduleForTomorrow()
