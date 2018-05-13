import configparser
import os
from dateutil import relativedelta
from datetime import timedelta, datetime


def parse_config(config_path=os.path.join('..', '..', 'config', 'config.ini')):
    config = configparser.RawConfigParser()
    config.read(config_path)
    return config


def parse_period(period):
    """Parse period from string to :obj:`datetime.timedelta`

    Args:
        period (str): Period of repeating in format [d | w | m | y], where
                        d - day, w - week, m - month, y - year.

    Raises:
        AttributeError: If `period` does not match pattern. 
    """
    if period == 'd':
        period = relativedelta.relativedelta(days=+1)
    elif period == 'w':
        period = relativedelta.relativedelta(weeks=+1)
    elif period == 'm':
        period = relativedelta.relativedelta(months=+1)
    elif period == 'y':
        period = relativedelta.relativedelta(years=+1)
    else:
        raise AttributeError('Unknown time period')
    return period


def parse_date(date, pattern='%d.%m.%Y %H:%M'):
    """Parse deadline deadline

    Note:
        Returns `deadline` if input string is valid.

    Args:
        date (str): Date of deadline in format [DD.MM.YYYY hh:mm].
        pattern (str): Format of deadline string representation.

    Raises:
        ValueError: If string does not math format.
        AttributeError: If deadline less than current deadline.

    """
    date = datetime.strptime(date, pattern)
    if date < datetime.now():
        raise AttributeError('Date cannot be less that current deadline')
    return date


def main():
    n = input()
    a = set(map(str, input().split()))
    print(len(a))
    print(' '.join(a))

if __name__ == '__main__':
    main()
