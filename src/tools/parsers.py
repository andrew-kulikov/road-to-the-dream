import configparser
import os
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
        period = timedelta(days=1)
    elif period == 'w':
        period = timedelta(weeks=1)
    elif period == 'm':
        period = timedelta(days=30)
    elif period == 'y':
        period = timedelta(days=365)
    else:
        raise AttributeError('Unknown time period')
    return period


def parse_date(date, pattern='%d.%m.%Y %H:%M'):
    """Parse deadline date

    Note:
        Returns `date` if input string is valid.

    Args:
        date (str): Date of deadline in format [DD.MM.YYYY hh:mm].
        pattern (str): Format of date string representation.

    Raises:
        ValueError: If string does not math format.
        AttributeError: If date less than current date.

    """
    date = datetime.strptime(date, pattern)
    if date < datetime.now():
        raise AttributeError('Date cannot be less that current date')
    return date


def main():
    d = parse_config()['DEFAULT']
    for key in d:
        print(key, d[key])

if __name__ == '__main__':
    main()
