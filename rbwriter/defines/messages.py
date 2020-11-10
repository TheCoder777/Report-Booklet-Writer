# internal modules
from ..defines.colors import MSG_NORMAL, MSG_SUCCESS, MSG_WARNING
from ..models.message import MSG


"""
Predefined messages for the messaging system!
"""


# custom ones


def custom_success(content):
    return MSG(content, MSG_SUCCESS)


def custom_normal(content):
    return MSG(content, MSG_NORMAL)


def custom_warning(content):
    return MSG(content, MSG_WARNING)


# missing fields
MISSING_USERNAME = MSG("Missing username!", MSG_WARNING)
MISSING_NAME = MSG("Missing name!", MSG_WARNING)
MISSING_SURNAME = MSG("Missing surname!", MSG_WARNING)
MISSING_PASSWORD = MSG("Missing password!", MSG_WARNING)
MISSING_EMAIL = MSG("Missing email address!", MSG_WARNING)
EMAIL_DOESNT_EXIST = MSG("This account doesn't exist!", MSG_WARNING)
EMAIL_ALREADY_EXISTS = MSG("This email address is already in use!", MSG_NORMAL)

# wrong/invalid fields
INVALID_EMAIL = MSG("Your email is invalid!<br>Did you spell it right?", MSG_WARNING)
WRONG_EMAIL = MSG("This email is wrong!<I'm sure there is a typo somewhere.", MSG_WARNING)
INVALID_PASSWORD = MSG("Wrong password!", MSG_WARNING)
PASSWORD_MISMATCH = MSG("The given passwords don't match!", MSG_WARNING)
USERNAME_NOT_AVAILABLE = MSG("This username is not available", MSG_WARNING)
UNFULFILLED_PASSWORD_REQUIREMENTS = MSG("Your Password doesn't match the requirements: <br/> \
                                      At least 8 characters total <br/> \
                                      One capital character, <br/> \
                                      one number, <br/> \
                                      and one Special character.", MSG_WARNING)
INVALID_DATE = MSG("The date you entered is in the wrong format!", MSG_WARNING)
INVALID_CALENDER_WEEK = MSG("Invalid calender week! (Too high)", MSG_WARNING)

# successful
LOGGED_IN = MSG("Successfully logged in!", MSG_SUCCESS)
REGISTERED = MSG("Successfully registered!", MSG_SUCCESS)
SAVED_TODO = MSG("Yes, we saved it!", MSG_SUCCESS)
SAVED_SETTINGS = MSG("Your settings are save!", MSG_SUCCESS)

# reset
RESET_USER_TO_DEFAULT = MSG("Successfully reset user to default settings!", MSG_NORMAL)
