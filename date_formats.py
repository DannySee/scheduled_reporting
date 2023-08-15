from datetime import  datetime, timedelta, date

now = date.today()

def sus(day):
    if day == 'today':
        return now.strftime('%Y%m%d')
    elif day == 'yesterday':
        return (now - timedelta(1)).strftime('%Y%m%d')
    elif day == 'beginning_of_last_week':
        return (now - timedelta(days=now.weekday()+8)).strftime('%Y%m%d')
    elif day == 'end_of_last_week':
        return (now - timedelta(days=now.weekday()+2)).strftime('%Y%m%d')
    elif day == 'beginning_of_month':
        return (datetime(now.year, now.month, 1)).strftime('%Y%m%d')
    elif day == 'end_of_month':
        next_month = now.replace(day=28) + timedelta(days=4)
        return (next_month - timedelta(days=next_month.day)).strftime('%Y%m%d')
    elif day == 'end_of_next_month':
        start_of_next_month = now.replace(day=1).replace(month=now.month % 12 + 1)
        end_of_next_month = start_of_next_month + timedelta(days=31)
        return end_of_next_month.strftime('%Y%m%d')
    else:
        return 'format not supported'

def pretty(day):
    if day == 'today':
        return now.strftime("%m-%d-%Y")
    elif day == 'yesterday':
        return (now - timedelta(1)).strftime("%m-%d-%Y")
    elif day == 'beginning_of_last_week':
        return (now - timedelta(days=now.weekday()+8)).strftime("%m-%d-%Y")
    elif day == 'end_of_last_week':
        return (now - timedelta(days=now.weekday()+2)).strftime("%m-%d-%Y")
    elif day == 'beginning_of_month':
        return (datetime(now.year, now.month, 1)).strftime("%m-%d-%Y")
    elif day == 'end_of_month':
        next_month = now.replace(day=28) + timedelta(days=4)
        return (next_month - timedelta(days=next_month.day)).strftime("%m-%d-%Y")
    elif day == 'end_of_next_month':
        start_of_next_month = now.replace(day=1).replace(month=now.month % 12 + 1)
        end_of_next_month = start_of_next_month + timedelta(days=31)
        return end_of_next_month.strftime("%m/%d/%Y")
    elif day == 'month_back':
        return (now - timedelta(30)).strftime("%m/%d/%Y")
    elif day == 'week_back':
        return (now - timedelta(7)).strftime("%m/%d/%Y")
    else:
        return 'format not supported'