import time

from ics import Calendar
from ics.timeline import Timeline
import arrow
from datetime import timedelta
import requests

from secret import calendar_url, tg_token, tg_chat

tz = 'Europe/Helsinki'

# iCalendar

def get_events_tomorrow():
    calendar = Calendar(requests.get(calendar_url).text)
    return Timeline(calendar).on(arrow.now().shift(days=1))

def arrow_to_local_str(time):
    return time.to(tz).strftime('%H:%M')

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



# Telegram
def getUpdates(offset):
    url = 'https://api.telegram.org/bot%s/getUpdates?offset=%d' % (tg_token, offset)
    response = requests.get(url).json()
    return response['result']

def sendMessage(chat_id, text):
    url = 'https://api.telegram.org/bot%s/sendMessage' % tg_token
    data = {'chat_id': chat_id, 'text': text}
    requests.post(url, data)

def sendMessageToGroup(text):
    sendMessage(tg_chat, text)



# Scheduler

def sendScheduleForTomorrow():
    text = 'Schedule for tomorrow 😊'
    for event in get_events_tomorrow():
        text += '\n\n'
        text += event_to_tg(event)
    sendMessageToGroup(text)

def get_time_until_next_daily():
    now = arrow.now(tz)
    posting = now.replace(hour=18, minute=0, second=0, microsecond=0)
    if now > posting:
        posting = posting.shift(days=1)
    return (posting - now).total_seconds()



while True:
    t = get_time_until_next_daily()
    print('Sleeping', t)
    time.sleep(t)
    sendScheduleForTomorrow()
