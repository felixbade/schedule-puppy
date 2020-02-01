import datetime

from schedule_puppy.config import tz


def format_events_to_message(events, reference_day):
    text = 'Schedule for tomorrow 😊'
    for event in events:
        text += '\n\n'
        text += event_to_tg(event, reference_day)
    return text

def event_to_tg(event, reference_day):
    rows = []

    timestamp = event_timespan_to_tg(event, reference_day)
    if timestamp is not None:
        rows.append(timestamp)

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



def event_timespan_to_tg(event, reference_day):
    begin = event.begin
    end = event.end

    begin_time = time_of(begin)
    begin_date = date_of(begin, reference_day)
    end_time = time_of(end)
    end_date = date_of(end, reference_day, end=True)

    single_day = ends_on(end, begin)
    begins_on_reference_day = begins_on(begin, reference_day)

    if event.all_day:
        if single_day:
            if begins_on_reference_day:
                return None
            else:
                # Thu
                return begin_date
        else:
            # Thu – Fri
            return begin_date + ' – ' + end_date

    elif event.duration <= datetime.timedelta(minutes=15):
        if begins_on_reference_day:
            # 13:00
            return begin_time
        else:
            # Thu 13:00
            return begin_date + ' ' + begin_time

    else:
        if single_day:
            if begins_on_reference_day:
                # 13:00–16:00
                return begin_time + '–' + end_time
            else:
                # Thu 13:00–16:00
                return begin_date + ' ' + begin_time + '–' + end_time
        else:
            # Thu 13:00 – Fri 16:00
            begin_s = begin_date + ' ' + begin_time
            end_s = end_date + ' ' + end_time
            return begin_s + ' – ' + end_s


def time_of(time):
    return time.to(tz).strftime('%H:%M')

def date_of(time, reference_day, end=False):
    t = time.to(tz)

    if end and (time.time() == datetime.time(0, 0)):
        t = t.shift(days=-1)

    text = t.strftime('%A') # Monday

    include_day_of_month = abs(time.date() - reference_day.date()).days > 2
    include_month = time.date().month != reference_day.date().month
    include_year = time.date().year != reference_day.date().year

    if include_year:
        include_month = True
    if include_month:
        include_day_of_month = True

    if include_day_of_month:
        day = t.date().day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        text += ' ' + str(day) + suffix

    if include_month:
        month = t.strftime('%B') # December
        text += ' of ' + month

    if include_year:
        year = t.date().year
        text += ' ' + str(year)

    return text

def begins_on(begin_time, day):
    day_begins = day.replace(hour=0, minute=0, second=0, microsecond=0)
    day_ends = day_begins.shift(days=1)
    return ((begin_time >= day_begins) and (begin_time < day_ends))

def ends_on(end_time, day):
    day_begins = day.replace(hour=0, minute=0, second=0, microsecond=0)
    day_ends = day_begins.shift(days=1)
    return ((end_time > day_begins) and (end_time <= day_ends))
