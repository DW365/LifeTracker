from datetime import datetime, timedelta


def today():
    return datetime.now().replace(hour=0, minute=0, second=0)


def tomorrow():
    return today() + timedelta(days=1)


def next_week():
    return today() + timedelta(days=7)
