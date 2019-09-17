from ics import Calendar
from ics.timeline import Timeline
import arrow
from datetime import timedelta
import requests

from secret import calendar_url, tg_token, tg_chat

calendar = Calendar(requests.get(calendar_url).text)
events_on = Timeline(calendar).on(arrow.now().shift(days=5))


# iCalendar

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
