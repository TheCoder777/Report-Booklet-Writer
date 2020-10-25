
from defines.colors import MSG_NORMAL, MSG_SUCCESS, MSG_WARNING
from models.message import MSG


"""
Predefined messages for the messaging system!
"""

# missing fields
MISSING_USERNAME = MSG("Missing username!", MSG_WARNING)
MISSING_NAME = MSG("Missing name!", MSG_WARNING)
MISSING_SURNAME = MSG("Missing surname!", MSG_WARNING)
MISSING_PASSWORD = MSG("Missing password!", MSG_WARNING)
MISSING_EMAIL = MSG("Missing email address!", MSG_WARNING)

# wrong/invalid fields
INVALID_EMAIL = MSG("Your email is invalid!<br>Did you spell it right?", MSG_WARNING)
WRONG_EMAIL = MSG("This email is wrong!<I'm sure there is a typo somewhere.", MSG_WARNING)
INVALID_PASSWORD = MSG("Wrong password!", MSG_WARNING)
PASSWORD_MISMATCH = MSG("The given passwords don't match!", MSG_WARNING)
USERNAME_NOT_AVAILABLE = MSG("This username is not aviable", MSG_WARNING)
UNFULFILLED_PASSWORD_REQUIREMENTS = MSG("Your Password doesn't match the requirements:<br> \
                                      At least 8 characters total<br> \
                                      One capital character,<br> \
                                      one number,<br> \
                                      and one Special character.", MSG_WARNING)

# successful
LOGGED_IN = MSG("Successfully logged in!", MSG_SUCCESS)
REGISTERED = MSG("Successfully registered!", MSG_SUCCESS)
SAVED = MSG("Yes, we saved it!", MSG_SUCCESS)
