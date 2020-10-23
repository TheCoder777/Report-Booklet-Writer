
from defines.colors import MSG_NORMAL, MSG_SUCCESS, MSG_WARNING

"""
Predefined messages for the messaging system!
"""

# missing fields
MISSING_USERNAME = ("Missing username!", MSG_WARNING)
MISSING_NAME = ("Missing name!", MSG_WARNING)
MISSING_SURNAME = ("Missing surname!", MSG_WARNING)
MISSING_PASSWORD = ("Missing passwords!", MSG_WARNING)
MISSING_EMAIL = ("Missing email address!", MSG_WARNING)

# wrong/invalid fields
INVALID_EMAIL = ("Your email is invalid!<br>Did you spell it right?", MSG_WARNING)
WRONG_EMAIL = ("This email is wrong!<I'm sure there is a typo somewhere.", MSG_WARNING)
INVALID_PASSWORD = ("Wrong password!", MSG_WARNING)
PASSWORD_MISSMATCH = ("The given passwords don't match!", MSG_WARNING)
USERNAME_NOT_AVIABLE = ("This username is not aviable", MSG_WARNING)
UNFULFILLED_PASSWORD_REQUIREMENTS = ("Your Password doesn't match the requirements:<br> \
                                      At least 8 characters total<br> \
                                      One capital character,<br> \
                                      one number,<br> \
                                      and one Special character.", MSG_WARNING)

# successfull
LOGGED_IN = ("Successfully logged in!", MSG_SUCCESS)
REGISTERED = ("Successfully registered!", MSG_SUCCESS)
SAVED = ("Yes, we saved it!", MSG_SUCCESS)
