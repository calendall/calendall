import re

from .models import CalendallUser


# precompiled regex

# Check username is: A-Z, a-z and only dashes
# Can't start wiht a dash
# 30 max
username_regex = re.compile("^.(?<!\-)[a-zA-Z0-9\-]{1,29}$")
# Only letters
letters_regex = re.compile("[a-zA-Z]")
# Only numbers
numbers_regex = re.compile("[0-9]")


def valid_username(username):
    """Checks if the username has a valid string"""
    return bool(username_regex.match(username))


def valid_password(password):
    """Checks if the password has a valid string"""

    min_password_chars = 7
    has_letter = letters_regex.search(password)
    has_number = numbers_regex.search(password)

    return len(password) >= min_password_chars and has_number and has_letter


def email_exists(email):
    return CalendallUser.objects.filter(email=email).exists()


def username_exists(username):
    return CalendallUser.objects.filter(username=username).exists()
