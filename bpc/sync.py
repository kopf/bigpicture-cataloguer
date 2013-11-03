from datetime import datetime
import os

from dateutil.relativedelta import relativedelta


# The Big Picture series began on this date:
START = datetime(2008, 05, 1)


def get_months(path):
    """Returns a list of the months to be synced"""
    now = datetime.now()
    retval = []
    month_iterator = get_start_date(path)
    while month_iterator.year != now.year and month_iterator.month != now.month:
        retval.append(month_iterator)
        month_iterator += relativedelta(months=1)
    return retval


def get_start_date(path):
    """Returns the start date at which to start downloading"""
    if not os.path.exists(path):
        return START
    years = os.listdir(path)
    if not years:
        return START
    most_recent_year = get_latest(years) or START.year
    months = os.listdir(os.path.join(path, str(most_recent_year)))
    most_recent_month = get_latest(months) or 1
    return datetime(most_recent_year, most_recent_month, 1)


def get_latest(dir_list):
    """Returns the newest month or year from a list of directories"""
    int_list = []
    for directory in dir_list:
        try:
            int_list.append(int(directory))
        except ValueError:
            pass
    if not int_list:
        return None
    return max(int_list)
