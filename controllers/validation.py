import re
from datetime import datetime, timedelta

def validate_name(name):
    """Name should not contain numeric or special characters."""
    if re.match(r"^[A-Za-z\s]+$", name):
        return True
    return False

def validate_email(email):
    """Standard email format."""
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

def validate_phone(phone):
    """Exact 10 digits, numbers only."""
    if re.match(r"^\d{10}$", phone):
        return True
    return False

def validate_date(date_str):
    """Format: YYYY-MM-DD, must be within next 3 months."""
    try:
        travel_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        max_date = today + timedelta(days=90)
        
        if today.date() <= travel_date.date() <= max_date.date():
            return True, travel_date
        else:
            return False, "Travel date must be between today and the next 3 months."
    except ValueError:
        return False, "That doesn't look like a valid date. Please use YYYY-MM-DD format."

def validate_train_number_unique(train_no, TRAINS):
    return train_no not in TRAINS

def validate_time_format(time_str):
    """HH:MM format."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
