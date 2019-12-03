from datetime import timedelta

from config import tz


def format_events_to_message(events):
    text = 'Schedule for tomorrow 😊'
    for event in events:
        text += '\n\n'
        text += event_to_tg(event)
    return text

def event_to_tg(event):
    rows = []
    if not event.all_day:
        rows.append(event_time_to_tg(event))

    if event.location:
        rows.append('📍 ' + event.location)

    busy = not event.transparent
    if busy:
        rows.append('👉 ' + event.name)
    else:
        rows.append('🏝 ' + event.name)

    if event.description:
        rows.append('ℹ️ ' + event.description)

    return '\n'.join(rows)



def event_time_to_tg(event):
    event_time = arrow_to_local_str(event.begin)
    if event.duration > timedelta(minutes=15):
        event_time += '–' + arrow_to_local_str(event.end)
    return event_time

def arrow_to_local_str(time):
    return time.to(tz).strftime('%H:%M')
