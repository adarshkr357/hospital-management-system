from datetime import datetime, date, timedelta
from typing import Tuple, Optional


def validate_date_range(start_date: date, end_date: date) -> bool:
    """
    Validate if the date range is valid.
    """
    return start_date <= end_date


def get_date_range(range_type: str = "week") -> Tuple[date, date]:
    """
    Get start and end dates for different ranges.
    range_type: 'day', 'week', 'month', 'year'
    """
    today = date.today()

    if range_type == "day":
        return today, today
    elif range_type == "week":
        start = today - timedelta(days=today.weekday())
        return start, start + timedelta(days=6)
    elif range_type == "month":
        start = today.replace(day=1)
        if today.month == 12:
            end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        return start, end
    elif range_type == "year":
        start = today.replace(month=1, day=1)
        end = today.replace(month=12, day=31)
        return start, end
    else:
        raise ValueError("Invalid range type")


def format_date(date_obj: date, format_str: str = "%Y-%m-%d") -> str:
    """
    Format date object to string.
    """
    return date_obj.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[date]:
    """
    Parse date string to date object.
    """
    try:
        return datetime.strptime(date_str, format_str).date()
    except ValueError:
        return None


def calculate_age(birth_date: date) -> int:
    """
    Calculate age from birth date.
    """
    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
