from datetime import datetime, timedelta

def days_to_datestring(days: int) -> str:
    """Converts number of days since 1.1.1997 to a string"""
    date = datetime(1997, 1, 1) + timedelta(days=days)
    return date.strftime("%d.%m.%Y")

def datestring_to_days(datestring: str) -> int:
    """Converts a date in a string into number of days since 1.1.1997"""
    date = datetime.strptime(datestring, "%d.%m.%Y")
    delta = date - datetime(1997, 1, 1)
    return delta.days
